import py_trees
import random


class Non_Blocking_Leaf(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        self.serene_info_variable = "non_blocking"

        super(Non_Blocking_Leaf, self).__init__(name)

    def update(self):

        decision = random.choice([py_trees.common.Status.SUCCESS, py_trees.common.Status.FAILURE])

        return decicion

