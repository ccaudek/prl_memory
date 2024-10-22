import pygame
import random
import time
import os
import csv
from datetime import datetime
import sys
import gc

# Definire i colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inizializzare pygame
pygame.init()
pygame.mixer.init()

# Clock per controllare il framerate
clock = pygame.time.Clock()

# Caricare i suoni
nice_sound = pygame.mixer.Sound("beeps/pleasant.wav")
ugly_sound = pygame.mixer.Sound("beeps/unpleasant.wav")

# Definire la mappatura delle condizioni con gli intervalli di immagini
image_ranges = {
    "A": (1, 50),  # Self/surprise: immagini 1-50
    "B": (51, 100),  # Self/no-surprise: immagini 51-100
    "C": (1, 50),  # Stranger/surprise: immagini 1-50
    "D": (51, 100),  # Stranger/no-surprise: immagini 51-100
}


# Funzione per caricare immagini da un percorso, selezionando solo l'intervallo specificato
def load_images_from_folder(folder, start, end):
    images = []
    for i in range(start, end + 1):
        filename = f"{folder.split('/')[-1]}_img_{i:03d}.png"
        img_path = os.path.join(folder, filename)
        if os.path.exists(img_path):
            img = pygame.image.load(img_path)
            images.append((img, filename))
    return images


# Funzione per chiudere il programma in modo sicuro e salvare i dati prima di uscire
def safe_exit(subject_code, condition, trial_results, filename):
    print("Uscita dal programma. Salvataggio dei dati...")
    save_data(subject_code, condition, trial_results, filename)
    pygame.quit()
    sys.exit(0)


# Funzione per salvare i dati in un file CSV
def save_data(subject_code, condition, trial_results, filename):
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=trial_results[0].keys())
        if os.stat(filename).st_size == 0:
            writer.writeheader()  # Scrive l'header solo se il file è vuoto
        writer.writerows(trial_results)


