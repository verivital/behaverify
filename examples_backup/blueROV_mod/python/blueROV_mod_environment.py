import random
import serene_safe_assignment


class blueROV_mod_environment():
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
        self.fls_range = serene_safe_assignment.fls_range(random.choice(['danger_zone', 'safe']))
        self.obstacle_in_view = serene_safe_assignment.obstacle_in_view(random.choice([True, False]))
        self.battery = serene_safe_assignment.battery(random.choice([0, 1]))
        self.lec_dd_am = serene_safe_assignment.lec_dd_am(random.choice([True, False]))
        self.bb_rth = serene_safe_assignment.bb_rth(random.choice([True, False]))
        self.bb_geofence = serene_safe_assignment.bb_geofence(random.choice([True, False]))
        self.lec2_am_l = serene_safe_assignment.lec2_am_l(random.choice(['safe', 'speed', 'pipe', 'speed_pipe']))
        self.lec2_am_r = serene_safe_assignment.lec2_am_r(random.choice(['safe', 'speed', 'pipe', 'speed_pipe']))
        self.bb_pipelost = serene_safe_assignment.bb_pipelost(random.choice([True, False]))
        self.bb_sensor_failure = serene_safe_assignment.bb_sensor_failure(random.choice([True, False]))
        self.bb_waypoints_completed = serene_safe_assignment.bb_waypoints_completed(random.choice([True, False]))
        self.bb_home_dist = serene_safe_assignment.bb_home_dist(random.choice([10, 100]))
        self.rtreach_result = serene_safe_assignment.rtreach_result(random.choice(['safe', 'short', 'long', 'short_long']))
        return

    def check_tick_condition(self):
        return not (self.blackboard.BLUEROV_SURFACED)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.battery = serene_safe_assignment.battery(1)
        self.bb_geofence = serene_safe_assignment.bb_geofence(False)
        self.bb_home_dist = serene_safe_assignment.bb_home_dist(10)
        self.bb_pipelost = serene_safe_assignment.bb_pipelost(False)
        self.bb_rth = serene_safe_assignment.bb_rth(False)
        self.bb_sensor_failure = serene_safe_assignment.bb_sensor_failure(False)
        self.bb_waypoints_completed = serene_safe_assignment.bb_waypoints_completed(False)
        self.fls_range = serene_safe_assignment.fls_range('safe')
        self.lec_dd_am = serene_safe_assignment.lec_dd_am(False)
        self.lec2_am_l = serene_safe_assignment.lec2_am_l('safe')
        self.lec2_am_r = serene_safe_assignment.lec2_am_r('safe')
        self.obstacle_in_view = serene_safe_assignment.obstacle_in_view(False)
        self.rtreach_result = serene_safe_assignment.rtreach_result('safe')

    def check_waypoints_completed(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.bb_waypoints_completed == True)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.bb_waypoints_completed == True)

    def fls2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def fls2bb_read__0(self, node):
        return (self.fls_range == 'danger_zone')

    def fls_warning2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def fls_warning2bb_read__0(self, node):
        return (self.blackboard.bb_fls_warning or self.obstacle_in_view)

    def fls_warning2bb_read__1(self, node):
        return (self.blackboard.emergency_stop_warning or self.obstacle_in_view)

    def battery2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def battery2bb_read__0(self, node):
        return (self.battery <= 0)

    def ddlecam2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def ddlecam2bb_read__0(self, node):
        return self.lec_dd_am

    def rth2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def rth2bb_read__0(self, node):
        return (self.blackboard.bb_rth_warning or self.bb_rth)

    def geofence2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def geofence2bb_read__0(self, node):
        return (self.blackboard.bb_geofence_warning or self.bb_geofence)

    def lec2_am_l_2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def lec2_am_l_2bb_read__0(self, node):
        return ((self.lec2_am_l == 'speed') or (self.lec2_am_l == 'speed_pipe'))

    def lec2_am_l_2bb_read__1(self, node):
        return ((self.lec2_am_l == 'pipe') or (self.lec2_am_l == 'speed_pipe'))

    def lec2_am_r_2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def lec2_am_r_2bb_read__0(self, node):
        return ((self.lec2_am_r == 'speed') or (self.lec2_am_r == 'speed_pipe'))

    def lec2_am_r_2bb_read__1(self, node):
        return ((self.lec2_am_r == 'pipe') or (self.lec2_am_r == 'speed_pipe'))

    def pipe_lost2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def pipe_lost2bb_read__0(self, node):
        return (self.bb_pipelost and (self.blackboard.bb_mission == 'pipe_following'))

    def sensor_failure2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def sensor_failure2bb_read__0(self, node):
        return (self.blackboard.bb_sensor_failure_warning or self.bb_sensor_failure)

    def waypoints_completed2bb_read__condition(self, node):
        if True:
            return True
        else:
            return False


    def waypoints_completed2bb_read__0(self, node):
        return random.choice([True, False])

    def home2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def home2bb_read__0(self, node):
        return (self.blackboard.bb_home_reached or (self.bb_home_dist < 15))

    def rtreach2bb_read__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def rtreach2bb_read__0(self, node):
        return ((self.rtreach_result == 'long') or (self.rtreach_result == 'short_long'))

    def rtreach2bb_read__1(self, node):
        return ((self.rtreach_result == 'short') or (self.rtreach_result == 'short_long'))

    def obstacle_avoidance_read__condition(self, node):
        if True:
            return True
        else:
            return False


    def obstacle_avoidance_read__0(self, node):
        return random.choice([True, False])

    def mission_server_read__condition(self, node):
        if True:
            return True
        else:
            return False


    def mission_server_read__0(self, node):
        return (
            random.choice([True, False])
            if (self.blackboard.next_mission and self.blackboard.finished_missions) else
            (
            self.blackboard.finished_missions
        ))

    def mission_server_read2__condition(self, node):
        if True:
            return True
        else:
            return False


    def mission_server_read2__0(self, node):
        return (
            random.choice(['waypoint_following', 'e_stop', 'pipe_following'])
            if (self.blackboard.next_mission and not (self.blackboard.finished_missions)) else
            (
            self.blackboard.bb_mission
        ))

    def dd_lec_read__condition(self, node):
        if True:
            return True
        else:
            return False


    def dd_lec_read__0(self, node):
        return random.choice(['safe', 'z_warn', 'xy_warn'])
