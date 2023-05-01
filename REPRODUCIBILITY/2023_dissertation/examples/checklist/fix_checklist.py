import re
import sys

CTL_RE = re.compile(r'CTLSPEC AG\(\(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> \(success_node(?P<val2>(_\d+)?)\.status = success\)\)\);')
CTL_RE_NOT = re.compile(r'CTLSPEC AG\(\(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> !\(\(success_node(?P<val2>(_\d+)?)\.status = success\)\)\)\);')
LTL_RE = re.compile(r'LTLSPEC G\(\(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> \(success_node(?P<val2>(_\d+)?)\.status = success\)\)\);')
LTL_RE_NOT = re.compile(r'LTLSPEC G\(\(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> !\(\(success_node(?P<val2>(_\d+)?)\.status = success\)\)\)\);')
INVAR_RE = re.compile(r'INVARSPEC \(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> \(success_node(?P<val2>(_\d+)?)\.status = success\)\);')
INVAR_RE_NOT = re.compile(r'INVARSPEC \(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> !\(\(success_node(?P<val2>(_\d+)?)\.status = success\)\)\);')


def aut_ctl(matchobj):
    return (
        'CTLSPEC AG(((success_failure_node' + matchobj.group('val1') + '.status = failure) -> (A [(active_node > 0) U (success_node' + matchobj.group('val1') + '.status = success)])));'
    )


def aut_ctl_not(matchobj):
    return (
        'CTLSPEC AG(((success_failure_node' + matchobj.group('val1') + '.status = failure) -> !(A [(active_node > 0) U (success_node' + matchobj.group('val1') + '.status = success)])));'
    )


def aut_ltl(matchobj):
    return (
        'LTLSPEC G(((success_failure_node' + matchobj.group('val1') + '.status = failure) -> ((active_node > 0) U (success_node' + matchobj.group('val1') + '.status = success))));'
    )


def aut_ltl_not(matchobj):
    return (
        'LTLSPEC G(((success_failure_node' + matchobj.group('val1') + '.status = failure) -> !((active_node > 0) U (success_node' + matchobj.group('val1') + '.status = success))));'
    )


def aut_handle_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.read()
        (lines, _) = CTL_RE.subn(aut_ctl, lines, 0)
        (lines, _) = CTL_RE_NOT.subn(aut_ctl_not, lines, 0)
        (lines, _) = LTL_RE.subn(aut_ltl, lines, 0)
        (lines, _) = LTL_RE_NOT.subn(aut_ltl_not, lines, 0)
        (lines, _) = INVAR_RE.subn(r'', lines, 0)
        (lines, _) = INVAR_RE_NOT.subn(r'', lines, 0)
    with open(file_name, 'w') as f:
        f.write(lines)


AUT_S_CTL_RE = re.compile(r'CTLSPEC AG\(\(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> \((?P<val2>success_node(_\d+)?)\.status = success\)\)\);')
AUT_S_CTL_RE_NOT = re.compile(r'CTLSPEC AG\(\(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> !\(\((?P<val2>success_node(_\d+)?)\.status = success\)\)\)\);')
AUT_S_LTL_RE = re.compile(r'LTLSPEC G\(\(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> \((?P<val2>success_node(_\d+)?)\.status = success\)\)\);')
AUT_S_LTL_RE_NOT = re.compile(r'LTLSPEC G\(\(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> !\(\((?P<val2>success_node(_\d+)?)\.status = success\)\)\)\);')
AUT_S_INVAR_RE = re.compile(r'INVARSPEC \(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> \((?P<val2>success_node(_\d+)?)\.status = success\)\);')
AUT_S_INVAR_RE_NOT = re.compile(r'INVARSPEC \(\((?P<val1>success_failure_node(_\d+)?)\.status = failure\) -> !\(\((?P<val2>success_node(_\d+)?)\.status = success\)\)\);')


def aut_s_ctl(matchobj):
    return (
        'CTLSPEC AG(((active_node = node_names.' + matchobj.group('val1') + ' & current_status = failure) -> (A [(active_node > 0) U (active_node = node_names.' + matchobj.group('val2') + ' & current_status = success)])));'
    )


def aut_s_ctl_not(matchobj):
    return (
        'CTLSPEC AG(((active_node = node_names.' + matchobj.group('val1') + ' & current_status = failure) -> !(A [(active_node > 0) U (active_node = node_names.' + matchobj.group('val2') + ' & current_status = success)])));'
    )


def aut_s_ltl(matchobj):
    return (
        'LTLSPEC G(((active_node = node_names.' + matchobj.group('val1') + ' & current_status = failure) -> ((active_node > 0) U (active_node = node_names.' + matchobj.group('val2') + ' & current_status = success))));'
    )


def aut_s_ltl_not(matchobj):
    return (
        'LTLSPEC G(((active_node = node_names.' + matchobj.group('val1') + ' & current_status = failure) -> !((active_node > 0) U (active_node = node_names.' + matchobj.group('val2') + ' & current_status = success))));'
    )


def aut_s_handle_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.read()
        (lines, _) = AUT_S_CTL_RE.subn(aut_s_ctl, lines, 0)
        (lines, _) = AUT_S_CTL_RE_NOT.subn(aut_s_ctl_not, lines, 0)
        (lines, _) = AUT_S_LTL_RE.subn(aut_s_ltl, lines, 0)
        (lines, _) = AUT_S_LTL_RE_NOT.subn(aut_s_ltl_not, lines, 0)
        (lines, _) = AUT_S_INVAR_RE.subn(r'', lines, 0)
        (lines, _) = AUT_S_INVAR_RE_NOT.subn(r'', lines, 0)
    with open(file_name, 'w') as f:
        f.write(lines)


path = sys.argv[1]
base_name = sys.argv[2]
aut_handle_file(path + 'smv/aut_' + base_name)
aut_s_handle_file(path + 'smv/aut_s_' + base_name)
aut_s_handle_file(path + 'smv/depth_' + base_name)
