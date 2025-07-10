import random
from abc import ABC, abstractmethod


class MarkovChain(ABC):
    @abstractmethod
    def next(self, curr):
        pass

    @abstractmethod
    def produce_complete(self, n, start):
        pass


class RhthymController(MarkovChain):
    def __init__(self, transitions):
        self.beats = [1, 0.5, 0.4]  # whole, half, quarter
        self.transitions = transitions

    def next(self, curr):
        probabilities = list(self.transitions[curr].values())
        next_beats = list(self.transitions[curr].keys())
        return random.choices(next_beats, weights=probabilities)[0]

    def produce_complete(self, n, start=1):
        current_beat = start
        beats = [start]

        for _ in range(n):
            next_beat = self.next(current_beat)
            beats.append(next_beat)
            current_beat = next_beat

        return beats
