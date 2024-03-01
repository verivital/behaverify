from pathlib import Path
import py_trees
import whatever_file


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'fib_val', access = py_trees.common.Access.WRITE)
    blackboard_reader.fib_val = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):


    def fib_val(index):
        fib_val = [None] * 20
        fib_val[0] = 0
        if 0 == index:
            return fib_val[0]
        fib_val[1] = 1
        if 1 == index:
            return fib_val[1]
        fib_val[2] = (fib_val[1] + fib_val[0])
        if 2 == index:
            return fib_val[2]
        fib_val[3] = (fib_val[2] + fib_val[1])
        if 3 == index:
            return fib_val[3]
        fib_val[4] = (fib_val[3] + fib_val[2])
        if 4 == index:
            return fib_val[4]
        fib_val[5] = (fib_val[4] + fib_val[3])
        if 5 == index:
            return fib_val[5]
        fib_val[6] = (fib_val[5] + fib_val[4])
        if 6 == index:
            return fib_val[6]
        fib_val[7] = (fib_val[6] + fib_val[5])
        if 7 == index:
            return fib_val[7]
        fib_val[8] = (fib_val[7] + fib_val[6])
        if 8 == index:
            return fib_val[8]
        fib_val[9] = (fib_val[8] + fib_val[7])
        if 9 == index:
            return fib_val[9]
        fib_val[10] = (fib_val[9] + fib_val[8])
        if 10 == index:
            return fib_val[10]
        fib_val[11] = (fib_val[10] + fib_val[9])
        if 11 == index:
            return fib_val[11]
        fib_val[12] = (fib_val[11] + fib_val[10])
        if 12 == index:
            return fib_val[12]
        fib_val[13] = (fib_val[12] + fib_val[11])
        if 13 == index:
            return fib_val[13]
        fib_val[14] = (fib_val[13] + fib_val[12])
        if 14 == index:
            return fib_val[14]
        fib_val[15] = (fib_val[14] + fib_val[13])
        if 15 == index:
            return fib_val[15]
        fib_val[16] = (fib_val[15] + fib_val[14])
        if 16 == index:
            return fib_val[16]
        fib_val[17] = (fib_val[16] + fib_val[15])
        if 17 == index:
            return fib_val[17]
        fib_val[18] = (fib_val[17] + fib_val[16])
        if 18 == index:
            return fib_val[18]
        fib_val[19] = (fib_val[18] + fib_val[17])
        if 19 == index:
            return fib_val[19]

    blackboard_reader.fib_val = fib_val
    return


def create_tree(environment):
    whatever = whatever_file.whatever('whatever')
    return whatever
