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
condition = "orange_rewarded_first"
n_epochs = 2
trials_per_epoch = 20
response_keys = {pygame.K_f: 'Left', pygame.K_j: 'Right', pygame.K_ESCAPE: 'Exit'}
video_trials = [0, 10, 20, 30]

# Reward probabilities based on condition and epoch
reward_probabilities = {
    "orange_rewarded_first": [(0.9, 0.1), (0.1, 0.9)],
    "white_rewarded_first": [(0.1, 0.9), (0.9, 0.1)]
}

def determine_reward(epoch, stimulus_color):
    orange_prob, white_prob = reward_probabilities[condition][epoch]
    return random.random() < (orange_prob if stimulus_color == 'Orange' else white_prob)

def load_images(image_folder):
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]
    image_files.sort()
    return [pygame.image.load(os.path.join(image_folder, img)) for img in image_files]

orange_images = load_images('orange') * 5
white_images = load_images('white') * 5
random.shuffle(orange_images)
random.shuffle(white_images)

def select_videos():
    videos = [f"surprise/effect_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos)
    return cycle(videos)

videos_to_play = select_videos()

def display_fixation(duration=0.5):
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (screen_width / 2 - 10, screen_height / 2),
                     (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, BLACK, (screen_width / 2, screen_height / 2 - 10),
                     (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    time.sleep(duration)

def get_image_file_name(key_pressed, images):
    # Dummy function for demonstration
    return "orange.jpg" if "orange" in images[0] else "white.jpg"

experiment_data = []  # Initialize list to store trial data

def save_data(trial_data, filename='experiment_data.csv', mode='a'):
    fieldnames = ["Trial Number", "Epoch", "Stimulus Position", "Key Pressed", "Reaction Time", "Feedback Received", "Chosen Image", "Most Rewarded Stimulus in Epoch"]
    with open(filename, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if it's writing mode
            writer.writeheader()
        writer.writerows(trial_data)

# Initially create the file with a header
save_data([], mode='w')  # This creates the file with the header only

trial_count = 0  # Counter to keep track of trials for saving every five trials

# Main experiment loop
for epoch in range(n_epochs):
    for trial in range(trials_per_epoch):
        trial_count += 1

        if trial in video_trials:
            video_path = next(videos_to_play, None)
            if video_path:
                display_fixation()
                play_video(video_path)

        display_fixation()
        orange_img = orange_images.pop()
        white_img = white_images.pop()
        orange_pos, key_pressed, reaction_time, _ = display_images_and_get_response(orange_img, white_img, epoch, None)

        is_correct = determine_reward(epoch, 'Orange' if orange_pos == key_pressed else 'White')
        
        chosen_image = get_image_file_name(key_pressed, [orange_images[-1], white_images[-1]])
        most_rewarded_stimulus = 'Orange' if epoch % 2 == 0 else 'White'
        trial_data = {
            "Trial Number": trial + 1,
            "Epoch": epoch + 1,
            "Stimulus Position": orange_pos,
            "Key Pressed": key_pressed,
            "Reaction Time": reaction_time,
            "Feedback Received": is_correct,
            "Chosen Image": chosen_image,
            "Most Rewarded Stimulus in Epoch": most_rewarded_stimulus
        }
        experiment_data.append(trial_data)

        # Save every 5 trials
        if trial_count % 5 == 0 or (epoch == n_epochs - 1 and trial == trials_per_epoch - 1):
            save_data(experiment_data)
            experiment_data = []  # Reset for the next batch


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


# Function to display images and get response
def display_images_and_get_response(orange_img, white_img, epoch, last_video_played):
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

    start_time = time.time()
    key_pressed = None
    while key_pressed is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in response_keys:
                key_pressed = response_keys[event.key]
                reaction_time = time.time() - start_time
                break  # Added to exit the loop once a key is pressed

    # No need to calculate reward here as it's not part of the output
    return orange_pos, key_pressed, reaction_time, last_video_played

# Main experiment loop
trial_results = []
video_iterator = iter(videos_to_play)  # Iterator for videos
last_video_played = None  # Track the last video played

for epoch in range(n_epochs):
    for trial in range(trials_per_epoch):
        if trial in video_trials:
            video_path = next(video_iterator, None)
            if video_path:
                display_fixation()
                play_video(video_path)
                last_video_played = video_path  # Update the last video played

        display_fixation()
        orange_img = orange_images.pop()
        white_img = white_images.pop()
        orange_pos, key_pressed, reaction_time, video_played = display_images_and_get_response(orange_img, white_img, epoch, last_video_played)

        is_correct = determine_reward(epoch, 'Orange' if orange_pos == key_pressed else 'White')  # Determine correctness based on chosen color
        trial_results.append([epoch, trial, orange_pos, key_pressed, reaction_time, is_correct, video_played])

# Save results to CSV with is_correct column and video file
with open('experiment_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['Epoch', 'Trial', 'Orange Position', 'Key Pressed', 'Reaction Time', 'Is Correct', 'Last Video Played']
    writer.writerow(header)
    writer.writerows(trial_results)

# Close Pygame
pygame.quit()