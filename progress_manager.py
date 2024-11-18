import json
import os

# Standarddata för en ny spelare
default_progress = {
    "level": 1,
    "current_session": 1,
    "total_earnings": 0,
    "guest_satisfaction": 100,
    "unlocked_upgrades": [],
}

# Filnamn för att lagra spelarens framsteg
PROGRESS_FILE = "progress.json"

# Funktion för att ladda framsteg
def load_progress():
    if os.path.exists(PROGRESS_FILE):  # Kontrollera om filen finns
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)  # Ladda data från filen
    else:
        return default_progress  # Om ingen fil finns, använd standarddata

# Funktion för att spara framsteg
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file, indent=4)

# Funktion för att återställa framsteg
def reset_progress():
    save_progress(default_progress)
