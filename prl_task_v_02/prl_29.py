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

# Check if the correct number of command-line arguments is provided
if len(sys.argv) < 4:
    print("Usage: python3 prl.py <subject_code> <condition> <orange_first>")
    print("<condition> can be 'A', 'B', 'C', or 'D'")
    print(
        "<orange_first> can be 'T' for orange rewarded first or 'F' for white rewarded first"
    )
    sys.exit(1)  # Exit the script if the necessary arguments are not provided

# Parse command line arguments
subject_code = sys.argv[1]  # e.g., "subject_1"
condition_code = sys.argv[2]  # "A", "B", "C", "D"
orange_first_arg = sys.argv[3]  # "T" for orange first, "F" for white first

# Ensure valid condition
condition_map = {
    "A": "self_surprise",
    "B": "self_no_surprise",
    "C": "stranger_surprise",
    "D": "stranger_no_surprise",
}

if condition_code not in condition_map:
    print("Invalid condition code")
    sys.exit(1)

# Set the variable orange_first based on the input "T" or "F"
orange_first = True if orange_first_arg == "T" else False

# Define the mapping of conditions to image ranges and video type
image_ranges = {
    "A": (1, 50),  # Self/surprise: images 1-50
    "B": (51, 100),  # Self/no-surprise: images 51-100
    "C": (1, 50),  # Stranger/surprise: images 1-50
    "D": (51, 100),  # Stranger/no-surprise: images 51-100
}

video_type_map = {
    "A": "surprise",
    "B": "nosurprise",
    "C": "surprise",
    "D": "nosurprise",
}

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


import csv
from datetime import datetime


