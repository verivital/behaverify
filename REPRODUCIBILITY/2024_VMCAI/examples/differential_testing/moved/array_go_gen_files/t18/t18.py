import c1_file
import c2_file
import a1_file
import a2_file
import a3_file
import a4_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'blVAR0', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'blVAR2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'blDEFINE4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'blDEFINE7', access = py_trees.common.Access.WRITE)
    blackboard_reader.blVAR0 = [None] * 2
    __temp_var__ = serene_safe_assignment.blVAR0([(0, (
        min(-2, max(-5, abs(40)))
        if (True == True) else
        (
            min(-2, max(-5, -3))
            if (True ^ (-74 != -2)) else
            (
            min(-2, max(-5, ([(-59 < -79), (False == (not ((True ^ True)))), (True ^ False)].count(True))))
    )))), (1, (
        min(-2, max(-5, -66))
        if True else
        (
            min(-2, max(-5, -34))
            if (2 > -77) else
            (
            min(-2, max(-5, ([(False == False), (True and True), (True or False)].count(True))))
    ))))])
    for (index, val) in __temp_var__:
        blackboard_reader.blVAR0[index] = val
    blackboard_reader.blVAR2 = [None] * 3
    __temp_var__ = serene_safe_assignment.blVAR2([(0, (
        min(5, max(2, (max(blackboard_reader.blVAR0[1], 21) - (blackboard_reader.blVAR0[0] + blackboard_reader.blVAR0[1] + 72 + 90))))
        if True else
        (
            min(5, max(2, (blackboard_reader.blVAR0[0] + 27)))
            if ((not (((not (True)) or ((blackboard_reader.blVAR0[1] == blackboard_reader.blVAR0[1]))))) or ((not ((True ^ True))))) else
            (
            min(5, max(2, abs(([(blackboard_reader.blVAR0[1] == 72), (32 <= blackboard_reader.blVAR0[1]), ('yes' == 'no'), (not ((((not (False)) or (True)) ^ ('both' == 'both'))))].count(True)))))
    )))), (1, min(5, max(2, blackboard_reader.blVAR0[0]))), (2, (
        min(5, max(2, blackboard_reader.blVAR0[0]))
        if (not ((True ^ False))) else
        (
        min(5, max(2, (min(blackboard_reader.blVAR0[1], 94) * -98 * ([(blackboard_reader.blVAR0[0] > blackboard_reader.blVAR0[0]), (False and False), (blackboard_reader.blVAR0[0] >= -57)].count(True)) * blackboard_reader.blVAR0[0])))
    )))])
    for (index, val) in __temp_var__:
        blackboard_reader.blVAR2[index] = val


    def blDEFINE4():
        return (
            (not ((False ^ True)))
            if ((False or True) or True) else
            (
                False
                if False else
                (
                False
        )))

    blackboard_reader.blDEFINE4 = blDEFINE4
    blackboard_reader.blDEFINE7 = [None] * 3


    def blDEFINE7(index):
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing blDEFINE7: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing blDEFINE7: ' + str(index))
        if index == 0:
            return (
                min(5, max(2, ((blackboard_reader.blVAR2[1] + (blackboard_reader.blVAR0[0] * blackboard_reader.blVAR0[1] * 57) + (86 + blackboard_reader.blVAR0[0] + blackboard_reader.blVAR0[1]) + (86 - blackboard_reader.blVAR2[1])) - min(blackboard_reader.blVAR0[1], max(blackboard_reader.blVAR0[0], 90)))))
                if ('yes' != 'yes') else
                (
                min(5, max(2, 52))
            ))
        elif index == 1:
            return min(5, max(2, (-78 * blackboard_reader.blVAR0[0] * -69 * 92)))
        elif index == 2:
            return (
                min(5, max(2, 39))
                if (min(-3, 53) >= -68) else
                (
                    min(5, max(2, min(-(min(blackboard_reader.blVAR0[0], blackboard_reader.blVAR2[1])), 47)))
                    if False else
                    (
                    min(5, max(2, (-(blackboard_reader.blVAR2[0]) - (blackboard_reader.blVAR0[0] - blackboard_reader.blVAR2[2]))))
            )))
        raise Exception('Reached unreachable state when accessing blDEFINE7: ' + str(index))

    blackboard_reader.blDEFINE7 = blDEFINE7
    return blackboard_reader

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


def create_tree(environment):
    a4 = a4_file.a4('a4', environment)
    c1 = c1_file.c1('c1')
    a1 = a1_file.a1('a1', environment)
    p_one2 = py_trees.composites.Parallel(name = 'p_one2', policy = py_trees.common.ParallelPolicy.SuccessOnOne(), children = [a4, c1, a1])
    p_one2.tick = parallel_better_tick.__get__(p_one2, py_trees.composites.Parallel)
    a4_1 = a4_file.a4('a4_1', environment)
    p_all1 = py_trees.composites.Parallel(name = 'p_all1', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [p_one2, a4_1])
    p_all1.tick = parallel_better_tick.__get__(p_all1, py_trees.composites.Parallel)
    dec_rf0 = py_trees.decorators.RunningIsFailure(name = 'dec_rf0', child = p_all1)
    dec_rf0.tick = decorator_better_tick.__get__(dec_rf0, py_trees.decorators.Decorator)
    return dec_rf0
