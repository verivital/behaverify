import random
import serene_safe_assignment


class t700_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def pre_tick_environment_update(self):
        return

    def post_tick_environment_update(self):
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), max((-25), (min(50, max((-50), -((-1))))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                )))), (max(0, min(2, (min(50, max((-50), (29 + 29 + (min(50, max((-50), abs(self.blackboard.blDEFINE5(max(0, min(1, (-9)))))))) + (min(50, max((-50), abs(self.blackboard.blVAR3)))))))))), (
                    self.envDEFINE8(max(0, min(2, (-20))))
                    if (((-9) < (-22)) or True) else
                    (
                        'yes'
                        if (self.envDEFINE6() != 'both') else
                        (
                        'both'
                ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(2, 23)), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, (min(50, max((-50), ((-33) * self.blackboard.blVAR3)))))), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, 23)), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, (min(50, max((-50), ((-33) * self.blackboard.blVAR3)))))), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, 23)), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, (min(50, max((-50), ((-33) * self.blackboard.blVAR3)))))), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, 23)), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                )))), (max(0, min(2, (min(50, max((-50), ((-33) * self.blackboard.blVAR3)))))), (
                    self.envDEFINE6()
                    if (False or ((not True) or True)) else
                    (
                        self.envDEFINE6()
                        if False else
                        (
                        self.envDEFINE6()
                ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
                    self.envDEFINE6()
                    if ((not False) or True) else
                    (
                        self.envDEFINE8(max(0, min(2, (-43))))
                        if True else
                        (
                        'both'
                )))), (1, (
                    self.envDEFINE6()
                    if ((not False) or True) else
                    (
                        self.envDEFINE8(max(0, min(2, (-43))))
                        if True else
                        (
                        'both'
                ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [(
            'no'
            if (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] > (min(50, max((-50), min(5, 34))))) else
            (
                'yes'
                if (2 >= 3) else
                (
                'yes'
        ))) for _ in range(3)]
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, (-34))), (
                    'both'
                    if (([(((not False) or False) or (not ((False ^ True)))), (not (((self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 3)), 3)] < 4) ^ False)))].count(True)) > 5) else
                    (
                    'both'
                ))), (max(0, min(2, 29)), 'no')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val


        def envDEFINE6():
            return self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, self.blackboard.blVAR3)), 3)]

        self.envDEFINE6 = envDEFINE6


        def envDEFINE8(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing envDEFINE8: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise ValueError('Index out of bounds when accessing envDEFINE8: ' + str(index))
            envDEFINE8 = [self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-16))), 3)] for _ in range(3)]
            seen_indices = set()
            for (new_index, new_value) in [(max(0, min(2, ([((-3) <= (min(50, max((-50), (self.blackboard.blDEFINE7() + 50 + (-5)))))), (not ((True ^ False)))].count(True)))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, (min(50, max((-50), -(self.blackboard.blVAR3)))))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, ([((-3) <= (min(50, max((-50), (self.blackboard.blDEFINE7() + 50 + (-5)))))), (not ((True ^ False)))].count(True)))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, (min(50, max((-50), -(self.blackboard.blVAR3)))))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, ([((-3) <= (min(50, max((-50), (self.blackboard.blDEFINE7() + 50 + (-5)))))), (not ((True ^ False)))].count(True)))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, (min(50, max((-50), -(self.blackboard.blVAR3)))))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, ([((-3) <= (min(50, max((-50), (self.blackboard.blDEFINE7() + 50 + (-5)))))), (not ((True ^ False)))].count(True)))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    ))), (max(0, min(2, (min(50, max((-50), -(self.blackboard.blVAR3)))))), (
                        'yes'
                        if ((False or True) == (self.blackboard.blDEFINE5(max(0, min(1, (-17)))) >= (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3)))))) else
                        (
                        'no'
                    )))]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing envDEFINE8: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 3:
                    raise ValueError('Index out of bounds when accessing envDEFINE8: ' + str(new_index))
                if type(new_value) is not str:
                    raise ValueError('Variable envDEFINE8 is type str. Got type(new_value)')
                envDEFINE8[new_index] = new_value
            return envDEFINE8[index]

        self.envDEFINE8 = envDEFINE8

    def a1_read_after_0__condition(self, node):
        if (self.blackboard.blVAR3 > (min(50, max((-50), max(self.blackboard.blDEFINE5(max(0, min(1, (-23)))), self.blackboard.blDEFINE5(max(0, min(1, (-23))))))))):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return [(0, (
                    min(5, max(2, 43))
                    if ((True == False) and ((3 > self.blackboard.blDEFINE5(max(0, min(1, node.localVAR2)))) or False)) else
                    (
                    min(5, max(2, (min(50, max((-50), -((-7)))))))
                ))), (1, (
                    min(5, max(2, 43))
                    if ((True == False) and ((3 > self.blackboard.blDEFINE5(max(0, min(1, node.localVAR2)))) or False)) else
                    (
                    min(5, max(2, (min(50, max((-50), -((-7)))))))
                )))]

    def a2_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blDEFINE5(max(0, min(1, 39))))))) - self.blackboard.blDEFINE7())))))), 'yes'), (max(0, min(2, (-4))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, self.blackboard.blDEFINE7())), 3)])])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))) - (min(50, max((-50), (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 5)), 3)] * 2)))))))) - (-44))))))), self.envVAR1[serene_safe_assignment.index_func(max(0, min(2, (-4))), 3)]), (max(0, min(2, (min(50, max((-50), -(((-4) if (not ((False ^ True))) else 40))))))), (
                    'no'
                    if (self.blackboard.blDEFINE7() < 12) else
                    (
                        'no'
                        if ((-46) < ((min(50, max((-50), (self.blackboard.blDEFINE5(max(0, min(1, self.blackboard.blDEFINE7()))) + self.blackboard.blDEFINE5(max(0, min(1, self.blackboard.blDEFINE7()))))))) if ('no' != 'yes') else (min(50, max((-50), (20 + 20 + 20)))))) else
                        (
                        'yes'
                )))), (max(0, min(2, (min(50, max((-50), max((min(50, max((-50), min(self.blackboard.blDEFINE7(), self.blackboard.blDEFINE7())))), (min(50, max((-50), -((min(50, max((-50), min(0, 0)))))))))))))), (
                    'no'
                    if (self.blackboard.blDEFINE7() < 12) else
                    (
                        'no'
                        if ((-46) < ((min(50, max((-50), (self.blackboard.blDEFINE5(max(0, min(1, self.blackboard.blDEFINE7()))) + self.blackboard.blDEFINE5(max(0, min(1, self.blackboard.blDEFINE7()))))))) if ('no' != 'yes') else (min(50, max((-50), (20 + 20 + 20)))))) else
                        (
                        'yes'
                ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return
