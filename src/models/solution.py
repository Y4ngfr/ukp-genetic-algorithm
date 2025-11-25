from typing import List
from .toy import Toy

class Solution:
    """Printa a solução para o UKP"""
    
    def __init__(self, toys: List[Toy], quantities: List[int] = None):
        self.toys = toys    # todos os tipos de brinquedos
        self._total_cost = None
        self._total_profit = None

        if quantities:      # quantidades de cada tipo de brinquedo
            self.quantities = quantities
        else:
            self.quantities = [0] * len(toys)   # [0, 0, ..., 0] com len(toys) posições
    
    def total_cost(self) -> float:
        """Calcula o custo total da solução"""
        if self._total_cost is None:
            self._total_cost = 0
            for toy, qty in zip(self.toys, self.quantities):
                self._total_cost += toy.production_cost * qty
        return self._total_cost
    
    def total_profit(self) -> float:
        """Calcula o lucro total da solução"""
        if self._total_profit is None:
            self._total_profit = 0
            for toy, qty in zip(self.toys, self.quantities):
                self._total_profit += toy.profit() * qty
        return self._total_profit

    def invalidate_cache(self):
        """Limpa o cache após mutação/crossover"""
        self._total_cost = None
        self._total_profit = None
    
    def is_valid(self, budget: float) -> bool:
        """Verifica se a solução respeita o orçamento"""
        return self.total_cost() <= budget
    
    def __repr__(self):
        return f"Solution(cost={self.total_cost():.2f}, profit={self.total_profit():.2f}, quantities={self.quantities})"