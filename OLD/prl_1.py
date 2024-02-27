from psychopy import visual, core, event, data, gui
import random
import csv

# Define parameters
n_epochs = 4
trials_per_epoch = 5
n_trials = n_epochs * trials_per_epoch
image_paths = ['im1.jpg', 'im2.jpg']  # Update with correct paths
response_keys = ['f', 'j']  # Use 'f' and 'j' as response keys
feedback_images = {'reward': 'happy.png', 'punishment': 'sad.png'}  # Update with correct paths

# Initialize PsychoPy components
win = visual.Window(fullscr=True, color=(1, 1, 1))
images = [visual.ImageStim(win, image=path) for path in image_paths]
feedback_stims = {key: visual.ImageStim(win, image=path) for key, path in feedback_images.items()}
fixation = visual.TextStim(win, text='+', color=(-1, -1, -1))
trial_clock = core.Clock()

# Function to display fixation cross
def display_fixation(duration):
    fixation.draw()
    win.flip()
    core.wait(duration)

# Function to display images and get response
def display_images_and_get_response(images):
    positions = random.sample([[-0.5, 0], [0.5, 0]], k=2)
    for img, pos in zip(images, positions):
        img.pos = pos
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
    reward = random.random() < 0.75 if response_keys.index(choice) == correct_choice else random.random() < 0.25
    return reward, correct_choice

# Function to display feedback
def display_feedback(is_reward):
    feedback_type = 'reward' if is_reward else 'punishment'
    feedback_stims[feedback_type].draw()
    win.flip()
    core.wait(0.5)

# Main experiment loop
experiment_data = []
for trial in range(n_trials):
    epoch = trial // trials_per_epoch

    # Display fixation cross
    display_fixation(random.uniform(0.2, 1.2))

    # Display images and get response
    key_pressed, reaction_time = display_images_and_get_response(images)

    if key_pressed is not None:
        reward, most_rewarded_stimulus = determine_reward(key_pressed, epoch)
        display_feedback(reward)

        # Record trial data
        trial_data = {
            "Trial Number": trial,
            "Epoch": epoch,
            "Stimulus Position": "Right" if images[0].pos[0] > 0 else "Left",
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
