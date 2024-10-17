# PRL e Memoria

Versione: Thu Oct 17 09:09:08 CEST 2024

---

Questo documento descrive la procedura sperimentale per il progetto PRL e memoria, distinguendo tra la generazione degli stimoli, l'organizzazione dei materiali per il compito di PRL e l'organizzazione dei materiali per il compito di memoria.

## Creazione degli Stimoli per ciascun soggetto

La prima fase consiste nella generazione degli stimoli specifici per ciascun soggetto.

1. **Cartella _images_:** Per ogni soggetto, si crea una cartella il cui nome corrisponde al codice del soggetto. Per esempio, `ma_ro_1999_03_06_312_m`.

TODO Per adesso, la cartella di ciascun soggetto è chiamata `subject_1`, `subject_2`, ...

Questa cartella contiene quattro sottocartelle, ciascuna con 100 immagini:
   - `self_orange` (self_orange_1.jpg, ..., self_orange_100.jpg)
   - `self_white` (self_white_1.jpg, ..., self_white_100.jpg)
   - `stranger_orange` (stranger_orange_1.jpg, ..., stranger_orange_100.jpg)
   - `stranger_white` (stranger_white_1.jpg, ..., stranger_white_100.jpg)

   Le immagini sono generate utilizzando lo script `collage/script_collage_img.py` e le immagini di partenza, specifiche per ciascun soggetto, sono chiamate `collage/background_orange.png` e `collage/background_white.png`. Una volta completata la generazione, le immagini sono spostate manualmente nelle cartelle appropriate (`ma_ro_1999_03_06_312_m/self_orange`, ecc.).

    È necessario generare un totale di **100 immagini per ciascuna delle 4 conditioni, per ciascun soggetto**, quindi:

    - 100 immagini per `self_white`
    - 100 immagini per `self_orange`
    - 100 immagini per `stranger_white`
    - 100 immagini per `stranger_orange`

    Questo porta a un totale di **400 immagini** (100 per ogni combinazione).

## PRL Task

2. **Cartella per il compito PRL:** Per ogni soggetto, si crea una cartella separata denominata `images/subject_code` (es., `images/ma_ro_1999_03_06_312_m`), che contiene quattro sottocartelle:
   - `self_orange`
   - `self_white`
   - `stranger_orange`
   - `stranger_white`

   Nella cartella `images/subject_code` di ciascun soggetto si spostano le 4 cartelle con 100 immagini ciascuna che sono state create in precedenza (`collage/output_folder`).

   La cartella del progetto contiene anche lo script Python per eseguire l'esperimento, `prl.py`.

   Quando si eseguo l'eseprimento, la sequenza delle sessioni PRL viene determinata utilizzando lo script `gen_seq_conditions.R`. 
   
   Lo script `prl.py` è eseguito con stringhe simili alle seguenti: 
   
   TODO check the arguments!

   ```bash
   python3 prl.py "A" "co_ba_1999_03_23_333_f" "Y" "self"
   ```

   Dove gli argomenti specificano:

   - "A" per la condizione "orange_rewarded_first".
   - "B" per la condizione "white_rewarded_first".
   - "Y" per "video sorprendenti".
   - "N" per "video non sorprendenti".
   - "self" per "ritratto del soggetto".
   - "stranger" per "ritratto di un estraneo".

   Ogni sessione PRL produce un file Excel con i risultati del partecipante in quella condizione. Ad esempio:

```bash
python prl.py "B" "codice_soggetto" "N" "self"
python prl.py "A" "codice_soggetto" "Y" "self"
python prl.py "B" "codice_soggetto" "Y" "stranger"
python prl.py "B" "codice_soggetto" "N" "stranger"
```

Nota: gli argomenti devono essere specificati tra virgolette nel terminale. 

## Compito di Memoria

3. **Cartella per il compito di memoria:** Per ogni soggetto, si crea una cartella denominata `nome_cognome_memory`, dove vengono inseriti i materiali e lo script `memory.py`.

   Durante il compito di memoria, si utilizzano le stesse immagini presentate nel compito PRL, ma vengono abbinate con immagini nuove ("new"):

   - **Prima sessione `self` (es. `surprise`)**: si usano le immagini OLD da 1 a 50 dalle cartelle `self_white` e `self_orange`, abbinate con immagini NEW da 101 a 150.
   - **Seconda sessione `self` (es. `non-surprise`)**: si usano le immagini OLD da 51 a 100, abbinate con immagini NEW da 151 a 200.
   - Lo stesso schema è applicato per le sessioni `stranger`.

   Ogni prova presenta due immagini, una vecchia e una nuova, entrambe con lo stesso sfondo (bianco o arancione), con la posizione e il tipo di prova randomizzati.

### Procedura del Compito di Memoria

Immediatamente dopo il completamento del compito PRL, viene somministrato il compito di memoria. Il partecipante deve identificare l’immagine "old" premendo il tasto `j` (destra) o `f` (sinistra). Il compito include:

- Uno schermo nero tra le prove per un intervallo casuale (200-1000 ms).
- Un punto di fissazione presentato per 100 ms, seguito dalla presentazione delle due immagini, che restano sullo schermo fino alla risposta o per un massimo di 5 secondi.

L’output registra:

- Data e ora di ogni prova
- Codice del soggetto
- Condizione (video sorprendenti o non sorprendenti)
- Tipo di immagine (self o stranger)
- Numero della sessione (1, 2, 3, 4)
- Nomi dei file delle immagini mostrate (sinistra/destra)
- Risposta del soggetto e correttezza della risposta (corretta se l’indice dell’immagine è inferiore a 101)
- Tempo di reazione (dalla presentazione alla risposta).

Le immagini sono posizionate a destra e a sinistra del punto di fissazione, distanziate orizzontalmente. La posizione del punto di fissazione è determinata casualmente aggiungendo una piccola variazione casuale (x, y) alla posizione centrale dello schermo.

---

## Struttura delle Sessioni

Ogni volta che si esegue `prl.py` con gli argomenti appropriati, viene generato un file CSV che contiene i risultati del partecipante per quella condizione. Ogni partecipante deve generare 4 file.

## Ambiente virtuale

È necessario attivare un ambiente virtuale con le appropriate librerie.

```bash
# Create the pygame_env environment
conda create -n pygame_env -c conda-forge python=3.12.1 pygame opencv numpy
# Activate the environment
conda activate pygame_env
# pip install pygame_gui
pip install pygame_gui -U
```


## Debugging

For debugging, use a trimmed version of the videos.


---

## PyInstaller

To generate a binary file, use the file `prl_experiment.spec` and execute

```bash
pyinstaller prl_experiment.spec
```

This will create the executable `./dist/PRL_Experiment`.

To run the experiment with this binary file, use the instruction:

```bash
./dist/PRL_Experiment "A" "co_ba_1999_03_23_333_f" "Y"
```

TODO 

1. I need to be sure that all arguments are passed to the script, so as to be able to distinguish between the outputs of the 4 different conditions. Also I need to know the order in which the outputs had been generated.

2. Change the Python script so that the Excel files are all saved in the `output_data_prl_memory` directory.
