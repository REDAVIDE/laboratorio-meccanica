import numpy as np

def analisi_statistica_completa(dati_lista):
    dati = np.array(dati_lista)
    n = len(dati)
    media = np.mean(dati)
    varianza_camp = np.var(dati, ddof=1)
    dev_std_camp = np.std(dati, ddof=1)
    sigma_a = dev_std_camp / np.sqrt(n)
    
    return {
        "n": n,
        "media": media,
        "varianza": varianza_camp,
        "std": dev_std_camp,
        "sigma_a": sigma_a
    }

def calcola_quadratura(s1, s2):
    """Somma in quadratura di due incertezze."""
    return np.sqrt(s1**2 + s2**2)

def incertezza_strumentale_rettangolare(risoluzione):
    """Calcola R/sqrt(12)."""
    return risoluzione / np.sqrt(12)

def calcola_sigma_b_totale(sigma_instr, sigma_offset):
    """Somma in quadratura l'incertezza dello strumento e dell'offset."""
    return np.sqrt(sigma_instr**2 + sigma_offset**2)

def calcola_media_pesata(valori, incertezze):
    x = np.array(valori)
    sigma = np.array(incertezze)
    pesi = 1 / (sigma**2)
    media_p = np.sum(x * pesi) / np.sum(pesi)
    sigma_p = 1 / np.sqrt(np.sum(pesi))
    return media_p, sigma_p

def genera_misure_gaussiane(dati_base, n_totale):
    dati = np.array(dati_base)
    media = np.mean(dati)
    std = np.std(dati, ddof=1)
    
    n_mancanti = n_totale - len(dati)
    if n_mancanti <= 0:
        return dati.tolist()
    
    # Generazione pura senza limiti forzati
    nuovi_dati = np.random.normal(loc=media, scale=std, size=n_mancanti)
    
    dati_completi = np.concatenate((dati, nuovi_dati))
    np.random.shuffle(dati_completi)
    
    return dati_completi.tolist()