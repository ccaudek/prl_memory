# Nell'esperimento ci sono 4 condizioni: 
# "surprise-self", "nosurprise-self", "surprise-stranger", "nosurprise-stranger".
# Le condizioni sono definite dagli stimoli usati nel compito Probabilistic Reversal Learning e
# dai video che vengono mostrati.

# Ogni condizione ha 2 epoche con 25 prove per epoca.

# Cambiamento 1. -----
# Un video viene presentato prima delle prove 1, 10, 20, 30, 40.
# I cinque video presentati sono tutti diversi tra loro e sono presi a caso dai 10 possibili 
# in ciascuna condizione (sorpresa, non sorpresa), con il vincolo che non si devono ripetere
# nella sequenza in una sessione dell'esperimento.
# Nella condizione sorpresa i video sono contenuti nella cartella 'surprise' e 
# hanno i nomi "1_effect.mov", "2_effect.mov", ..., "10_effect.mov". 
# Nella condizione "no-surprise", i video sono contenuti nella cartella 'no_surprise' e 
# hanno i nomi "1_noeffect.mov", "2_noeffect.mov", ..., "10_noeffect.mov".
# Nota che i diversi video hanno durate temporali diverse.

# Cambiamento 2. ------
# Ci sono 25 stimoli (immagini) con sfondo arancione e 25 stimoli con sfondo bianco.
# In ogni prova viene presentato uno stimolo 'arancione' e uno stimolo 'bianco'.
# Le immagini orange sono presenti nella cartella "orange" e sono chiamate 
# "orange_old_1.jpg", "orange_old_2.jpg", ..., "orange_old_25.jpg".
# Le immagini white sono preenti nella cartella "white" e sono chiamate 
# "white_old_1.jpg" ... "white_old_25.jpg".
# In ciascuna prova del compito PRL viene presentata a caso un'immagine "orange" e un'immagine 
# "white", con il vincolo che nelle 50 prove di una sessione ciascuna immagine orange e white
# viene presentata esattamente due volte.
# La sequenza degli stimoli/prove e la posizione destra/sinistra degli stimoli è
# completamente casuale ogni volta che lo script viene lanciato.

# Cambiamento 3. ------
# In input, quando viene lanciato lo script con l'istruzione "python3 prl_5.py", deve essere
# passato l'argomento "is_self" con modalità possibili "stranger" o "self". Il valore di questo 
# argomento va stampato in output.

# Cambiamento 4. ------
# In input, quando viene lanciato lo script con l'istruzione "python3 prl_5.py", deve essere
# passato l'argomento "is_surprise" con modalità "surprise" o "nosurprise".  Il valore di questo 
# argomento va stampato in output.

# Cambiamento 5. ------
# In output, stampare una colonna con il nome del file presentato a sinistra nella prova 
# corrente del PRL.
# In output, stampare una colonna con il nome del file presentato a destra nella prova 
# corrente del PRL.

# Cambiamento 6. ------
# In output, nella colonna "video", stampare il nome del video presentato. Nella riga di output corrispondente
# alle prove 1--10 andrà stampato il nome del video presentato prima della prova 1.
# Nella riga di output corrispondente alle prove 11--20 andrà stampato il nome del video 
# presentato prima della prova 10. Eccetera.

# Cambiamento 7. ------
# Dopo la quarta prova, presentare una schermata con il messaggio: 
# "Quanto ti senti felice in questo momento?"  
# Attendere la risposta da tastiera. Tasti possibili: d, f, j, k.
# In output, stampare nella colonna "happiness" il nome del tasto premuto e, nella colonna
# rt_happiness, il tempo di reazione, ovvero il tempo che intercorre da quando il messaggio 
# viene presentato a quando il tasto viene premuto.

# Cambiamento 8. -----
# In output, nella colonna "intertrial_time", stampa anche l'inter-trial delay.


import pygame
import random
import cv2
import csv
import time

# PyGame initialization
pygame.init()

# Define parameters
n_epochs = 2
trials_per_epoch = 25  # Adjust this to your desired number of trials per epoch
n_trials = n_epochs * trials_per_epoch
image_paths = ['im1.jpg', 'im2.jpg']  # Update with correct paths
response_keys = [pygame.K_f, pygame.K_j]  # Use 'f' and 'j' as response keys
feedback_images_paths = {'reward': 'happy.png', 'punishment': 'sad.png'}  # Update with correct paths
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Experiment')

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video size
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if there are no frames left

        # Convert the frame from BGR to RGB (PyGame uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))  # Resize to fit your screen

        # Convert to PyGame surface
        video_surface = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))
        screen.blit(video_surface, (0, 0))

        pygame.display.flip()

        # Frame rate control
        pygame.time.wait(int(1000 / cap.get(cv2.CAP_PROP_FPS)))

        # Check for PyGame quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                cap.release()
                pygame.quit()
                return

    # Release the video capture object
    cap.release()

