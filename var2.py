import requests
import time
import random
import ollama
import re
import sys
from collections import defaultdict

# Configuration
host = ""
NUM_ROUNDS = 10

# Player words dictionary (unchanged)
player_words = {
    1: {"word": "Sandpaper", "cost": 8},
    2: {"word": "Oil", "cost": 10},
    3: {"word": "Steam", "cost": 15},
    4: {"word": "Acid", "cost": 16},
    5: {"word": "Gust", "cost": 18},
    6: {"word": "Boulder", "cost": 20},
    7: {"word": "Drill", "cost": 20},
    8: {"word": "Vacation", "cost": 20},
    9: {"word": "Fire", "cost": 22},
    10: {"word": "Drought", "cost": 24},
    11: {"word": "Water", "cost": 25},
    12: {"word": "Vacuum", "cost": 27},
    13: {"word": "Laser", "cost": 28},
    14: {"word": "Life Raft", "cost": 30},
    15: {"word": "Bear Trap", "cost": 32},
    16: {"word": "Hydraulic Jack", "cost": 33},
    17: {"word": "Diamond Cage", "cost": 35},
    18: {"word": "Dam", "cost": 35},
    19: {"word": "Sunshine", "cost": 35},
    20: {"word": "Mutation", "cost": 35},
    21: {"word": "Kevlar Vest", "cost": 38},
    22: {"word": "Jackhammer", "cost": 38},
    23: {"word": "Signal Jammer", "cost": 40},
    24: {"word": "Grizzly", "cost": 41},
    25: {"word": "Reinforced Steel Door", "cost": 42},
    26: {"word": "Bulldozer", "cost": 42},
    27: {"word": "Sonic Boom", "cost": 45},
    28: {"word": "Robot", "cost": 45},
    29: {"word": "Glacier", "cost": 45},
    30: {"word": "Love", "cost": 45},
    31: {"word": "Fire Blanket", "cost": 48},
    32: {"word": "Super Glue", "cost": 48},
    33: {"word": "Therapy", "cost": 48},
    34: {"word": "Disease", "cost": 50},
    35: {"word": "Fire Extinguisher", "cost": 50},
    36: {"word": "Satellite", "cost": 50},
    37: {"word": "Confidence", "cost": 50},
    38: {"word": "Absorption", "cost": 52},
    39: {"word": "Neutralizing Agent", "cost": 55},
    40: {"word": "Freeze", "cost": 55},
    41: {"word": "Encryption", "cost": 55},
    42: {"word": "Proof", "cost": 55},
    43: {"word": "Molotov Cocktail", "cost": 58},
    44: {"word": "Rainstorm", "cost": 58},
    45: {"word": "Viral Meme", "cost": 58},
    46: {"word": "War", "cost": 59},
    47: {"word": "Dynamite", "cost": 60},
    48: {"word": "Seismic Dampener", "cost": 60},
    49: {"word": "Propaganda", "cost": 60},
    50: {"word": "Explosion", "cost": 62},
    51: {"word": "Lightning", "cost": 65},
    52: {"word": "Evacuation", "cost": 65},
    53: {"word": "Flood", "cost": 67},
    54: {"word": "Lava", "cost": 68},
    55: {"word": "Reforestation", "cost": 70},
    56: {"word": "Avalanche", "cost": 72},
    57: {"word": "Earthquake", "cost": 74},
    58: {"word": "H-bomb", "cost": 75},
    59: {"word": "Dragon", "cost": 75},
    60: {"word": "Innovation", "cost": 75},
    61: {"word": "Hurricane", "cost": 76},
    62: {"word": "Tsunami", "cost": 78},
    63: {"word": "Persistence", "cost": 80},
    64: {"word": "Resilience", "cost": 85},
    65: {"word": "Terraforming Device", "cost": 89},
    66: {"word": "Anti-Virus Nanocloud", "cost": 90},
    67: {"word": "AI Kill Switch", "cost": 90},
    68: {"word": "Nanobot Swarm", "cost": 92},
    69: {"word": "Reality Resynchronizer", "cost": 92},
    70: {"word": "Cataclysm Containment Field", "cost": 92},
    71: {"word": "Solar Deflection Array", "cost": 93},
    72: {"word": "Planetary Evacuation Fleet", "cost": 94},
    73: {"word": "Antimatter Cannon", "cost": 95},
    74: {"word": "Planetary Defense Shield", "cost": 96},
    75: {"word": "Singularity Stabilizer", "cost": 97},
    76: {"word": "Orbital Laser", "cost": 98},
    77: {"word": "Time", "cost": 100}
}

