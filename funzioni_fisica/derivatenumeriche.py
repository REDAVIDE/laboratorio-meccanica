import numpy as np

def calcola_velocita_indipendente(x, t=None, dt_fisso=None):
    """
    Calcola la velocità prendendo i punti a 2 a 2 per evitare correlazioni.
    Se dt_fisso è fornito, usa la formula per tempi costanti e può generare 't' in automatico.
    """
    # Se i tempi non vengono forniti ma ho un dt_fisso, li genero da zero
    if t is None or len(t) == 0:
        if dt_fisso is not None:
            t = (np.arange(len(x)) + 1) * dt_fisso
        else:
            raise ValueError("Devi fornire i tempi o un dt_fisso!")

    v_list = []
    t_v_list = []
    
    for i in range(0, len(x) - 1, 2):
        x1, x2 = x[i], x[i+1]
        t1, t2 = t[i], t[i+1]
        
        # Scegli quale dt usare
        dt = dt_fisso if dt_fisso is not None else (t2 - t1)
        if dt == 0:
            continue
            
        v = (x2 - x1) / dt
        t_m = (t1 + t2) / 2.0 
        
        v_list.append(v)
        t_v_list.append(t_m)
        
    return np.array(t_v_list), np.array(v_list)

def calcola_accelerazione_indipendente(x, t=None, dt_fisso=None):
    """
    Calcola l'accelerazione prendendo i punti a 3 a 3. 
    Se dt_fisso è fornito, usa la formula semplificata: a = (x3 - 2x2 + x1) / dt^2
    """
    if t is None or len(t) == 0:
        if dt_fisso is not None:
            t = (np.arange(len(x)) + 1) * dt_fisso
        else:
            raise ValueError("Devi fornire i tempi o un dt_fisso!")

    a_list = []
    t_a_list = []
    
    for i in range(0, len(x) - 2, 3):
        x1, x2, x3 = x[i], x[i+1], x[i+2]
        t1, t2, t3 = t[i], t[i+1], t[i+2]
        
        if dt_fisso is not None:
            # FORMULA SEMPLIFICATA
            a = (x3 - 2.0*x2 + x1) / (dt_fisso**2)
        else:
            # FORMULA GENERALE
            dt1 = t2 - t1
            dt2 = t3 - t2
            dt31 = t3 - t1
            if dt1 == 0 or dt2 == 0 or dt31 == 0:
                continue
            a = 2.0 * ((x3 - x2)*dt1 - (x2 - x1)*dt2) / (dt31 * dt1 * dt2)
            
        t_m = t2 
        
        a_list.append(a)
        t_a_list.append(t_m)
        
    return np.array(t_a_list), np.array(a_list)
