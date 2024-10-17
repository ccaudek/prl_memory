# Unique to v. 18.
# Append a unique identifier (a timestamp, which is both unique and informative) to
# the filename each time the script is run.

import pygame
import random
import cv2
import csv
import time
import os
import gc
from itertools import cycle
from datetime import datetime

# PyGame initialization
pygame.init()
# Initialize mixer for playing sounds
pygame.mixer.init()  # Initialize the mixer module

# Define screen dimensions
screen_width = 1000
screen_height = 800

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Probabilistic Learning Experiment")

# Load feedback images
happy_img = pygame.image.load(os.path.join("feedback_imgs", "happy.png"))
sad_img = pygame.image.load(os.path.join("feedback_imgs", "sad.png"))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define parameters
condition = "orange_rewarded_first"
n_epochs = 2
trials_per_epoch = 25
response_keys = {pygame.K_f: "Left", pygame.K_j: "Right", pygame.K_ESCAPE: "Exit"}
video_trials = [0, 10, 20, 30]

# Reward probabilities based on condition and epoch
reward_probabilities = {
    "orange_rewarded_first": [(0.9, 0.1), (0.1, 0.9)],
    "white_rewarded_first": [(0.1, 0.9), (0.9, 0.1)],
}


# Define a function to play sounds
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


def load_images(image_folder):
    image_files = [
        f for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".png")
    ]
    image_files.sort()
    images = [pygame.image.load(os.path.join(image_folder, img)) for img in image_files]
    return images, image_files


orange_images, orange_image_files = load_images("orange")
white_images, white_image_files = load_images("white")


def prepare_epoch_images():
    random.shuffle(orange_images)
    random.shuffle(white_images)
    random.shuffle(orange_image_files)
    random.shuffle(white_image_files)