# Creating a word id lookup by word name
word_id_by_name = {v["word"].lower(): k for k, v in player_words.items()}

logical_counters = {
    # Common materials
    "paper": ["Fire", "Acid", "Water", "Scissors", "Laser"],
    "rock": ["Drill", "Jackhammer", "Acid", "Dynamite", "Bulldozer", "Laser"],
    "metal": ["Acid", "Laser", "Fire", "Drill", "Rust"],
    "wood": ["Fire", "Saw", "Acid", "Sandpaper", "Drill", "Termites"],
    "glass": ["Sonic Boom", "Sandpaper", "Hammer", "Boulder", "Explosion"],
    "plastic": ["Fire", "Acid", "Laser", "Scissors"],
    "concrete": ["Jackhammer", "Dynamite", "Acid", "Drill", "Bulldozer"],
    "ice": ["Fire", "Steam", "Sunshine", "Laser"],
    "rubber": ["Fire", "Laser", "Acid", "Scissors"],

    # Elements & phenomena
    "water": ["Drought", "Vacuum", "Absorption", "Dam", "Freeze"],
    "fire": ["Water", "Fire Extinguisher", "Fire Blanket", "Vacuum", "Foam"],
    "earth": ["Jackhammer", "Drill", "Bulldozer", "Dynamite", "Earthquake"],
    "air": ["Vacuum", "Absorption", "Containment", "Pressure"],
    "wind": ["Dam", "Wall", "Mountain", "Shelter"],
    "lightning": ["Grounding", "Faraday Cage", "Rubber", "Insulation"],

    # Concepts & events
    "stress": ["Vacation", "Therapy", "Love", "Meditation"],
    "fear": ["Confidence", "Love", "Therapy", "Knowledge"],
    "time": ["Persistence", "Resilience", "Love", "Innovation"],
    "virus": ["Anti-Virus Nanocloud", "Neutralizing Agent", "Vaccination"],
    "attack": ["Defense", "Kevlar Vest", "Diamond Cage", "Force Field"],
    "disaster": ["Evacuation", "Preparation", "Planning", "Insurance"],

    # Digital/technical
    "signal": ["Signal Jammer", "Encryption", "Absorption", "Interference"],
    "data": ["Encryption", "Deletion", "Corruption", "AI Kill Switch"],
    "computer": ["Virus", "Water", "Hammer", "Electricity Outage"],
    "sensor": ["Signal Jammer", "Laser", "Obstruction", "Overload"],

    # Force & pressure
    "pressure": ["Release Valve", "Hydraulic Jack", "Absorption", "Vacuum"],
    "explosion": ["Containment", "Absorption", "Evacuation", "Distance"],
    "earthquake": ["Seismic Dampener", "Reinforced Steel Door", "Evacuation"],
    "flood": ["Dam", "Absorption", "Evacuation", "High Ground"],

    # Generic fallbacks
    "unknown": ["Water", "Fire", "Resilience", "Innovation", "Time"],
    "default": ["Resilience", "Innovation", "Time", "Love", "Water", "Fire"]
}

#ensuring all counter words actually exist in our player_words
for sys_word, counters in logical_counters.items():
    logical_counters[sys_word] = [word for word in counters if word.lower() in [v["word"].lower() for v in player_words.values()]]

def get_random_system_word():
    """Get system word from stdin"""
    sys_word = sys.stdin.readline().strip()
    return sys_word

