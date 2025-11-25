import random
from typing import List
from ..models.toy import global_toys, add_toy

class DataGenerator:    # Classe utilitária (todos os métodos estáticos)
    """Gerador de instâncias do problema UKP"""
    
    @staticmethod
    def generate_toys(num_toys: int,            # tipos de brinquedos
                     min_cost: float,           # custo mínimo de um brinquedo 
                     max_cost: float,           # custo máximo de um brinquedo
                     min_profit_margin: float,  # percentual de lucro mínimo de um brinquedo
                     max_profit_margin: float,  # percentual de lucro máximo de um brinquedo
                     seed=None) -> List[int]:
        """
        Gera uma lista de brinquedos com parâmetros aleatórios
        """
        
        if seed is not None:
            random.seed(seed)
        
        generated_ids = []
        for _ in range(num_toys):
            cost = random.uniform(min_cost, max_cost)
            profit_margin = random.uniform(min_profit_margin, max_profit_margin)
            sale_price = cost + cost * profit_margin      # cost*profit_margin --> lucro em valor absoluto
            
            # adiciona o brinquedo no dicionario global/estatic de brinquedos
            toy = add_toy(
                name=f"Brinquedo_{len(global_toys) + 1}",
                production_cost=cost,
                sale_price=sale_price
            )
            generated_ids.append(toy.id)
        
        return generated_ids
    
    @staticmethod
    def save_instance(toys_ids: List[int], filename: str):
        """Salva uma instância em arquivo"""
        with open(filename, 'w') as f:
            f.write("id,name,cost,price\n")
            for toy_id in toys_ids:
                toy = global_toys[toy_id]
                f.write(f"{toy.id},{toy.name},{toy.production_cost:.2f},{toy.sale_price:.2f}\n")
    
    @staticmethod
    def load_instance(filename: str) -> List[int]:
        """Carrega uma instância de arquivo"""
        loaded_ids = []
        with open(filename, 'r') as f:
            next(f)  # Pula cabeçalho
            for line in f:
                id_str, name, cost_str, price_str = line.strip().split(',')
                toy = add_toy(
                    name=name,
                    production_cost=float(cost_str),
                    sale_price=float(price_str)
                )
                loaded_ids.append(toy.id)  # agora adiciona o id
        return loaded_ids