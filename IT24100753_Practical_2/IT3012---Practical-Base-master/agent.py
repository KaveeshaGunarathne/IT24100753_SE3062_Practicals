# agent.py
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept.get('agent_pos', [0, 0])
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:
    def sense_and_act(self, percept):
        if percept.get('food_here'):
            return 'eat'
        elif percept.get('wall_ahead'):
            return 'turn_left'
        else:
            return 'move_forward'

class ModelBasedAgent:
    def __init__(self):
        self.visited_cells = set()
        self.pos = (0, 0)
        self.direction = 'UP'
        self.last_action = None

    def sense_and_act(self, percept):
        if self.last_action == 'move_forward':
            if self.direction == 'UP': self.pos = (self.pos[0], self.pos[1] + 1)
            elif self.direction == 'DOWN': self.pos = (self.pos[0], self.pos[1] - 1)
            elif self.direction == 'LEFT': self.pos = (self.pos[0] - 1, self.pos[1])
            elif self.direction == 'RIGHT': self.pos = (self.pos[0] + 1, self.pos[1])
        elif self.last_action == 'turn_left':
            if self.direction == 'UP': self.direction = 'LEFT'
            elif self.direction == 'LEFT': self.direction = 'DOWN'
            elif self.direction == 'DOWN': self.direction = 'RIGHT'
            elif self.direction == 'RIGHT': self.direction = 'UP'
            
        self.visited_cells.add(self.pos)

        if percept.get('food_here'):
            self.last_action = 'eat'
        elif percept.get('wall_ahead'):
            self.last_action = 'turn_left'
        else:
            next_pos = self.pos
            if self.direction == 'UP': next_pos = (self.pos[0], self.pos[1] + 1)
            elif self.direction == 'DOWN': next_pos = (self.pos[0], self.pos[1] - 1)
            elif self.direction == 'LEFT': next_pos = (self.pos[0] - 1, self.pos[1])
            elif self.direction == 'RIGHT': next_pos = (self.pos[0] + 1, self.pos[1])
            
            if next_pos in self.visited_cells:
                self.last_action = 'turn_left'
            else:
                self.last_action = 'move_forward'

        return self.last_action