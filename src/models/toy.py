class Toy:
    """Classe que representa um tipo de brinquedo"""
    
    def __init__(self, id: int, name: str, production_cost: float, sale_price: float):
        self.id = id
        self.name = name
        self.production_cost = production_cost  # custo de produção
        self.sale_price = sale_price            # preço do produto na venda
    
    def profit(self) -> float:
        """Calcula o lucro do brinquedo"""
        return self.sale_price - self.production_cost   # preço - custo
    
    def __repr__(self):
        """Função que define como o objeto será printado como string"""
        return f"Toy(id={self.id}, name='{self.name}', cost={self.production_cost}, price={self.sale_price})"