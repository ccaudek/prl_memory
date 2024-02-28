# I need a script in python for a probabilistic learning experiment. 
#
# In each trial there are two stimuli, one "orange" and one "white" and are 
# displayed side by side on the right and the left of the screen.
#
# The orange stimuli are called 
# orange_images = ["orange_old_1.jpg", "orange_old_2.jpg", ..., "orange_old_25.jpg"] 
# and are placed in a folder called "orange". 
# The white stimuli are called 
# white_images = ["white_old_1.jpg", "white_old_2.jpg", ..., "white_old_25.jpg"]
# and are placed in a folder called "white".
#
# On each trial, one white and one orange image is selected at random and the two
# images are shown on the screen. The constraint is that, in the total 50 trials of the 
# experiment, each image can be show exactly twice. The random-order presentation will
# vary randomly each time the script is run.
#
# Before the trials 1, 11, 21, 31, 41, a video will be shown. 
# In the condition "surprise", the five videos will be chosen randomly from 10 possible. 
# The 10 video files for the condition surprise are contained in the folder "surprise" 
# and are called "1_effect.mov", ..., "10_effect.mov".
# In the condition "nosurprise", the five videos will be chosen randomly from 10 possible. 
# The 10 video files for the condition nosurprise are contained in the folder "nosurprise" 
# and are called "1_noeffect.mov", ..., "10_noeffect.mov".
#
# In the condition "orange_reward_first", in the first epoch the orange stimulus will be 
# rewarded with probability 0.9  and the white stimulus will be rewarded with probability 
# 0.1; in the second epoch, the orange stimulus will be rewarded with probability 0.1 
# and the white stimulus will be rewarded with probability 0.9. 
# In the condition "white_reward_first", in the first epoch the orange stimulus will be 
# rewarded with probability 0.1 and the white stimulus will be rewarded with probability 
# 0.9; in the second epoch, the orange stimulus will be rewarded with probability 0.9 
# and the white stimulus will be rewarded with probability 0.1.
#
# Key press mapping: Pressing the "f" key in a trial means that the subject chooses the 
# stimulus on the left; pressing the "j" key in a trial means that the subject chooses the 
# stimulus on the right.
#
# The csv output file will contain the following information:
# Trial Number, Epoch, Orange stimulus position, Withe stimulus position, key pressed,
# Reaction time (the time between the presentation of the two stimuli and the key press), 
# Feedback received (positive or negative), Image chosen by the subject (the name of
# the file corresponding to the image chosen by the subject), Image shown on the left (the
# name of the file of the image shown on the left), Image shown on the right (the
# name of the file of the image shown on the right), Video (name of the file of the last video 
# shown).


import pygame
import random
import cv2
import csv
import time
import os
from itertools import cycle
import gc  # For garbage collection

# PyGame initialization
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('Experiment')

# Define parameters
condition = "surprise"
n_epochs = 2
trials_per_epoch = 25
n_trials = n_epochs * trials_per_epoch
response_keys = {pygame.K_f: 'f', pygame.K_j: 'j'}

# Load images into lists and ensure they're presented exactly twice
def load_images(image_folder):
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    image_files.sort()  # Ensure the order is correct
    return [os.path.join(image_folder, img) for img in image_files]

orange_images = load_images('orange')
white_images = load_images('white')

orange_cycle = cycle(orange_images * 2)
white_cycle = cycle(white_images * 2)

# Function to display fixation cross
def display_fixation(duration):
    screen.fill((255, 255, 255))  # White background
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2 - 10, screen_height / 2), 
                     (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2, screen_height / 2 - 10), 
                     (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    time.sleep(duration)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    resize_needed = cap.get(cv2.CAP_PROP_FRAME_WIDTH) != screen_width or cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != screen_height
    
def display_images_and_get_response():
    screen.fill((255, 255, 255))  # White background
    # Randomly select one image from each category
    orange_img_path = random.choice(orange_images)
    white_img_path = random.choice(white_images)
    orange_img = pygame.image.load(orange_img_path)
    white_img = pygame.image.load(white_img_path)
    
    # Randomize the position of the images and display them
    positions = ['Left', 'Right']
    random.shuffle(positions)
    orange_pos = positions.pop()
    white_pos = positions.pop()
    
    # Blit the orange image on the chosen position
    if orange_pos == 'Left':
        screen.blit(orange_img, (screen_width / 4 - orange_img.get_width() / 2, screen_height / 2 - orange_img.get_height() / 2))
    else:
        screen.blit(orange_img, (3 * screen_width / 4 - orange_img.get_width() / 2, screen_height / 2 - orange_img.get_height() / 2))
    
    # Blit the white image on the remaining position
    if white_pos == 'Left':
        screen.blit(white_img, (screen_width / 4 - white_img.get_width() / 2, screen_height / 2 - white_img.get_height() / 2))
    else:
        screen.blit(white_img, (3 * screen_width / 4 - white_img.get_width() / 2, screen_height / 2 - white_img.get_height() / 2))
    
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
    
# Select videos for the given condition
def select_videos_for_condition(condition):
    folder = 'surprise' if condition == 'surprise' else 'no_surprise'
    prefix = 'effect' if condition == 'surprise' else 'noeffect'
    videos_to_play = [f"{folder}/{prefix}_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos_to_play)  # Shuffle to randomize order
    return videos_to_play

videos_to_play = select_videos_for_condition(condition)

# Function to get image file name based on condition
def get_image_file_name(key_pressed, image_list):
    if key_pressed == 'f':
        image_name = [img for img in image_list if 'orange' in img][0]
    else:
        image_name = [img for img in image_list if 'white' in img][0]
    return os.path.basename(image_name)

# Main experiment loop
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch
    trial_in_epoch = trial % trials_per_epoch + 1

    # Play video if it's the first or fifth trial of the epoch
    if trial_in_epoch in [1, 5]:
        video_index = (trial_in_epoch - 1) // 5
        play_video(videos_to_play[video_index])

    display_fixation(0.5)  # Display fixation cross for 0.5 seconds
    key_pressed, reaction_time, stimulus_position = display_images_and_get_response()

    # Determine if the choice was correct and display feedback
    is_correct_choice = determine_reward(key_pressed, epoch, stimulus_position, True)
    display_feedback(is_correct_choice)

    # Record trial data
    chosen_image = get_image_file_name(key_pressed, [orange_images[trial_in_epoch - 1], white_images[trial_in_epoch - 1]])
    most_rewarded_stimulus = 'A' if epoch % 2 == 0 else 'B'  # This is a placeholder
    trial_data = {
        "Trial Number": trial + 1,
        "Epoch": epoch + 1,
        "Stimulus Position": stimulus_position,
        "Key Pressed": key_pressed,
        "Reaction Time": reaction_time,
        "Feedback Received": is_correct_choice,
        "Chosen Image": chosen_image,
        "Most Rewarded Stimulus in Epoch": most_rewarded_stimulus
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
