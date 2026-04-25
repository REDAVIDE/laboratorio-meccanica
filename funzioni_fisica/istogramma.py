import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def crea_figura_istogramma(dati, n_bins, n_ticks, label_x, label_y, titolo, colore_barre, decimali):
    dati = np.array(dati)
    mu = np.mean(dati)
    std = np.std(dati, ddof=1)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Istogramma e Gaussiana
    ax.hist(dati, bins=n_bins, density=True, alpha=0.7, 
            color=colore_barre, edgecolor='white', linewidth=1, label='Dati Sperimentali')
    
    x_curva = np.linspace(min(dati) - 2*std, max(dati) + 2*std, 300)
    ax.plot(x_curva, norm.pdf(x_curva, mu, std), color='black', lw=2, label='Profilo Gaussiano')
    
    # Media e Sigma (senza testo sopra, come preferivi)
    ax.axvline(mu, color='black', linestyle='--', lw=1.5, label=rf'Media $\mu$: {mu:.{decimali}f}')
    y_pos_sigma = norm.pdf(mu + std, mu, std)
    ax.hlines(y=y_pos_sigma, xmin=mu, xmax=mu + std, color='black', 
              linestyle='-.', lw=2, label=rf'Deviazione $\sigma$: {std:.{decimali}f}')

    # Box per i Label
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor=colore_barre, alpha=0.3, edgecolor=colore_barre, linewidth=1.5)
    ax.set_xlabel(label_x, labelpad=20, bbox=bbox_props)
    ax.set_ylabel(label_y, labelpad=20, bbox=bbox_props)
    ax.set_title(titolo, fontweight='bold', fontstyle='italic', fontsize=15, pad=30)
    
    # --- NUOVA GESTIONE TICK X ---
    # Genera esattamente il numero di tick richiesti tra il minimo e il massimo
    ax.set_xticks(np.linspace(min(dati), max(dati), n_ticks))
    plt.xticks(rotation=45, fontsize=9)
    
    ax.legend(loc='best', shadow=True)
    ax.grid(True, linestyle=':', alpha=0.4)
    plt.tight_layout(pad=4.0)
    
    return fig