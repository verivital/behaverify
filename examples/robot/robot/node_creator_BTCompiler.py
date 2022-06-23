import os

def create_bt_tick_generator():
    return ("MODULE bt_tick_generator(top_level_bt)" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tinit(top_level_bt.enable) := TRUE;" + os.linesep
            + "\t\tnext(top_level_bt.enable) := (top_level_bt.output != bt_output_none);" + os.linesep
            + "MODULE bt_single_tick_generator(top_level_bt)" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tinit(top_level_bt.enable) := TRUE;" + os.linesep
            + "\t\tnext(top_level_bt.enable) := FALSE;" + os.linesep
    )
#----------------------------------------------------------------------
def create_bt_skill():
    return ("MODULE bt_skill" + os.linesep
            + "\tIVAR" + os.linesep
            + "\t\tinput : { bt_input_running, bt_input_false, bt_input_true };" + os.linesep
            + "\tVAR" + os.linesep
            + "\t\toutput : { bt_output_none, bt_output_running, bt_output_false, bt_output_true};" + os.linesep
            + "\t\tenable : boolean;" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tinit(output) := bt_output_none;" + os.linesep
            + "\t\tnext(output) :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\t! enable : bt_output_none;" + os.linesep
            + "\t\t\t\tinput = bt_input_running : bt_output_running;" + os.linesep
            + "\t\t\t\tinput = bt_input_false : bt_output_false;" + os.linesep
            + "\t\t\t\tinput = bt_input_true : bt_output_true;" + os.linesep
            + "\t\t\tesac;" + os.linesep
    )

def create_bt_non_blocking_skill():
    return ("MODULE bt_non_blocking_skill" + os.linesep
            + "\tIVAR" + os.linesep
            + "\t\tinput : {bt_input_false, bt_input_true };" + os.linesep
            + "\tVAR" + os.linesep
            + "\t\toutput : { bt_output_none, bt_output_running, bt_output_false, bt_output_true};" + os.linesep
            + "\t\tenable : boolean;" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tinit(output) := bt_output_none;" + os.linesep
            + "\t\tnext(output) :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\t! enable : bt_output_none;" + os.linesep
            + "\t\t\t\tinput = bt_input_false : bt_output_false;" + os.linesep
            + "\t\t\t\tinput = bt_input_true : bt_output_true;" + os.linesep
            + "\t\t\tesac;" + os.linesep
    )

def create_bt_placeholder():
    return("MODULE bt_placeholder" + os.linesep
           + "\tVAR" + os.linesep
           + "\t\tenable : boolean;" + os.linesep
           + "\tDEFINE" + os.linesep
           + "\t\toutput := bt_output_true;" + os.linesep
    )
#----------------------------------------------------------------------


def create_bt_is_running():
    return("MODULE bt_is_running(child_bt)" + os.linesep
           + "\tVAR" + os.linesep
           + "\t\tenable : boolean;" + os.linesep
           + "\tASSIGN" + os.linesep
           + "\t\tchild_bt.enable := enable;" + os.linesep
           + "\tDEFINE" + os.linesep
           + "\t\toutput :=" + os.linesep
           + "\t\t\tcase" + os.linesep
           + "\t\t\t\tchild_bt.output in { bt_output_false, bt_output_true } : bt_output_false;" + os.linesep
           + "\t\t\t\tchild_bt.output = bt_output_running : bt_output_true;" + os.linesep
           + "\t\t\t\tTRUE : bt_output_none;" + os.linesep
           + "\t\t\tesac;" + os.linesep
    )

