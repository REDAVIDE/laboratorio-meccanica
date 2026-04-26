import numpy as np
import sympy as sp

def analizza_formula_calibrazione(formula_str):
    """
    Analizza la stringa della formula e restituisce i simboli (parametri) 
    escludendo la variabile 'x'.
    """
    expr = sp.sympify(formula_str)
    simboli = list(expr.free_symbols)
    
    x_sym = sp.Symbol('x')
    parametri = [s for s in simboli if s != x_sym]
    # Ordiniamo alfabeticamente
    parametri.sort(key=lambda s: s.name)
    
    return expr, x_sym, parametri

def esegui_calibrazione(expr, x_sym, parametri_valori, dati_grezzi):
    """
    Applica la formula ai dati.
    expr: espressione sympy
    x_sym: il simbolo della variabile x
    parametri_valori: dizionario {Symbol: valore}
    dati_grezzi: array numpy di dati
    """
    # Sostituisce i parametri fissi (A, B, ecc.)
    expr_finale = expr.subs(parametri_valori)
    
    # Trasforma in funzione numpy veloce
    f_numpy = sp.lambdify(x_sym, expr_finale, modules="numpy")
    
    # Ritorna i dati trasformati
    return f_numpy(dati_grezzi), expr_finale
