from src.utils.data_generator import DataGenerator as Dg
import argparse
import os


def create_parser():
    """Cria o parser de argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description="Unbounded Knapsack Problem com Algoritmo Genético")
    subparsers = parser.add_subparsers(dest='command', help='Comandos Disponíveis')

    # Comando para gerar instâncias
    generate_parser = subparsers.add_parser('generate', help='Gerar instância do problema')
    generate_parser.add_argument('--num_toys', type=int, default=10, help='Número de tipos de brinquedos')
    generate_parser.add_argument('--min_cost', type=float, default=1.0, help='Custo mínimo')
    generate_parser.add_argument('--max_cost', type=float, default=100.0, help='Custo máximo')
    generate_parser.add_argument('--min_margin', type=float, default=0.1, help='Margem de lucro mínima')
    generate_parser.add_argument('--max_margin', type=float, default=2.0, help='Margem de lucro máxima')
    generate_parser.add_argument('--seed', type=int, default=None, help='Seed para reprodutibilidade')
    generate_parser.add_argument('--output', type=str, default='data/instances/instance.csv', help='Arquivo de saída')

    # Comando para resolver
    solve_parser = subparsers.add_parser('solve', help='Resolver instância do problema')
    solve_parser.add_argument('--instance', type=str, required=True, help='Arquivo da instância')
    solve_parser.add_argument('--budget', type=float, required=True, help='Orçamento disponível')
    solve_parser.add_argument('--population', type=int, default=100, help='Tamanho da população')
    solve_parser.add_argument('--generations', type=int, default=1000, help='Número de gerações')
    solve_parser.add_argument('--crossover_rate', type=float, default=0.8, help='Taxa de crossover')
    solve_parser.add_argument('--mutation_rate', type=float, default=0.1, help='Taxa de mutação')
    solve_parser.add_argument('--selection_type', type=str, default='tournament', help='Tipo de seleção (tournament, roulette)')
    solve_parser.add_argument('--crossover_type', type=str, default='single_point', help='Tipo de crossover (single_point, two_point)')
    solve_parser.add_argument('--mutation_type', type=str, default='uniform', help='Tipo de mutação (uniform, gaussian)')
    solve_parser.add_argument('--seed', type=int, default=None, help='Seed para reprodutibilidade')

    return parser


def setup():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'generate':
        # Gera instância
        toys_ids = Dg.generate_toys(
            num_toys=args.num_toys,
            min_cost=args.min_cost,
            max_cost=args.max_cost,
            min_profit_margin=args.min_margin,
            max_profit_margin=args.max_margin,
            seed = args.seed
        )
        Dg.save_instance(toys_ids, args.output)
        print(f"Instância gerada com {args.num_toys} brinquedos em {args.output}")

    elif args.command == 'solve':
        # Resolve instância
        toys_ids = Dg.load_instance(args.instance)
        from src.algorithms.genetic_algorithm import GeneticAlgorithm
        
        ga = GeneticAlgorithm(
            population_size=args.population,
            generations=args.generations,
            crossover_rate=args.crossover_rate,
            mutation_rate=args.mutation_rate,
            selection_type=args.selection_type,
            crossover_type=args.crossover_type,
            mutation_type=args.mutation_type,
            seed=args.seed
        )
        
        best_solution = ga.solve(toys_ids, args.budget)
        print(best_solution)

        # salva na pasta data/solution com o mesmo nome do csv de instances
        base = os.path.basename (args.instance)
        caminho = os.path.join("data", "solutions", base)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)

        best_solution.save_to_csv(caminho)