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
    
global_toys = {}
next_toy_id = 0

def add_toy(name: str, production_cost: float, sale_price: float) -> Toy:
    global next_toy_id  # variavel global precisa ser declarada dentro da funcao
    
    toy = Toy(
        id = next_toy_id,
        name = name,
        production_cost=production_cost,
        sale_price=sale_price
    )
    global_toys[next_toy_id] = toy
    next_toy_id += 1
    return toy

def get_toy_by_id(toy_id: int) -> Toy:
    return global_toys.get(toy_id, None)

def remove_toy_by_id(toy_id: int):
    if toy_id in global_toys:
        del global_toys[toy_id]
    else:
        raise KeyError(f"Brinquedo com id {toy_id} nao encontrado.")