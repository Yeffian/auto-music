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

    def generate_bar(self, start=1, max_beats=4.0):
        curr = start
        rhythm = []
        total = 0.0

        while total < max_beats:
            remaining = max_beats - total
            # filter transitions to fit remaining duration
            valid_next = {k: v for k, v in self.transitions[curr].items() if abs(k) <= remaining}
            if not valid_next:
                break
            next_beat = random.choices(list(valid_next.keys()), weights=list(valid_next.values()))[0]
            rhythm.append(next_beat)
            total += abs(next_beat)
            curr = next_beat

        return rhythm