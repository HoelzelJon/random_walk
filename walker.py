import numpy as np
import random as rng

class walker:
    def __init__(self, dimension, num_walkers=1, record_steps=False):
        self.dim = dimension
        self.num = num_walkers
        self.coord = [np.zeros(dimension, dtype=int) for w in range(num_walkers)]

        self.maxes = np.zeros(dimension, dtype=int)
        self.mins = np.zeros(dimension, dtype=int)

        self.recording = record_steps
        if (record_steps):
            self.path = [[self.coord[w].copy()] for w in range(num_walkers)]

    def take_steps(self, num_steps):
        for i in range(num_steps):
            self.take_step()

    def take_step(self):
        for w in range(self.num):
            rand = rng.randint(0, (self.dim * 2) - 1)
            idx = rand // 2

            if rand % 2 == 0:
                self.coord[w][idx] += 1

                if self.coord[w][idx] > self.maxes[idx]:
                    self.maxes[idx] = self.coord[w][idx]
            else:
                self.coord[w][idx] -= 1

                if self.coord[w][idx] < self.mins[idx]:
                    self.mins[idx] = self.coord[w][idx]

            if (self.recording):
                self.path[w].append(self.coord[w].copy())

    def get_path_matrix(self):
        if not self.recording:
            return None

        matrix = np.zeros([self.maxes[i] - self.mins[i] + 1 for i in range(self.dim)])

        for steps in self.path:
            for step in steps:
                matrix[tuple(step - self.mins)] += 1

        return matrix, -self.mins