# Funzione per creare il compito di memoria
def memory_task(
    subject_code,
    condition,
    old_orange_images,
    old_white_images,
    new_orange_images,
    new_white_images,
    filename,
):
    # Impostazioni della finestra
    screen_width, screen_height = (
        pygame.display.Info().current_w,
        pygame.display.Info().current_h,
    )
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Memory Task")

    # Caricare tutte le immagini old e new
    all_old_images = old_orange_images + old_white_images
    new_images_by_color = {"orange": new_orange_images, "white": new_white_images}

    # Funzione per mostrare un punto di fissazione
    def display_fixation():
        screen.fill(WHITE)
        pygame.draw.line(
            screen,
            BLACK,
            (screen_width // 2 - 10, screen_height // 2),
            (screen_width // 2 + 10, screen_height // 2),
            5,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (screen_width // 2, screen_height // 2 - 10),
            (screen_width // 2, screen_height // 2 + 10),
            5,
        )
        pygame.display.flip()
        pygame.time.wait(100)

    # Funzione per mostrare schermo nero per un intervallo casuale
    def display_black_screen():
        screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.wait(random.randint(200, 1000))

    # Funzione per visualizzare le immagini e raccogliere la risposta
    def display_images_and_get_response(old_image, new_image, old_image_side):
        screen.fill(WHITE)

        # Randomizzare la posizione dell'immagine old (sinistra o destra)
        if old_image_side == "left":
            image_left, image_right = old_image, new_image
        else:
            image_left, image_right = new_image, old_image

        # Visualizzare le immagini a sinistra e a destra
        screen.blit(
            image_left[0],
            (
                screen_width // 4 - image_left[0].get_width() // 2,
                screen_height // 2 - image_left[0].get_height() // 2,
            ),
        )
        screen.blit(
            image_right[0],
            (
                3 * screen_width // 4 - image_right[0].get_width() // 2,
                screen_height // 2 - image_right[0].get_height() // 2,
            ),
        )
        pygame.display.flip()

        start_time = time.time()
        key_pressed = None

        # Attendere la risposta dell'utente o un timeout di 3 secondi
        while time.time() - start_time < 3:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        safe_exit(
                            subject_code, condition, trial_results, filename
                        )  # Uscita con ESC e salvataggio dei dati
                    elif event.key == pygame.K_f:
                        key_pressed = "left"
                    elif event.key == pygame.K_j:
                        key_pressed = "right"
                    if key_pressed:
                        reaction_time = time.time() - start_time
                        return key_pressed, reaction_time

        # Se il partecipante non risponde entro 3 secondi
        reaction_time = 3
        return None, reaction_time

    # Preparare la sequenza delle prove
    trials = []
    for old_image in all_old_images:
        color = "orange" if old_image in old_orange_images else "white"
        new_image = random.choice(
            new_images_by_color[color]
        )  # Scegliere una nuova immagine dello stesso colore
        old_image_side = random.choice(
            ["left", "right"]
        )  # Determinare se l'immagine old va a sinistra o a destra
        trials.append((old_image, new_image, old_image_side))

    # Randomizzare l'ordine delle prove
    random.shuffle(trials)

    # Eseguire il compito di memoria
    trial_results = []
    for trial_num, (old_image, new_image, old_image_side) in enumerate(trials):
        display_black_screen()
        display_fixation()

        # Visualizzare le immagini e raccogliere la risposta
        key_pressed, reaction_time = display_images_and_get_response(
            old_image, new_image, old_image_side
        )

        # Determinare se la risposta è corretta
        if key_pressed == old_image_side:
            correct = True
            nice_sound.play()  # Suono di feedback corretto
        else:
            correct = False
            ugly_sound.play()  # Suono di feedback sbagliato

        # Salvare i risultati della prova
        trial_data = {
            "Trial Number": trial_num + 1,
            "Old Image": old_image[1],
            "New Image": new_image[1],
            "Old Image Side": old_image_side,
            "Key Pressed": key_pressed,
            "Correct": correct,
            "Reaction Time": reaction_time,
            "Condition": condition,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        trial_results.append(trial_data)

        pygame.time.wait(500)  # Attendere mezzo secondo dopo la risposta

        # Salvare ogni 5 prove
        if (trial_num + 1) % 5 == 0:
            save_data(subject_code, condition, trial_results, filename)
            trial_results = []  # Ripristina i risultati memorizzati temporaneamente

    return trial_results


# Eseguire il compito di memoria
def run_memory_task(subject_code, condition):
    # Determinare l'intervallo di immagini da usare in base alla condizione
    start, end = image_ranges[condition]

    # Determinare il percorso delle cartelle delle immagini
    base_path = (
        f"./images/{subject_code}_{'self' if condition in ['A', 'B'] else 'stranger'}"
    )
    old_orange_folder = os.path.join(base_path, "old_orange")
    old_white_folder = os.path.join(base_path, "old_white")
    new_orange_folder = os.path.join(base_path, "new_orange")
    new_white_folder = os.path.join(base_path, "new_white")

    # Caricare le immagini dalle cartelle con l'intervallo corretto
    old_orange_images = load_images_from_folder(old_orange_folder, start, end)
    old_white_images = load_images_from_folder(old_white_folder, start, end)
    new_orange_images = load_images_from_folder(new_orange_folder, start, end)
    new_white_images = load_images_from_folder(new_white_folder, start, end)

    # Creare un file per salvare i risultati
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memory_task_{subject_code}_{condition}_{timestamp}.csv"

    # Eseguire il compito di memoria
    trial_results = memory_task(
        subject_code,
        condition,
        old_orange_images,
        old_white_images,
        new_orange_images,
        new_white_images,
        filename,
    )

    # Salvare i risultati finali
    if trial_results:
        save_data(subject_code, condition, trial_results, filename)

    # Chiudere pygame
    pygame.quit()


# Esempio di esecuzione
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python memory_task.py <subject_code> <condition>")
        sys.exit(1)

    subject_code = sys.argv[1]
    condition = sys.argv[2]

    run_memory_task(subject_code, condition)
