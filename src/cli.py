from src.utils.data_generator import DataGenerator as Dg
import argparse
import sys

def create_parser():
    """Cria o parser de argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description="Unbounded Knapsack Problem com Algoritmo Genético")
    subparsers = parser.add_subparsers(dest='command', help='Comandos Disponíveis')

    # Comando para gerar instâncias
    generate_parser = subparsers.add_parser('generate', help='Gerar instância do problema')
    generate_parser.add_argument('--num_toys', type=int, default=10, help='Número de tipos de brinquedos')
    generate_parser.add_argument('--min_cost', type=float, default=1.0, help='Custo mínimo')
    generate_parser.add_argument('--max_cost', type=float, default=100.0, help='Custo máximo')
    generate_parser.add_argument('--min-margin', type=float, default=0.1, help='Margem de lucro mínima')
    generate_parser.add_argument('--max-margin', type=float, default=2.0, help='Margem de lucro máxima')
    generate_parser.add_argument('--output', type=str, default='data/instances/instance.csv', help='Arquivo de saída')

    # Comando para resolver
    solve_parser = subparsers.add_parser('solve', help='Resolver instância do problema')
    solve_parser.add_argument('--instance', type=str, required=True, help='Arquivo da instância')
    solve_parser.add_argument('--budget', type=float, required=True, help='Orçamento disponível')
    solve_parser.add_argument('--population', type=int, default=100, help='Tamanho da população')
    solve_parser.add_argument('--generations', type=int, default=1000, help='Número de gerações')
    solve_parser.add_argument('--crossover-rate', type=float, default=0.8, help='Taxa de crossover')
    solve_parser.add_argument('--mutation-rate', type=float, default=0.1, help='Taxa de mutação')

    return parser


def process_arguments():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'generate':
        # Gera instância
        toys = Dg.generate_toys(
            num_toys=args.num_toys,
            min_cost=args.min_cost,
            max_cost=args.max_cost,
            min_profit_margin=args.min_margin,
            max_profit_margin=args.max_margin
        )