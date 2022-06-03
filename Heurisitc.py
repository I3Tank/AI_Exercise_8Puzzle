# in this class we have the two heuristics needed
class Heuristic:

    # static method to check the misplaced blocks
    @staticmethod
    def check_misplaced_blocks(state_to_check, goal_state):
        misplaced_blocks = 0

        for i in goal_state:
            if goal_state[i] != state_to_check[i]:
                misplaced_blocks += 1
        return misplaced_blocks

