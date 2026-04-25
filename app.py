import streamlit as st
import numpy as np
import sympy as sp

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Laboratorio di Meccanica", layout="wide", page_icon="⚛️")

#  region--- IMPORTAZIONE MODULI DAL TUO PACCHETTO ---
try:
    from funzioni_fisica.statistica import (
        analisi_statistica_completa, 
        calcola_quadratura, 
        incertezza_strumentale_rettangolare,
        calcola_sigma_b_totale,
        calcola_media_pesata,
        genera_misure_gaussiane
    )
except ImportError:
    st.error("Errore: Non trovo il modulo 'funzioni_fisica.statistica'. Verifica la struttura delle cartelle.")
    
try:
    from funzioni_fisica.propagazione import calcola_propagazione_simbolica, valuta_formula
except ImportError:
    st.error("Errore nell'importazione dei moduli di propagazione.")

try:
    from funzioni_fisica.fit import minimi_quadrati_pesati, plot_fit_completo, plot_residui_migliorato
except ImportError:
    st.error("Errore: Modulo fit non trovato.")
import io # Serve per scaricare i grafici

# endregion

# region GESTIONE MODULI
# Inizializza il modulo corrente se non esiste ancora
if 'modulo_scelto' not in st.session_state:
    st.session_state.modulo_scelto = "Home"

# Funzione per cambiare modulo dai tasti della Home
def cambia_modulo(nome_modulo):
    st.session_state.modulo_scelto = nome_modulo
    
#endregion

