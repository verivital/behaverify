import os
import re
from behaverify.behaverify_common import tab_indent

# -----------------------------------------------------------------
# the blackboard

STATUS_STRING = 'status__'


def create_names_module(node_name_to_number):
    return ('MODULE define_nodes' + os.linesep
            + '\tDEFINE' + os.linesep
            + ''.join([('\t\t' + node_name + ' := ' + str(node_name_to_number[node_name]) + ';' + os.linesep) for node_name in node_name_to_number])
            )


def create_blackboard(nodes, variables, root_node_name, tick_condition):

    STAGE_RE = re.compile(r'_stage_\d+')

    def remove_stage(condition):
        return STAGE_RE.sub('', condition)
    define_string = ''
    frozenvar_string = ''
    var_string = ''
    init_string = ''
    next_string = ''

    use_exist = False

    for variable_name_key in variables:
        # print(variable_name)
        variable = variables[variable_name_key]
        variable_name = variable['name']
        # -----------------------------------
        # define are static.
        if variable['mode'].strip() == 'DEFINE':
            if len(variable['next_value']) > 0:
                (_, _, stage) = variable['next_value']
                define_string += (
                    tab_indent(2) + variable_name + ' :=' + os.linesep
                    + tab_indent(3) + 'case' + os.linesep
                    + ''.join(
                        [
                            (tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep)
                            for condition_pair in stage
                        ]
                    )
                    + tab_indent(3) + 'esac;' + os.linesep
                )
            if use_exist:
                define_string += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        elif variable['mode'].strip() == 'FROZENVAR' or len(variable['next_value']) == 0:
            frozenvar_string += ('\t\t' + variable_name + ' : '
                                 + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                 + ';' + os.linesep)
            # if variable['initial_value'] is not None:
            #     init_string += ('\t\tinit(' + variable_name + ') := ' + os.linesep
            #                     + '\t\t\tcase' + os.linesep
            #                     + ''.join([('\t\t\t\t' + remove_stage(condition_pair[0]) + ' : ' + remove_stage(condition_pair[1]) + ';' + os.linesep) for condition_pair in variable['initial_value']])
            #                     + '\t\t\tesac;' + os.linesep
            #                     )
            init_string += (
                ('\t\tinit(' + variable_name + ') := ' + os.linesep
                 + '\t\t\tcase' + os.linesep
                 + ''.join([('\t\t\t\t' + remove_stage(condition_pair[0]) + ' : ' + remove_stage(condition_pair[1]) + ';' + os.linesep) for condition_pair in variable['initial_value']])
                 + '\t\t\tesac;' + os.linesep
                 )
                if variable['initial_value'] is not None else
                (tab_indent(2) + 'init(' + variable_name + ') := '
                 + (
                     str(variable['min_value']) if variable['custom_value_range'] is None else
                     variable['custom_value_range'].split(',')[0].replace('{', '').strip()
                 )
                 + ';' + os.linesep
                 )
            )
            if use_exist:
                define_string += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        # --------------------------------
        # ok, so we've handled define and frozenvar, so all that's left
        # is actual variable.
        else:
            var_string += (tab_indent(2) + variable_name + ' : '
                           + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                           + ';' + os.linesep)
            init_string += (
                ('' if variable['initial_value'] is None else (
                    '\t\tinit(' + variable_name + ') := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + ''.join([('\t\t\t\t' + remove_stage(condition_pair[0]) + ' : ' + remove_stage(condition_pair[1]) + ';' + os.linesep) for condition_pair in variable['initial_value'][2]])
                    + '\t\t\tesac;' + os.linesep
                ))
            )
            # print(variable['next_value'])
            next_string += (tab_indent(2) + 'next(' + variable_name + ') :=' + os.linesep
                            + tab_indent(3) + 'case' + os.linesep
                            + ''.join(
                                [
                                    (''.join(
                                        [
                                            (tab_indent(4)
                                             + (
                                                 ('(active_node = node_names.' + node_name + ')') if node_name is not None else (
                                                     '(active_node = -1) & ' + tick_condition
                                                 )
                                             )
                                             + ' & (' + remove_stage(condition_pair[0]) + ') : ' + remove_stage(condition_pair[1]) + ';' + os.linesep)
                                            for condition_pair in stage
                                        ]
                                    ))
                                    for (node_name, non_determinism, stage) in variable['next_value']
                                ]
                            )
                            + tab_indent(4) + 'TRUE : ' + variable_name + ';' + os.linesep
                            + tab_indent(3) + 'esac;' + os.linesep
                            )
    return (define_string,
            frozenvar_string,
            var_string,
            init_string,
            next_string
            )

# -----------------------------------------------------------------
# status module


