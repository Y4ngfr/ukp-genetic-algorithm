# Unbounded Knapsack Problem com Algoritmo Genético

Este projeto implementa uma solução para o Unbounded Knapsack Problem (UKP) utilizando Algoritmo Genético, desenvolvido como parte do Trabalho 1 da disciplina de Teoria da Computação.

## Descrição do Problema

O problema consiste em otimizar a produção de uma fábrica de brinquedos, determinando a quantidade ideal de cada tipo de brinquedo a ser produzida. As características do problema são:

- Cada tipo de brinquedo tem um custo de produção e um preço de venda
- Não há limite para a quantidade de cada tipo de brinquedo que pode ser produzido
- Existe um orçamento máximo disponível para produção
- O objetivo é maximizar o lucro total respeitando o orçamento

## Estrutura do Projeto

```
ukp-genetic-algorithm/
├── data/
│   └── instances/        # Instâncias do problema
├── src/
│   ├── algorithms/
│   │   └── genetic_algorithm.py  # Implementação do algoritmo genético parametrizável
│   ├── models/
│   │   ├── toy.py           # Classe Toy
│   │   └── solution.py      # Classe Solution
│   ├── utils/
│   │   └── data_generator.py     # Gerador de instâncias
│   └── cli.py               # Interface de linha de comando
└── main.py                 # Ponto de entrada da aplicação
```

## Como Usar

### Gerando uma Instância

```bash
python main.py generate --num_toys 10 --min_cost 1.0 --max_cost 100.0 --min_margin 0.1 --max_margin 2.0 --seed 42 --output data/instances/instance.csv
```

### Resolvendo uma Instância

```bash
python main.py solve --instance data/instances/instance.csv --budget 1000.0 --population 100 --generations 1000 --seed 42
```

## Parâmetros

### Geração de Instâncias
- `num_toys`: Número de tipos de brinquedos
- `min_cost`: Custo mínimo de produção
- `max_cost`: Custo máximo de produção
- `min_margin`: Margem de lucro mínima (percentual)
- `max_margin`: Margem de lucro máxima (percentual)
- `output`: Arquivo de saída para a instância
- `seed`: Seed para reprodutibilidade

### Algoritmo Genético
- `instance`: Arquivo da instância a ser resolvida
- `budget`: Orçamento disponível para produção
- `population`: Tamanho da população
- `generations`: Número de gerações
- `crossover_rate`: Taxa de crossover
- `mutation_rate`: Taxa de mutação
- `selection_type`: Tipo de seleção - tournament ou roulette (padrão: tournament)
- `crossover_type`: Tipo de crossover - single_point ou two_point (padrão: single_point)
- `mutation_type`: Tipo de mutação - uniform ou gaussian (padrão: uniform)
- `seed`: Seed para reprodutibilidade

## Desenvolvedores
- Adriam de Souza
- Cristhian de Avilla
- Francys dos Anjos
- Lucas Rodrigues
- Yang Rodrigues