# region --- SIDEBAR ---
modulo = st.sidebar.radio(
    "Seleziona Modulo:", 
    ["Home", "Statistica Base", "Istogrammi", "Generatore Misure", "Fit Lineare", "Media Pesata", "Propagazione Incertezze"],
    key="modulo_scelto",
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Impostazioni")
decimali = st.sidebar.slider("Cifre decimali:", 2, 10, 4)

st.sidebar.markdown("---")
st.sidebar.text_area("Appunti di Laboratorio:", placeholder="Scrivi qui i tuoi promemoria...")

# endregion

# --- LOGICA DEI MODULI ---

if modulo == "Home":
    st.title("⚛️ Laboratorio Digitale di Fisica")
    st.subheader("Benvenuto! Seleziona un'area di analisi:")

    # Creazione di card con colonne
    col1, col2 = st.columns(2)

    with col1:
        st.info("### 📊 Statistica Base")
        st.write("Calcolo media, deviazioni standard, correzione offset e propagazione delle incertezze in quadratura.")
        st.button("Apri Statistica", on_click=cambia_modulo, args=("Statistica Base",))

    with col2:
        st.success("### 📈 Istogrammi")
        st.write("Visualizza la distribuzione dei tuoi dati con fit gaussiani professionali e personalizzazione estetica totale.")
        st.button("Apri Istogrammi", on_click=cambia_modulo, args=("Istogrammi",))
        
    st.divider()
    
    col3, col4 = st.columns(2)
    with col3:
        st.warning("### 🪄 Generatore")
        st.write("Simula esperimenti generando misure gaussiane a partire da un piccolo campione reale.")
        st.button("Apri Generatore", on_click=cambia_modulo, args=("Generatore Misure",))
    
    with col4:
        st.error("### 📉 Fit Lineare")
        st.write("Analisi dei dati tramite minimi quadrati, calcolo di pendenza, intercetta e residui.")
        st.button("Apri Fit Lineare", on_click=cambia_modulo, args=("Fit Lineare",))

    st.divider()

    col5, col6 = st.columns(2)
    with col5:
        st.info("### ⚖️ Media Pesata")
        st.write(fr"Calcolo di media e incertezza pesata, nel caso di $\sigma_i$ diverse.")
        st.button("Apri Media Pesata", on_click=cambia_modulo, args=("Media Pesata",))

    with col6:
        st.success("### 🧮 Propagazione Incertezze")
        st.write("Calcolo della formula di propagazione a partire dalla definizione di una osservabile (ad esempio g), e risultato numerico.")
        st.button("Apri Propagazione", on_click=cambia_modulo, args=("Propagazione Incertezze",))

elif modulo == "Statistica Base":
    st.title("📊 Statistica con Correzione Offset")
    
    # 1. INPUT DATI
    testo_dati = st.text_area("Incolla i dati qui:", height=100)
    
    # 2. PARAMETRI INCERTEZZA E OFFSET
    st.subheader("Parametri Strumentali e Offset")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ris = st.number_input("Risoluzione ($R$):", value=0.0, format="%.6f")
    with c2:
        s_man = st.number_input(r"$\sigma_B$ manuale:", value=0.0, format="%.6f")
    with c3:
        v_off = st.number_input("Valore Offset:", value=0.0, format="%.6f")
    with c4:
        s_off = st.number_input(r"$\sigma$ Offset:", value=0.0, format="%.6f")

    if testo_dati:
        try:
            # Elaborazione dati
            dati_grezzi = [float(x.replace(',', '.')) for x in testo_dati.split()]
            # Correzione Offset
            dati_corretti = [x - v_off for x in dati_grezzi]
            
            if len(dati_corretti) > 1:
                res = analisi_statistica_completa(dati_corretti)
                
                # Logica Incertezza B (Precedenza Manuale > Risoluzione)
                s_base = s_man if s_man > 0 else incertezza_strumentale_rettangolare(ris)
                s_b_tot = calcola_sigma_b_totale(s_base, s_off)
                
                # Incertezza Totale
                sigma_tot = calcola_quadratura(res['sigma_a'], s_b_tot)
                
# Visualizzazione Principale
                st.divider()
                st.markdown("### Risultato Finale")
                st.success(f"Valore per la relazione: ({res['media']:.{decimali}f} ± {sigma_tot:.{decimali}f})")
                
                # Nuova sezione per la dispersione dei dati
                st.markdown("#### Analisi della Dispersione")
                d1, d2 = st.columns(2)
                d1.metric("Deviazione Standard Campionaria(s)", f"{res['std']:.{decimali}f}", help="Indica quanto sono sparsi i singoli dati (non scalata su √N)")
                d2.metric("N. Misure", f"{res['n']}")

                st.markdown("#### Scomposizione delle Incertezze (per la Media)")
                r1, r2, r3 = st.columns(3)
                r1.metric("Media Corretta", f"{res['media']:.{decimali}f}")
                r2.metric("σ_A (Statistica)", f"{res['sigma_a']:.{decimali}f}", help="Errore della media: s / √N")
                r3.metric("σ_TOTALE", f"{sigma_tot:.{decimali}f}")
                
                # Scomposizione Tipo B (come avevamo già impostato)
                st.markdown("##### Dettaglio Incertezza Tipo B")
                b1, b2, b3 = st.columns(3)
                b1.metric("σ Strumentale", f"{s_base:.{decimali}f}")
                b2.metric("σ Offset", f"{s_off:.{decimali}f}")
                b3.metric("σ_B Totale", f"{s_b_tot:.{decimali}f}")
            else:
                st.warning("Inserisci almeno 2 dati.")
        except ValueError:
            st.error("Formato dati non valido.")

elif modulo == "Generatore Misure":
    st.title("🪄 Generatore di Misure (Simulatore)")
    st.write("Inserisci un piccolo campione di misure reali. Il sistema calcolerà media e deviazione standard per generare una lista più lunga di dati statisticamente compatibili.")
    
    
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        dati_input = st.text_area("Inserisci le tue misure reali (es. 5-10 dati):")
    with col_gen2:
        n_totale = st.number_input("Quante misure vuoi in totale?", min_value=10, max_value=1000, value=50, step=10)
        
    if dati_input:
        try:
            dati_base = [float(x.replace(',', '.')) for x in dati_input.split()]
            if len(dati_base) >= 3:
                dati_generati = genera_misure_gaussiane(dati_base, n_totale)
                
                st.success(f"Generazione completata: {len(dati_generati)} misure totali.")
                
                # Mostra i dati formattati pronti per essere copiati
                dati_testo = "\n".join([f"{x:.{decimali}f}" for x in dati_generati])
                st.text_area("Copia questi dati per la tua relazione:", value=dati_testo, height=200)
                
            else:
                st.warning("Inserisci almeno 3 misure reali per avere una stima sensata della dispersione.")
        except ValueError:
            st.error("Assicurati di inserire solo numeri.")

elif modulo == "Istogrammi":
    st.title("📈 Generatore Istogrammi Professionale")
    
    from funzioni_fisica.istogramma import crea_figura_istogramma
    import io

    with st.expander("Configurazione Estetica", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            titolo_input = st.text_input("Titolo del grafico:", value="Analisi Statistica delle Misure")
        with c2:
            label_x = st.text_input("Label Asse X:", value="Valore Misurato")
        with c3:
            label_y = st.text_input("Label Asse Y:", value="Densità di Probabilità")


        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            n_bins = st.slider("Risoluzione (Bin):", 5, 60, 20)
        with c_col2:
            # NUOVO SLIDER TICK
            n_ticks = st.slider("Numero di Tick X:", 2, 30, 10)
        with c_col3:
            colore_scelto = st.color_picker("Colore Tema:", "#3498db")

    dati_input = st.text_area("Incolla i tuoi dati qui (uno per riga o separati da spazio):", height=150)

    if dati_input:
        try:
            dati = [float(x.replace(',', '.')) for x in dati_input.split()]
            
            if len(dati) > 3:
                # Creazione del grafico
                fig = crea_figura_istogramma(
                    dati, n_bins, n_ticks, label_x, label_y, 
                    titolo_input, colore_scelto, decimali
                )
                
                # Visualizzazione
                st.pyplot(fig)
                
                # Download con padding di sicurezza
                buf = io.BytesIO()
                # bbox_inches='tight' con pad_inches assicura lo spazio bianco esterno
                fig.savefig(buf, format="png", dpi=300, bbox_inches='tight', pad_inches=0.5)
                
                st.download_button(
                    label="💾 Scarica Grafico per Relazione (PNG Alta Ris.)",
                    data=buf.getvalue(),
                    file_name=f"istogramma_{titolo_input.replace(' ', '_')}.png",
                    mime="image/png"
                )
            else:
                st.warning("Carica almeno 4 dati per visualizzare la distribuzione.")
        except ValueError:
            st.error("Errore: controlla che i dati siano numerici.")

elif modulo == "Fit Lineare":
    st.title("📉 Regressione Lineare Avanzata")
    st.write("Analisi completa con minimi quadrati, inviluppi e residui.")

    # --- 1. INPUT DATI ---
    st.subheader("1. Inserimento Dati")
    col_x, col_y, col_sy = st.columns(3)
    with col_x:
        input_x = st.text_area("Valori X:", placeholder="1.0\n2.0\n3.0", height=150)
    with col_y:
        input_y = st.text_area("Valori Y:", placeholder="2.1\n3.9\n6.2", height=150)
    with col_sy:
        input_sy = st.text_area("Incertezze σ_Y:", placeholder="0.1\n0.2\n0.1", height=150)

  # --- Punto 2 OPZIONI ---
    with st.expander("🛠️ Impostazioni Grafica e Inviluppi", expanded=True):
        c_lab1, c_lab2, c_lab3 = st.columns(3)
        with c_lab1:
            titolo_fit = st.text_input("Titolo Grafico:", value="Fit Lineare Sperimentale")
        with c_lab2:
            label_x = st.text_input("Asse X (es. $L [m]$):", value="X")
        with c_lab3:
            label_y = st.text_input("Asse Y (es. $T^2 [s^2]$):", value="Y")
            
        c_opt1, c_opt2, c_opt3 = st.columns(3)
        with c_opt1:
            colore_punti = st.color_picker("Colore Punti/Errori:", "#000080")
        with c_opt2:
            colore_retta = st.color_picker("Colore Retta:", "#FFA500")
        with c_opt3:
            n_ticks = st.slider("Numero Tick asse X:", 3, 20, 8)

        st.divider()
        # --- NUOVO LAYOUT ALLINEATO ---
        col_inv1, col_inv2 = st.columns([1, 1])
        with col_inv1:
            st.write(" ") # Spazio per allineare verticalmente al numero
            mostra_inv = st.toggle("Abilita Inviluppo", value=True, help="Mostra le curve di incertezza della retta")
        with col_inv2:
            k_sigma = st.number_input("Moltiplicatore K-Sigma:", 1, 3, 1)

    # --- 3. LOGICA DI CALCOLO ---
    if st.button("🚀 Esegui Analisi Fit", type="primary", key="main_run"):
        st.session_state.analisi_fatta = True # Salviamo che abbiamo premuto il tasto

    if st.session_state.get('analisi_fatta', False):
        if input_x and input_y and input_sy:
            try:
                vx = np.array([float(v.replace(',', '.')) for v in input_x.split()])
                vy = np.array([float(v.replace(',', '.')) for v in input_y.split()])
                vsy = np.array([float(v.replace(',', '.')) for v in input_sy.split()])
                
                #1. Calcolo Standard iniziale
                m, c, sm, sc, cov, res, chi2 = minimi_quadrati_pesati(vx, vy, vsy)
                ndf = len(vx) - 2

                # 2. LINEA E CHECKBOX (La parte nuova)
                st.divider() 
                st.subheader("🔄 Raffinamento Analisi")
                applica_post = st.checkbox("Applica correzione σ a posteriori (dai residui)")

                if applica_post:
                    sigma_post = np.sqrt(np.sum(res**2) / ndf)
                    vsy = np.full_like(vsy, sigma_post) # Sovrascrive le sigma con quella stimata
                    # Ricalcola m, c e chi2 con la nuova sigma
                    m, c, sm, sc, cov, res, chi2 = minimi_quadrati_pesati(vx, vy, vsy)
                    st.warning(f"⚠️ Calcolo aggiornato con σ_y stimata: {sigma_post:.{decimali}f}")

                # --- VISUALIZZAZIONE RISULTATI IN BOX ---
                st.divider()
                st.subheader("📊 Analisi Statistica")
                
                # Prima riga: Parametri della retta
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""<div style='text-align: center; border: 2px solid #60b4ff; padding: 15px; border-radius: 10px; background-color: rgba(96, 180, 255, 0.1);'>
                        <p style='color: #60b4ff; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;'>Pendenza (m)</p>
                        <h2 style='margin: 0;'>{m:.{decimali}f} ± {sm:.{decimali}f}</h2>
                        </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div style='text-align: center; border: 2px solid #2ecc71; padding: 15px; border-radius: 10px; background-color: rgba(46, 204, 113, 0.1);'>
                        <p style='color: #2ecc71; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;'>Intercetta (c)</p>
                        <h2 style='margin: 0;'>{c:.{decimali}f} ± {sc:.{decimali}f}</h2>
                        </div>""", unsafe_allow_html=True)

                st.write("") # Spazio tra le righe

                # Seconda riga: Covarianza e Chi Quadro
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f"""<div style='text-align: center; border: 1px dashed #888; padding: 10px; border-radius: 10px;'>
                        <p style='color: #888; font-weight: bold; margin-bottom: 0;'>Covarianza (m, c)</p>
                        <code style='font-size: 1.2em;'>{cov:.2e}</code>
                        </div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""<div style='text-align: center; border: 1px dashed #888; padding: 10px; border-radius: 10px;'>
                        <p style='color: #888; font-weight: bold; margin-bottom: 0;'>Test χ² / ndf</p>
                        <code style='font-size: 1.2em;'>{chi2:.2f} / {ndf}</code>
                        </div>""", unsafe_allow_html=True)

                # --- GRAFICI ---
                st.divider()
                st.subheader("📈 Grafici di Analisi")
                
                # Tab per non affollare troppo la pagina
                tab1, tab2 = st.tabs(["Fit Lineare", "Analisi dei Residui"])
                
                with tab1:
                    fig1 = plot_fit_completo(vx, vy, vsy, m, c, sm, sc, cov, 
                                             label_x, label_y, titolo_fit, colore_punti, 
                                             colore_retta, n_ticks, decimali, mostra_inv, k_sigma)
                    st.pyplot(fig1)
                    
                    # Bottone download per il fit
                    buf1 = io.BytesIO()
                    fig1.savefig(buf1, format="png", dpi=300, bbox_inches='tight', pad_inches=0.2)
                    st.download_button("💾 Scarica Fit", buf1.getvalue(), "fit.png", "image/png")

                with tab2:
                    # Chiamiamo la funzione per i residui che avevamo nel modulo fit
                    fig2 = plot_residui_migliorato(vx, res, vsy, label_x, colore_punti, colore_retta, n_ticks, decimali)
                    st.pyplot(fig2)
                    
                    # Bottone download per i residui
                    buf2 = io.BytesIO()
                    fig2.savefig(buf2, format="png", dpi=300, bbox_inches='tight', pad_inches=0.2)
                    st.download_button("💾 Scarica Residui", buf2.getvalue(), "residui.png", "image/png")

            except ValueError:
                st.error("Errore: Controlla i dati inseriti.")

elif modulo == "Propagazione Incertezze":
    st.title("🧬 Propagazione Automatica delle Incertezze")
    st.write("Inserisci la formula analitica. Il sistema calcolerà le derivate parziali e l'incertezza numerica.")

    # 1. INPUT FORMULA
    formula_input = st.text_input("Formula (usa * per moltiplicare e ** per le potenze):", 
                                 value="4 * pi**2 * L / T**2", 
                                 help="Esempio: m * g * h oppure 2 * pi * sqrt(L/g)")

    if formula_input:
        try:
            # Analisi simbolica
            risultato_simb = calcola_propagazione_simbolica(formula_input)
            
            # Mostra le formule in LaTeX
            st.markdown("#### Formule Analitiche")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.write("**Grandezza (f):**")
                st.latex(sp.latex(risultato_simb['espressione_base']))
            with c_f2:
                st.write(r"**Incertezza ($\sigma_f$):**")
                st.latex(sp.latex(risultato_simb['formula_incertezza']))

            with st.expander("📄 Copia Codice LaTeX per la relazione"):
                st.write("Copia questi blocchi nel tuo documento (es. Overleaf o LaTeX editor):")
                
                # Formula della grandezza
                latex_f = sp.latex(risultato_simb['espressione_base'])
                st.code(f"f = {latex_f}", language="latex")
                
                # Formula dell'incertezza
                latex_sigma = sp.latex(risultato_simb['formula_incertezza'])
                st.code(f"\\sigma_f = {latex_sigma}", language="latex")
                
                st.caption("Consiglio: Se usi l'ambiente 'equation', incolla solo la parte dopo l'uguale.")

            st.divider()

            # 2. INPUT NUMERICO DINAMICO
            st.markdown("#### Inserimento Valori e Incertezze")
            simboli = risultato_simb['simboli_variabili']
            valori_input = {}
            
            # Creiamo una griglia di input: per ogni variabile, due caselle (valore e sigma)
            for sim in simboli:
                col_v, col_s = st.columns(2)
                with col_v:
                    val = st.number_input(f"Valore di {sim.name}:", value=1.0, format="%.6f", key=f"val_{sim.name}")
                    valori_input[sim] = val
                with col_s:
                    sig = st.number_input(f"Incertezza \u03C3_{sim.name}:", value=0.1, format="%.6f", key=f"sig_{sim.name}")
                    # Mappiamo il simbolo della sigma creato nel motore alla variabile numerica
                    sigma_simbolo = risultato_simb['simboli_sigma'][sim.name]
                    valori_input[sigma_simbolo] = sig

            # 3. CALCOLO FINALE
            if st.button("Calcola Risultato Numerico", type="primary"):
                valore_finale = valuta_formula(risultato_simb['espressione_base'], valori_input)
                sigma_finale = valuta_formula(risultato_simb['formula_incertezza'], valori_input)
                
                st.success("### Risultato Numerico")
                st.subheader(f"({valore_finale:.{decimali}f} \u00B1 {sigma_finale:.{decimali}f})")
                
                # Bonus: Formato pronto per LaTeX
                st.code(f"({valore_finale:.{decimali}f} \\pm {sigma_finale:.{decimali}f})", language="latex")

        except Exception as e:
            st.error(f"Errore nella formula: {e}. Controlla la sintassi (es. usa sempre '*' per le moltiplicazioni).")

elif modulo == "Media Pesata":
    st.title("⚖️ Calcolo Media Pesata")
    st.write("Utilizza questo modulo quando hai diverse misure della stessa grandezza con incertezze differenti.")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        input_valori = st.text_area("Valori ($x_i$):", placeholder="10.1\n10.5\n9.8")
    with col_m2:
        input_sigma = st.text_area(r"Incertezze ($\sigma_i$):", placeholder="0.2\n0.5\n0.3")
        
    if st.button("Calcola Media Pesata", type="primary"):
        if input_valori and input_sigma:
            try:
                vals = np.array([float(v.replace(',', '.')) for v in input_valori.split()])
                sigs = np.array([float(s.replace(',', '.')) for s in input_sigma.split()])
                
                if len(vals) == len(sigs):
                    media_p, sigma_p = calcola_media_pesata(vals, sigs)
                    
                    st.divider()
                    res_c1, res_c2 = st.columns(2)
                    with res_c1:
                        st.success(f"### Media Pesata: {media_p:.{decimali}f}")
                    with res_c2:
                        st.success(f"### Incertezza: {sigma_p:.{decimali}f}")
                    
                    st.info(f"**Risultato per la relazione:** ({media_p:.{decimali}f} ± {sigma_p:.{decimali}f})")
                    st.write("")
                    with st.expander("🔍 Visualizza pesi delle singole misure"):
                        # Calcolo dei pesi
                        pesi = 1 / (sigs**2)
                        peso_totale = np.sum(pesi)
                        pesi_percentuali = (pesi / peso_totale) * 100
                        
                        # Creazione di una lista testuale per ogni misura
                        for i, (v, s, p) in enumerate(zip(vals, sigs, pesi_percentuali)):
                            st.write(f"**Misura {i+1}:** {v} ± {s}  ➜  **Peso:** {p:.1f}%")
                        
                        # Opzionale: un piccolo grafico a barre dei pesi
                        st.bar_chart(pesi_percentuali)
                else:
                    st.error("Il numero di valori deve coincidere con il numero di incertezze.")
            except Exception as e:
                st.error(f"Errore nel calcolo: {e}")

# region Credits
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Sviluppato da Davide De Luca**  
     *Laboratorio di Meccanica*  
         Facoltà di Fisica  
             Sapienza Università di Roma  
""")
# endregion
