from src.utils.data_generator import DataGenerator as Dg
from src.models.solution import Solution as Sol


if __name__ == '__main__':





    toys = Dg.generate_toys(5, 10, 350, 0.2, 1)
    Dg.save_instance(toys, "data/instances/instance_1")

    toys2 = Dg.load_instance("data        # Resolve instância
/instances/instance_1")
    
    for toy in toys2:
        print(toy)
    print()

    solution_vec = [3, 12, 1, 15, 11]

    solution = Sol(toys2, solution_vec)

    print(solution)