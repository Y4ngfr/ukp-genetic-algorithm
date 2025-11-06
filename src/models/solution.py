from typing import List
from .toy import Toy

class Solution:
    """Printa a solução para o UKP"""
    
    def __init__(self, toys: List[Toy], quantities: List[int] = None):
        self.toys = toys    # todos os tipos de brinquedos

        if quantities:      # quantidades de cada tipo de brinquedo
            self.quantities = quantities
        else:
            self.quantities = [0] * len(toys)   # [0, 0, ..., 0] com len(toys) posições
    
    def total_cost(self) -> float:
        """Calcula o custo total da solução"""
        sum = 0
        for toy, qty in zip(self.toys, self.quantities):
            sum += toy.production_cost * qty
        return sum
    
    def total_profit(self) -> float:
        """Calcula o lucro total da solução"""
        sum = 0
        for toy, qty in zip(self.toys, self.quantities):
            sum += (toy.sale_price - toy.production_cost) * qty
        return sum
    
    def is_valid(self, budget: float) -> bool:
        """Verifica se a solução respeita o orçamento"""
        return self.total_cost() <= budget
    
    def __repr__(self):
        return f"Solution(cost={self.total_cost():.2f}, profit={self.total_profit():.2f}, quantities={self.quantities})"