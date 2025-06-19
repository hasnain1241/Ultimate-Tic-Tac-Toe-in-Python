
---

##  Project Overview

This project is a complete implementation of **Ultimate Tic Tac Toe** in Python, featuring:

* A fully interactive **GUI** using `tkinter`.
* Multiple play modes:

  * Human vs Human
  * Human vs AI
  * AI vs AI
* AI with three difficulty levels:

  * **Easy**: Random move selection
  * **Medium**: Heuristic blocking and winning strategy
  * **Hard**: Minimax search with CSP (Constraint Satisfaction Problem) techniques including:

    * Forward checking
    * Arc consistency (AC-3)
    * Alpha-beta pruning
    * MRV heuristic for variable selection

---

##  Game Rules (Ultimate Tic Tac Toe)

* The board consists of 9 smaller tic tac toe boards arranged in a 3x3 grid.
* Players take turns playing in the small boards.
* The twist: Your move determines the board your opponent must play in.
* Winning a small board claims it on the main board.
* Win the overall game by winning 3 small boards in a row on the big board.

---

##  AI Overview

* **Minimax with CSP**:

  * **Evaluation Function**: Assesses both small and big board progress, with special emphasis on center and corner control.
  * **Move Ordering**: Prioritizes center, corner, and edge moves.
  * **AC-3**: Ensures arc consistency between possible moves.
  * **Forward Checking**: Avoids assigning values that block future moves.
  * **MRV Heuristic**: Chooses variables with the smallest legal domain.

---

##  How to Run

###  Prerequisites

* Python 3.x
* Tkinter (comes pre-installed with standard Python distributions)

###  Running the Game

```bash
python Tic_Tac_Toe.py
```

---

## 🎮 Features

| Feature                     | Status |
| --------------------------- | ------ |
| GUI with 9 sub-boards       | ✅      |
| Human vs Human              | ✅      |
| Human vs AI                 | ✅      |
| AI vs AI                    | ✅      |
| Easy / Medium / Hard AI     | ✅      |
| CSP Integration (Hard mode) | ✅      |
| AC-3 and Forward Checking   | ✅      |
| Full Rule Enforcement       | ✅      |

---



##  Key Classes

* `UltimateTicTacToe`: Main game logic and GUI
* `UltimateTicTacToeCSP`: Handles CSP formulation, AC-3, forward checking, and backtracking

---

##  File Structure

```
Tic_Tac_Toe.py      # Main script (includes GUI and AI logic)
README.md           # Project documentation
```

---

##  Concepts Used

* Game Tree Search (Minimax, Alpha-Beta)
* Heuristic Evaluation
* Constraint Satisfaction Problems (CSP)
* Tkinter GUI
* Object-Oriented Design

---

##  Educational Value

This project is ideal for students learning:

* Game AI
* CSPs
* GUI programming
* Advanced Python logic and modular design