def find_most_affordable_counter(counter_words, budget=None):
    """Find the cheapest counter word from the given list that's within budget"""
    available_counters = []

    for word in counter_words:
        #finding the word ID
        for id, details in player_words.items():
            if details["word"].lower() == word.lower():
                if budget is None or details["cost"] <= budget:
                    available_counters.append((id, details["cost"]))
                break

    if not available_counters:
        return None

    #sort by cost and return the cheapest id
    available_counters.sort(key=lambda x: x[1])
    return available_counters[0][0]

def what_beats(sys_word, used_words=None):
    """Improved strategy to select the best counter word"""
    sys_word_lower = sys_word.lower()
    used_words = used_words or set()

    #direct matches in our logical counters (?)
    if sys_word_lower in logical_counters:
        counter_words = logical_counters[sys_word_lower]

        #available counters not used before (?)
        available_counters = [w for w in counter_words if w not in used_words]
        if available_counters:
            counter_id = find_most_affordable_counter(available_counters)
            if counter_id:
                return counter_id

    #partial matches against our keys
    for key in logical_counters:
        if key in sys_word_lower or sys_word_lower in key:
            counter_words = logical_counters[key]
            available_counters = [w for w in counter_words if w not in used_words]
            if available_counters:
                counter_id = find_most_affordable_counter(available_counters)
                if counter_id:
                    return counter_id

    #trying using a few effective general counters based on cost brackets -> these are versatile words that often make logical sense as counters
    general_counters = [
        # Low cost effective counters
        "Acid", "Fire", "Water", "Drill", "Sandpaper",
        # Medium cost effective counters
        "Laser", "Vacuum", "Hydraulic Jack", "Fire Extinguisher",
        # High cost powerful counters
        "Resilience", "Innovation", "Time"
    ]

    available_counters = [w for w in general_counters if w not in used_words]
    if available_counters:
        counter_id = find_most_affordable_counter(available_counters)
        if counter_id:
            return counter_id

    #last resort - choosing the cheapest word not used before
    affordable_words = sorted([(id, details["cost"]) for id, details in player_words.items()
                              if details["word"] not in used_words],
                             key=lambda x: x[1])

    if affordable_words:
        return affordable_words[0][0]

    #if we've used all words, just pick the cheapest
    return min(player_words.items(), key=lambda x: x[1]["cost"])[0]

def play_game(player_id):
    word_usage = defaultdict(int)
    used_words = set()

    for round_id in range(1, NUM_ROUNDS + 1):
        sys_word = get_random_system_word()
        print(f"\nRound {round_id}: Sistemul a ales '{sys_word}'")

        chosen_word_id = what_beats(sys_word, used_words)
        chosen_word = player_words[chosen_word_id]["word"]
        word_usage[chosen_word] += 1
        used_words.add(chosen_word)

        print(f"Eu aleg '{chosen_word}' (ID: {chosen_word_id}, Cost: {player_words[chosen_word_id]['cost']})")
        print(f"Statistici utilizare: {dict(word_usage)}")

        print(f"Justificare: '{chosen_word}' contracareaza '{sys_word}' pentru ca: ", end="")
        if sys_word.lower() in logical_counters and chosen_word in logical_counters[sys_word.lower()]:
            print(f"este un contraatac direct definit")
        else:
            #explanations....
            if "metal" in sys_word.lower() and chosen_word in ["Acid", "Laser"]:
                print("acid corodează metalul / laser topeste metalul")
            elif "paper" in sys_word.lower() and chosen_word in ["Fire", "Water", "Acid"]:
                print("focul arde hartia / apa dizolva hartia / acidul distruge hartia")
            elif "rock" in sys_word.lower() and chosen_word in ["Drill", "Jackhammer", "Dynamite"]:
                print("burghiul / ciocanul penetreaza piatra / dinamita distruge piatra")
            else:
                print("logic general, oferă un avantaj strategic")

        if host:
            data = {"player_id": player_id, "word_id": chosen_word_id, "round_id": round_id}
            try:
                response = requests.post(f"{host}/submit-word", json=data, timeout=3)
                print("Raspuns server:", response.json())
            except requests.exceptions.RequestException as e:
                print(f"Eroare trimitere: {e}")

        time.sleep(1)

if __name__ == "__main__":
    player_id = "abc123"
    play_game(player_id)