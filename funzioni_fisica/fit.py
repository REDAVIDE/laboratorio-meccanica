import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import to_rgba


def minimi_quadrati_pesati(x, y, sy):
    x, y, sy = np.array(x), np.array(y), np.array(sy)
    w = 1 / (sy**2)
    sum_w, sum_wx, sum_wy = np.sum(w), np.sum(w * x), np.sum(w * y)
    sum_wxx, sum_wxy = np.sum(w * x**2), np.sum(w * x * y)
    
    Delta = sum_w * sum_wxx - (sum_wx)**2
    m = (sum_w * sum_wxy - sum_wx * sum_wy) / Delta
    c = (sum_wxx * sum_wy - sum_wx * sum_wxy) / Delta
    
    sigma_m = np.sqrt(sum_w / Delta)
    sigma_c = np.sqrt(sum_wxx / Delta)
    cov_mc = -sum_wx / Delta
    
    residui = y - (m * x + c)
    chi2 = np.sum((residui / sy)**2)
    
    return m, c, sigma_m, sigma_c, cov_mc, residui, chi2


def plot_fit_completo(x, y, sy, m, c, sm, sc, cov,
                       label_x, label_y, titolo,
                       col_punti, col_retta, n_ticks,
                       decimali, mostra_inviluppo=False, k_sigma=1):

    fig, ax = plt.subplots(figsize=(9, 6))
    
    # Titolo e label (stile moderno)
    ax.set_title(titolo, fontweight='bold', fontsize=14, pad=15)

    # Definizione dello stile del box per le etichette
    box_label = dict(boxstyle="round,pad=0.3", fc=to_rgba(col_punti, alpha=0.25), ec=to_rgba(col_punti, alpha=0.6), lw=1.5)

    # Etichette assi con box
    ax.set_xlabel(label_x, fontsize=10, bbox=box_label, labelpad=12)
    ax.set_ylabel(label_y, fontsize=10, bbox=box_label, labelpad=12)

    # Forzatura decimali sui tick (così non cambiano a caso)
    ax.xaxis.set_major_formatter(FormatStrFormatter(f'%.{decimali}f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter(f'%.{decimali}f'))

    # Assi zero
    ax.axhline(0, color='gray', lw=1, ls='--', alpha=0.5)
    ax.axvline(0, color='gray', lw=1, ls='--', alpha=0.5)

    # Plot Dati
    ax.errorbar(x, y, yerr=sy, fmt='o', markersize=3, color=col_punti, 
                ecolor=col_punti, capsize=3, label='Dati Sperimentali', zorder=3)

    # Plot Retta
    x_min, x_max = min(x), max(x)
    dx = x_max - x_min
    
    # parte un po' prima dello zero (o del minimo) e finisce un po' dopo il massimo
    disegno_x_min = min(-0.2 * dx, x_min - 0.2 * dx)
    disegno_x_max = x_max + 0.2 * dx
    
    # Genera i punti per la retta e l'inviluppo su questo range esteso
    x_range = np.linspace(disegno_x_min, disegno_x_max, 500)


    fit_y = m * x_range + c
    ax.plot(x_range, fit_y, color=col_retta, lw=2, label='Retta di Best Fit', zorder=2)

    # Marker intercetta rosso a diamante
    ax.plot(0, c, marker='d', color=col_punti, markersize=6, label=f' c: {c:.{decimali}f} ± {sc:.{decimali}f}', zorder=5)

    # Legenda (m e c con i valori)
    ax.plot([], [], '-', color=col_punti, label=f' m: {m:.{decimali}f} ± {sm:.{decimali}f}')

    # Inviluppo
    if mostra_inviluppo:
        sigma_f = np.sqrt(sc**2 + (x_range**2)*(sm**2) + 2*x_range*cov)
        ax.fill_between(x_range, fit_y - k_sigma*sigma_f, fit_y + k_sigma*sigma_f,
                        color=col_retta, alpha=0.1, label=fr"Inviluppo {k_sigma}$\sigma$")


    # 1. LEGENDA 
    ax.legend(fontsize=9, loc='best', fancybox=True, shadow=True, framealpha=0.9)

    # Questo comando forza la visualizzazione di tutti e 4 i bordi
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)
        spine.set_color('black')
        spine.set_position(('outward', 0)) 

    # ASSI INTERNI (La croce grigia tratteggiata per l'intercetta)
    ax.axhline(0, color='black', lw=0.8, ls='--', alpha=0.4, zorder=1)
    ax.axvline(0, color='black', lw=0.8, ls='--', alpha=0.4, zorder=1)

    # GESTIONE MARGINI (Per non far finire l'asse Y sul bordo)
    x_min, x_max = min(x), max(x)
    dx = x_max - x_min
    # Impostiamo il limite sinistro un po' prima dello zero o del dato minimo
    ax.set_xlim(left=min(-0.1 * dx, x_min - 0.1*dx), right=x_max + 0.1*dx)

    # GRIGLIA E LAYOUT
    ax.grid(True, ls=':', alpha=0.5)
    ax.xaxis.set_major_locator(plt.MaxNLocator(n_ticks))
    
    plt.tight_layout() # Fondamentale per non tagliare i box dei label
    
    return fig


def plot_residui_migliorato(x, residui, sy, label_x, col_punti, col_retta, n_ticks, decimali):
    fig, ax = plt.subplots(figsize=(9, 4))
    
    # Linea dello zero
    ax.axhline(0, color=col_retta, lw=1.5, ls='-', alpha=0.8)
    
    # Punti dei residui
    ax.errorbar(x, residui, yerr=sy, fmt='o', color=col_punti, 
                ecolor=col_punti, capsize=3, markersize=5)
    
    ax.set_title("Distribuzione dei Residui", fontweight='bold', fontsize=12)

    box_label = dict(boxstyle="round,pad=0.3", fc=to_rgba(col_punti, alpha=0.25), ec=to_rgba(col_punti, alpha=0.6), lw=1.5)

    # Etichette assi con box
    ax.set_xlabel(label_x, fontsize=10, bbox=box_label, labelpad=12)
    ax.set_ylabel('Residui', fontsize=10, bbox=box_label, labelpad=12)
    
    ax.xaxis.set_major_formatter(FormatStrFormatter(f'%.{decimali}f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter(f'%.{decimali}f'))

    # Griglia e stile
    ax.grid(True, ls=':', alpha=0.6)
    ax.xaxis.set_major_locator(plt.MaxNLocator(n_ticks))
    
    return fig