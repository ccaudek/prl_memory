# PRL e Memoria

Versione: Thu Oct 17 09:09:08 CEST 2024

---

Questo documento descrive la procedura sperimentale per il progetto PRL e memoria, distinguendo tra la generazione degli stimoli, l'organizzazione dei materiali per il compito di PRL e l'organizzazione dei materiali per il compito di memoria.

## Project structure

In this project, two tasks will be run by each subject, each in 4 different conditions:

1. a probabilistic reversal learning task, with videos, and mood ratings;
2. an old/new memory task.

```bash
project/
├── prl_28.py
└── images/
    ├── subject_1_self/
    │   ├── old_orange/     # 100 images (001-100)
    │   ├── old_white/      # 100 images (001-100)
    │   ├── new_orange/     # 100 images (001-100)
    │   └── new_white/      # 100 images (001-100)
    └── subject_1_stranger/
        ├── old_orange/     # 100 images (001-100)
        ├── old_white/      # 100 images (001-100)
        ├── new_orange/     # 100 images (001-100)
        └── new_white/      # 100 images (001-100)
```

The project folder contains the Python script, called prl_28.py and a folder called "images". In the images folder, there are two folders for each participant. For example, subject_1_self and subject_1_stranger.

The folder subject_1_self, for example, contains 4 folders: old_orange, old_white, new_orange, new_white.
Each of these 4 folders has 100 images. For example, the folder new_orange has images new_orange_img_001.jpg, ..., new_orange_img_100.jpg. Similarly the other 3 folders.

The folder subject_1_stranger, has the same structure. It contains 4 folders: old_orange, old_white, new_orange, new_white. Each of these 4 folders has 100 images. For example, the folder new_orange has images new_orange_img_001.jpg, ..., new_orange_img_100.jpg. Similarly the other 3 folders.

The images in the subject_1_self folder and those of the subject_1_stranger are different. They differ because a different background is used for each of them.

The other subjects will have also two folders each, with the same structure as above.

I need 50 unique white images and 50 unique orange images for the "surprise" condition, and 50 unique white images and 50 unique orange images for the "no-surprise" condition. In each trial of a session (having 50 trials) two images are shown: a white and an orange image.

In the Python script, the conditions is determined as follows:

image_ranges = {
    "A": (1, 50),  # Self/surprise: images 1-50 from the "old" subject_1_self folder
    "B": (51, 100),  # Self/no-surprise: images 51-100 from the "old" subject_1_self folder
    "C": (1, 50),  # Stranger/surprise: images 1-50 from the "old" subject_1_stranger folder
    "D": (51, 100),  # Stranger/no-surprise: images 51-100 from the "old" subject_1_stranger folder
}

When running the script, I use one of these 4 options to deterine which condition will be run.

So, with the argument "A" I will run the Self/surprise condition, with white and orange "old" images indiced from 1 to 50; with the argument "B" I will run the Self/no-surprise condition, with white and orange images indiced from 51 to 100; with the argument "C" I will run the Stranger/surprise condition, with white and orange images indiced from 1 to 50; and so on.

The images in the "new" folders are used in another task: an old/new memory task that will be run immediately after each session of the PRL task.

## Creazione degli Stimoli per ciascun soggetto

Prima di somministrare i due compiti ai soggetti è necessario generare gli stimoli che verranno usati. Una dimensione che viene considerata nel progetto è l'impatto dell'informazione autoriferita sull'esecuzione del compito. Il secondo aspetto è il ruolo della sorpresa.

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

### 1. **Design**

Lo script Python genera un compito di apprendimento probabilistico con inversione (probabilistic reversal learning), che include video e valutazioni del mood.

Ci sono **4 condizioni** per ciascun soggetto, che variano in base a due fattori: la presenza o assenza di sorpresa e il tipo di informazione (auto-riferita o etero-riferita). Ogni soggetto completa 4 sessioni, una per ciascuna condizione.

Oltre a queste 4 condizioni, c'è una variabile aggiuntiva che viene determinata casualmente per ciascun soggetto, ma non aumenta il numero di condizioni. Questa variabile stabilisce se l'immagine arancione viene premiata con una probabilità maggiore rispetto a quella bianca nella prima epoca (prima del reversal). Il valore di questa variabile viene determinato casualmente con lo script R `gen_seq_conditions.R`.

Per ogni soggetto, vengono create due cartelle denominate `images/subject_code_self` (esempio: `images/ma_ro_1999_03_06_312_m_self`) e `images/subject_code_stranger`. Ciascuna di queste due cartelle contiene quattro sottocartelle:

