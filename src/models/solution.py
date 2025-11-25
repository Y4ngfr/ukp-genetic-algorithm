from typing import List
from .toy import Toy
import csv

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
            lines = []
            lines.append("=== SOLUCAO ===")
            lines.append(f"Custo total: R$ {self.total_cost():.2f}")
            lines.append(f"Lucro total: R$ {self.total_profit():.2f}")
            lines.append("")

            # Cabeçalho da tabela
            lines.append(f"{'Brinquedo':16}    {'Qtd':>5}    {'Custo de Prod':>14}    {'Lucro':>10}")
            lines.append("-" * 55)

            gap = " " * 4
            # Linhas por brinquedo
            for toy, qty in zip(self.toys, self.quantities):
                if qty > 0:
                    production_cost = toy.production_cost * qty
                    profit_total = toy.profit() * qty
                    lines.append(
                        f"{toy.name:16}    "
                        f"{qty:5d}    "
                        f"R$ {production_cost:11.2f}    "
                        f"R$ {profit_total:7.2f}"
                    )

            # Caso nenhuma quantidade tenha sido produzida
            if all(q == 0 for q in self.quantities):
                lines.append("(nenhum brinquedo produzido)")

            return "\n".join(lines)
        #return f"Solution (custo = {self.total_cost():.2f}, lucro = {self.total_profit():.2f}, quantities={self.quantities})"

    def save_to_csv(self, filename: str):
        """Salva os brinquedos usados na solução como CSV."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Cabeçalho
            writer.writerow([
                "id",
                "name",
                "unit_cost",
                "unit_price",
                "unit_profit",
                "qty",
                "total_cost",
                "total_profit"
            ])

            # Linhas de dados
            for toy, qty in zip(self.toys, self.quantities):
                if qty > 0:
                    unit_profit = toy.profit()
                    total_production_cost = toy.production_cost * qty
                    total_profit = unit_profit * qty

                    writer.writerow([
                        toy.id,
                        toy.name,
                        f"{toy.production_cost:.2f}",
                        f"{toy.sale_price:.2f}",
                        f"{unit_profit:.2f}",
                        qty,
                        f"{total_production_cost:.2f}",
                        f"{total_profit:.2f}"
                    ])