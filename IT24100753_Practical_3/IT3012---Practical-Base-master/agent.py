# agent.py
import random
from collections import deque
import heapq

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


class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    def get_successors(self, state, walls, grid_size):
        x, y = state
        w, h = grid_size
        successors = []
        for action, dx, dy in [('Up', 0, 1), ('Down', 0, -1), ('Left', -1, 0), ('Right', 1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in walls:
                successors.append(((nx, ny), action))
        return successors

    def bfs_search(self, start, goal, walls, grid_size):
        queue = deque([(start, [])])
        reached = {start}
        while queue:
            state, path = queue.popleft()
            if state == goal:
                return path
            for next_state, action in self.get_successors(state, walls, grid_size):
                if next_state not in reached:
                    reached.add(next_state)
                    queue.append((next_state, path + [action]))
        return []

    def dfs_search(self, start, goal, walls, grid_size):
        stack = [(start, [])]
        reached = {start}
        while stack:
            state, path = stack.pop()
            if state == goal:
                return path
            for next_state, action in self.get_successors(state, walls, grid_size):
                if next_state not in reached:
                    reached.add(next_state)
                    stack.append((next_state, path + [action]))
        return []

    def ucs_search(self, start, goal, walls, grid_size):
        pq = [(0, start, [])]
        reached = {start: 0}
        while pq:
            cost, state, path = heapq.heappop(pq)
            if state == goal:
                return path
            if cost > reached.get(state, float('inf')):
                continue
            for next_state, action in self.get_successors(state, walls, grid_size):
                new_cost = cost + 1
                if new_cost < reached.get(next_state, float('inf')):
                    reached[next_state] = new_cost
                    heapq.heappush(pq, (new_cost, next_state, path + [action]))
        return []

    def sense_and_act(self, percept):
        if not self.plan:
            all_food = percept.get('all_food', [])
            if not all_food:
                return 'Stay'
            
            start = percept.get('agent_pos', (0, 0))
            if isinstance(start, list):
                start = tuple(start)
                
            walls = set(percept.get('walls', []))
            grid_size = percept.get('grid_size', (10, 10))
            
            closest_food = min(all_food, key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1]))
            
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, closest_food, walls, grid_size)
                
        if self.plan:
            return self.plan.pop(0)
        return 'Stay'