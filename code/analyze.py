import math
import numpy as np
from typing import Tuple


class Analyze:
    def __init__(self, mu, teta, lam, queue_size=12, is_expnential=True) -> None:
        self.mu: float = mu
        self.teta: float = teta
        self.lam: int = lam
        self.queue_size: int = queue_size
        self.is_expnential = is_expnential
        self.PB = 0
        self.PD = 0

    def CalculateGama(self, n):
        return self.exponentialGama(n) if self.is_expnential else self.constantGama(n)

    def exponentialGama(self, n):
        return n/self.teta if n > 0 else 0

    def constantGama(self, n):
        return self.mu / ((math.e ** (self.mu * self.teta / n)) - 1) if n > 0 else 0

    def calculatePB(self):
        self.PB = self.calculateP0() * (self.lam ** self.queue_size)/np.prod([(self.mu + self.CalculateGama(i)) for i in range(1,13)])
        return self.PB

    def calculateP0(self):
        return 1 / (1 + sum([(self.lam ** i)/np.prod([(self.mu + self.CalculateGama(j)) for j in range(1,i+1)]) for i in range(1, 13)]))

    def calculatePD(self):
        self.PD = (1 - (self.mu/self.lam) * (1 - self.calculateP0())) - self.PB
        return self.PD

    def analyze(self) -> Tuple[float, float]:
        self.calculatePB()
        self.calculatePD()
        return self.PB, self.PD
