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
        
    # Nome do arquivo
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"evolution_with_validity_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # === GRÁFICO 1: Fitness Evolution ===
    ax1.plot(generation_history, best_fitness_history, 'b-', linewidth=2, 
             label='Melhor Fitness', alpha=0.8)
    ax1.plot(generation_history, avg_fitness_history, 'r-', linewidth=1.5, 
             label='Média de Fitness', alpha=0.7)
    
    ax1.set_xlabel('Geração', fontsize=12)
    ax1.set_ylabel('Fitness', fontsize=12)
    ax1.set_title('Evolução do Fitness', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Estatísticas do fitness
    final_best = best_fitness_history[-1] if best_fitness_history else 0
    final_avg = avg_fitness_history[-1] if avg_fitness_history else 0
    improvement = ((final_best - best_fitness_history[0]) / best_fitness_history[0] * 100) if best_fitness_history and best_fitness_history[0] != 0 else 0
        
    # === GRÁFICO 2: Taxa de Soluções Válidas ===
    ax2.plot(generation_history, validity_rate_history, 'g-', linewidth=2, 
             label='Taxa de Soluções Válidas', alpha=0.8)
    
    ax2.set_xlabel('Geração', fontsize=12)
    ax2.set_ylabel('Taxa de Soluções Válidas (%)', fontsize=12)
    ax2.set_title('Evolução da Validade das Soluções', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 100)  # Taxa de 0% a 100%
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Linha horizontal de referência (80% de soluções válidas)
    ax2.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='Meta (80%)')
    
    # Estatísticas da validade
    final_validity = validity_rate_history[-1] if validity_rate_history else 0
    avg_validity = np.mean(validity_rate_history) if validity_rate_history else 0
    
    # Caixa de estatísticas para validade
    validity_stats = f'Taxa Final: {final_validity:.1f}%\nMédia Geral: {avg_validity:.1f}%\nObjetivo: ≥80%'
    ax2.text(0.02, 0.98, validity_stats, transform=ax2.transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
             fontsize=10)
    
    # Título geral
    fig.suptitle('Evolução do Algoritmo Genético - UKP com Análise de Validade', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    
    # Salvar
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filepath