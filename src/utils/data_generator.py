import random
from typing import List
from ..models.toy import Toy

class DataGenerator:    # Classe utilitária (todos os métodos estáticos)
    """Gerador de instâncias do problema UKP"""
    
    @staticmethod
    def generate_toys(num_toys: int,            # tipos de brinquedos
                     min_cost: float,           # custo mínimo de um brinquedo 
                     max_cost: float,           # custo máximo de um brinquedo
                     min_profit_margin: float,  # percentual de lucro mínimo de um brinquedo
                     max_profit_margin: float   # percentual de lucro máximo de um brinquedo
                     ) -> List[Toy]:
        """
        Gera uma lista de brinquedos com parâmetros aleatórios
        """
        
        toys = []
        for i in range(num_toys):
            cost = random.uniform(min_cost, max_cost)
            profit_margin = random.uniform(min_profit_margin, max_profit_margin)
            sale_price = cost + cost*profit_margin      # cost*profit_margin --> lucro em valor absoluto
            
            toy = Toy(
                id=i,
                name=f"Brinquedo_{i+1}",
                production_cost=cost,
                sale_price=sale_price
            )
            toys.append(toy)
        
        return toys
    
    @staticmethod
    def save_instance(toys: List[Toy], filename: str):
        """Salva uma instância em arquivo"""
        with open(filename, 'w') as f:
            f.write("id,name,cost,price\n")
            for toy in toys:
                f.write(f"{toy.id},{toy.name},{toy.production_cost:.2f},{toy.sale_price:.2f}\n")
    
    @staticmethod
    def load_instance(filename: str) -> List[Toy]:
        """Carrega uma instância de arquivo"""
        toys = []
        with open(filename, 'r') as f:
            next(f)  # Pula cabeçalho
            for line in f:
                id_str, name, cost_str, price_str = line.strip().split(',')
                toy = Toy(
                    id=int(id_str),
                    name=name,
                    production_cost=float(cost_str),
                    sale_price=float(price_str)
                )
                toys.append(toy)
        return toys