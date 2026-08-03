# Coin Change Algorithm - Sunway Campus Cafeteria Change-Making System

## Overview
When paying in cash at a Sunway campus cafeteria counter, the cashier needs to give change using the **fewest possible coins/notes** to keep the till efficient and reduce handling time. The **Coin Change Algorithm (Dynamic Programming)** determines the minimum number of coins needed to make up a given change amount from the denominations available at the counter.

## Problem Description
Given a target amount and a set of available coin denominations (assumed to be available in unlimited supply), the goal is to determine the **minimum number of coins** required to make up exactly that amount. If the amount cannot be formed using the available denominations, this is reported clearly instead of an incorrect result.

## How the Algorithm Works
1. **Build a table** `dp[a]`, where `dp[a]` stores the minimum number of coins needed to make amount `a`, for every amount from `0` up to the target.
2. **Base case:** `dp[0] = 0` — no coins are needed to make an amount of zero.
3. **Fill the table bottom-up:** for each amount `a` from `1` to the target, try every available coin `c` where `c ≤ a`, and take:
   ```
   dp[a] = min(dp[a], dp[a - c] + 1)
   ```
   This means: for each coin that could be the *last* coin used, check the best known solution for the remaining amount and add one coin.
4. **Track which coin was used** at each amount, so the exact combination of coins can be reconstructed afterward (not just the count).
5. **Backtrack** from the target amount down to `0` using the tracked coins to output the actual coins used.
6. Output the minimum coin count, the coins used, and a breakdown by denomination — or a "not possible" message if the amount is unreachable.

Because every smaller amount is solved exactly once and reused whenever it recurs (instead of being recomputed, as a naive recursive approach would), this reduces the time complexity from exponential to polynomial.

**Time Complexity:** O(amount × number of coin types)
**Space Complexity:** O(amount)

## Requirements
- Python 3.x (no external libraries required)

## How to Run
```bash
python3 problem2_coin_change.py
```

## Usage
1. Choose option 1 (enter own coins/amount) or option 2 (use the built-in sample dataset).
2. If entering your own data:
   - Enter available coin denominations, space-separated (e.g. `1 5 10 20 50`)
   - Enter the target amount
3. The program will display:
   - The full **DP table** (minimum coins needed for every amount from 0 up to the target)
   - The **minimum number of coins** needed for the target amount
   - The **specific coins used** in one optimal combination
   - A **breakdown by denomination** (how many of each coin were used)

### Example
**Input (sample dataset):**
```
Coin denominations: 1 5 10 20 50
Target amount: 67
```

**Output:**
```
Minimum number of coins needed: 5
Coins used (one possible optimal combination):
  1 + 1 + 5 + 10 + 50 = 67

Breakdown by denomination:
Denomination   Count
-------------------------
1              2
5              1
10             1
50             1
```

**Example (unreachable amount):**
```
Coin denominations: 5 10
Target amount: 7

It is not possible to make 7 using the given coin denominations.
```

## Input Validation
- Non-numeric coin denominations or amounts are rejected with an error message.
- Zero or negative denominations are automatically filtered out.
- If the target amount cannot be formed with the given denominations, the program reports this clearly instead of returning an incorrect count.

## Strengths
- Guarantees the mathematically **minimum** number of coins (provably optimal), unlike a greedy coin-picking approach, which can fail for certain denomination sets (e.g. denominations `[1, 3, 4]` for amount `6`: greedy gives `4+1+1` = 3 coins, but the true optimum is `3+3` = 2 coins).
- Efficient: reduces an exponential brute-force search down to polynomial time by solving each subproblem only once.
- Reconstructs the **actual coins used**, not just the count, making the output directly useful and easy to verify.

## Limitations
- Table size scales with the **target amount itself**, not just the number of coin types — very large amounts require a proportionally large table.
- Assumes an **unlimited supply** of each coin denomination; a limited-supply variant would need a different (2D) formulation.
- Only works with **integer** amounts and denominations, since the table is indexed by whole-number amount.

## File Structure
```
.
├── problem2_coin_change.py   # Main program
└── README_problem2_coin_change.md   # This file
```
