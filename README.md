# Battleship Automation 🎯

Automation bot for the online Battleship game built with Python and Playwright.
The bot launches a browser, joins a match, places ships automatically, selects a random player, 
waits for its turn, and shoots at available cells using strategy.

---

## 🚀 How to Run

```bash
git clone https://github.com/viktoriyabuter/battleship-automation
cd battleship-automation

python -m venv .venv
.venv\\Scripts\\activate   # Windows
# source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
playwright install

python application/run_battleship.py
```

---

## ⚙️ Strategy Algorithm

The bot uses a two-phase shooting strategy:

### 1. Search Phase (Checkerboard)

The bot shoots using a **checkerboard pattern** to maximize board coverage while minimizing wasted shots.
Since ships occupy multiple cells, this pattern increases the probability of finding a ship faster than random selection.

### 2. Destroy Phase (Ship Finishing)

Once the bot registers a hit, it switches behavior:

1. Identify neighboring cells (up, down, left, right).
2. Continue shooting adjacent cells to determine the ship's orientation.
3. Follow the detected direction until the ship is fully destroyed.
4. Return to the checkerboard search.

### Full Gameplay Loop

1. Launch the browser and open the Battleship website.
2. Wait for an opponent.
3. Wait for the bot's turn.
4. Collect available (empty) enemy cells.
5. Shoot using the checkerboard pattern.
6. If a hit is detected — switch to destroy phase.
7. Resume search phase after the ship is sunk.
8. Repeat until the game ends.

---



