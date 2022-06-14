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
