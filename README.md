# 8-Queen Problem — Hill Climbing Solver

A Python implementation of the classic [8-Queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle) using **Greedy Hill Climbing** with an incremental placement approach.

## How It Works

1. Queens are placed one at a time in a random available column.
2. After each placement, the algorithm checks for conflicts (row and diagonal violations).
3. If violations exist, hill climbing iteratively moves each conflicting queen to the lowest-cost row in its column.
4. Once all violations are resolved, the next queen is placed.
5. The process repeats until all 8 queens are on the board with zero conflicts.

## Requirements

- Python 3.6+
- NumPy

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the solver
python main.py
```

Solved board states are appended to `results.txt` on each run.

## Example Output

```
FINAL MATRIX:
[[  Q          ]
 [      Q      ]
 [          Q  ]
 [  Q          ]
 [        Q    ]
 [            Q]
 [Q            ]
 [    Q        ]]
```

## Project Structure

```
main.py                          # Core solver (queen & board classes + hill climbing)
8 Queen - Hill Climbing.ipynb    # Jupyter notebook version with explanations
results.txt                      # Accumulated solved board outputs
requirements.txt                 # Python dependencies
```

## License

This project is provided as-is for educational purposes.
