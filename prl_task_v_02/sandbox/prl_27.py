"""
Script Instructions:

Stimulus Selection:
- Press the "f" key to select the stimulus located on the LEFT side of the screen.
- Press the "j" key to select the stimulus located on the RIGHT side of the screen.

Mood Slider Adjustment:
- Use the "f" key for a small decrement and the "d" key for a large decrement to adjust the mood slider leftwards.
- Use the "j" key for a small increment and the "k" key for a large increment to adjust the mood slider rightwards.

Coded Experiment Conditions:
- Argument "A" corresponds to the "orange_rewarded_first" condition.
- Argument "B" corresponds to the "white_rewarded_first" condition.

Video type can be 'Y' for Surprise videos or 'N' for No-Surprise videos.

Data File Naming:

Each run of the script generates a uniquely named data file, incorporating a timestamp to 
ensure distinctiveness and traceability.

Debugging:

In the debugging phase, the `reward_probabilities` are set to 0.9 and 0.1. 
In the experiment, these values will be 0.8 and 0.2.

Example:

python3 prl_26.py "A" "co_ba_1999_03_23_333_f" "Y"
python3 prl_26.py "B" "co_ba_1999_03_23_333_f" "N"

Version: 0.27
Date: 2024-10-14
"""

import pygame
import random
import cv2
import csv
import time
import os
import gc
import pygame_gui
import sys
from itertools import cycle
from datetime import datetime

# Check if the command line argument for condition is provided
if len(sys.argv) < 4:
    print("Usage: python3 prl_27.py <code> <subject_code> <video_type>")
    print("<code> can be 'A' or 'B'")
    print("<video_type> can be 'Y' for S videos or 'N' for N videos")
    sys.exit(1)  # Exit the script if the necessary arguments are not provided


# Parse command line arguments
code = sys.argv[1]  # "A", "B", "C", "D"
subject_code = sys.argv[2]  # subject_1, subject_2, etc.
video_type_arg = sys.argv[3]  # Y for surprise, N for no surprise

# Load the images based on the subject and condition
orange_images, white_images = load_images(subject_code, code)

condition_map = {
    "A": "orange_rewarded_first",
    "B": "white_rewarded_first",
}

# Map the video type argument to the corresponding description for output file writing
video_type_description_map = {
    "Y": "surprise_videos",
    "N": "not_surprising_videos",
}

if video_type_arg not in video_type_description_map:
    print("Invalid video type. Please choose 'Y' for surprise or 'N' for no surprise.")
    sys.exit(1)  # Exit the script if an invalid video type argument is provided

# Set the video description based on the decoded value
video_description = video_type_description_map[video_type_arg]

video_type_map = {
    "Y": "surprise",
    "N": "nosurprise",
}

# Set the condition based on the decoded value
condition = condition_map[code]

if code not in condition_map:
    print("Invalid code. Please choose 'A' or 'B'.")
    sys.exit(1)  # Exit the script if an invalid code is provided

if video_type_arg not in video_type_map:
    print("Invalid video type. Please choose 'Y' for surprise or 'N' for no surprise.")
    sys.exit(1)  # Exit the script if an invalid video type argument is provided

# Set the video folder based on the decoded value
video_folder = video_type_map[video_type_arg]

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Set up the display to full screen
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
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
# condition = "orange_rewarded_first"
n_epochs = 2
trials_per_epoch = 25
video_trials = [0, 10, 20, 30]
response_keys = {pygame.K_f: "Left", pygame.K_j: "Right", pygame.K_ESCAPE: "Exit"}

# Reward probabilities based on condition and epoch
reward_probabilities = {
    "orange_rewarded_first": [(0.9, 0.1), (0.1, 0.9)],  # 0.8, 0.2
    "white_rewarded_first": [(0.1, 0.9), (0.9, 0.1)],
}


def display_mood_slider():
    pygame.mouse.set_visible(True)  # Show cursor for visual feedback
    manager = pygame_gui.UIManager(
        (screen_width, screen_height), "data/themes/theme.json"
    )

    initial_value = 50  # Default start value
    slider_rect = pygame.Rect(
        (screen_width / 2 - 450, screen_height / 2 - 25), (900, 50)
    )  # Center the slider
    mood_slider = pygame_gui.elements.UIHorizontalSlider(
        slider_rect, initial_value, (0, 100), manager
    )
    # Continue button is no longer needed to be visible, managed by spacebar press
    slider_changed = False  # Track if the slider has been changed

    def adjust_slider_value(key):
        nonlocal slider_changed
        current_value = mood_slider.get_current_value()
        if key in [pygame.K_d, pygame.K_k]:  # Large movement keys
            step = 10 if key == pygame.K_k else -10
        elif key in [pygame.K_f, pygame.K_j]:  # Small movement keys
            step = 1 if key == pygame.K_j else -1
        else:
            step = 0
        new_value = max(0, min(100, current_value + step))
        mood_slider.set_current_value(new_value)
        if new_value != initial_value:
            slider_changed = True  # Mark slider as changed when it moves from initial

    running = True
    font = pygame.font.SysFont(None, 24)  # Adjust font size as needed
    text_surface_left = font.render("Molto male", True, BLACK)
    text_surface_right = font.render("Molto bene", True, BLACK)
    text_rect_left = text_surface_left.get_rect(
        center=(slider_rect.left - 60, slider_rect.centery)
    )  # Adjust position
    text_rect_right = text_surface_right.get_rect(
        center=(slider_rect.right + 60, slider_rect.centery)
    )  # Adjust position

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    safe_exit()
                adjust_slider_value(event.key)  # Adjust slider based on key press
                if (
                    event.key == pygame.K_SPACE and slider_changed
                ):  # Check if slider changed before proceeding
                    running = False

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill(WHITE)
        screen.blit(text_surface_left, text_rect_left)
        screen.blit(text_surface_right, text_rect_right)
        manager.draw_ui(screen)
        pygame.display.flip()

    mood_value = mood_slider.get_current_value()
    pygame.mouse.set_visible(False)  # Hide cursor again
    return mood_value