- `new_orange`
- `new_white`
- `old_orange`
- `old_white`

Nella cartella `images/subject_code_self` di ciascun soggetto vengono spostate le 4 cartelle (ciascuna con 100 immagini) create in precedenza con il processo `collage/output_folder`.

Nella cartella `images/subject_code_stranger` di ciascun soggetto vengono spostate 4 cartelle con 100 immagini ciascuna, create usando le immagini di una persona sconosciuta al soggetto ma dello stesso genere.

La struttura di cartelle è replicata per ogni soggetto, che avrà due cartelle (self e stranger), ciascuna con 4 sottocartelle contenenti le immagini.

Lo script Python `prl.py` gestisce l'esperimento e utilizza lo script R `gen_seq_conditions.R` per determinare la sequenza delle sessioni PRL.

Le immagini nella cartella `subject_1_self` e quelle nella cartella `subject_1_stranger` sono differenti, poiché usano sfondi diversi.

Ogni sessione include 50 immagini bianche e 50 immagini arancioni per le condizioni "sorpresa" e "no-sorpresa". In ciascun trial di una sessione (50 trial), vengono mostrate una immagine bianca e una arancione.

### 2. **Configurazione delle Condizioni**

Nel codice Python, le condizioni sono mappate come segue:

```python
condition_map = {
    "A": "self_surprise",
    "B": "self_no_surprise",
    "C": "stranger_surprise",
    "D": "stranger_no_surprise",
}
```

La selezione delle immagini avviene in questo modo:

```python
image_ranges = {
    "A": (1, 50),  # Self/surprise: immagini 1-50 dalla cartella "old" di subject_1_self
    "B": (51, 100),  # Self/no-surprise: immagini 51-100 dalla cartella "old" di subject_1_self
    "C": (1, 50),  # Stranger/surprise: immagini 1-50 dalla cartella "old" di subject_1_stranger
    "D": (51, 100),  # Stranger/no-surprise: immagini 51-100 dalla cartella "old" di subject_1_stranger
}
```

Inoltre, è necessario specificare la variabile `orange_first`, che determina quale immagine viene premiata maggiormente nella prima epoca.

- Se `orange_first` è True, le probabilità di ricompensa saranno `[(0.9, 0.1), (0.1, 0.9)]` (arancione premiata nella prima epoca).
- Se `orange_first` è False, le probabilità saranno `[(0.1, 0.9), (0.9, 0.1)]` (bianca premiata nella prima epoca).

La variabile `orange_first` viene determinata tramite un argomento passato nella riga di comando:

- `T` indica che `orange_first` è True (arancione premiata per prima).
- `F` indica che `orange_first` è False (bianca premiata per prima).

### 3. **Esecuzione dello Script**

Per eseguire lo script Python, ad esempio:

```bash
python3 prl.py "subject_1" "B" "T"
```

- Il primo argomento, `"subject_1"`, specifica il codice del soggetto, che viene usato per selezionare le cartelle con le immagini (`subject_1_self` o `subject_1_stranger`).
- Il secondo argomento, `"B"`, specifica la condizione (`self_no_surprise` in questo caso), determinando quali immagini vengono usate.
- Il terzo argomento, `"T"`, indica che l'immagine arancione sarà premiata per prima.

Le immagini contenute nelle cartelle "new" saranno utilizzate in un altro compito, un task di memoria old/new, che viene eseguito subito dopo ogni sessione del compito PRL.

### 4. **Esecuzione delle Sessioni e Produzione dei Risultati**

Le sessioni del compito PRL vengono eseguite utilizzando il comando seguente, dove gli argomenti specificano:

```bash
python3 prl_29.py "subject_code" "condition" "orange_first"
```

Ad esempio:

```bash
python3 prl_29.py "subject_1" "A" "T"  # self_surprise, arancione premiata prima
python3 prl_29.py "subject_1" "B" "F"  # self_no_surprise, bianca premiata prima
python3 prl_29.py "subject_1" "C" "F"  # stranger_surprise, bianca premiata prima
python3 prl_29.py "subject_1" "D" "T"  # stranger_no_surprise, arancione premiata prima
```

Ogni sessione produce un file CSV con i risultati del partecipante per quella condizione. Ad esempio, per la sessione `"subject_1"`, `"C"`, `"F"`, viene prodotto un file con i risultati che includono i dati raccolti durante la sessione, come il tempo di reazione, il feedback ricevuto, le immagini selezionate e la valutazione del mood.


