import py_trees
import math
import operator
import random
import serene_safe_assignment


class action_one(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(action_one, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('index_var'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('foo'), access = py_trees.common.Access.WRITE)
        self.bar = [None] * 3
        __temp_var__ = serene_safe_assignment.bar([(0, (
            'increase'
            if (0 == 0) else
            (
                'decrease'
                if (1 == 0) else
                (
                'nope'
        )))), (1, (
            'increase'
            if (0 == 1) else
            (
                'decrease'
                if (1 == 1) else
                (
                'nope'
        )))), (2, (
            'increase'
            if (0 == 2) else
            (
                'decrease'
                if (1 == 2) else
                (
                'nope'
        ))))])
        for (index, val) in __temp_var__:
            self.bar[index] = val

    def update(self):
        __temp_var__ = serene_safe_assignment.foo([(self.blackboard.index_var, (
            min(10, (self.blackboard.foo[self.blackboard.index_var] + 1))
            if ('increase' == self.bar[self.blackboard.index_var]) else
            (
                max(0, (self.blackboard.foo[self.blackboard.index_var] - 1))
                if ('decrease' == self.bar[self.blackboard.index_var]) else
                (
                self.blackboard.foo[self.blackboard.index_var]
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.foo[index] = val
        return_status = py_trees.common.Status.SUCCESS
        __temp_var__ = serene_safe_assignment.bar([(0, (
            random.choice(['decrease', 'nope'])
            if ('increase' == self.bar[0]) else
            (
                random.choice(['nope', 'increase'])
                if ('decrease' == self.bar[0]) else
                (
                random.choice(['increase', 'decrease'])
        )))), (1, (
            random.choice(['decrease', 'nope'])
            if ('increase' == self.bar[1]) else
            (
                random.choice(['nope', 'increase'])
                if ('decrease' == self.bar[1]) else
                (
                random.choice(['increase', 'decrease'])
        )))), (2, (
            random.choice(['decrease', 'nope'])
            if ('increase' == self.bar[2]) else
            (
                random.choice(['nope', 'increase'])
                if ('decrease' == self.bar[2]) else
                (
                random.choice(['increase', 'decrease'])
        ))))])
        for (index, val) in __temp_var__:
            self.bar[index] = val
        return return_status