def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            safe_exit()
            # Ensure cursor is visible when exiting
            pygame.mouse.set_visible(True)


# Define a function to play sounds
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


# Define the mapping of conditions to image ranges
image_ranges = {
    "A": (1, 25),  # Self/surprise: images 1-25
    "B": (26, 50),  # Self/no-surprise: images 26-50
    "C": (51, 75),  # Stranger/surprise: images 51-75
    "D": (76, 100),  # Stranger/no-surprise: images 76-100
}


def load_images(subject_code, condition_code):
    # Get the range of images for the given condition
    orange_range, white_range = image_ranges[condition_code]

    # Construct paths to the subject's image directories
    orange_folder = os.path.join("images", subject_code, "orange")
    white_folder = os.path.join("images", subject_code, "white")

    # Load the appropriate range of images for orange and white
    orange_images = [
        pygame.image.load(os.path.join(orange_folder, f"orange_old_{i}.jpg"))
        for i in range(orange_range[0], orange_range[1] + 1)
    ]
    white_images = [
        pygame.image.load(os.path.join(white_folder, f"white_old_{i}.jpg"))
        for i in range(white_range[0], white_range[1] + 1)
    ]

    return orange_images, white_images


orange_images, orange_image_files = load_images("orange")
white_images, white_image_files = load_images("white")


def prepare_epoch_images():
    random.shuffle(orange_images)
    random.shuffle(white_images)
    random.shuffle(orange_image_files)
    random.shuffle(white_image_files)


def select_videos():
    # Use the video_folder variable to determine the path
    folder_path = video_folder
    if folder_path == "surprise":
        videos = [f"{folder_path}/effect_{i}.mov" for i in range(1, 11)]
    else:  # folder_path == "nosurprise"
        videos = [f"{folder_path}/noeffect_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos)
    return cycle(videos)


videos_to_play = select_videos()


def display_fixation():
    duration = random.uniform(
        0.25, 1.25
    )  # Random duration between 0.25 and 1.25 seconds
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
    start_time = time.time()
    while time.time() - start_time < duration:
        check_for_exit()


def get_image_file_name(key_pressed, images, image_files):
    chosen_index = 0 if key_pressed == "Left" else 1
    return image_files[chosen_index]


experiment_data = []  # Initialize list to store trial data


def save_data(trial_data, filename="experiment_data.csv", mode="a"):
    fieldnames = [
        "Subject Code",
        "Condition",  # Add condition to output
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
        "Mood Slider Value",
        "Video Type",  # New field for video type
        "Video File Name",
    ]
    with open(filename, mode, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()  # Write the header only if the file is new
        for data in trial_data:
            data["Subject Code"] = subject_code
            data["Condition"] = condition_map[code]  # Include condition
            data["Video Type"] = video_description  # Include video type
        writer.writerows(trial_data)  # Write the trial data


# Use the provided subject_code when generating the filename for experiment data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
experiment_filename = f"experiment_data_{subject_code}_{timestamp}.csv"
save_data([], filename=experiment_filename, mode="w")  # Create the file with the header


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None  # Return None if the video couldn't be opened

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
        check_for_exit()

    cap.release()
    del video_surface, frame  # Explicitly delete the objects
    gc.collect()  # Invoke garbage collector to reclaim memory
    screen.fill(BLACK)  # Clear the screen after the video
    pygame.display.flip()

    return os.path.basename(video_path)  # Return the name of the video file played


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
            if event.type == pygame.KEYDOWN:
                if event.key in response_keys:
                    key_pressed = response_keys[event.key]
                    reaction_time = time.time() - start_time
                    break
                elif event.key == pygame.K_ESCAPE:
                    safe_exit()

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
# Modify the main experiment loop to include the mood slider display every four trials
for epoch in range(n_epochs):
    prepare_epoch_images()  # Ensure this function shuffles both images and their filenames
    for trial in range(trials_per_epoch):
        trial_count += 1
        check_for_exit()

        video_file_name = None  # Initialize outside the loop
        if trial in video_trials:
            video_path = next(videos_to_play, None)
            if video_path:
                display_fixation()
                video_file_name = play_video(video_path)  # Capture the video file name

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

        if trial_count % 4 == 0:
            mood_slider_value = display_mood_slider()  # Capture the slider value
        else:
            mood_slider_value = (
                None  # Or a default value indicating the slider was not shown
            )

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
            "Mood Slider Value": mood_slider_value,
            "Video Type": video_description,  # Keep including video type as before
            "Video File Name": video_file_name,  # Include the video file name in the trial data
        }
        experiment_data.append(trial_data)

        # Save every 5 trials
        if trial_count % 5 == 0 or (
            epoch == n_epochs - 1 and trial == trials_per_epoch - 1
        ):
            save_data(
                experiment_data, filename=experiment_filename
            )  # Pass the updated filename
            experiment_data = []  # Reset for the next batch of data

    # Ensure cursor is visible when exiting
    pygame.mouse.set_visible(True)

safe_exit()
