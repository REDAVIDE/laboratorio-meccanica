import sympy as sp

def calcola_propagazione_simbolica(espressione_str):
    """
    Prende una stringa, ne calcola le derivate parziali e restituisce
    l'espressione simbolica dell'incertezza propagata.
    """
    # Trasforma la stringa in un'espressione matematica di SymPy
    # Trasformiamo anche pi in un simbolo noto, così non lo tratta come variabile
    expr = sp.sympify(espressione_str, locals={'pi': sp.pi})
    
    # Trova tutte le variabili libere (es. 'L', 'T', 'm') escludendo costanti matematiche
    simboli = list(expr.free_symbols)
    
    varianze_quadratura = []
    simboli_sigma = {}

    for sim in simboli:
        # Crea il simbolo dell'incertezza per questa variabile (es. sigma_L)
        nome_sigma = f"\\sigma_{{{sim.name}}}"
        sigma_sim = sp.Symbol(nome_sigma, positive=True)
        simboli_sigma[sim.name] = sigma_sim
        
        # Calcola la derivata parziale dell'espressione rispetto alla variabile
        derivata = sp.diff(expr, sim)
        
        # Aggiunge il termine (derivata * sigma)^2
        varianze_quadratura.append((derivata * sigma_sim)**2)
    
    # L'incertezza totale è la radice della somma in quadratura
    formula_incertezza = sp.sqrt(sum(varianze_quadratura))
    
    return {
        "espressione_base": expr,
        "formula_incertezza": formula_incertezza,
        "simboli_variabili": simboli,
        "simboli_sigma": simboli_sigma
    }

def valuta_formula(espressione_sympy, dizionario_valori):
    """
    Sostituisce i numeri dentro la formula simbolica e restituisce il risultato numerico.
    """
    risultato = espressione_sympy.evalf(subs=dizionario_valori)
    return float(risultato)