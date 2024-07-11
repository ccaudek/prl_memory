# Define the possible values for each argument
first_arg_values <- c("A", "B")
third_arg_values <- c("Y", "N")
fourth_arg_values <- c("self", "stranger")

# Create a function to generate the sequence
get_random_conditions <- function() {
  # Create a list to store the selected conditions
  selected_conditions <- list()
  
  # Define the required combinations
  required_combinations <- list(
    list(third_arg = "Y", fourth_arg = "self"),
    list(third_arg = "N", fourth_arg = "self"),
    list(third_arg = "Y", fourth_arg = "stranger"),
    list(third_arg = "N", fourth_arg = "stranger")
  )
  
  # Randomly select the first argument for each combination
  for (combination in required_combinations) {
    first_arg <- sample(first_arg_values, 1)
    selected_conditions <- c(selected_conditions, list(
      list(first_arg = first_arg, third_arg = combination$third_arg, fourth_arg = combination$fourth_arg)
    ))
  }
  
  # Shuffle the selected conditions
  selected_conditions <- sample(selected_conditions)
  
  return(selected_conditions)
}

# Get the random conditions
random_conditions <- get_random_conditions()

# Print the commands
for (condition in random_conditions) {
  cat(paste("python prl_26.py", condition$first_arg, "codice_soggetto", condition$third_arg, condition$fourth_arg, "\n"))
}
