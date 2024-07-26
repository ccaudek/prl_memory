# PRL e Memoria

Questo documento descrive la procedura sperimentale per il progetto PRL e memoria, includendo la generazione degli stimoli e la somministrazione dei compiti di PRL e memoria.

## Creazione degli stimoli

La prima fase riguarda la creazione degli stimoli specifici per ciascun soggetto.

Per ogni soggetto, si crea una cartella denominata `nome_cognome_images` (es. `mario_rossi`, utilizzando solo lettere minuscole). All'interno di questa cartella, saranno presenti quattro sottocartelle, ciascuna contenente 200 immagini:

- `self_orange` (self_orange_1.jpg, ..., self_orange_200.jpg)
- `self_white` (self_white_1.jpg, ..., self_white_200.jpg)
- `stranger_orange` (stranger_orange_1.jpg, ..., stranger_orange_200.jpg)
- `stranger_white` (stranger_white_1.jpg, ..., stranger_white_200.jpg)

Ogni sottocartella conterrà 200 immagini generate dallo script `script_collage_img.py` utilizzando l'immagine di partenza appropriata.

Le immagini di partenza sono due: `background_orange.png` e `background_white.png`. Gli stimoli `_orange` si generano utilizzando `background_orange.png`, mentre gli stimoli `_white` si generano utilizzando `background_white.png`.

## PRL Task

Per ciascun soggetto, si crea una cartella denominata `nome_cognome_prl`.

All'interno di questa cartella, saranno presenti lo script `prl.py` e quattro sottocartelle denominate `self_orange`, `stranger_orange`, `self_white` e `stranger_white`. Queste cartelle conterranno una selezione degli stimoli generati in precedenza:

- Nella cartella `self_orange` si trovano le prime 50 immagini ("old") provenienti dalla cartella `nome_cognome_images/self_orange` o le immagini 51-100.
- Nella cartella `stranger_orange` si trovano le prime 50 immagini ("old") provenienti dalla cartella `nome_cognome_images/stranger_orange` o le immagini 51-100.
- Nella cartella `self_white` si trovano le prime 50 immagini ("old") provenienti dalla cartella `nome_cognome_images/self_white` o le immagini 51-100.
- Nella cartella `stranger_white` si trovano le prime 50 immagini ("old") provenienti dalla cartella `nome_cognome_images/stranger_white` o le immagini 51-100.

La seconda fase prevede la somministrazione del compito di probabilistic reversal learning (PRL), che verrà completato quattro volte.

L'esecuzione del programma richiede una stringa simile alla seguente:

```bash
python3 prl.py "A" "co_ba_1999_03_23_333_f" "Y" "self"
```

Gli argomenti specificati sono i seguenti:

- "A" indica la condizione "orange_rewarded_first".
- "B" indica la condizione "white_rewarded_first".
- "Y" indica "surprise_videos".
- "N" indica "not_surprising_videos".
- "self" indica "subject_portrait".
- "stranger" indica "stranger_portrait".

L'esecuzione dello script `gen_seq_conditions.R` consente di ottenere la sequenza delle quattro condizioni per ciascun soggetto. Ad esempio:

```bash
python prl.py B codice_soggetto N self
python prl.py A codice_soggetto Y self
python prl.py B codice_soggetto Y stranger
python prl.py B codice_soggetto N stranger
```

Nota: gli argomenti devono essere specificati tra virgolette nel terminale.

Nella sequenza di quattro sessioni, nella prima sessione `self` verranno utilizzate le immagini 1-50 delle cartelle `nome_cognome_images/self_white` e `nome_cognome_images/self_orange`; nella seconda sessione `self` verranno utilizzate le immagini 51-100 delle stesse cartelle.

Nella prima sessione `stranger` verranno utilizzate le immagini 1-50 delle cartelle `nome_cognome_images/stranger_white` e `nome_cognome_images/stranger_orange`; nella seconda sessione `stranger` verranno utilizzate le immagini 51-100 delle stesse cartelle.

Ogni volta che si esegue lo script `prl.py` con gli argomenti appropriati, si ottiene un file Excel con i risultati del partecipante in quella condizione.

## Memory Task

Immediatamente dopo il completamento del compito PRL, viene somministrato il compito di memoria.

Nel compito PRL, sono state utilizzate le immagini bianche 1-50 e le immagini arancioni 1-50 nella prima sessione `self`, e le immagini bianche 51-100 e le immagini arancioni 51-100 nella seconda sessione `self`. Lo stesso vale per le due sessioni `stranger`.

Ogni compito di memoria include 100 prove. In ciascuna prova, lo script `memory.py` mostra due immagini sullo schermo: entrambe con sfondo bianco o entrambe con sfondo arancione. Una delle immagini è "old" e l'altra è "new". Il tipo di prova (orange, white) è randomizzato nella sequenza delle 100 prove. La posizione spaziale degli stimoli old e new (destra, sinistra) è randomizzata.

Nella prima sessione `self` (ad esempio, `surprise`), verranno utilizzate le stesse 50 immagini bianche e le stesse 50 immagini arancioni usate nel compito PRL. Queste sono indicizzate da 1 a 50. Ad ogni immagine sarà accoppiata una nuova immagine (NEW) non mostrata in precedenza, indicizzata da 101 a 150, sia per le immagini arancioni che per le immagini bianche.

Nella seconda sessione `self` (ad esempio, `non-surprise`), le immagini OLD sono indicizzate da 51 a 100 e le immagini NEW da 151 a 200.

Nel compito di memoria, ciascuna immagine (indicizzata da 1 a 200) prelevata dalle quattro cartelle può essere mostrata una sola volta.

Il partecipante identifica l'immagine OLD in ciascuna prova premendo il tasto `j` per scegliere l'immagine di destra e il tasto `f` per l'immagine di sinistra. Vi è un intervallo casuale tra le prove, compreso tra 200 e 1000 ms (schermo nero). In ogni prova, un punto di fissazione compare sullo schermo nero per 100 ms, seguito dalla presentazione delle due immagini che restano sullo schermo fino alla risposta del soggetto, ma non oltre 5 secondi.

L'output del programma mostra, per ciascuna prova, la data e l'ora (minuto e secondo) di conclusione della prova, il codice del soggetto fornito in input, la condizione (surprise_videos; not_surprising_videos), il tipo di immagine (self, stranger), il numero d'ordine della sessione (1, 2, 3, 4), il nome del file dell'immagine mostrata a sinistra, il nome del file dell'immagine mostrata a destra, il tasto premuto dal soggetto, se la risposta è corretta (la risposta è corretta se la scelta del soggetto identifica l'immagine il cui indice è minore di 101), e il tempo di reazione (tra il momento in cui l'immagine è presentata sullo schermo e il momento in cui il soggetto preme il tasto di risposta).

Le immagini sono posizionate eccentricamente (a destra e a sinistra del punto di fissazione, con uno spazio orizzontale pari a metà della dimensione dell'immagine tra le due). La posizione del punto di fissazione è determinata casualmente in ciascuna prova aggiungendo una componente casuale x e y alla posizione centrale dello schermo.
