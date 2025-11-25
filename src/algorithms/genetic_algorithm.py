import random
from typing import List
from ..models.solution import Solution
from ..models.toy import global_toys, get_toy_by_id


class GeneticAlgorithm:
    """Algoritmo genético para resolver o UKP"""
    
    def __init__(self, population_size=100, generations=1000, 
                 crossover_rate=0.8, mutation_rate=0.1,
                 selection_type='tournament', crossover_type='single_point', 
                 mutation_type='uniform', seed=None):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.budget = None
        self.toys = None
        
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
            # Avaliar população
            fitness_values = [self._fitness(solution) for solution in population]
            
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
                child1 = self._mutation(child1)
                child2 = self._mutation(child2)
                
                offspring.extend([child1, child2])
            
            population = offspring[:self.population_size]
        
        # Retornar melhor solução
        fitness_values = [self._fitness(solution) for solution in population]
        best_idx = fitness_values.index(max(fitness_values))
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
            penalty = excess * 2  # Penalidade arbitrária
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
    
    def _mutation(self, solution: Solution) -> Solution:
        """Aplica mutação à solução"""
        if self.mutation_type == 'uniform':
            return self._uniform_mutation(solution)
        elif self.mutation_type == 'gaussian':
            return self._gaussian_mutation(solution)
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