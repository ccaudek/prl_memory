import pygame
import random
import csv
import time

# PyGame initialization
pygame.init()

# Define parameters
n_epochs = 4
trials_per_epoch = 2  # Adjust this to your desired number of trials per epoch
n_trials = n_epochs * trials_per_epoch
image_paths = ['im1.jpg', 'im2.jpg']  # Update with correct paths
response_keys = [pygame.K_f, pygame.K_j]  # Use 'f' and 'j' as response keys
feedback_images_paths = {'reward': 'happy.png', 'punishment': 'sad.png'}  # Update with correct paths
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Experiment')

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
    reward_probabilities = [(0.9, 0.1), (0.1, 0.9)]  # (Epochs 1&3, Epochs 2&4)
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
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch

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
