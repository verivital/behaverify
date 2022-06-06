import py_trees



def create_root(print_pic):
    # skill_goto_kitchen : bt_skill;
    # skill_find_bottle : bt_skill;
    # skill_fetch_bottle : bt_skill;
    # skill_find_glass : bt_skill;
    # skill_fetch_glass : bt_skill;
    # skill_pour_drink : bt_skill;
    # skill_ask_for_help : bt_skill;
    # --
    # do_bottle : bt_sequence(skill_find_bottle, skill_fetch_bottle);
    # do_glass : bt_sequence(skill_find_glass, skill_fetch_glass);
    # do_pour_drink : bt_sequence(do_bottle_and_glass, skill_pour_drink);
    # do_pour_drink_in_kitchen : bt_sequence(skill_goto_kitchen, do_pour_drink);
    # bt_root : bt_fallback(do_pour_drink_in_kitchen, skill_ask_for_help);

    # do_bottle_and_glass : bt_sequence(do_bottle, do_glass);
    # tick_generator : bt_tick_generator(bt_root);

    
    
    skill_goto_kitchen = py_trees.behaviours.Dummy('skill_goto_kitchen')
    skill_find_bottle = py_trees.behaviours.Dummy('skill_find_bottle')
    skill_fetch_bottle = py_trees.behaviours.Dummy('skill_fetch_bottle')
    skill_find_glass = py_trees.behaviours.Dummy('skill_find_glass')
    skill_fetch_glass = py_trees.behaviours.Dummy('skill_fetch_glass')
    skill_pour_drink = py_trees.behaviours.Dummy('skill_pour_drink')
    skill_ask_for_help = py_trees.behaviours.Dummy('skill_ask_for_help')
    
    do_bottle = py_trees.composites.Sequence('do_bottle', children = [skill_find_bottle, skill_fetch_bottle])
    do_glass = py_trees.composites.Sequence('do_glass', children = [skill_find_glass, skill_fetch_glass])

    do_bottle_and_glass = py_trees.composites.Sequence('do_bottle_and_glass', children = [do_bottle, do_glass])
    
    do_pour_drink = py_trees.composites.Sequence('do_pour_drink', children = [do_bottle_and_glass, skill_pour_drink])
    do_pour_drink_in_kitchen = py_trees.composites.Sequence('do_pour_drink_in_kitchen', children = [skill_goto_kitchen, do_pour_drink])
    
    bt_root = py_trees.composites.Selector('bt_root', children = [do_pour_drink_in_kitchen, skill_ask_for_help])

    
    if print_pic:
        py_trees.display.render_dot_tree(bt_root, target_directory = '../pictures/serene_uc1')#works
        
    return bt_root
    

