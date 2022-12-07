"""
pytree code from textX model using jinja2
"""
from __future__ import unicode_literals
from os import mkdir
from os.path import exists, dirname, join
import jinja2
# import os
from textx import metamodel_from_file
# from textx.export import metamodel_export, model_export
import sys


this_folder = dirname(__file__)


def get_btree_mm(debug=False):
    btree_mm = metamodel_from_file(join(this_folder, '..', 'grammar', 'btree.tx'),
                                   classes = [],
                                   builtins = {},
                                   debug = debug)

    return btree_mm

# def read_user_code(filename,user_code):
#     if (not os.path.exists(filename)):
#         return user_code
#     f = open(filename,'r')
#     code = f.readlines()
#     f.close()

#     return getUserUpdates(code, user_code)


# def getUserUpdates(code, user_code):
#     contents = user_code
#     begins_prefix="############<<USER "
#     begins_suffix=" CODE BEGINS>>##############################"
#     ends_prefix="############<<USER "
#     ends_suffix=" CODE ENDS>>################################"
#     if (not code):
#         return contents
#     codelist = code
#     cur_key = ''
#     lines = []
#     contents = {}
#     for l in codelist:
#         x = l.strip()
#         #if (not x):
#         #    continue
#         if x.startswith(begins_prefix):
#             if not cur_key and x.endswith(begins_suffix):
#                 cur_key = x[len(begins_prefix):-1*len(begins_suffix)]
#                 continue
#             if cur_key and x.endswith(ends_suffix):
#                 if (len(lines)):
#                     contents[cur_key] = ''.join(lines)
#                 lines = []
#                 cur_key = ''
#                 continue
#         if cur_key:
#             lines.append(l)
#     return contents


