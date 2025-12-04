import matplotlib.pyplot as plt
import numpy as np
import os
import time

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
                   hamming_distance_history=None,
                   total_difference_history=None,
                   max_profit=None,
                   efficiency_history=None,
                   output_dir="data/results"):
    """
    Gera múltiplos gráficos de evolução do algoritmo genético.
    
    max_profit: Limite superior teórico de lucro (não deve aparecer no gráfico 1)
    """
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepaths = []
    
    # Cria diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # === GRÁFICO 1: Evolução do Fitness ===
    plt.figure(figsize=(10, 6))
    plt.plot(generation_history, best_fitness_history, 'b-', linewidth=2, 
             label='Melhor Fitness', alpha=0.8)
    plt.plot(generation_history, avg_fitness_history, 'r-', linewidth=1.5, 
             label='Média de Fitness', alpha=0.7)
    
    # NOTA: max_profit é ROI teórico, NÃO deve aparecer aqui como limite de fitness
    
    plt.xlabel('Geração', fontsize=12)
    plt.ylabel('Fitness (Lucro Total)', fontsize=12)
    plt.title('Evolução do Fitness - Algoritmo Genético UKP', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Salvar gráfico
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
    plt.title('Evolução da Validade das Soluções', fontsize=14, fontweight='bold')
    plt.ylim(0, 100)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    validity_filename = f"validity_evolution_{timestamp}.png"
    validity_filepath = os.path.join(output_dir, validity_filename)
    plt.savefig(validity_filepath, dpi=300, bbox_inches='tight')
    plt.close()
    filepaths.append(validity_filepath)
    
    # === GRÁFICO 3: Diversidade Hamming ===
    if hamming_distance_history is not None and len(hamming_distance_history) > 0:
        plt.figure(figsize=(10, 6))
        
        hamming_array = np.array(hamming_distance_history)
        generations_array = np.array(generation_history[:len(hamming_distance_history)])
        
        plt.plot(generations_array, hamming_array, 'm-', linewidth=2, 
                 label='Diversidade Hamming', alpha=0.8)
        
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('Diversidade Hamming Normalizada', fontsize=12)
        plt.title('Evolução da Diversidade Hamming', fontsize=14, fontweight='bold')
        plt.ylim(0, 1.0)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        hamming_filename = f"hamming_diversity_{timestamp}.png"
        hamming_filepath = os.path.join(output_dir, hamming_filename)
        plt.savefig(hamming_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        filepaths.append(hamming_filepath)
    
    # === GRÁFICO 4: Diferença Total ===
    if total_difference_history is not None and len(total_difference_history) > 0:
        plt.figure(figsize=(10, 6))
        
        diff_array = np.array(total_difference_history)
        generations_array = np.array(generation_history[:len(total_difference_history)])
        
        plt.plot(generations_array, diff_array, 'c-', linewidth=2, 
                 label='Diferença Total Média', alpha=0.8)
        
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('Diferença Absoluta Média por Posição', fontsize=12)
        plt.title('Evolução da Magnitude das Diferenças', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        diff_filename = f"total_difference_{timestamp}.png"
        diff_filepath = os.path.join(output_dir, diff_filename)
        plt.savefig(diff_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        filepaths.append(diff_filepath)
    
    # === GRÁFICO 5: Eficiência (ROI) com Linha do ROI Teórico Máximo ===
    if efficiency_history is not None and len(efficiency_history) > 0:
        plt.figure(figsize=(10, 6))
        
        efficiency_array = np.array(efficiency_history)
        generations_array = np.array(generation_history[:len(efficiency_history)])
        
        # Plot da eficiência (ROI)
        plt.plot(generations_array, efficiency_array, 'purple', linewidth=2, 
                 label='ROI Real (Lucro/Custo)', alpha=0.8)
        
        # Adiciona linha do ROI teórico máximo (max_profit)
        if max_profit is not None:
            # max_profit é o ROI teórico máximo
            plt.axhline(y=max_profit, color='green', linestyle='--', 
                       linewidth=2, alpha=0.7, 
                       label=f'ROI Teórico Máximo: {max_profit:.2f}')
        
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('ROI (Lucro Total / Custo Total)', fontsize=12)
        plt.title('Evolução da Eficiência (ROI) com Referência Teórica', 
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        efficiency_filename = f"efficiency_evolution_{timestamp}.png"
        efficiency_filepath = os.path.join(output_dir, efficiency_filename)
        plt.savefig(efficiency_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        filepaths.append(efficiency_filepath)
    
    return filepaths