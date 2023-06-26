
import typing
import itertools

def selector_better_tick(self) -> typing.Iterator[py_trees.behaviour.Behaviour]:
    """
    Customise the tick behaviour for a selector.

    This implements priority-interrupt style handling amongst the selector's children.
    The selector's status is always a reflection of it's children's status.

    Yields:
        :class:`~py_trees.py_trees.behaviour.Behaviour`: a reference to itself or one of its children
    """
    self.logger.debug("%s.tick()" % self.__class__.__name__)
    # initialise
    if self.status != py_trees.common.Status.RUNNING:
        # selector specific initialisation - leave initialise() free for users to
        # re-implement without having to make calls to super()
        self.logger.debug(
            "%s.tick() [!RUNNING->reset current_child]" % self.__class__.__name__
        )
        self.current_child = self.children[0] if self.children else None

        # reset the children - don't need to worry since they will be handled
        # a) prior to a remembered starting point, or
        # b) invalidated by a higher level priority

        # user specific initialisation
        self.initialise()

    # nothing to do
    if not self.children:
        self.current_child = None
        self.__serene_print__ = 'FAILURE'
        self.stop(py_trees.common.Status.FAILURE)
        yield self
        return

    # starting point
    if self.memory:
        assert self.current_child is not None  # should never be true, help mypy out
        index = self.children.index(self.current_child)
        # clear out preceding status' - not actually necessary but helps
        # visualise the case of memory vs no memory
        for child in itertools.islice(self.children, None, index):
            child.stop(py_trees.common.Status.INVALID)
    else:
        index = 0

    # actual work
    previous = self.current_child
    for child in itertools.islice(self.children, index, None):
        for node in child.tick():
            yield node
            if node is child:
                if (
                    node.status == py_trees.common.Status.RUNNING
                    or node.status == py_trees.common.Status.SUCCESS
                ):
                    self.current_child = child
                    self.status = node.status
                    self.__serene_print__ = self.status.value
                    if previous is None or previous != self.current_child:
                        # we interrupted, invalidate everything at a lower priority
                        passed = False
                        for child in self.children:
                            if passed:
                                if child.status != py_trees.common.Status.INVALID:
                                    child.stop(py_trees.common.Status.INVALID)
                            passed = True if child == self.current_child else passed
                    yield self
                    return
    # all children failed, set failure ourselves and current child to the last bugger who failed us
    self.status = py_trees.common.Status.FAILURE
    self.__serene_print__ = self.status.value
    try:
        self.current_child = self.children[-1]
    except IndexError:
        self.current_child = None
    yield self


def sequence_better_tick(self) -> typing.Iterator[py_trees.behaviour.Behaviour]:
    """
    Tick over the children.

    Yields:
        :class:`~py_trees.py_trees.behaviour.Behaviour`: a reference to itself or one of its children
    """
    self.logger.debug("%s.tick()" % self.__class__.__name__)

    # initialise
    index = 0
    if self.status != py_trees.common.Status.RUNNING:
        self.current_child = self.children[0] if self.children else None
        for child in self.children:
            if child.status != py_trees.common.Status.INVALID:
                child.stop(py_trees.common.Status.INVALID)
        self.initialise()  # user specific initialisation
    elif self.memory and py_trees.common.Status.RUNNING:
        assert self.current_child is not None  # should never be true, help mypy out
        index = self.children.index(self.current_child)
    elif not self.memory and py_trees.common.Status.RUNNING:
        self.current_child = self.children[0] if self.children else None
    else:
        # previous conditional checks should cover all variations
        raise RuntimeError("Sequence reached an unknown / invalid state")

    # nothing to do
    if not self.children:
        self.current_child = None
        self.__serene_print__ = 'SUCCESS'
        self.stop(py_trees.common.Status.SUCCESS)
        yield self
        return

    # actual work
    for child in itertools.islice(self.children, index, None):
        for node in child.tick():
            yield node
            if node is child and node.status != py_trees.common.Status.SUCCESS:
                self.status = node.status
                self.__serene_print__ = self.status.value
                if not self.memory:
                    # invalidate the remainder of the sequence
                    # i.e. kill dangling runners
                    for child in itertools.islice(self.children, index + 1, None):
                        if child.status != py_trees.common.Status.INVALID:
                            child.stop(py_trees.common.Status.INVALID)
                yield self
                return
        try:
            # advance if there is 'next' sibling
            self.current_child = self.children[index + 1]
            index += 1
        except IndexError:
            pass

    self.__serene_print__ = 'SUCCESS'
    self.stop(py_trees.common.Status.SUCCESS)
    yield self


