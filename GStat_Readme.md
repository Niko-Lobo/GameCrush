

### How It Works

This script simulates the crash game over a user-specified number of cycles to test the RTP. Instead of prompting the player for inputs each round, it uses reasonable random values for game parameters. Here’s a breakdown:

#### 1. **Inputs**
- **Desired RTP**: The target RTP (e.g., 97 for 97%), entered by the user.
- **Number of Cycles**: The number of rounds to simulate, entered by the user.

#### 2. **Random Parameters**
For each cycle, the script generates:
- **Bet Amount**: Fixed at 1.0 for simplicity (RTP holds regardless of bet size).
- **Auto-Cashout Multiplier (\( M \))**: Randomly between 1.1 and 10.0.
- **Send Feature** (50% chance to use):
  - **Send Multiplier (\( M_s \))**: Randomly between 1.1 and \( M \).
  - **Send Percentage (\( P \))**: Randomly between 0% and 100%.
- **Fireproof Feature** (50% chance to buy):
  - **Fireproof Multiplier (\( M_f \))**: Randomly between 1.1 and 3.0.
  - **Fireproof Cost**: Calculated to maintain RTP based on \( M_f \) and bet.

#### 3. **Simulation Logic**
- **Total Spent**: Sum of bet (1.0) plus fireproof cost (if purchased).
- **Crash Point (\( C \))**: Generated based on the RTP.
- **Winnings**:
  - **Fireproof Payout**: \( \text{bet} \times M_f \) if \( C \geq M_f \) and fireproof is bought.
  - **Send Amount**: \( (P / 100) \times \text{bet} \times M_s \) if \( C \geq M_s \) and send is used, with remaining bet adjusted.
  - **Payout**: \( \text{remaining_bet} \times M \) if \( C \geq M \).
- **Total Winnings**: Sum of fireproof payout, send amount, and payout per round.

#### 4. **Statistics**
After all cycles, the script displays:
- **Total Cycles**: Number of rounds simulated.
- **Total Spent**: Total amount wagered (bets + fireproof costs).
- **Total Winnings**: Total amount won.
- **Achieved RTP**: \( (\text{total_winnings} / \text{total_spent}) \times 100 \), compared to the target RTP.

---

### Example Output

```
Welcome to Bathyscaphe Depths RTP Simulation!
Enter desired RTP (e.g., 97 for 97%): 97
Enter number of cycles to simulate: 100000

Simulation Complete
Total cycles: 100000
Total spent: 124567.89
Total winnings: 120987.65
Achieved RTP: 97.12% (Target RTP: 97.0%)
```

*(Note: Values will vary due to randomness, but the achieved RTP should approximate the target RTP over many cycles.)*

---

### Key Features

- **Efficiency**: Computes outcomes directly using the crash point, avoiding step-by-step multiplier simulation.
- **Randomness**: Uses reasonable ranges for multipliers and percentages, with a 50% chance for optional features.
- **RTP Verification**: The achieved RTP should closely match the target RTP (e.g., 97%) over a large number of cycles, confirming the game mechanics are balanced.

This script fulfills the request by replacing player inputs with random values, running the specified number of cycles, and displaying comprehensive statistics at the end.