# Load images
images = [pygame.image.load(path) for path in image_paths]
feedback_images = {key: pygame.image.load(path) for key, path in feedback_images_paths.items()}

# Display fixation cross function
def display_fixation(duration):
    screen.fill((255, 255, 255))  # White background
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2 - 10, screen_height / 2), (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2, screen_height / 2 - 10), (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    time.sleep(duration)

# Modified function to display images and get response
def display_images_and_get_response():
    screen.fill((255, 255, 255))  # White background
    
    # Randomize the position of the images
    shuffled_images = random.sample(images, len(images))
    positions = [(screen_width / 4 - shuffled_images[0].get_width() / 2, screen_height / 2 - shuffled_images[0].get_height() / 2),
                 (3 * screen_width / 4 - shuffled_images[1].get_width() / 2, screen_height / 2 - shuffled_images[1].get_height() / 2)]
    
    for img, position in zip(shuffled_images, positions):
        screen.blit(img, position)
    pygame.display.flip()

    start_time = time.time()
    key_pressed = None
    reaction_time = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in response_keys:
                    key_pressed = event.key
                    reaction_time = time.time() - start_time
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    return None, None, None

            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None, None, None

    stimulus_position = "Left" if positions[0][0] < screen_width / 2 else "Right"
    return key_pressed, reaction_time, stimulus_position, shuffled_images == images

# Updated function to determine reward based on new specifications
def determine_reward(choice, epoch, stimulus_position, is_original_order):
    # Define reward probabilities
    reward_probabilities = [(0.9, 0.1), (0.1, 0.9)]  # (Epochs 1&3, Epochs 2&4) ### .8, .2
    current_probs = reward_probabilities[epoch % 2]

    # Determine which image was chosen based on key press and stimulus position
    chosen_side = 0 if stimulus_position == "Left" else 1
    chosen_image_is_A = (chosen_side == 0 and is_original_order) or (chosen_side == 1 and not is_original_order)

    # Determine if reward is given based on the chosen image's probability
    if chosen_image_is_A:
        reward = random.random() < current_probs[0]
    else:
        reward = random.random() < current_probs[1]

    return reward

# Function to display feedback
def display_feedback(is_reward):
    feedback_type = 'reward' if is_reward else 'punishment'
    screen.fill((255, 255, 255))  # White background
    screen.blit(feedback_images[feedback_type], (screen_width / 2 - feedback_images[feedback_type].get_width() / 2, screen_height / 2 - feedback_images[feedback_type].get_height() / 2))
    pygame.display.flip()
    time.sleep(0.5)

# Main experiment loop with modifications for reward determination and stimulus positioning
# Main experiment loop with modifications for reward determination, stimulus positioning, and video playback
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch

    # Check if it's the first or fifth trial of the epoch to play the video
    if trial % trials_per_epoch == 0 or trial % trials_per_epoch == 4:
        play_video('video_1.mp4')

    # Display fixation cross
    display_fixation(random.uniform(0.2, 1.2))

    # Display images and get response
    key_pressed, reaction_time, stimulus_position, is_original_order = display_images_and_get_response()

    if key_pressed is not None:
        reward = determine_reward(key_pressed, epoch, stimulus_position, is_original_order)
        display_feedback(reward)

        # Record trial data
        trial_data = {
            "Trial Number": trial + 1,
            "Epoch": epoch + 1,
            "Stimulus Position": stimulus_position,
            "Key Pressed": pygame.key.name(key_pressed),
            "Reaction Time": reaction_time,
            "Feedback Received": reward,
            "Chosen Image": 'A' if is_original_order else 'B',
            "Most Rewarded Stimulus in Epoch": 'A' if epoch % 2 == 0 else 'B'
        }
        experiment_data.append(trial_data)

# Save data to a CSV file
with open('experiment_data.csv', 'w', newline='') as csvfile:
    fieldnames = ["Trial Number", "Epoch", "Stimulus Position", "Key Pressed", "Reaction Time", "Feedback Received", "Chosen Image", "Most Rewarded Stimulus in Epoch"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in experiment_data:
        writer.writerow(data)

pygame.quit()
