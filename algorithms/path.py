class Path:
    def __init__(self, positions, moves):
        self.positions = positions
        self.moves = moves
        self.turns = self.calculate_turns(moves)
        self.length = len(moves)
        self.feasibility_score = self.calculate_feasibility_score()

    def calculate_turns(self, moves):
        turns = 0
        for i in range(len(moves)-1):
            if moves[i] != moves[i+1]:
                turns += 1
        return turns
    
    def calculate_feasibility_score(self):
        # Lesser turns and shorter paths are more feasible
        complexity = self.length + self.turns
        if complexity == 0:
            return float('inf')
        return 1/complexity