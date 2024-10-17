from psychopy import visual, core, event, data, gui
import random
import csv

# Define parameters
n_epochs = 4
trials_per_epoch = 40
n_trials = n_epochs * trials_per_epoch
image_paths = ['im1.jpg', 'im2.jpg']  # Update with correct paths
response_keys = ['f', 'j']  # Use 'f' and 'j' as response keys

# Initialize PsychoPy components
win = visual.Window(fullscr=True, color=(1, 1, 1))
images = [visual.ImageStim(win, image=path) for path in image_paths]
trial_clock = core.Clock()

# Function to display images and get response
def display_images_and_get_response(images, trial):
    # Randomize positions for the trial
    positions = [[-0.5, 0], [0.5, 0]] if trial % 2 == 0 else [[0.5, 0], [-0.5, 0]]
    for img, pos in zip(images, positions):
        img.pos = pos

    # Draw images
    for img in images:
        img.draw()
    win.flip()

    trial_clock.reset()
    keys = event.waitKeys(keyList=response_keys, timeStamped=trial_clock)
    if keys:
        key, reaction_time = keys[0]
    else:
        key, reaction_time = None, None

    return key, reaction_time

# Function to determine reward
def determine_reward(choice, epoch):
    correct_choice = epoch % 2  # Switches every epoch
    if response_keys.index(choice) == correct_choice:
        return random.random() < 0.75, correct_choice
    else:
        return random.random() < 0.25, correct_choice

# Main experiment loop
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch
    key_pressed, reaction_time = display_images_and_get_response(images, trial)
    if key_pressed is not None:
        reward, most_rewarded_stimulus = determine_reward(key_pressed, epoch)

        # Record trial data
        trial_data = {
            "Trial Number": trial,
            "Epoch": epoch,
            "Stimulus Position": "Right" if trial % 2 == 0 else "Left",
            "Key Pressed": key_pressed,
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

win.close()
