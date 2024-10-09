import os
import py_trees
import ANSR
import ANSR_environment
import serene_randomizer as serene_randomizer_module


def full_tick(tree, environment):
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def run_tree():
    serene_randomizer = serene_randomizer_module.serene_randomizer()
    blackboard_reader = ANSR.create_blackboard(serene_randomizer)
    environment = ANSR_environment.ANSR_environment(blackboard_reader)
    serene_randomizer.set_blackboard_and_environment(blackboard_reader, environment)
    ANSR.initialize_blackboard(blackboard_reader)
    environment.initialize_environment()
    root = ANSR.create_tree(environment)
    tree = py_trees.trees.BehaviourTree(root)
    for _ in range(200):
        if environment.check_tick_condition():
            full_tick(tree, environment)
        else:
            break


if __name__ == '__main__':
    run_tree()