def main(debug=False):

    model_file = sys.argv[1]
    output_folder = sys.argv[2]

    this_folder = dirname(__file__)

    btree_mm = get_btree_mm(debug)

    # Build Person model from person.ent file
    btree_model = btree_mm.model_from_file(model_file)

    # Create output folder
    srcgen_folder = output_folder
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    def get_default(obj):
        if obj.default or obj.default is False:
            print(obj.name)
            if obj.type.name.lower() == "string":
                return "\""+obj.default+"\""
            return str(obj.default)
        return "None"

    def is_instance(obj, type_names):
        from textx import textx_isinstance
        for type_name in type_names:
            if textx_isinstance(obj, btree_mm[type_name]):
                return True
        return False

    def is_task(obj):
        return is_instance(obj, ["TaskNode"])

    def is_message(obj):
        return is_instance(obj, ["MessageType"])

    def is_basearraytype(obj):
        return is_instance(obj, ["BaseArrayType"])

    def is_parallel(obj):
        return is_instance(obj, ["ParBTNode"])

    def is_sequence(obj):
        return is_instance(obj, ["SeqBTNode"])

    def is_selector(obj):
        return is_instance(obj, ["SelBTNode"])

    def is_sif(obj):
        return is_instance(obj, ["SIFBTNode"])

    def is_parent(obj):
        return is_instance(obj, ["ParBTNode", "SeqBTNode", "SelBTNode", "SIFBTNode"])

    def is_condition(obj):
        if is_instance(obj, ["ParBTNode", "SeqBTNode", "SelBTNode"]):
            if obj.cond:
                return True
        return False

    def is_exec_task(obj):
        return is_instance(obj, ["TaskBTNode"])

    def is_timer(obj):
        return is_instance(obj, ["TimerBTNode"])

    def is_check(obj):
        return is_instance(obj, ["CheckBTNode"])

    def is_monitor(obj):
        return is_instance(obj, ["MonBTNode"])

    def get_init(type_name):
        if (type_name.lower() in ['integer', 'int']):
            return 'int'
        if (type_name.lower() in ['float', 'double']):
            return 'float'
        if (type_name.lower() in ['bool', 'boolean']):
            return 'bool'
        return ''

    sif_nodes = []
    condition_nodes = []
    timer_nodes = []
    std_behavior_nodes = []
    composite_nodes = []

    def get_type(btree_node):
        if is_parallel(btree_node):
            return 'Parallel'
        if is_sequence(btree_node):
            return 'Sequence'
        if is_selector(btree_node):
            return 'Selector'

    def get_task_node_type(task_node):
        return task_node.type.capitalize()

    def get_condition_status(btree_node):
        return btree_node.cond.upper()

    def get_child_names(btree_node):
        child_names = []

        if (is_sif(btree_node)):
            for check_node in btree_node.checks:
                child_names.append(check_node.name)

        for node in btree_node.nodes:
            if (is_monitor(node)):
                for m in node.mon:
                    child_names.append(m.name)
                continue
            if (is_exec_task(node)):
                for t in node.task:
                    child_names.append(t.name)
                continue
            if (is_check(node)):
                for chk in node.check:
                    child_names.append(chk.name)
                continue
            child_names.append(node.name)
        return child_names

    def gather_all_tree_nodes(btree_node, tree_nodes, nodes_name_list):
        if (is_monitor(btree_node) or is_exec_task(btree_node) or is_check(btree_node)):
            return (tree_nodes, nodes_name_list)
        if (is_timer(btree_node)):
            timer_nodes.append(btree_node)
            return (tree_nodes, nodes_name_list)

        if btree_node.name in tree_nodes:
            return (tree_nodes, nodes_name_list)

        nodes_name_list.append(btree_node.name)
        tree_nodes[btree_node.name] = {'name' : btree_node.name, 'child_names' : []}

        if is_sif(btree_node):
            sif_nodes.append(btree_node)
        elif is_condition(btree_node):
            btree_node.type = get_type(btree_node)
            btree_node.expected_status = get_condition_status(btree_node)
            condition_nodes.append(btree_node)
        else:
            btree_node.type = get_type(btree_node)
            composite_nodes.append(btree_node)

        tree_nodes[btree_node.name]['child_names'] = get_child_names(btree_node)
        for node in btree_node.nodes:
            gather_all_tree_nodes(node, tree_nodes, nodes_name_list)

        return tree_nodes, nodes_name_list

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    jinja_env.globals['is_task']            = is_task
    jinja_env.globals['is_basearraytype']   = is_basearraytype
    jinja_env.globals['is_message']         = is_message
    jinja_env.globals['is_parallel']        = is_parallel
    jinja_env.globals['is_sequence']        = is_sequence
    jinja_env.globals['is_sif']             = is_sif
    jinja_env.globals['is_parent']          = is_parent
    jinja_env.globals['is_exec_task']       = is_exec_task
    jinja_env.globals['is_timer']           = is_timer
    jinja_env.globals['is_check']           = is_check
    jinja_env.globals['undefined']          = jinja2.StrictUndefined
    jinja_env.globals['get_default']        = get_default
    jinja_env.globals['get_init']           = get_init

    # Load Java template
    bb_node_template   = jinja_env.get_template('btree_bbnode.template')
    task_node_template = jinja_env.get_template('btree_tasknode.template')
    tree_template      = jinja_env.get_template('btree_tree.template')

    tree_nodes = {}
    nodes_name_list = []
    tree_nodes, nodes_name_list = gather_all_tree_nodes(btree_model.tree.btree, tree_nodes, nodes_name_list)
    parent_nodes = []
    for node_name in nodes_name_list:
        parent_nodes.append(tree_nodes[node_name])

    task_nodes = []
    for task_node in btree_model.taskNodes:
        if (is_task(task_node)):
            task_nodes.append(task_node)
        else:
            task_node.type = get_task_node_type(task_node)
            std_behavior_nodes.append(task_node)

    check_nodes_w_data = []
    for check_node in btree_model.checkNodes:
        if (is_message(check_node.bbvar.type)):
            print(check_node.name)
            check_nodes_w_data.append(check_node.name)

    for bb_node in btree_model.bbNodes:
        user_code = {}
        user_code['IMPORT'] = ''
        user_code['INIT'] = ''
        user_code['UPDATE'] = ''
        user_code['CUSTOM'] = ''
        # user_code = read_user_code(join(srcgen_folder,"bb_%s.py" % bb_node.name),user_code)
        with open(join(srcgen_folder,
                       "bb_%s.py" % bb_node.name), 'w') as f:
            f.write(bb_node_template.render(bb_node=bb_node, user_code=user_code))

    for task_node in task_nodes:
        print(task_node.name)
        try:
            if not task_node.input_topics:
                task_node.input_topics = {}
        except:
            task_node.input_topics = {}
        try:
            if not task_node.output_topics:
                task_node.output_topics = {}
        except:
            task_node.output_topics = {}

        user_code = {}
        user_code['IMPORT'] = ''
        user_code['INIT'] = ''
        user_code['SETUP'] = ''
        user_code['UPDATE'] = ''
        user_code['TERMINATE'] = ''
        user_code['CUSTOM'] = ''
        for input_topic_var in task_node.input_topics:
            user_code['SUB_'+input_topic_var.name] = ''
        for output_topic_var in task_node.output_topics:
            user_code['PUB_'+output_topic_var.name] = ''
        # user_code = read_user_code(join(srcgen_folder,"task_%s.py" % task_node.name), user_code)
        with open(join(srcgen_folder,
                       "task_%s.py" % task_node.name), 'w') as f:
            f.write(task_node_template.render(task_node=task_node, user_code=user_code))
    
    with open(join(srcgen_folder,btree_model.name+"_tree.py"), 'w') as f:
            f.write(tree_template.render(btree=btree_model,
                                        check_nodes_w_data = check_nodes_w_data,
                                        task_nodes=task_nodes,
                                        composite_nodes=composite_nodes,
                                        sif_nodes=sif_nodes,
                                        condition_nodes = condition_nodes,
                                        std_task_nodes=std_behavior_nodes,
                                        timer_nodes = timer_nodes,
                                        parent_nodes =  parent_nodes ))

if __name__ == "__main__":
    main()