def create_status_module(statuses):
    status_module = ('MODULE ' + statuses + '_DEFAULT_module'
                     + os.linesep
                     + '\tCONSTANTS' + os.linesep
                     + '\t\tsuccess, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'reset : invalid;' + os.linesep
                     + tab_indent(4) + '!(active) : previous_status;' + os.linesep
                     + tab_indent(4) + 'TRUE : ' + statuses + ';' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(1) + 'VAR' + os.linesep
                     + tab_indent(2) + 'previous_status : {' + statuses + ', invalid};' + os.linesep
                     + tab_indent(1) + 'ASSIGN' + os.linesep
                     + tab_indent(2) + 'init(previous_status) := invalid;' + os.linesep
                     + tab_indent(2) + 'next(previous_status) := status;' + os.linesep
                     )
    return status_module

# -----------------------------------------------------------------
# decorator nodes


def create_decorator_X_is_Y(node):
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := '
            + STATUS_STRING + node['children'][0] + ' = ' + node['additional_arguments'][0]
            + ' ? ' + node['additional_arguments'][1] + ' : ' + STATUS_STRING + node['children'][0] + ';' + os.linesep)


def create_decorator_inverter(node):
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + tab_indent(4) + STATUS_STRING + node['children'][0] + ' = failure : success;' + os.linesep
            + tab_indent(4) + STATUS_STRING + node['children'][0] + ' = success : failure;' + os.linesep
            + tab_indent(4) + 'TRUE : ' + STATUS_STRING + node['children'][0] + ';' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


# -----------------------------------------------------------------
# composite nodes


def create_composite_selector_with_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + '(' + STATUS_STRING + children[child_index] + ' != failure) & (' + str(child_index) + ' >= RESUME THINGY HERE) : ' + STATUS_STRING + children[child_index] + ';' + os.linesep)
                 for child_index in range(len(children))])
            + tab_indent(4) + 'TRUE : failure;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_selector_without_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + STATUS_STRING + child + ' != failure : ' + STATUS_STRING + child + ';' + os.linesep)
                 for child in children])
            + tab_indent(4) + 'TRUE : failure;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_sequence_with_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + '(' + STATUS_STRING + children[child_index] + ' != success) & (' + str(child_index) + ' >= RESUME THINGY HERE) : ' + STATUS_STRING + children[child_index] + ';' + os.linesep)
                 for child_index in range(len(children))])
            + tab_indent(4) + 'TRUE : success;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_sequence_without_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + STATUS_STRING + child + ' != success : ' + STATUS_STRING + child + ';' + os.linesep)
                 for child in children])
            + tab_indent(4) + 'TRUE : success;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_parallel_success_on_all_with_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + '((' + STATUS_STRING + children[child_index] + ' = failure) | (' + STATUS_STRING + children[child_index] + ' = invalid)) & (' + str(child_index) + ' >= RESUME THINGY HERE) : ' + STATUS_STRING + children[child_index] + ';' + os.linesep)
                 for child_index in range(len(children))])
            + ''.join(
                [(tab_indent(4) + '(' + STATUS_STRING + children[child_index] + ' = running) & (' + str(child_index) + ' >= RESUME THINGY HERE) : running;' + os.linesep)
                 for child_index in range(len(children))])
            + tab_indent(4) + 'TRUE : success;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_parallel_success_on_all_without_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + '(' + STATUS_STRING + children[child_index] + ' = failure) | (' + STATUS_STRING + children[child_index] + ' = invalid) : ' + STATUS_STRING + children[child_index] + ';' + os.linesep)
                 for child_index in range(len(children))])
            + ''.join(
                [(tab_indent(4) + STATUS_STRING + children[child_index] + ' = running : running;' + os.linesep)
                 for child_index in range(len(children))])
            + tab_indent(4) + 'TRUE : success;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)


def create_composite_parallel_success_on_one_with_memory(node):
    return create_composite_parallel_success_on_one_without_memory(node)


def create_composite_parallel_success_on_one_without_memory(node):
    children = node['children']
    return (tab_indent(2) + STATUS_STRING + node['name'] + ' := ' + os.linesep
            + tab_indent(3) + 'case' + os.linesep
            + ''.join(
                [(tab_indent(4) + '(' + STATUS_STRING + children[child_index] + ' = failure) | (' + STATUS_STRING + children[child_index] + ' = invalid) : ' + STATUS_STRING + children[child_index] + ';' + os.linesep)
                 for child_index in range(len(children))])
            + ''.join(
                [(tab_indent(4) + STATUS_STRING + children[child_index] + ' = success : success;' + os.linesep)
                 for child_index in range(len(children))])
            + tab_indent(4) + 'TRUE : running;' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep)

# -----------------------------------------------------------------
