class ToBlackboard(subscribers.ToBlackboard):
    def __init__(self):
        self.blackboard.battery_low_warning = False
    def update(self):
        status = super(ToBlackboard, self).update()
        if status == py_trees.common.Status.RUNNING:
            return status
        if self.blackboard.battery.batt_charge_remaining > self.failsafe_battery_low_threshold + 0.05:
            self.blackboard.battery_low_warning = False
        elif self.blackboard.battery.batt_charge_remaining < self.failsafe_battery_low_threshold:
            self.blackboard.battery_low_warning = True
        return status
