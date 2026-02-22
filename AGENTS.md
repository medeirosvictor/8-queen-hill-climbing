# 8-Queen Hill Climbing

## Project Overview
A Python implementation of the classic 8-Queens puzzle solved using a Greedy Hill Climbing algorithm with an incremental approach. Queens are placed one at a time on an 8×8 board, and after each placement the algorithm iteratively moves queens to lower-conflict positions until zero violations are achieved.

## Key Files
| Path | Purpose |
|------|---------|
| `main.py` | Core implementation — `queen` class, `board` class with hill climbing logic, and main execution loop |
| `8 Queen - Hill Climbing.ipynb` | Jupyter notebook version of the same algorithm with markdown explanations |
| `results.txt` | Accumulated output of solved board states from previous runs |
| `.vscode/` | VS Code debug/launch configuration |

## Pipeline / Architecture
1. **Initialization** — An empty 8×8 board is created.
2. **Incremental Queen Placement** — Queens are added one-by-one to random positions (one per column, enforced by `__column_check__`).
3. **Violation Detection** — After each placement, row and diagonal conflicts are counted across all queens. Violations are halved to avoid double-counting.
4. **Hill Climbing** — For each queen with violations > 0, a cost board is computed showing the violation count at every row in that queen's column. The queen is moved to the lowest-cost position.
5. **Convergence** — Steps 3-4 repeat until board violations reach 0, then the next queen is placed.
6. **Output** — Final board state and queen positions are printed and appended to `results.txt`.

## Tech Stack
- **Language:** Python 3
- **Dependencies:** `numpy` (matrix operations, diagonal extraction), `math`, `sys`, `random`, `copy` (all stdlib except numpy)
- **Environment:** Anaconda (per `.vscode/settings.json`), Jupyter Notebook

## Conventions
- Classes use PascalCase (`Queen`, `Board`)
- Public methods use snake_case (`add_queen`, `hill_climb`, `check_violations_on_board`)
- Board is represented as a 2D list of `" "` and `"Q"` strings
- Queens are stored as `self.queens` on the `Board` instance (no global state)
- Type hints on all method signatures; docstrings on all public methods
- Hill climbing has a `MAX_HILL_CLIMB_ITERATIONS` safeguard with random restart on plateau

## How to Run
```bash
# Install dependency
pip install numpy

# Run the solver
python main.py
```
Results are appended to `results.txt` on each run.
