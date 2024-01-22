import not_finished_file
import next_value_file
import py_trees


def create_tree():
    collatz = py_trees.composites.Sequence('collatz', False)
    not_finished = not_finished_file.not_finished('not_finished')
    next_value = next_value_file.next_value('next_value')
    collatz.add_children([not_finished, next_value])
    return collatz
