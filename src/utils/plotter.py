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
                   hamming_distance_history=None,
                   total_difference_history=None,  # ✅ NOVO PARÂMETRO
                   output_dir="data/results"):
    
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepaths = []
    
    # Cria diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
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
    plt.legend(fontsize=11)
    
    # Salvar segundo gráfico
    validity_filename = f"validity_evolution_{timestamp}.png"
    validity_filepath = os.path.join(output_dir, validity_filename)
    plt.savefig(validity_filepath, dpi=300, bbox_inches='tight')
    plt.close()
    filepaths.append(validity_filepath)
    
    # === GRÁFICO 3: Diversidade Hamming ===
    if hamming_distance_history is not None and len(hamming_distance_history) > 0:
        plt.figure(figsize=(10, 6))
        
        # Converter para array numpy
        hamming_array = np.array(hamming_distance_history)
        generations_array = np.array(generation_history[:len(hamming_distance_history)])
        
        # Plot da diversidade Hamming
        plt.plot(generations_array, hamming_array, 'm-', linewidth=2, 
                 label='Diversidade Hamming', alpha=0.8, marker='o', markersize=3)
        
        # Linhas de referência para interpretação
        plt.axhline(y=0.2, color='red', linestyle='--', alpha=0.5, linewidth=1,)
                   #label='Baixa diversidade (<20%)')
        plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, linewidth=1,)
                   #label='Diversidade moderada (50%)')
        plt.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, linewidth=1,)
                #    label='Alta diversidade (>80%)')
        
        # Preenchimento de áreas
        plt.fill_between(generations_array, 0, 0.2, alpha=0.1, color='red')
        plt.fill_between(generations_array, 0.2, 0.5, alpha=0.1, color='orange')
        plt.fill_between(generations_array, 0.5, 0.8, alpha=0.1, color='yellow')
        plt.fill_between(generations_array, 0.8, 1.0, alpha=0.1, color='green')
        
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('Diversidade Hamming Normalizada', fontsize=12)
        plt.title('Evolução da Diversidade Hamming - Algoritmo Genético UKP', 
                 fontsize=14, fontweight='bold')
        plt.ylim(0, 1.0)  # Escala de 0 a 1 (normalizada)
        plt.legend(fontsize=10, loc='upper right')
        plt.grid(True, alpha=0.3)
        
        # Adicionar estatísticas
        if len(hamming_array) > 0:
            avg_diversity = np.mean(hamming_array)
            final_diversity = hamming_array[-1]
            
            stats_text = (f'Média: {avg_diversity:.3f}\n'
                         f'Final: {final_diversity:.3f}')
            
            plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                    fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Salvar gráfico
        hamming_filename = f"hamming_diversity_{timestamp}.png"
        hamming_filepath = os.path.join(output_dir, hamming_filename)
        plt.savefig(hamming_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        filepaths.append(hamming_filepath)
    
    # === GRÁFICO 4: Diferença Total (NOVO!) ===
    if total_difference_history is not None and len(total_difference_history) > 0:
        plt.figure(figsize=(10, 6))
        
        # Converter para array numpy
        diff_array = np.array(total_difference_history)
        generations_array = np.array(generation_history[:len(total_difference_history)])
        
        # Plot da diferença total
        plt.plot(generations_array, diff_array, 'c-', linewidth=2, 
                 label='Diferença Total Média', alpha=0.8, marker='s', markersize=3)
        
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('Diferença Absoluta Média por Posição', fontsize=12)
        plt.title('Evolução da Magnitude das Diferenças - Algoritmo Genético UKP', 
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        # Adicionar linha de tendência (se houver dados suficientes)
        if len(diff_array) > 10:
            # Cria linha de tendência polinomial de grau 3
            z = np.polyfit(generations_array, diff_array, 3)
            p = np.poly1d(z)
            
            # Suaviza a linha de tendência
            smooth_gen = np.linspace(generations_array.min(), generations_array.max(), 300)
            plt.plot(smooth_gen, p(smooth_gen), 'r--', linewidth=2, 
                    alpha=0.6, label='Tendência')
            plt.legend(fontsize=11)
        
        # Estatísticas da diferença total
        if len(diff_array) > 0:
            avg_diff = np.mean(diff_array)
            final_diff = diff_array[-1]
            max_diff = np.max(diff_array)
            min_diff = np.min(diff_array)
            
            plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                    fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Salvar gráfico
        diff_filename = f"total_difference_{timestamp}.png"
        diff_filepath = os.path.join(output_dir, diff_filename)
        plt.savefig(diff_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        filepaths.append(diff_filepath)
    
    return filepaths