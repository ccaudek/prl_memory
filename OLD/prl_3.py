import pygame
import random
import csv
import time

# PyGame initialization
pygame.init()

# Define parameters
n_epochs = 4
trials_per_epoch = 2
n_trials = n_epochs * trials_per_epoch
image_paths = ['im1.jpg', 'im2.jpg']  # Update with correct paths
response_keys = [pygame.K_f, pygame.K_j]  # Use 'f' and 'j' as response keys
feedback_images = {'reward': 'happy.png', 'punishment': 'sad.png'}  # Update with correct paths
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Experiment')

# Load images
images = [pygame.image.load(path) for path in image_paths]
feedback_images = {key: pygame.image.load(path) for key, path in feedback_images.items()}

# Function to display fixation cross
def display_fixation(duration):
    screen.fill((255, 255, 255))  # White background
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2 - 10, screen_height / 2), (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2, screen_height / 2 - 10), (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    time.sleep(duration)

# Function to display images and get response
def display_images_and_get_response(images):
    screen.fill((255, 255, 255))  # White background
    
    # Correctly assign positions within the loop
    for index, img in enumerate(images):
        if index == 0:
            position = (screen_width / 4 - img.get_width() / 2, screen_height / 2 - img.get_height() / 2)
        else:
            position = (3 * screen_width / 4 - img.get_width() / 2, screen_height / 2 - img.get_height() / 2)
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
                    return None, None
            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None, None

    return key_pressed, reaction_time


# Function to determine reward
def determine_reward(choice, epoch):
    correct_choice = epoch % 2  # Switches every epoch
    reward = random.random() < 0.75 if response_keys.index(choice) == correct_choice else random.random() < 0.25
    return reward, correct_choice

# Function to display feedback
def display_feedback(is_reward):
    feedback_type = 'reward' if is_reward else 'punishment'
    screen.fill((255, 255, 255))  # White background
    screen.blit(feedback_images[feedback_type], (screen_width / 2 - feedback_images[feedback_type].get_width() / 2, screen_height / 2 - feedback_images[feedback_type].get_height() / 2))
    pygame.display.flip()
    time.sleep(0.5)

# Main experiment loop
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch

    # Display fixation cross
    display_fixation(random.uniform(0.2, 1.2))

    # Display images and get response
    key_pressed, reaction_time = display_images_and_get_response(images)

    if key_pressed is not None:
        # Assuming the first image is always positioned on the left and the second on the right
        stimulus_position = "Left" if key_pressed == response_keys[0] else "Right"

        reward, most_rewarded_stimulus = determine_reward(key_pressed, epoch)
        display_feedback(reward)

        # Record trial data
        trial_data = {
            "Trial Number": trial,
            "Epoch": epoch,
            "Stimulus Position": stimulus_position,
            "Key Pressed": pygame.key.name(key_pressed),
            "Reaction Time": reaction_time,
            "Feedback Received": reward,
            "Most Rewarded Stimulus in Epoch": most_rewarded_stimulus
        }
        experiment_data.append(trial_data)

# Save data to a CSV file
with open('experiment_data.csv', 'w', newline='') as csvfile:
    fieldnames = ["Trial Number", "Epoch", "Stimulus Position", "Key Pressed", "Reaction Time", "Feedback Received", "Most Rewarded Stimulus in Epoch"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in experiment_data:
        writer.writerow(data)

pygame.quit()
