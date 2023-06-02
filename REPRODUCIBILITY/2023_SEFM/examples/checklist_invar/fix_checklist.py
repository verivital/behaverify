import re
import sys

INVAR_RE = re.compile(r'INVARSPEC \(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> \(success_node(?P<val2>(_\d+)?)\.status = success\)\);')
INVAR_RE_NOT = re.compile(r'INVARSPEC \(\(success_failure_node(?P<val1>(_\d+)?)\.status = failure\) -> !\(\(success_node(?P<val2>(_\d+)?)\.status = success\)\)\);')


def aut_invar(matchobj):
    return (
        'INVARSPEC ((active_node = 0) -> ((success_failure_node' + matchobj.group('val1') + '.status = failure) -> (success_node' + matchobj.group('val2') + '.status = success)));'
    )


def aut_invar_not(matchobj):
    return (
        'INVARSPEC ((active_node = 0) -> ((success_failure_node' + matchobj.group('val1') + '.status = failure) -> !(success_node' + matchobj.group('val2') + '.status = success)));'
    )


def aut_handle_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.read()
        (lines, _) = INVAR_RE.subn(aut_invar, lines, 0)
        (lines, _) = INVAR_RE_NOT.subn(aut_invar_not, lines, 0)
    with open(file_name, 'w') as f:
        f.write(lines)


path = sys.argv[1]
base_name = sys.argv[2]
aut_handle_file(path + 'smv/aut_' + base_name)
