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

def plot_evolution(best_fitness_history, avg_fitness_history, 
                   validity_rate_history, generation_history, 
                   output_dir="data/results"):
    
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepaths = []
    
    # === GRÁFICO 1: Fitness Evolution ===
    plt.figure(figsize=(10, 6))
    plt.plot(generation_history, best_fitness_history, 'b-', linewidth=2, 
             label='Melhor Fitness', alpha=0.8)
    plt.plot(generation_history, avg_fitness_history, 'r-', linewidth=1.5, 
             label='Média de Fitness', alpha=0.7)
    
    plt.xlabel('Geração', fontsize=12)
    plt.ylabel('Fitness', fontsize=12)
    plt.title('Evolução do Fitness - Algoritmo Genético UKP', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Salvar primeiro gráfico
    fitness_filename = f"fitness_evolution_{timestamp}.png"
    fitness_filepath = os.path.join(output_dir, fitness_filename)
    plt.savefig(fitness_filepath, dpi=300, bbox_inches='tight')
    plt.close()
    filepaths.append(fitness_filepath)
    
    # === GRÁFICO 2: Taxa de Soluções Válidas ===
    plt.figure(figsize=(10, 6))
    plt.plot(generation_history, validity_rate_history, 'g-', linewidth=2, 
             label='Taxa de Soluções Válidas', alpha=0.8)
    
    plt.xlabel('Geração', fontsize=12)
    plt.ylabel('Taxa de Soluções Válidas (%)', fontsize=12)
    plt.title('Evolução da Validade das Soluções - Algoritmo Genético UKP', fontsize=14, fontweight='bold')
    plt.ylim(0, 100)  # Taxa de 0% a 100%
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Linha horizontal de referência (80% de soluções válidas)
    plt.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='Meta (80%)')
    
    # Salvar segundo gráfico
    validity_filename = f"validity_evolution_{timestamp}.png"
    validity_filepath = os.path.join(output_dir, validity_filename)
    plt.savefig(validity_filepath, dpi=300, bbox_inches='tight')
    plt.close()
    filepaths.append(validity_filepath)
    
    return filepaths