import random
import serene_safe_assignment


class ANSR_tree_environment():
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
        self.tar_x = serene_safe_assignment.tar_x((
            (self.tar_x if ((temp := random.randint(0, 2)) == 0) else (min(10, (self.tar_x + 1)) if temp == 1 else (max(0, (self.tar_x - 1)))))
            if (self.timer == 0) else
            (
            self.tar_x
        )))
        self.tar_y = serene_safe_assignment.tar_y((
            (self.tar_y if ((temp := random.randint(0, 2)) == 0) else (min(10, (self.tar_y + 1)) if temp == 1 else (max(0, (self.tar_y - 1)))))
            if (self.timer == 0) else
            (
            self.tar_y
        )))
        self.timer = serene_safe_assignment.timer((
            10
            if (self.timer == 0) else
            (
            max(0, (self.timer - 1))
        )))
        return

    def check_tick_condition(self):
        return not (self.blackboard.victory)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def tree_x(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing tree_x: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise ValueError('Index out of bounds when accessing tree_x: ' + str(index))
            tree_x = [2 for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(1, 5)]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing tree_x: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 2:
                    raise ValueError('Index out of bounds when accessing tree_x: ' + str(new_index))
                if type(new_value) is not int:
                    raise ValueError('Variable tree_x is type int. Got type(new_value)')
                tree_x[new_index] = new_value
            return tree_x[index]

        self.tree_x = tree_x


        def tree_y(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing tree_y: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise ValueError('Index out of bounds when accessing tree_y: ' + str(index))
            tree_y = [2 for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(1, 5)]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing tree_y: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 2:
                    raise ValueError('Index out of bounds when accessing tree_y: ' + str(new_index))
                if type(new_value) is not int:
                    raise ValueError('Variable tree_y is type int. Got type(new_value)')
                tree_y[new_index] = new_value
            return tree_y[index]

        self.tree_y = tree_y
        self.tar_x = serene_safe_assignment.tar_x((0 if ((temp := random.randint(0, 10)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10))))))))))))
        self.tar_y = serene_safe_assignment.tar_y((0 if ((temp := random.randint(0, 10)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10))))))))))))
        self.timer = serene_safe_assignment.timer(10)

    def target_in_sight(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x(0) - self.tar_x)) + abs((self.tree_y(0) - self.tar_y))) > 2) or ((self.tree_x(0) == self.blackboard.cur_x) and (self.tree_y(0) == self.blackboard.cur_y)) or ((self.tree_x(0) == self.tar_x) and (self.tree_y(0) == self.tar_y)) or ((self.tree_x(0) < self.blackboard.cur_x) and (self.tree_x(0) < self.tar_x)) or ((self.tree_y(0) < self.blackboard.cur_y) and (self.tree_y(0) < self.tar_y)) or ((self.tree_x(0) > self.blackboard.cur_x) and (self.tree_x(0) > self.tar_x)) or ((self.tree_y(0) > self.blackboard.cur_y) and (self.tree_y(0) > self.tar_y))) and (((abs((self.tree_x(1) - self.tar_x)) + abs((self.tree_y(1) - self.tar_y))) > 2) or ((self.tree_x(1) == self.blackboard.cur_x) and (self.tree_y(1) == self.blackboard.cur_y)) or ((self.tree_x(1) == self.tar_x) and (self.tree_y(1) == self.tar_y)) or ((self.tree_x(1) < self.blackboard.cur_x) and (self.tree_x(1) < self.tar_x)) or ((self.tree_y(1) < self.blackboard.cur_y) and (self.tree_y(1) < self.tar_y)) or ((self.tree_x(1) > self.blackboard.cur_x) and (self.tree_x(1) > self.tar_x)) or ((self.tree_y(1) > self.blackboard.cur_y) and (self.tree_y(1) > self.tar_y))))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x(0) - self.tar_x)) + abs((self.tree_y(0) - self.tar_y))) > 2) or ((self.tree_x(0) == self.blackboard.cur_x) and (self.tree_y(0) == self.blackboard.cur_y)) or ((self.tree_x(0) == self.tar_x) and (self.tree_y(0) == self.tar_y)) or ((self.tree_x(0) < self.blackboard.cur_x) and (self.tree_x(0) < self.tar_x)) or ((self.tree_y(0) < self.blackboard.cur_y) and (self.tree_y(0) < self.tar_y)) or ((self.tree_x(0) > self.blackboard.cur_x) and (self.tree_x(0) > self.tar_x)) or ((self.tree_y(0) > self.blackboard.cur_y) and (self.tree_y(0) > self.tar_y))) and (((abs((self.tree_x(1) - self.tar_x)) + abs((self.tree_y(1) - self.tar_y))) > 2) or ((self.tree_x(1) == self.blackboard.cur_x) and (self.tree_y(1) == self.blackboard.cur_y)) or ((self.tree_x(1) == self.tar_x) and (self.tree_y(1) == self.tar_y)) or ((self.tree_x(1) < self.blackboard.cur_x) and (self.tree_x(1) < self.tar_x)) or ((self.tree_y(1) < self.blackboard.cur_y) and (self.tree_y(1) < self.tar_y)) or ((self.tree_x(1) > self.blackboard.cur_x) and (self.tree_x(1) > self.tar_x)) or ((self.tree_y(1) > self.blackboard.cur_y) and (self.tree_y(1) > self.tar_y))))