def parallel_better_tick(self) -> typing.Iterator[py_trees.behaviour.Behaviour]:
    """
    Tick over the children.

    Yields:
        :class:`~py_trees.py_trees.behaviour.Behaviour`: a reference to itself or one of its children

    Raises:
        RuntimeError: if the policy configuration was invalid
    """
    self.logger.debug("%s.tick()" % self.__class__.__name__)
    self.validate_policy_configuration()

    # reset
    if self.status != py_trees.common.Status.RUNNING:
        self.logger.debug("%s.tick(): re-initialising" % self.__class__.__name__)
        for child in self.children:
            # reset the children, this ensures old SUCCESS/FAILURE status flags
            # don't break the synchronisation logic below
            if child.status != py_trees.common.Status.INVALID:
                child.stop(py_trees.common.Status.INVALID)
        self.current_child = None
        # subclass (user) handling
        self.initialise()

    # nothing to do
    if not self.children:
        self.current_child = None
        self.__serene_print__ = 'SUCCESS'
        self.stop(py_trees.common.Status.SUCCESS)
        yield self
        return

    # process them all first
    for child in self.children:
        if self.policy.synchronise and child.status == py_trees.common.Status.SUCCESS:
            continue
        for node in child.tick():
            yield node

    # determine new status
    new_status = py_trees.common.Status.RUNNING
    self.current_child = self.children[-1]
    try:
        failed_child = next(
            child
            for child in self.children
            if child.status == py_trees.common.Status.FAILURE
        )
        self.current_child = failed_child
        new_status = py_trees.common.Status.FAILURE
    except StopIteration:
        if type(self.policy) is py_trees.common.ParallelPolicy.SuccessOnAll:
            if all([c.status == py_trees.common.Status.SUCCESS for c in self.children]):
                new_status = py_trees.common.Status.SUCCESS
                self.current_child = self.children[-1]
        elif type(self.policy) is py_trees.common.ParallelPolicy.SuccessOnOne:
            successful = [
                child
                for child in self.children
                if child.status == py_trees.common.Status.SUCCESS
            ]
            if successful:
                new_status = py_trees.common.Status.SUCCESS
                self.current_child = successful[-1]
        elif type(self.policy) is py_trees.common.ParallelPolicy.SuccessOnSelected:
            if all(
                [c.status == py_trees.common.Status.SUCCESS for c in self.policy.children]
            ):
                new_status = py_trees.common.Status.SUCCESS
                self.current_child = self.policy.children[-1]
        else:
            raise RuntimeError(
                "this parallel has been configured with an unrecognised policy [{}]".format(
                    type(self.policy)
                )
            )
    # this parallel may have children that are still running
    # so if the parallel itself has reached a final status, then
    # these running children need to be terminated so they don't dangle
    self.__serene_print__ = new_status.value
    if new_status != py_trees.common.Status.RUNNING:
        self.stop(new_status)
    self.status = new_status
    yield self



def decorator_better_tick(self) -> typing.Iterator[py_trees.behaviour.Behaviour]:
    """
    Manage the decorated child through the tick.

    Yields:
        a reference to itself or one of its children
    """
    self.logger.debug("%s.tick()" % self.__class__.__name__)
    # initialise just like other behaviours/composites
    if self.status != py_trees.common.Status.RUNNING:
        self.initialise()
    # interrupt proceedings and process the child node
    # (including any children it may have as well)
    for node in self.decorated.tick():
        yield node
    # resume normal proceedings for a Behaviour's tick
    new_status = self.update()
    if new_status not in list(py_trees.common.Status):
        self.logger.error(
            "A behaviour returned an invalid status, setting to INVALID [%s][%s]"
            % (new_status, self.name)
        )
        new_status = py_trees.common.Status.INVALID
    self.__serene_print__ = new_status.value
    if new_status != py_trees.common.Status.RUNNING:
        self.stop(new_status)
    self.status = new_status
    yield self
