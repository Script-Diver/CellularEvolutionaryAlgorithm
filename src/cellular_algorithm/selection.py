import math
import random
from abc import ABC, abstractmethod


class Selection(ABC):
    @abstractmethod
    def select(self, individuals, num, params):
        ...


class TournamentSelection(Selection):
    def __init__(self, tournament_size, parents_num):
        self.tournament_size = tournament_size
        self.parents_num = parents_num

    def get_winner(self, tournament, maximize):
        if maximize:
            return max(tournament, key=lambda individual: individual.fitness)
        else:
            return min(tournament, key=lambda individual: individual.fitness)

    def select(self, individuals, maximize):
        """
        Arguments:
            individuals: list of the individuals we choose from

        """
        parents = []
        for _ in range(self.parents_num):
            tournament = random.choices(individuals, k=self.tournament_size)
            winner = self.get_winner(tournament, maximize)
            parents.append(winner)
        return parents


class RouletteWheelSelection(Selection):
    ...


class RankSelection(Selection):
    def __init__(self, fraction=None, number=2):
        """
        Arguments:
            fraction: float  (0, 1)
            number: number of individuals that will be returned

        """
        assert bool(fraction) ^ bool(number), "Select one: fraction or number"
        if fraction:
            assert fraction > 0 and fraction < 1, "Fraction needs to be > 0 and < 1"
        self.fraction = fraction
        self.number = number

    def select(self, individuals, maximize):
        """
        Arguments:
            individuals: list of the individuals we choose from

        """
        # maximize = True => descending
        individuals = sorted(individuals, key=lambda x: x.fitness, reverse=maximize)
        if self.fraction:
            individuals_num = math.ceil(len(individuals) * self.fraction)
        else:
            individuals_num = self.number

        return individuals[:individuals_num]