## Compito di Memoria

Una volta completata ciascuna delle 4 sessioni del PRL, il soggetto completa un compito di memoria. 

Le 4 sessioni del PRL possono anche essere somministrate in giorni diversi. Però, ogni volta che una sessione PRL viene somministrata, deve essere immediatamente dopo somministrato il compito di memoria.

Il compito di memoria è un compito di riconoscimento old/new.

In ciascuna prova del compito di memoria vengono presentate due immagini: una immagine "old" (ovvero, un'immagine che era stata utilizzata nel compito PRL appena eseguito dal soggetto) e una immagine "new" (un'immagine che proviene dai folders "new_orange" o "new_white" che il soggetto non ha mai visto). Le immagini old e new sono mostrate una a fianco all'altra (posizionate a destra e a sinistra).

Le immagini "old" sono le stesse immagini che sono state utilizzate nel compito PRL di quella condizione (es., self-surprise).

Nel compito di memoria vengono mostrate tutte le 50 immagini orange e tutte le 50 immagini white della sessione PRL che il soggetto ha appena completato. Queste sono le immagini "old". In ciascuna prova, a ciascuna immagine old viene accoppiata un'immagine "new" (che il soggetto non ha mai visto prima).

In ogni prova vengono mostrate o due immagini orange (una old e una new) o due immagini white (una old e una new).

Nel compito di memoria, vengono presentate tutte le prove "orange" e tutte le prove "white" nella stessa sequenza, in cui l'ordine delle prove è randomizzato. La posizione spaziale (destra / sinistra) di ciascuna coppia di immagini old e new è determinata casualmente in ciascuna prova.

Il partecipante deve identificare l’immagine "old" premendo il tasto `j` (se pensa che l'immagine old sia quella posizionata a destra) o `f` (se pensa che l'immagine old sia quella posizionata a sinistra). 

Il compito include:

- Uno schermo nero tra le prove per un intervallo casuale (200-1000 ms).
- Un punto di fissazione presentato per 100 ms, seguito dalla presentazione delle due immagini, che restano sullo schermo fino alla risposta o per un massimo di 3 secondi.

L’output registra:

- Data e ora di ogni prova
- Codice del soggetto
- Condizione ("A" self-surprise, "B" self-no-surprise, "C" stranger-surpise, "D" stranger-no-surprise)
- Numero della sessione (1, 2, 3, 4)
- Nomi dei file delle immagini mostrate (immagine a sinistra/ immagine a destra)
- Tasto premuto dal soggetto 
- Correttezza della risposta (corretta se il soggetto ha scelto l'immagine "old")
- Tempo di reazione (tempo trascorso dalla presentazione dello stimolo alla risposta).

Le immagini sono posizionate a destra e a sinistra del punto di fissazione, distanziate orizzontalmente. La posizione del punto di fissazione è determinata casualmente aggiungendo una piccola variazione spaziale casuale (x, y) alla posizione centrale dello schermo.

Il compito di memoria viene eseguito 4 volte, subito dopo il completamento di ciascuna delle 4 condizioni del compito PRL.

# Esempio di esecuzione

if **name** == "**main**":
    if len(sys.argv) < 3:
        print("Uso: python memory_task.py <subject_code> <condition>")
        sys.exit(1)

    subject_code = sys.argv[1]
    condition = sys.argv[2]

    run_memory_task(subject_code, condition)

### Procedura del Compito di Memoria

Immediatamente dopo il completamento del compito PRL, viene somministrato il compito di memoria. 

---

## Struttura delle Sessioni

Ogni volta che si esegue `prl.py` con gli argomenti appropriati, viene generato un file CSV che contiene i risultati del partecipante per quella condizione. Ogni partecipante deve generare 4 file.

## Ambiente virtuale

Innanzitutto, è necessario creare un ambiente virtuale con le appropriate librerie.

```bash
# Create the pygame_env environment
conda create -n pygame_env -c conda-forge python=3.12.1 pygame opencv numpy
# Activate the environment
conda activate pygame_env
# pip install pygame_gui
pip install pygame_gui -U
```

Per eseguire l'esperimento, usando il codice Python, è necessario attivare l'ambiente virtuale:

```bash
conda deactivate
# Activate the environment
conda activate pygame_env
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

---

```bash
python3 prl_28.py "A" "subject_1" "Y"
```