def create_bt_not():
    return("MODULE bt_not(child_bt)" + os.linesep
           + "\tVAR" + os.linesep
           + "\t\tenable : boolean;" + os.linesep
           + "\tASSIGN" + os.linesep
           + "\t\tchild_bt.enable := enable;" + os.linesep
           + "\tDEFINE" + os.linesep
           + "\t\toutput :=" + os.linesep
           + "\t\t\tcase" + os.linesep
           + "\t\t\t\tchild_bt.output = bt_output_false : bt_output_true;" + os.linesep
           + "\t\t\t\tchild_bt.output = bt_output_true : bt_output_false;" + os.linesep
           + "\t\t\t\tTRUE : child_bt.output;" + os.linesep
           + "\t\t\tesac;" + os.linesep
    )

def create_bt_do_once():
    return("MODULE bt_do_once(child_bt, reset_bt)" + os.linesep
           + "\tVAR" + os.linesep
           + "\t\tsucceded : boolean;" + os.linesep
           + "\tASSIGN" + os.linesep
           + "\t\tinit(succeded) := FALSE;" + os.linesep
           + "\t\tnext(succeded) :=" + os.linesep
           + "\t\t\tcase" + os.linesep
           + "\t\t\t\treset_bt.enable : FALSE;" + os.linesep
           + "\t\t\t\tchild_bt.output = bt_output_true : TRUE;" + os.linesep
           + "\t\t\t\tTRUE : succeded;" + os.linesep
           + "\t\t\tesac;" + os.linesep
           + "\tDEFINE" + os.linesep
           + "\t\toutput :=" + os.linesep
           + "\t\t\tcase" + os.linesep
           + "\t\t\t\tsucceed : bt_output_true;" + os.linesep
           + "\t\t\t\tTRUE : child_bt.output;" + os.linesep
           + "\t\t\tesac;" + os.linesep
    )



#----------------------------------------------------------------------
def create_bt_fallback():
    return ("MODULE bt_fallback(left_bt, right_bt)" + os.linesep
            + "\tVAR"  + os.linesep
            + "\t\tenable : boolean;"  + os.linesep
            + "\tASSIGN"  + os.linesep
            + "\t\tleft_bt.enable := enable;"  + os.linesep
            + "\t\tright_bt.enable := (left_bt.output = bt_output_false);"  + os.linesep
            + "\tDEFINE"  + os.linesep
            + "\t\toutput :="  + os.linesep
            + "\t\t\tcase"  + os.linesep
            + "\t\t\t\tleft_bt.output in { bt_output_running, bt_output_true } : left_bt.output;"  + os.linesep
            + "\t\t\t\tTRUE : right_bt.output;"  + os.linesep
            + "\t\t\tesac;"  + os.linesep
    )


def create_bt_fallback_with_memory():
    return ("MODULE bt_fallback_with_memory(left_bt, right_bt)" + os.linesep
            + "\tVAR" + os.linesep
            + "\tenable : boolean;" + os.linesep
            + "\thas_left_bt_failed : boolean;" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\tinit(has_left_bt_failed) := FALSE;" + os.linesep
            + "\tnext(has_left_bt_failed) :=" + os.linesep
            + "\tcase" + os.linesep
            + "\tright_bt.output in { bt_output_true, bt_output_false } : FALSE; -- Reset." + os.linesep
            + "\tleft_bt.output = bt_output_false : TRUE; -- Engage." + os.linesep
            + "\tTRUE : has_left_bt_failed;" + os.linesep
            + "\tesac;" + os.linesep
            + "\tleft_bt.enable := enable & !has_left_bt_failed;" + os.linesep
            + "\tright_bt.enable := (left_bt.output = bt_output_false) | (enable & has_left_bt_failed);" + os.linesep
            + "\tDEFINE" + os.linesep
            + "\toutput :=" + os.linesep
            + "\tcase" + os.linesep
            + "\tleft_bt.output in { bt_output_running, bt_output_true } : left_bt.output;" + os.linesep
            + "\tTRUE : right_bt.output;" + os.linesep
            + "\tesac;" + os.linesep
    )


