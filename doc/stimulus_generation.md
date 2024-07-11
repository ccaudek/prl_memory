# PRL e Memoria

Questo documento descrive le varie operazioni che devono essere compiute per generare gli stimoli che verranno usati dai singoli soggetti. L'obiettivo è di creare una procedura automatizzata che consenta di generare una cartella con tutti gli scipt Python e gli stimoli necessari ad un soggetto per eseguire l'esperimento sul proprio computer.

## Creazione degli stimoli

Per ciascun soggetto, si crea una cartella `nome_cognome`. All'interno di quella cartella ci saranno 4 cartelle, con 100 immagini ciascuna:

- self_orange (self_orange_1.jpg, ..., self_orange_100.jpg)
- self_white (self_white_1.jpg, ..., self_white_100.jpg)
- stranger_orange (stranger_orange_1.jpg, ..., stranger_orange_100.jpg)
- stranger_white (stranger_white_1.jpg, ..., stranger_white_100.jpg)

Ciascuna cartella conterrà le 100 immagini generate dallo scipt `script_collage_img.py`, usando l'appropriata immagine di partenza. Si devono usare due immagini di partenza, chiamate `background_orange.png` e `background_white.png`. Gli stimoli `_orange` si generano con `background_orange.png` e gli stimoli `_white` si generano con `background_white.png`.

## PRL task

Nella versione corrente, il PRL task si esegue con lo script `prl_26.py` contenuto nella cartella `prl`. La cartella `prl` contiene 4 cartelle con gli stimoli: `self_orange`, `stranger_orange`, `self_white` e `stranger_white`.

L'esecuzione del programma richiede che

- nella cartella `orange` si trovino le prime 25 immagini (“old”) provenienti dalla cartella `nome_cognome` `self_orange` o `stranger_orange`;
- nella cartella `white` si trovino le prime 25 immagini (“old”) provenienti dalla cartella `nome_cognome` `self_white` o `stranger_white`.

Si esegue lo script da `prl_26` usando come argomento `nome_cognome_self_prl_SUR` nella condizione self-surprise. Nelle altre condizioni cambieremo `SUR` in `NOSUR` e `SELF` in `STRANGER`.

Otterremo così un file Excel con i risultati in ciascuna condizione.

TODO: Nella nuova versione, il file zippato che si passa a ciascun soggetto (che conterrà gli stimoli e gli scripts Python), avrà come come il codice del soggetto. Per esempio, `co_ba_1999_03_23_333_f`.

The script can dynamically read the folder name and use it as the subject code.

Here's how you can set up the Bash script to automatically fetch the folder name, use it as the subject code, and process the script execution for each condition:

Given the requirements and the setup where each participant's folder contains everything needed to run the experiment, the workflow can be further simplified. You'll place a script named `prl` in each participant's folder that takes a single parameter (1, 2, 3, or 4) to execute the corresponding condition. This script will handle everything from checking if the output already exists to running the Python script with the right arguments.

Each subject has to complete 4 conditions:

python3 prl_26.py "A" "co_ba_1999_03_23_333_f" "Y"
python3 prl_26.py "A" "co_ba_1999_03_23_333_f" "Y"
python3 prl_26.py "A" "co_ba_1999_03_23_333_f" "Y"
python3 prl_26.py "A" "co_ba_1999_03_23_333_f" "Y"

Here's how you can set up the script and explain the procedure to the participants:

### Folder Structure Example

Each participant has a folder like this:

```
co_ba_1999_03_23_333_f/
│
├── prl_26.py
├── prl (Bash script)
└── other necessary files...
```

### Script (`prl`)

Place this script in each participant's directory:

```bash
#!/bin/bash

# Check if the correct argument was passed
if [ "$#" -ne 1 ] || [[ ! "$1" =~ ^[1-4]$ ]]; then
    echo "Usage: ./prl [1|2|3|4]"
    exit 1
fi

# Define arguments for each condition
declare -a args=("arg1" "arg2" "arg3" "arg4")

# Assign arguments based on input
condition_arg="${args[$1-1]}"

# Set the output file name
output_file="output$1.xlsx"

# Check if the output already exists
if [ -f "$output_file" ]; then
    echo "Output for condition $1 already exists: $output_file"
    exit 0
fi

# Execute the Python script
python3 prl_26.py "A" "$(basename "$PWD")" "$condition_arg"

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "Condition $1 completed successfully. Output file: $output_file"
else
    echo "Error: Failed to complete condition $1."
fi
```

### Explanation of the Script

1. **Parameter Check**: The script starts by checking if a valid argument (1, 2, 3, or 4) was passed.
2. **Arguments Definition**: Maps the command number to specific arguments (`arg1`, `arg2`, etc.) that will be passed to the Python script.
3. **Output Check**: Before running the Python script, it checks if the output file for the given condition already exists to avoid redoing the work.
4. **Script Execution**: Runs the `prl_26.py` script using the subject's folder name as the subject code, which is retrieved using `basename "$PWD"` (this fetches the name of the current directory).
5. **Execution Feedback**: Provides feedback on whether the Python script ran successfully.

### Setting Execution Permissions

Instruct participants to ensure the `prl` script has execution permissions:

```bash
chmod +x prl
```

### Running the Experiment

Participants should open their terminal, navigate to their folder (`cd path/to/their_folder`), and type:

```bash
./prl 1
```

or the appropriate number (1, 2, 3, or 4) to run the desired condition.

This setup ensures that the participant only needs to interact minimally with the system, just by entering a single command corresponding to the condition they wish to run. Everything else, including condition management and subject code handling, is automated by the script.

## Memory task
