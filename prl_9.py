import pygame
import random
import cv2
import csv
import time
import os
import gc
from itertools import cycle

# PyGame initialization
pygame.init()

# Define screen dimensions
screen_width = 1000
screen_height = 800

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Probabilistic Learning Experiment')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define parameters
condition = "orange_rewarded_first"  # Updated to new condition
n_epochs = 2
trials_per_epoch = 20
response_keys = {pygame.K_f: 'Left', pygame.K_j: 'Right'}
video_trials = [0, 10, 20, 30]

# Reward probabilities based on condition and epoch
reward_probabilities = {
    "orange_rewarded_first": [(0.9, 0.1), (0.1, 0.9)]  # (epoch1: (orange, white), epoch2: (orange, white))
}

# Function to determine reward based on the current epoch and stimulus
def determine_reward(epoch, stimulus_color):
    orange_prob, white_prob = reward_probabilities[condition][epoch]
    if stimulus_color == 'Orange':
        return random.random() < orange_prob
    else:  # stimulus_color == 'White'
        return random.random() < white_prob

# Load images into lists
def load_images(image_folder):
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]
    image_files.sort()  # Ensures the order is consistent
    return [pygame.image.load(os.path.join(image_folder, img)) for img in image_files]

orange_images = load_images('orange') * 5  # Adjusted for extended trial count
white_images = load_images('white') * 5
random.shuffle(orange_images)
random.shuffle(white_images)

# Function to select and shuffle videos
def select_videos():
    videos = [f"surprise/effect_{i}.mov" for i in range(1, 11)]  # Adjusted for 10 videos
    random.shuffle(videos)
    return cycle(videos)  # Use cycle to repeat the video list if needed

videos_to_play = select_videos()

# Display functions
def display_fixation(duration=0.5):
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (screen_width / 2 - 10, screen_height / 2),
                     (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, BLACK, (screen_width / 2, screen_height / 2 - 10),
                     (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    time.sleep(duration)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    resize_needed = cap.get(cv2.CAP_PROP_FRAME_WIDTH) != screen_width or cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != screen_height

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if resize_needed:
            frame = cv2.resize(frame, (screen_width, screen_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_surface = pygame.surfarray.make_surface(frame.transpose([1, 0, 2]))
        screen.blit(video_surface, (0, 0))
        pygame.display.flip()

        pygame.time.wait(int(1000 / cap.get(cv2.CAP_PROP_FPS)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                cap.release()
                pygame.quit()
                return

    cap.release()
    del video_surface, frame  # Explicitly delete the objects
    gc.collect()  # Invoke garbage collector to reclaim memory

    screen.fill(BLACK)  # Clear the screen after the video
    pygame.display.flip()


def display_images_and_get_response(orange_img, white_img, epoch):
    screen.fill(WHITE)
    positions = ['Left', 'Right']
    random.shuffle(positions)
    orange_pos = positions.pop()
    white_pos = positions.pop()

    if orange_pos == 'Left':
        screen.blit(orange_img, (screen_width / 4 - orange_img.get_width() / 2, screen_height / 2 - orange_img.get_height() / 2))
        screen.blit(white_img, (3 * screen_width / 4 - white_img.get_width() / 2, screen_height / 2 - white_img.get_height() / 2))
    else:
        screen.blit(white_img, (screen_width / 4 - white_img.get_width() / 2, screen_height / 2 - white_img.get_height() / 2))
        screen.blit(orange_img, (3 * screen_width / 4 - orange_img.get_width() / 2, screen_height / 2 - orange_img.get_height() / 2))

    pygame.display.flip()

    # Capture response
    start_time = time.time()
    key_pressed = None
    while key_pressed is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in response_keys:
                key_pressed = response_keys[event.key]
                reaction_time = time.time() - start_time

                # Determine reward probabilities for current epoch
                if condition == "orange_rewarded_first":
                    reward_probabilities = {0: {'orange': 0.9, 'white': 0.1},
                                            1: {'orange': 0.1, 'white': 0.9}}
                else:
                    reward_probabilities = {0: {'orange': 0.1, 'white': 0.9},
                                            1: {'orange': 0.9, 'white': 0.1}}

                current_probabilities = reward_probabilities[epoch]
                correct_choice = 'orange' if random.random() < current_probabilities['orange'] else 'white'
                is_correct = (key_pressed == orange_pos and correct_choice == 'orange') or (key_pressed == white_pos and correct_choice == 'white')

                # Display feedback
                feedback_color = GREEN if is_correct else RED
                feedback_text = 'Correct!' if is_correct else 'Wrong!'
                font = pygame.font.SysFont(None, 55)
                text_surf = font.render(feedback_text, True, feedback_color)
                screen.blit(text_surf, (screen_width / 2 - text_surf.get_width() / 2, screen_height / 2 + 100))
                pygame.display.flip()

                time.sleep(0.5)  # Show feedback for 0.5 seconds
                return orange_pos, key_pressed, reaction_time, is_correct

# Main experiment loop
trial_results = []
video_iterator = iter(videos_to_play)  # Iterator for videos

for epoch in range(n_epochs):
    for trial in range(trials_per_epoch):
        if trial in video_trials:
            video_path = next(video_iterator, None)
            if video_path:
                display_fixation()
                play_video(video_path)

        display_fixation()
        orange_img = orange_images.pop()
        white_img = white_images.pop()
        orange_pos, key_pressed, reaction_time, is_correct = display_images_and_get_response(orange_img, white_img, epoch)

        trial_results.append([epoch, trial, orange_pos, key_pressed, reaction_time, is_correct])

# Close Pygame
pygame.quit()

# Save results to CSV with is_correct column
with open('experiment_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Epoch', 'Trial', 'Orange Position', 'Key Pressed', 'Reaction Time', 'Is Correct'])
    writer.writerows(trial_results)