def select_videos():
    videos = [f"surprise/effect_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos)
    return cycle(videos)


videos_to_play = select_videos()


def display_fixation(duration=0.5):
    screen.fill(WHITE)
    pygame.draw.line(
        screen,
        BLACK,
        (screen_width / 2 - 10, screen_height / 2),
        (screen_width / 2 + 10, screen_height / 2),
        5,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (screen_width / 2, screen_height / 2 - 10),
        (screen_width / 2, screen_height / 2 + 10),
        5,
    )
    pygame.display.flip()
    time.sleep(duration)


def get_image_file_name(key_pressed, images, image_files):
    chosen_index = 0 if key_pressed == "Left" else 1
    return image_files[chosen_index]


experiment_data = []  # Initialize list to store trial data


def save_data(trial_data, filename="experiment_data.csv", mode="a"):
    fieldnames = [
        "Trial Number",
        "Epoch",
        "Stimulus Position",
        "Key Pressed",
        "Reaction Time",
        "Feedback Received",
        "Chosen Image",
        "Most Rewarded Stimulus in Epoch",
        "Image Left",
        "Image Right",
    ]
    with open(filename, mode, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerows(trial_data)


# New lines to include a timestamp in the filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
experiment_filename = f"experiment_data_{timestamp}.csv"
save_data([], filename=experiment_filename, mode="w")  # Create the file with the header


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    resize_needed = (
        cap.get(cv2.CAP_PROP_FRAME_WIDTH) != screen_width
        or cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != screen_height
    )

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
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                cap.release()
                pygame.quit()
                return

    cap.release()
    del video_surface, frame  # Explicitly delete the objects
    gc.collect()  # Invoke garbage collector to reclaim memory
    screen.fill(BLACK)  # Clear the screen after the video
    pygame.display.flip()


# Function to display images and get response
def display_images_and_get_response(
    orange_img, white_img, epoch, orange_file, white_file
):
    screen.fill(WHITE)
    positions = ["Left", "Right"]
    random.shuffle(positions)

    if positions[0] == "Left":
        image_left_file = orange_file
        image_right_file = white_file
        screen.blit(
            orange_img,
            (
                screen_width / 4 - orange_img.get_width() / 2,
                screen_height / 2 - orange_img.get_height() / 2,
            ),
        )
        screen.blit(
            white_img,
            (
                3 * screen_width / 4 - white_img.get_width() / 2,
                screen_height / 2 - white_img.get_height() / 2,
            ),
        )
    else:
        image_left_file = white_file
        image_right_file = orange_file
        screen.blit(
            white_img,
            (
                screen_width / 4 - white_img.get_width() / 2,
                screen_height / 2 - white_img.get_height() / 2,
            ),
        )
        screen.blit(
            orange_img,
            (
                3 * screen_width / 4 - orange_img.get_width() / 2,
                screen_height / 2 - orange_img.get_height() / 2,
            ),
        )

    pygame.display.flip()

    start_time = time.time()
    key_pressed = None
    while key_pressed is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in response_keys:
                key_pressed = response_keys[event.key]
                reaction_time = time.time() - start_time
                break

    # Determine the chosen image based on the key pressed
    chosen_image_file = (
        image_left_file
        if key_pressed == response_keys[pygame.K_f]
        else image_right_file
    )

    return (
        positions[0],
        key_pressed,
        reaction_time,
        chosen_image_file,
        image_left_file,
        image_right_file,
    )


def determine_reward(epoch, stimulus_color):
    # Extract the reward probabilities for the current epoch and condition
    probs = reward_probabilities[condition][epoch]

    # Determine the probability of reward based on the chosen color
    reward_prob = probs[0] if stimulus_color == "Orange" else probs[1]

    # Generate a random number and compare it to the reward probability
    return random.random() < reward_prob


def select_videos():
    videos = [f"surprise/effect_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos)
    return cycle(videos)


def safe_exit():
    pygame.quit()
    exit()


def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            safe_exit()


# Main experiment loop
trial_results = []
trial_count = 0
for epoch in range(n_epochs):
    prepare_epoch_images()  # Ensure this function shuffles both images and their filenames
    for trial in range(trials_per_epoch):
        trial_count += 1
        check_for_exit()

        if trial in video_trials:
            video_path = next(videos_to_play, None)
            if video_path:
                display_fixation()
                play_video(video_path)

        display_fixation()

        orange_img = orange_images[trial]
        white_img = white_images[trial]
        orange_file = orange_image_files[trial]
        white_file = white_image_files[trial]

        (
            orange_pos,
            key_pressed,
            reaction_time,
            chosen_image,
            image_left,
            image_right,
        ) = display_images_and_get_response(
            orange_img, white_img, epoch, orange_file, white_file
        )

        # Determine the chosen color for feedback
        chosen_color = (
            "Orange"
            if key_pressed == "Left"
            and orange_pos == "Left"
            or key_pressed == "Right"
            and orange_pos == "Right"
            else "White"
        )

        # Get feedback based on the chosen color and epoch's reward probability
        is_correct = determine_reward(epoch, chosen_color)

        # After determining the feedback (is_correct variable)
        screen.fill(WHITE)  # Clear the screen
        if is_correct:
            screen.blit(
                happy_img,
                (
                    screen_width / 2 - happy_img.get_width() / 2,
                    screen_height / 2 - happy_img.get_height() / 2,
                ),
            )
            play_sound("beeps/pleasant.wav")
        else:
            screen.blit(
                sad_img,
                (
                    screen_width / 2 - sad_img.get_width() / 2,
                    screen_height / 2 - sad_img.get_height() / 2,
                ),
            )
            play_sound("beeps/unpleasant.wav")
        pygame.display.flip()
        time.sleep(0.5)  # Show the feedback image for 0.5 seconds

        trial_data = {
            "Trial Number": trial_count,
            "Epoch": epoch + 1,
            "Stimulus Position": orange_pos,
            "Key Pressed": key_pressed,
            "Reaction Time": reaction_time,
            "Feedback Received": is_correct,
            "Chosen Image": chosen_image,
            "Most Rewarded Stimulus in Epoch": (
                "Orange"
                if (condition == "orange_rewarded_first" and epoch == 0)
                or (condition == "white_rewarded_first" and epoch == 1)
                else "White"
            ),
            "Image Left": image_left,
            "Image Right": image_right,
        }
        experiment_data.append(trial_data)

        # Save every 5 trials
        if trial_count % 5 == 0 or (
            epoch == n_epochs - 1 and trial == trials_per_epoch - 1
        ):
            save_data(
                experiment_data, filename=experiment_filename
            )  # Pass the filename
            experiment_data = []  # Reset for the next batch

safe_exit()
