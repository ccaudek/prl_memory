#

import pygame
import random
import cv2
import os
from itertools import cycle
import gc  # For garbage collection


# PyGame initialization
pygame.init()

# Define screen dimensions
screen_width = 800  # Example width
screen_height = 600  # Example height

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('Experiment')


# Define parameters
condition = "surprise"  # Assuming you have a variable 'condition' that can be 'surprise' or 'nosurprise'

n_epochs = 2
trials_per_epoch = 25  # Adjust this to your desired number of trials per epoch
n_trials = n_epochs * trials_per_epoch
response_keys = [pygame.K_f, pygame.K_j]  # Use 'f' and 'j' as response keys
feedback_images_paths = {'reward': 'happy.png', 'punishment': 'sad.png'}  # Update with correct paths


# Assuming you've loaded the images into two lists: orange_images and white_images
# and have a way to ensure they're presented exactly twice.

orange_images = ["orange_old_1.jpg", "orange_old_2.jpg", "orange_old_3.jpg", 
                 "orange_old_4.jpg", "orange_old_5.jpg", "orange_old_6.jpg", 
                 "orange_old_7.jpg", "orange_old_8.jpg", "orange_old_9.jpg", 
                 "orange_old_10.jpg"]
white_images = ["white_old_1.jpg", "white_old_2.jpg", "white_old_3.jpg", 
                "white_old_4.jpg", "white_old_5.jpg", "white_old_6.jpg", 
                "white_old_7.jpg", "white_old_8.jpg", "white_old_9.jpg", 
                "white_old_10.jpg"]

def get_image_file_name(epoch, trial_number, key_pressed):
    # Assuming 'f' corresponds to "orange" folder and 'j' to "white" folder
    folder = "orange" if key_pressed == 'f' else "white"
    # Constructing the file name
    file_name = f"{folder}_old_{trial_number}.jpg"
    return file_name

# Create a cumulative count for each trial within an epoch
# Define the cumulative count logic
trial_numbers_by_epoch = {} 
trial_numbers_by_epoch = experiment_data.groupby('Epoch').cumcount() + 1

# Display the dataframe with the new column added
experiment_data[['Trial Number', 'Epoch', 'Key Pressed', 'Chosen Image', 'Chosen Image File']].head()


def randomize_images_for_pygame(folder_path, num_images=1):
    """
    Randomly selects `num_images` from the specified `folder_path` and loads them for Pygame.
    
    Parameters:
    - folder_path (str): Path to the folder containing images.
    - num_images (int): Number of images to select.
    
    Returns:
    - List of Pygame image objects.
    """
    all_images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
    selected_image_paths = random.sample(all_images, num_images)
    return [pygame.image.load(img_path) for img_path in selected_image_paths]

# Load images for the experiment
def load_images(folder_path):
    return [pygame.image.load(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.endswith('.jpg')]

orange_images = load_images('orange')  # Pass the correct folder path for orange images
white_images = load_images('white')    # Pass the correct folder path for white images

# Create cycles for both image sets
orange_cycle = cycle(orange_images * 2)  # Each image twice
white_cycle = cycle(white_images * 2)




video_played = []
videos_to_play = []

def select_videos_for_condition(condition):
    global videos_to_play
    folder = 'surprise' if condition == 'surprise' else 'no_surprise'
    prefix = 'effect' if condition == 'surprise' else 'noeffect'
    videos_to_play = [f"{folder}/{i}_{prefix}.mov" for i in range(1, 11)]
    shuffle(videos_to_play)  # Shuffle to randomize order

select_videos_for_condition(condition)  # Call this when condition is known

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

    # Optionally, clear the surface here if needed
    screen.fill((0, 0, 0))  # Fill the screen with black to clear it
    pygame.display.flip()

# Load images
images = [pygame.image.load(path) for path in image_paths]
feedback_images = {key: pygame.image.load(path) for key, path in feedback_images_paths.items()}

# Function to display fixation cross
def display_fixation(duration):
    screen.fill((255, 255, 255))  # White background
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2 - 10, screen_height / 2), (screen_width / 2 + 10, screen_height / 2), 5)
    pygame.draw.line(screen, (0, 0, 0), (screen_width / 2, screen_height / 2 - 10), (screen_width / 2, screen_height / 2 + 10), 5)
    pygame.display.flip()
    pygame.time.wait(int(duration * 1000))
    
# Select videos for the given condition
def select_videos_for_condition(condition):
    folder = 'surprise' if condition == 'surprise' else 'no_surprise'
    prefix = 'effect' if condition == 'surprise' else 'noeffect'
    videos_to_play = [f"{folder}/{i}_{prefix}.mov" for i in range(1, 11)]
    random.shuffle(videos_to_play)  # Shuffle to randomize order
    return videos_to_play

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

# Main experiment loop with modifications for reward determination and stimulus positioning
# Main experiment loop with modifications for reward determination, stimulus positioning, and video playback
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch
    
    # Determine the trial number within the current epoch
    epoch_trial_number = trial_numbers_by_epoch.setdefault(epoch, 0) + 1
    trial_numbers_by_epoch[epoch] = epoch_trial_number
    
    # Assuming you want to play videos at specific trials, adjust the condition as needed
    if trial % trials_per_epoch in [0, 4]:  # Example condition to play video at first and fifth trial of each epoch
        if videos_to_play:  # Ensure there is a video to play
            play_video(videos_to_play.pop(0))  # Play and remove the video from the list

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
            "Chosen Image": get_image_file_name(epoch, epoch_trial_number, key_pressed),
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
