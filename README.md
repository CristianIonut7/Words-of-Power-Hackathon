# Words of Power — Hackathon Project

> Developed for **BESTEM 2025** — a hackathon organized by **BEST Bucharest** and **Veridion**  
> Team project focused on creating a **smart word-based decision-making system**.

---

## Overview

**Words of Power** is a word-strategy game engine built for a hackathon challenge.  
The game simulates a battle of words — each player must select a **counter-word** that best neutralizes or overcomes the opponent’s word, while also **minimizing cost**.

The project combines:
- **Rule-based logic**
- **Semantic reasoning (Word2Vec model)**
- **API integration** with the Veridion game server

It showcases intelligent automation and linguistic decision-making using both symbolic and statistical reasoning.

---

## Core Idea

Each word represents an object, concept, or phenomenon with an assigned **cost** (energy or resource level).  
The goal is to **beat the system’s word** using the **cheapest effective counter**.  
When no direct counter exists, the program falls back to:
- semantic similarity (via `Word2Vec`)
- logical reasoning heuristics
- random low-cost strategies

---

## Architecture

Words-of-Power-Hackathon/
│
├── var1.py # Main gameplay logic + Word2Vec model + Veridion API integration
├── var2.py # Simplified offline strategy simulation (rule-based + reasoning)
└── README.md # Project documentation

### File Descriptions

#### `var1.py`
Implements the **full version** of the game logic:
- Connects to the Veridion game API
- Registers the player and handles multiple rounds
- Builds a local `Word2Vec` model for semantic reasoning
- Combines **logical counter maps** and **vector similarity** to choose optimal words

Key functions:
| Function | Description |
|-----------|--------------|
| `find_antonyms(word)` | Finds semantically distant or contrasting words using the trained model |
| `find_most_affordable_counter(counter_words, budget=None)` | Selects the lowest-cost counter from a given list |
| `what_beats(sys_word)` | Determines the best counter using logic, similarity, or antonyms |
| `play_game(player_id)` | Main loop for communicating with the API and choosing words each round |
| `register(player_id)` | Registers a player with the API server |

---

#### `var2.py`
Implements an **offline standalone simulator**:
- Does not use external APIs
- Runs local rounds with printed explanations
- Provides **human-readable reasoning** for each decision (why a counter was chosen)

Key functions:
| Function | Description |
|-----------|--------------|
| `what_beats(sys_word, used_words)` | Returns the most suitable counter word for a given system word |
| `play_game(player_id)` | Runs a complete 10-round simulation |
| `find_most_affordable_counter()` | Core helper to minimize resource cost |

### Veridion API Endpoints

When running in connected mode (var1.py):

Endpoint	Purpose
/register	Registers the player
/get-word	Retrieves the current round word
/submit-word	Submits chosen counter word
/status	Checks round progress

### Logical Counter Mapping

Each system word (e.g., "rock", "fire", "virus") has a predefined list of counter words ranked by effectiveness:
```console
logical_counters = {
    "rock": ["Drill", "Jackhammer", "Acid", "Dynamite", "Bulldozer", "Laser"],  
    "fire": ["Water", "Fire Extinguisher", "Fire Blanket", "Vacuum", "Foam"],  
    "virus": ["Anti-Virus Nanocloud", "Neutralizing Agent", "Vaccination"],  
    "fear": ["Confidence", "Love", "Therapy", "Knowledge"],  
    ...  
}  
```
If no direct counter is found, the AI uses:
1. Semantic similarity search
2. Antonym lookup via Word2Vec
3. Random low-cost fallback

### Running the Project

Option 1: Offline Mode (Simulation)

Run the offline version (var2.py):  
#### `python var2.py`  
You can enter system words manually (e.g., "fire", "metal") or pipe them in via stdin.

Option 2: Online Mode (API Mode)

Run the online version (var1.py):  
#### `python var1.py`  
Make sure the Veridion API is reachable and replace the default player ID if needed:  
#### `player_id = "your_player_id_here"`
