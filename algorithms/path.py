from regression import regress

class Path:
    def __init__(self, positions, moves):
        self.positions = positions
        self.moves = moves
        self.turns = self.calculate_turns(moves)
        self.length = len(moves)
        self.optimized_length, self.optimized_turns = self.optimize_length_and_turns()
        self.feasibility_score = self.calculate_feasibility_score()

    def calculate_turns(self, moves):
        turns = 0
        for i in range(len(moves)-1):
            if moves[i] != moves[i+1]:
                turns += 2 # Each change in direction counts as two 45 degree turns
                # Note that reverse turns won't exsist in this list since we removed loops.
        return turns
    
    def optimize_length_and_turns(self):
        # Optimally, the mouse should move diagonally whenever there are consecutive alternate horizontal or vertical moves
        optimized_length = self.length
        optimized_turns = self.turns
        streak = 0
        i = 0
        while i < len(self.moves) - 2:
            if(self.moves[i] != self.moves[i+1] and self.moves[i] == self.moves[i+2]):
                streak += 1
                i += 2
            else:
                optimized_length = optimized_length - 2*streak + streak*2**0.5  # Each streak of 2 turns can be optimized to a single diagonal move
                if streak > 0:
                    optimized_turns = optimized_turns - 4*streak + 2 # No turns for diagonal moves
                streak = 0
                i += 1
        return optimized_length, optimized_turns


    def calculate_feasibility_score(self):
        # Lesser turns and shorter paths are more feasible
        weight_length, weight_turns, intercept = regress()
        time = weight_length * self.optimized_length + weight_turns * self.optimized_turns + intercept
        if time == 0:
            return float('inf')
        return 1 / (time)