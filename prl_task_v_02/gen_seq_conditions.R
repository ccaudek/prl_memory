# Definire i possibili valori per orange_first (T, F)
orange_first_values <- c("T", "F")

# Funzione per generare la sequenza delle condizioni casuali
get_random_conditions <- function(subject_code) {
  # Creare una lista per memorizzare le condizioni selezionate
  selected_conditions <- list()
  
  # Definire le 4 combinazioni richieste (auto/etero-riferita con sorpresa/non sorpresa)
  required_combinations <- list(
    list(first_arg = "A", description = "self_surprise", orange_first = sample(orange_first_values, 1)),
    list(first_arg = "B", description = "self_no_surprise", orange_first = sample(orange_first_values, 1)),
    list(first_arg = "C", description = "stranger_surprise", orange_first = sample(orange_first_values, 1)),
    list(first_arg = "D", description = "stranger_no_surprise", orange_first = sample(orange_first_values, 1))
  )
  
  # Mescolare le condizioni selezionate in modo casuale
  selected_conditions <- sample(required_combinations)
  
  return(selected_conditions)
}

# Ottenere le condizioni casuali per il soggetto
subject_code <- "subject_1"  # Qui si può modificare il codice del soggetto
random_conditions <- get_random_conditions(subject_code)

# Stampare i comandi in formato appropriato per eseguire lo script Python
for (condition in random_conditions) {
  cat(paste("python3 prl_29.py", 
            sprintf('"%s"', subject_code), 
            sprintf('"%s"', condition$first_arg), 
            sprintf('"%s"', condition$orange_first), 
            "#", condition$description, ",", 
            ifelse(condition$orange_first == "T", "arancione premiata prima", "bianca premiata prima"), "\n"))
}
