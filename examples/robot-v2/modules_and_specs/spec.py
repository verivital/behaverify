import sys
import os

with open('./BTCompiler/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.output = bt_output_false);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.output = bt_output_false -> backup' + str(i) + '.enable = TRUE);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.output = bt_output_false -> backup' + str(i) + '.enable = FALSE);' + os.linesep)

with open('./total/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(backup' + str(i) + '.status = success));' + os.linesep)

with open('./total_no_IVAR/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(backup' + str(i) + '.status = success));' + os.linesep)


with open('./total_errorless/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(backup' + str(i) + '.status = success));' + os.linesep)

with open('./total_no_IVAR_errorless/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(backup' + str(i) + '.status = success));' + os.linesep)

with open('./total_no_IVAR_errorless_unique_child/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(backup' + str(i) + '.status = success));' + os.linesep)

with open('./leaf/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(active_node = -1) U backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(!(active_node = -1) U backup' + str(i) + '.status = success));' + os.linesep)
        
with open('./leaf_no_IVAR/' + sys.argv[1] + ".smv", 'w') as cur_file:
    for i in range(int(sys.argv[1])):
        #cur_file.write('CTLSPEC EF (safety_check' + str(i) + '.status = failure);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(active_node = -1) U backup' + str(i) + '.status = success);' + os.linesep)
        cur_file.write('LTLSPEC G (safety_check' + str(i) + '.status = failure -> !(!(active_node = -1) U backup' + str(i) + '.status = success));' + os.linesep)
