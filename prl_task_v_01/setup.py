from setuptools import setup

APP = ["prl_26.py"]
DATA_FILES = ["feedback_imgs", "orange", "white", "surprise", "nosurprise", "beeps"]
OPTIONS = {
    "argv_emulation": True,
    "packages": ["pygame", "cv2", "csv", "pygame_gui", "gc"],
    "resources": DATA_FILES,
    # "iconfile": "icon.icns",  # Opzionale: Aggiungi il percorso al tuo file icona se ne hai uno
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