def save_data(trial_data, filename="experiment_data.csv", mode="a"):
    fieldnames = [
        "Subject Code",
        "Condition",
        "Trial Number",
        "Epoch",
        "Chosen Color",
        "Orange First",
        "Stimulus Position",
        "Key Pressed",
        "Reaction Time",
        "Feedback Received",
        "Chosen Image",
        "Most Rewarded Stimulus in Epoch",
        "Image Left",
        "Image Right",
        "Mood Slider Value",
        "Video Type",
        "Video File Name",
    ]

    with open(filename, mode, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()  # Write the header only if the file is new
        for data in trial_data:
            data["Subject Code"] = subject_code
            data["Condition"] = condition_code  # Include condition code directly
            data["Video Type"] = video_type_map[condition_code]  # Include video type
        writer.writerows(trial_data)  # Write the trial data


# Use the provided subject_code and condition when generating the filename for experiment data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
experiment_filename = f"experiment_data_{subject_code}_{condition_code}_{timestamp}.csv"

save_data([], filename=experiment_filename, mode="w")  # Create the file with the header


# Define a function to play sounds
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


def determine_reward(epoch, stimulus_color):
    # Extract the reward probabilities for the current epoch
    probs = reward_probabilities[epoch]

    # Determine the probability of reward based on the chosen color
    reward_prob = probs[0] if stimulus_color == "Orange" else probs[1]

    # Generate a random number and compare it to the reward probability
    return random.random() < reward_prob


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


def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            safe_exit()
            # Ensure cursor is visible when exiting
            pygame.mouse.set_visible(True)


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


# Load images for the PRL task based on subject and condition
def load_images(subject_code, condition_code):
    start, end = image_ranges[condition_code]
    folder_type = "self" if condition_code in ["A", "B"] else "stranger"
    subject_folder = f"{subject_code}_{folder_type}"
    orange_folder = os.path.join("images", subject_folder, "old_orange")
    white_folder = os.path.join("images", subject_folder, "old_white")

    try:
        orange_images = [
            pygame.image.load(
                os.path.join(orange_folder, f"old_orange_img_{i:03d}.png")
            )
            for i in range(start, end + 1)
        ]
        white_images = [
            pygame.image.load(os.path.join(white_folder, f"old_white_img_{i:03d}.png"))
            for i in range(start, end + 1)
        ]
        orange_image_files = [
            f"old_orange_img_{i:03d}.png" for i in range(start, end + 1)
        ]
        white_image_files = [
            f"old_white_img_{i:03d}.png" for i in range(start, end + 1)
        ]
        return orange_images, white_images, orange_image_files, white_image_files
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading images from folders:\n{orange_folder}\n{white_folder}")
        print(f"Error details: {str(e)}")
        safe_exit()


# Load images based on the subject and condition
orange_images, white_images, orange_image_files, white_image_files = load_images(
    subject_code, condition_code
)

# Define reward probabilities based on the orange_first variable
if orange_first:
    reward_probabilities = [(0.9, 0.1), (0.1, 0.9)]  # Orange rewarded first
else:
    reward_probabilities = [(0.1, 0.9), (0.9, 0.1)]  # White rewarded first

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Set up the display to full screen
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Probabilistic Learning Experiment")

# Load feedback images
happy_img = pygame.image.load(os.path.join("feedback_imgs", "happy.png"))
sad_img = pygame.image.load(os.path.join("feedback_imgs", "sad.png"))


# Function to display the mood slider
def display_mood_slider():
    pygame.mouse.set_visible(True)
    manager = pygame_gui.UIManager(
        (screen_width, screen_height), "data/themes/theme.json"
    )
    initial_value = 50
    slider_rect = pygame.Rect(
        (screen_width / 2 - 450, screen_height / 2 - 25), (900, 50)
    )
    mood_slider = pygame_gui.elements.UIHorizontalSlider(
        slider_rect, initial_value, (0, 100), manager
    )
    slider_changed = False

    def adjust_slider_value(key):
        nonlocal slider_changed
        current_value = mood_slider.get_current_value()
        if key in [pygame.K_d, pygame.K_k]:
            step = 10 if key == pygame.K_k else -10
        elif key in [pygame.K_f, pygame.K_j]:
            step = 1 if key == pygame.K_j else -1
        else:
            step = 0
        new_value = max(0, min(100, current_value + step))
        mood_slider.set_current_value(new_value)
        if new_value != initial_value:
            slider_changed = True

    running = True
    font = pygame.font.SysFont(None, 24)
    text_surface_left = font.render("Molto male", True, (0, 0, 0))
    text_surface_right = font.render("Molto bene", True, (0, 0, 0))
    text_rect_left = text_surface_left.get_rect(
        center=(slider_rect.left - 60, slider_rect.centery)
    )
    text_rect_right = text_surface_right.get_rect(
        center=(slider_rect.right + 60, slider_rect.centery)
    )

    while running:
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    safe_exit()
                adjust_slider_value(event.key)
                if event.key == pygame.K_SPACE and slider_changed:
                    running = False
            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((255, 255, 255))
        screen.blit(text_surface_left, text_rect_left)
        screen.blit(text_surface_right, text_rect_right)
        manager.draw_ui(screen)
        pygame.display.flip()

    mood_value = mood_slider.get_current_value()
    pygame.mouse.set_visible(False)
    return mood_value


# Function to play videos based on the condition (surprise or no-surprise)
def select_videos(video_type):
    folder_path = "surprise" if video_type == "surprise" else "nosurprise"
    if folder_path == "surprise":
        videos = [f"{folder_path}/effect_{i}.mov" for i in range(1, 11)]
    else:
        videos = [f"{folder_path}/noeffect_{i}.mov" for i in range(1, 11)]
    random.shuffle(videos)
    return cycle(videos)


# Function to play a selected video
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
    screen.fill((0, 0, 0))  # Clear the screen after the video
    pygame.display.flip()

    return os.path.basename(video_path)  # Return the name of the video file played


# Safely exit the experiment
def safe_exit():
    pygame.mixer.stop()
    pygame.mixer.quit()
    pygame.display.quit()
    pygame.quit()
    gc.collect()
    sys.exit(0)


# Main experiment loop
trial_results = []
n_epochs = 2
trials_per_epoch = 25
video_trials = [0, 10, 20, 30]
trial_count = 0
response_keys = {pygame.K_f: "Left", pygame.K_j: "Right", pygame.K_ESCAPE: "Exit"}


# Determine video type from condition
video_type = video_type_map[condition_code]

# Select the video cycle based on the condition (surprise or no-surprise)
videos_to_play = select_videos(video_type)


for epoch in range(n_epochs):
    random.shuffle(orange_images)
    random.shuffle(white_images)
    random.shuffle(orange_image_files)
    random.shuffle(white_image_files)

    # Determine the most rewarded stimulus for this epoch
    if orange_first:
        most_rewarded_stimulus = "orange" if epoch == 0 else "white"
    else:
        most_rewarded_stimulus = "white" if epoch == 0 else "orange"

    for trial in range(trials_per_epoch):
        trial_count += 1
        check_for_exit()

        # Display fixation cross before each trial
        display_fixation()

        # Play a video if the trial is one of the video_trials
        video_file_name = None
        if trial in video_trials:
            video_path = next(videos_to_play, None)
            if video_path:
                video_file_name = play_video(video_path)

        orange_img = orange_images[trial % len(orange_images)]
        white_img = white_images[trial % len(white_images)]
        orange_file = orange_image_files[trial % len(orange_image_files)]
        white_file = white_image_files[trial % len(white_image_files)]

        # Present images and collect the response
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

        chosen_color = (
            "Orange"
            if (key_pressed == "Left" and orange_pos == "Left")
            or (key_pressed == "Right" and orange_pos == "Right")
            else "White"
        )
        is_correct = determine_reward(epoch, chosen_color)

        # Show feedback after choice
        screen.fill((255, 255, 255))
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
        pygame.time.wait(500)

        if trial_count % 4 == 0:
            mood_slider_value = display_mood_slider()
        else:
            mood_slider_value = None

        # Store trial data
        trial_data = {
            "Trial Number": trial_count,
            "Epoch": epoch + 1,
            "Chosen Color": chosen_color,
            "Stimulus Position": orange_pos,
            "Key Pressed": key_pressed,
            "Reaction Time": reaction_time,
            "Feedback Received": is_correct,
            "Orange First": orange_first,
            "Chosen Image": chosen_image,
            "Image Left": image_left,
            "Image Right": image_right,
            "Mood Slider Value": mood_slider_value,
            "Video File Name": video_file_name,
            "Most Rewarded Stimulus in Epoch": most_rewarded_stimulus,  # Add the computed value here
        }
        trial_results.append(trial_data)

        # Save data every 5 trials
        if trial_count % 5 == 0:
            save_data(trial_results, filename=experiment_filename)
            trial_results = []  # Clear trial results after saving to file

# Ensure any remaining data is saved at the end of the experiment
if trial_results:
    save_data(trial_results, filename=experiment_filename)

# Ensure cursor is visible when exiting
pygame.mouse.set_visible(True)

safe_exit()