def create_bt_sequence():
    return ("MODULE bt_sequence(left_bt, right_bt)" + os.linesep
            + "\tVAR" + os.linesep
            + "\t\tenable : boolean;" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tleft_bt.enable := enable;" + os.linesep
            + "\t\tright_bt.enable := (left_bt.output = bt_output_true);" + os.linesep
            + "\tDEFINE" + os.linesep
            + "\t\toutput :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\tleft_bt.output in { bt_output_running, bt_output_false } : left_bt.output;" + os.linesep
            + "\t\t\t\tTRUE : right_bt.output;" + os.linesep
            + "\t\t\tesac;" + os.linesep
    )

def create_bt_sequence_with_memory():
    return ("MODULE bt_sequence_with_memory(left_bt, right_bt)" + os.linesep
            + "\tVAR" + os.linesep
            + "\t\tenable : boolean;" + os.linesep
            + "\t\thas_left_bt_succeded : boolean;" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tinit(has_left_bt_succeded) := FALSE;" + os.linesep
            + "\t\tnext(has_left_bt_succeded) :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\tright_bt.output in { bt_output_true, bt_output_false } : FALSE; -- Reset." + os.linesep
            + "\t\t\t\tleft_bt.output = bt_output_true : TRUE; -- Engage." + os.linesep
            + "\t\t\t\tTRUE : has_left_bt_succeded; -- Hold." + os.linesep
            + "\t\t\tesac;" + os.linesep
            + "\t\tleft_bt.enable := enable & !has_left_bt_succeded;" + os.linesep
            + "\t\tright_bt.enable := (left_bt.output = bt_output_true) | (enable & has_left_bt_succeded);" + os.linesep
            + "\tDEFINE" + os.linesep
            + "\t\toutput :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\tleft_bt.output in { bt_output_running, bt_output_false } : left_bt.output;" + os.linesep
            + "\t\t\t\tTRUE : right_bt.output;" + os.linesep
            + "\t\t\tesac;" + os.linesep
    )


def create_bt_parallel():
    return ("MODULE bt_parallel(success_threshold, left_bt, right_bt)" + os.linesep
            + "\tVAR" + os.linesep
            + "\t\tenable : boolean;" + os.linesep
            + "\t\tleft_bt_stored_output : { bt_output_none, bt_output_running, bt_output_false, bt_output_true};" + os.linesep
            + "\tASSIGN" + os.linesep
            + "\t\tleft_bt.enable := enable;" + os.linesep
            + "\t\tright_bt.enable := is_left_bt_active;" + os.linesep
            + "\t\tinit(left_bt_stored_output) := bt_output_none;" + os.linesep
            + "\t\tnext(left_bt_stored_output) :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\tis_left_bt_active : left_bt.output;" + os.linesep
            + "\t\t\t\tTRUE : left_bt_stored_output;" + os.linesep
            + "\t\t\tesac;" + os.linesep
            + "\tDEFINE" + os.linesep
            + "\t\tis_left_bt_active := (left_bt.output != bt_output_none);" + os.linesep
            + "\t\tis_right_bt_active := (right_bt.output != bt_output_none);" + os.linesep
            + "\t\ttrue_output_count :=" + os.linesep
            + "\t\tcount(left_bt_stored_output = bt_output_true, right_bt.output = bt_output_true);" + os.linesep
            + "\t\trunning_output_count :=" + os.linesep
            + "\t\tcount(left_bt_stored_output = bt_output_running, right_bt.output = bt_output_running);" + os.linesep
            + "\t\toutput :=" + os.linesep
            + "\t\t\tcase" + os.linesep
            + "\t\t\t\tis_right_bt_active & true_output_count >= success_threshold : bt_output_true;" + os.linesep
            + "\t\t\t\tis_right_bt_active & success_threshold > true_output_count + running_output_count : bt_output_false;" + os.linesep
            + "\t\t\t\tis_right_bt_active : bt_output_running;" + os.linesep
            + "\t\t\t\tTRUE : bt_output_none;" + os.linesep
            + "\t\t\tesac;" + os.linesep
    )

