import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_all(py_trees.behaviour.Behaviour):
    def __init__(self, name, enum0, enum1, int0, int1, bool0, bool1):
        self.enum0 = enum0
        self.enum1 = enum1
        self.int0 = int0
        self.int1 = int1
        self.bool0 = bool0
        self.bool1 = bool1
        super(check_all, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((self.enum0 == self.enum1) and (self.int0 == self.int1) and (self.bool0 == self.bool1))) else (py_trees.common.Status.FAILURE))
        return return_status
