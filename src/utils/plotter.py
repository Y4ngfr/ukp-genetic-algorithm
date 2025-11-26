import matplotlib.pyplot as plt
import numpy as np
import os

def setup_matplotlib_for_plotting():
    """
    Setup matplotlib para plotting com configuração adequada.
    """
    import warnings
    warnings.filterwarnings('default')

    # Configurar matplotlib para modo não-interativo
    plt.switch_backend("Agg")

    # Definir estilo dos gráficos
    plt.style.use("default")
    
    # Configurar fontes
    plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["axes.unicode_minus"] = False

# Setup inicial
setup_matplotlib_for_plotting()

def plot_evolution_simple(best_fitness_history, avg_fitness_history, generation_history, output_dir="data/results"):
    """
    Gera um gráfico simples 2D da evolução do algoritmo genético.
    
    Args:
        best_fitness_history: Lista dos melhores fitness por geração
        avg_fitness_history: Lista das médias de fitness por geração  
        generation_history: Lista das gerações (0, 1, 2, ...)
        output_dir: Diretório para salvar o gráfico
    
    Returns:
        str: Caminho do arquivo salvo
    """
    
    # Criar diretório se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Nome do arquivo
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"evolution_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Criar gráfico
    plt.figure(figsize=(12, 8))
    
    # Plotar linhas
    plt.plot(generation_history, best_fitness_history, 'b-', linewidth=2, 
             label='Melhor Fitness', alpha=0.8)
    plt.plot(generation_history, avg_fitness_history, 'r-', linewidth=1.5, 
             label='Média de Fitness', alpha=0.7)
    
    # Configurações do gráfico
    plt.xlabel('Geração', fontsize=12)
    plt.ylabel('Fitness', fontsize=12)
    plt.title('Evolução do Algoritmo Genético - UKP', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Estatísticas finais
    final_best = best_fitness_history[-1] if best_fitness_history else 0
    final_avg = avg_fitness_history[-1] if avg_fitness_history else 0
    improvement = ((final_best - best_fitness_history[0]) / best_fitness_history[0] * 100) if best_fitness_history and best_fitness_history[0] != 0 else 0
    
    # Salvar
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filepath