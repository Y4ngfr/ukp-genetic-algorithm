import random
import numpy as np
from typing import List
from ..models.solution import Solution
from ..models.toy import global_toys, get_toy_by_id
from src.utils.plotter import plot_evolution

def upper_bound_greedy(toys, budget):
    """
    Limite superior: assume que pode produzir frações de brinquedos
    (relaxamento contínuo do problema)
    """
    # Calcula ROI de cada brinquedo
    toys_with_roi = []
    for toy in toys:
        roi = toy.profit() / toy.production_cost if toy.production_cost > 0 else 0
        toys_with_roi.append((toy, roi))
    
    # Ordena por ROI (maior primeiro)
    toys_with_roi.sort(key=lambda x: x[1], reverse=True)
    
    remaining_budget = budget
    max_profit = 0
    
    for toy, roi in toys_with_roi:
        if remaining_budget <= 0:
            break
        
        # Quantidade máxima que caberia no orçamento restante
        max_units = remaining_budget / toy.production_cost
        
        # Adiciona TODO o lucro possível deste brinquedo
        max_profit += max_units * toy.profit()
        remaining_budget -= max_units * toy.production_cost
    
    return max_profit

class GeneticAlgorithm:
    """Algoritmo genético para resolver o UKP"""
    
    def __init__(self, population_size=100, generations=1000, 
                 crossover_rate=0.8, mutation_rate=0.1,
                 selection_type='tournament', crossover_type='single_point', 
                 mutation_type='uniform', seed=None, penality=10):
        
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.budget = None
        self.toys = None
        self.penality = penality

        # Listas para armazenar histórico
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.generation_history = []
        self.validity_rate_history = []
        self.hamming_distance = []
        self.total_difference = []
        self.efficiency = []
        
        if seed is not None:
            random.seed(seed)


    
    def solve(self, toy_ids: List[int], budget: float) -> Solution:
        """Resolve o UKP usando algoritmo genético"""
        self.budget = budget
        self.toys = [get_toy_by_id(toy_id) for toy_id in toy_ids]
        
        # Inicializar população
        population = self._initialize_population()

        # Evoluir por gerações
        for generation in range(self.generations):
            print(f"gen {generation}")

            # Avaliar população
            fitness_values = [self._fitness(solution) for solution in population]
            
            # Armazenar métricas
            best_fitness = max(fitness_values)
            avg_fitness = sum(fitness_values) / len(fitness_values)
            valid_solutions = 0
            for solution in population:
                if solution.is_valid(self.budget):
                    valid_solutions += 1
            validity_rate = (valid_solutions / len(population)) * 100


            n_toys = len(population[0].quantities)
            num_pairs = 0
            differences = 0
            total_diff = 0
            for i in range(len(population)):
                for j in range(i+1, len(population)):
                    sol1 = population[i]
                    sol2 = population[j]

                    differences += sum(1 for a, b in zip(sol1.quantities, sol2.quantities) if a != b)
                    num_pairs += 1 

                    total_diff += sum(abs(a - b) for a, b in zip(sol1.quantities, sol2.quantities))


                    # normalized = differences / n_toys
                    # total_normalized_distance += normalized

            total_normalized_distance = differences / (n_toys * num_pairs)
            total_diff_normalized = total_diff / (n_toys * num_pairs)


            best_idx = fitness_values.index(best_fitness)
            best_solution = population[best_idx]
            best_efficiency = best_solution.total_profit() / best_solution.total_cost()
            
            self.efficiency.append(best_efficiency)    
            self.best_fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.generation_history.append(generation)
            self.validity_rate_history.append(validity_rate)
            self.hamming_distance.append(total_normalized_distance)
            self.total_difference.append(total_diff_normalized)

            # Selecionar pais
            parents = self._selection(population, fitness_values)
            
            # Criar nova população via crossover e mutação
            offspring = []
            for i in range(0, len(parents), 2):
                parent1 = parents[i]
                parent2 = parents[i + 1] if i + 1 < len(parents) else parents[0]
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                
                # Mutação
                child1 = self._mutation(child1, generation)
                child2 = self._mutation(child2, generation)
                
                offspring.extend([child1, child2])
            
            # Mantém os melhores (elitismo)
            fitness_values = [self._fitness(child) for child in offspring]
            indices_ordenados = sorted(range(len(offspring)), key=lambda i: fitness_values[i], reverse=True)
            population = [offspring[i] for i in indices_ordenados[:self.population_size]]

        # Retornar melhor solução
        fitness_values = [self._fitness(solution) for solution in population]
        best_idx = fitness_values.index(max(fitness_values))
        
        max_profit = upper_bound_greedy(self.toys,self.budget)

        # Gerar gráfico
        plot_path = None
        plot_path = plot_evolution(
            self.best_fitness_history,
            self.avg_fitness_history,
            self.validity_rate_history,
            self.generation_history,
            self.hamming_distance,
            self.total_difference,
            max_profit,
            self.efficiency
        )

        return population[best_idx]
    


    def _initialize_population(self) -> List[Solution]:
        """Cria população inicial com soluções aleatórias"""
        population = []
        for _ in range(self.population_size):
            quantities = []
            remaining_budget = self.budget
            
            for toy in self.toys:
                max_qty = int(remaining_budget / toy.production_cost)
                qty = random.randint(0, max_qty)
                quantities.append(qty)
                remaining_budget -= qty * toy.production_cost
            
            solution = Solution(self.toys, quantities)
            population.append(solution)
        
        return population
    
    def _fitness(self, solution: Solution) -> float:
        """Calcula fitness com penalização para soluções inválidas"""
        if solution.is_valid(self.budget):
            return solution.total_profit()
        else:
            # Penalização proporcional ao excesso de orçamento
            excess = solution.total_cost() - self.budget
            penalty = excess * self.penality  # Penalidade arbitrária
            return solution.total_profit() - penalty
    
    def _selection(self, population: List[Solution], fitness_values: List[float]) -> List[Solution]:
        """Seleciona pais baseado no tipo de seleção"""
        if self.selection_type == 'tournament':
            return self._tournament_selection(population, fitness_values)
        elif self.selection_type == 'roulette':
            return self._roulette_selection(population, fitness_values)
        else:
            return self._tournament_selection(population, fitness_values)
    
    def _tournament_selection(self, population: List[Solution], fitness_values: List[float]) -> List[Solution]:
        """Seleção por torneio (tamanho 3)"""
        selected = []
        tournament_size = 3
        
        for _ in range(len(population)):
            tournament_idx = random.sample(range(len(population)), tournament_size)
            best_idx = max(tournament_idx, key=lambda i: fitness_values[i])
            selected.append(population[best_idx])
        
        return selected
    
    def _roulette_selection(self, population: List[Solution], fitness_values: List[float]) -> List[Solution]:
        """Seleção por roleta (fitness proporcional)"""
        min_fitness = min(fitness_values)
        adjusted_fitness = [f - min_fitness + 1 for f in fitness_values]
        total_fitness = sum(adjusted_fitness)
        
        selected = []
        for _ in range(len(population)):
            pick = random.uniform(0, total_fitness)
            current = 0
            for i, fitness in enumerate(adjusted_fitness):
                current += fitness
                if current >= pick:
                    selected.append(population[i])
                    break
        
        return selected
    
    def _crossover(self, parent1: Solution, parent2: Solution) -> tuple:
        """Crossover entre dois pais"""
        if self.crossover_type == 'single_point':
            return self._single_point_crossover(parent1, parent2)
        elif self.crossover_type == 'two_point':
            return self._two_point_crossover(parent1, parent2)
        else:
            return self._single_point_crossover(parent1, parent2)
    
    def _single_point_crossover(self, parent1: Solution, parent2: Solution) -> tuple:
        """Crossover de um ponto"""
        crossover_point = random.randint(1, len(parent1.quantities) - 1)
        
        child1_qty = parent1.quantities[:crossover_point] + parent2.quantities[crossover_point:]
        child2_qty = parent2.quantities[:crossover_point] + parent1.quantities[crossover_point:]
        
        child1 = Solution(self.toys, child1_qty)
        child2 = Solution(self.toys, child2_qty)
        child1.invalidate_cache()
        child2.invalidate_cache()
        
        return child1, child2
    
    def _two_point_crossover(self, parent1: Solution, parent2: Solution) -> tuple:
        """Crossover de dois pontos"""
        point1 = random.randint(1, len(parent1.quantities) - 2)
        point2 = random.randint(point1 + 1, len(parent1.quantities) - 1)
        
        child1_qty = parent1.quantities[:point1] + parent2.quantities[point1:point2] + parent1.quantities[point2:]
        child2_qty = parent2.quantities[:point1] + parent1.quantities[point1:point2] + parent2.quantities[point2:]
        
        child1 = Solution(self.toys, child1_qty)
        child2 = Solution(self.toys, child2_qty)
        child1.invalidate_cache()
        child2.invalidate_cache()
        
        return child1, child2
    
    def _mutation(self, solution: Solution, generation: int) -> Solution:
        """Aplica mutação à solução"""
        if self.mutation_type == 'uniform':
            return self._uniform_mutation(solution)
        elif self.mutation_type == 'gaussian':
            return self._gaussian_mutation(solution)
        elif self.mutation_type == 'adaptative':
            return self._adaptive_mutation(solution, generation)
        else:
            return self._uniform_mutation(solution)
    
    def _uniform_mutation(self, solution: Solution) -> Solution:
        """Mutação uniforme: altera quantidade aleatória"""
        new_quantities = solution.quantities.copy()
        
        for i in range(len(new_quantities)):
            if random.random() < self.mutation_rate:
                max_qty = int(self.budget / self.toys[i].production_cost)
                new_quantities[i] = random.randint(0, max_qty)
        
        child = Solution(self.toys, new_quantities)
        child.invalidate_cache()
        return child
    
    def _gaussian_mutation(self, solution: Solution) -> Solution:
        """Mutação gaussiana: altera quantidade com variação pequena"""
        new_quantities = solution.quantities.copy()
        
        for i in range(len(new_quantities)):
            if random.random() < self.mutation_rate:
                delta = int(random.gauss(0, 2))
                new_qty = max(0, new_quantities[i] + delta)
                max_qty = int(self.budget / self.toys[i].production_cost)
                new_quantities[i] = min(new_qty, max_qty)
        
        child = Solution(self.toys, new_quantities)
        child.invalidate_cache()
        return child


    # def _adaptative_mutation(self, solution: Solution) -> Solution:
        # pass

    def _adaptive_mutation(self, solution: Solution, generation: int = None) -> Solution:
        """
        Mutação gaussiana com desvio padrão que varia com a geração:
        - Início: desvio ALTO (muita exploração)
        - Fim: desvio BAIXO (pouca exploração, muito refinamento)
        """
        new_quantities = solution.quantities.copy()
        
        for i in range(len(new_quantities)):
            if random.random() < self.mutation_rate:
                current_qty = new_quantities[i]
                max_qty = int(self.budget / self.toys[i].production_cost)
            
                if generation is not None and self.generations > 0:
                    progress = generation / self.generations  # 0 a 1
                    
                    # Desvio padrão decresce exponencialmente com as gerações
                    # Início: desvio alto (ex: 10-20% do valor atual)
                    # Fim: desvio baixo (ex: 1-2% do valor atual)
                    
                    # Opção 1: Linear (simples)
                    # max_std = 0.2  # 20% no início
                    # min_std = 0.02 # 2% no final
                    # std_dev_percent = max_std - (max_std - min_std) * progress
                    
                    # Opção 2: Exponencial (melhor!)
                    initial_std = 0.3    # 30% no início
                    final_std = 0.01     # 1% no final
                    decay_rate = 5.0     # Taxa de decaimento
                    std_dev_percent = final_std + (initial_std - final_std) * np.exp(-decay_rate * progress)
                    
                    # Opção 3: Por estágios (mais controlado)
                    # if progress < 0.3:        std_dev_percent = 0.25  # 25%
                    # elif progress < 0.6:      std_dev_percent = 0.1   # 10%
                    # elif progress < 0.8:      std_dev_percent = 0.05  # 5%
                    # else:                     std_dev_percent = 0.02  # 2%
                    
                else:
                    # Sem informação de geração, usa valor fixo
                    std_dev_percent = 0.1  # 10% padrão
                
                # ============================================
                # Aplica mutação gaussiana
                # ============================================
                if current_qty > 0:
                    # Desvio em unidades = porcentagem do valor atual
                    std_dev_units = max(1, int(current_qty * std_dev_percent))
                    
                    # Gerar delta gaussiano
                    delta = int(random.gauss(0, std_dev_units))
                    
                    # Aplicar delta
                    new_qty = current_qty + delta
                else:
                    # Se quantidade atual é 0, mutação especial
                    # Chance de começar a produzir este brinquedo
                    if random.random() < 0.3:  # 30% chance de ativar
                        # Começa com quantidade pequena
                        std_dev_units = max(1, int(max_qty * 0.05))  # 5% do máximo
                        new_qty = abs(int(random.gauss(std_dev_units, std_dev_units//2)))
                    else:
                        new_qty = 0  # Mantém zero
                
                # Garantir limites
                new_qty = max(0, new_qty)
                new_qty = min(new_qty, max_qty)
                
                # Ocasionalmente (5% chance), reiniciar completamente
                # Isso ajuda a escapar de ótimos locais
                if random.random() < 0.05:
                    new_qty = random.randint(0, max_qty)
                
                new_quantities[i] = new_qty
        
        child = Solution(self.toys, new_quantities)
        child.invalidate_cache()
        return child
    



# [1, 2, 3, 4]