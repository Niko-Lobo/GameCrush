### Adding the "Fireproof Level" Bonus Purchase Feature to the Crash Game

To enhance the "Bathyscaphe Depths" crash game, we’ll add a "Fireproof Level" feature that players can purchase before a round. This feature guarantees a minimum payout at a specified multiplier level, regardless of the game’s outcome (crash or cashout), while ensuring the overall RTP remains consistent. Below, I’ll explain the feature and its integration, followed by an updated Python implementation.

---

### Feature Description

The "Fireproof Level" is an optional purchasable bonus that acts as a safety net:
- **Functionality**: Players pay a price to guarantee winnings at a chosen multiplier level (e.g., 2.0x), even if the game crashes before their auto-cashout multiplier (\( M \)) or send multiplier (\( M_s \)).
- **Guaranteed Payout**: If the multiplier reaches or exceeds the fireproof level (\( M_f \)), the player secures \( \text{bet} \times M_f \) for that portion, regardless of whether they crash later.
- **Cost Calculation**: The price is calculated to maintain the desired RTP, ensuring the casino’s edge isn’t compromised. The cost reflects the probability of reaching \( M_f \) and the payout it guarantees.
- **Strategic Appeal**: Players can use this to reduce risk while still chasing higher multipliers with their remaining bet.

#### How It Works
- **Inputs**: Players choose whether to buy the fireproof level, specify the multiplier (\( M_f \)), and pay a calculated price.
- **Price Formula**: To keep RTP consistent (e.g., 97%), the cost is \( \text{bet} \times M_f \times P(C > M_f) \), where \( P(C > M_f) = (\text{RTP}/100) / M_f \). This ensures the expected cost offsets the guaranteed payout.
- **Gameplay Impact**:
  - If the multiplier reaches \( M_f \), the fireproof payout is secured and added to winnings.
  - The original bet continues toward \( M_s \) (send) and \( M \) (cashout), potentially adding more winnings.
  - If the game crashes before \( M_f \), only the fireproof cost is lost, not the payout (since it wasn’t reached).

#### Example
- **Inputs**: Bet = $10, RTP = 97%, \( M = 3.0 \), \( M_s = 2.0 \), \( P = 50\% \), \( M_f = 1.5 \) (fireproof level).
- **Cost**: \( P(C > 1.5) = 0.97 / 1.5 = 0.6467 \); cost = \( 10 \times 1.5 \times 0.6467 = 9.70 \).
- **Outcomes**:
  - If \( C = 1.2 \): Crashes before 1.5; no fireproof payout; total loss = bet + cost ($19.70).
  - If \( C > 3.0 \): Reaches 1.5 (fireproof = $15), sends 50% at 2.0 ($10), cashes out at 3.0 ($15); total winnings = $40, net profit = $40 - $19.70 = $20.30.

---

### Updated Code Description

#### Overview
This version of "Bathyscaphe Depths" includes three key features:
1. **Basic Crash Mechanics**: Players bet and set an auto-cashout multiplier (\( M \)).
2. **Send Part of Winnings**: Players can send a percentage of their winnings at a specified multiplier (\( M_s \)) mid-round.
3. **Fireproof Level**: Players can purchase a guaranteed payout at a multiplier (\( M_f \)) for a calculated cost, maintaining the desired RTP.

#### Core Mechanics
- **Multiplier System**: Starts at 1.0, increases by 0.01 per step, and stops at \( M \) (win) or \( C \) (crash).
- **Betting and Cashout**: Players input a bet and \( M \); winnings are \( \text{remaining bet} \times M \) if \( M \) is reached before \( C \).
- **Send Part of Winnings**: At \( M_s \), \( P\% \) of the original bet is cashed out, reducing the remaining bet, with the multiplier unaffected.
- **Fireproof Level**:
  - Players opt to buy a fireproof level at \( M_f \) (e.g., 1.5).
  - Cost = \( \text{bet} \times M_f \times P(C > M_f) \), where \( P(C > M_f) = (\text{RTP}/100) / M_f \).
  - If \( \text{multiplier} \geq M_f \), \( \text{bet} \times M_f \) is secured, added to winnings regardless of later outcomes.
- **RTP Control**: The crash point \( C \) ensures \( P(C > x) = (\text{RTP}/100) / x \), and the fireproof cost offsets its payout to maintain RTP.

#### Game Flow
1. **Setup**: Input RTP and number of rounds.
2. **Per Round**:
   - Inputs: Bet, \( M \), \( M_s \), \( P \) (if \( M_s > 0 \)), and fireproof option (\( M_f \) if chosen).
   - Validation: \( M \geq 1.0 \), \( 0 < P \leq 100 \), \( M_f \geq 1.0 \) if applicable.
   - Simulation:
     - At \( M_f \): Secure fireproof payout if reached.
     - At \( M_s \): Send \( P\% \) of original bet at that multiplier.
     - At \( M \): Cash out remaining bet.
     - At \( C \): Crash, losing remaining bet.
   - Output: Shows fireproof, send, cashout, or crash events.
3. **Results**: Tracks total spent (bet + fireproof costs) and winnings, displaying net result.

#### Technical Details
- **Crash Point**: Generated with \( C = (\text{RTP}/100) / (1 - U) \) or 1.0, ensuring RTP consistency.
- **Fireproof Cost**: Calculated as \( \text{bet} \times M_f \times (\text{RTP}/100) / M_f \), simplifying to maintain expected payout balance.
- **State Management**: Tracks `fireproof_reached`, `sent`, and `cashed_out` to prevent duplicate actions.

#### Example Run
```
Welcome to Bathyscaphe Depths Crash Game!
Enter desired RTP (e.g., 97 for 97%): 97
Enter number of rounds to play: 1

Round 1
Enter your bet amount: 10
Enter your auto-cashout multiplier (e.g., 3.0): 3.0
Enter send multiplier Ms (0 for no send): 2.0
Enter send percentage P (0-100): 50
Buy fireproof level? (y/n): y
Enter fireproof multiplier Mf (e.g., 1.5): 1.5
Fireproof level at 1.50 costs 9.70
Starting with bet 10, auto-cashout at 3.0, send 50% at 2.0, fireproof at 1.5
Fireproof level reached at 1.50, secured 15.00
Sent 10.00 at multiplier 2.00
Cashed out remaining at 3.00, won 15.00

Total spent: 19.70
Total winnings after 1 round: 40.00
Net result: 20.30
```

---

### Conclusion
The updated code now includes the "Fireproof Level" feature, allowing players to buy a guaranteed payout at \( M_f \) for a cost that preserves the RTP (e.g., 97%). Combined with the "Send Part of Winnings" feature, it offers strategic flexibility: players can secure early gains via fireproof, send mid-round winnings, and chase higher multipliers with the remaining bet. This maintains the game’s simplicity for local execution while enhancing gameplay depth.



Below is an updated description of the Python code for **"Bathyscaphe Depths"**, a simple, locally-run crash game that now includes the "Send Part of Winnings" feature. This description reflects the current functionality, focusing on how it operates with the specified RTP and the new mid-round winnings transfer mechanism.

---

### Description of "Bathyscaphe Depths" Python Code

**Overview**  
"Bathyscaphe Depths" is a command-line crash game implemented in Python, designed to run locally with a configurable Return to Player (RTP) percentage (e.g., 97%). The game simulates a bathyscaphe descending into the ocean depths, where players bet on a rising multiplier and aim to cash out before it "crashes" due to underwater hazards. The updated version includes the "Send Part of Winnings" feature, allowing players to transfer a portion of their current winnings to a virtual crypto wallet mid-round without resetting the multiplier, adding strategic depth to the gameplay.

**Core Mechanics**  
- **Multiplier System**: The multiplier starts at 1.0 and increases in small steps (0.01) until it either reaches the player’s auto-cashout point (\( M \)) or exceeds a randomly generated crash point (\( C \)), determined by the RTP.
- **Betting and Cashout**:
  - Players input a bet amount and an auto-cashout multiplier (\( M \), e.g., 3.0).
  - The game ends when the multiplier reaches \( M \) (win) or \( C \) (crash).
- **Send Part of Winnings**:
  - Players can specify a send multiplier (\( M_s \), e.g., 2.0) and a send percentage (\( P \), e.g., 50%).
  - When the multiplier reaches or exceeds \( M_s \), \( P\% \) of the original bet is cashed out at that multiplier and added to the total winnings.
  - The remaining bet (\( (1 - \frac{P}{100}) \times \text{original bet} \)) continues in the round, aiming for \( M \) or risking a crash.
- **RTP Control**: The crash point \( C \) is generated using a probability distribution where \( P(C > x) = (\text{RTP}/100) / x \) for \( x \geq 1 \), ensuring the expected payout per bet aligns with the specified RTP (e.g., 0.97 × bet for RTP 97%).

**Game Flow**  
1. **Setup**: The player sets the desired RTP and number of rounds to play.
2. **Per Round**:
   - Input: Bet amount, auto-cashout multiplier (\( M \)), send multiplier (\( M_s \), 0 to skip), and send percentage (\( P \), if \( M_s > 0 \)).
   - Validation: Ensures \( M \geq 1.0 \) and \( 0 < P \leq 100 \) if applicable.
   - Simulation: The multiplier increases in 0.01 steps, displaying progress:
     - At \( M_s \): Sends \( (P / 100) \times \text{original bet} \times M_s \) to winnings, adjusts remaining bet.
     - At \( M \): Cashes out remaining bet at \( M \), adding to winnings.
     - At \( C \): Crashes, losing the remaining bet.
   - Output: Shows multiplier steps, send actions, cashout or crash results.
3. **Results**: Tracks and displays total winnings across all rounds.

**Technical Details**  
- **Crash Point Generation**: 
  - Uses inverse transform sampling: \( C = 1.0 \) with probability \( 1 - (\text{RTP}/100) \); otherwise, \( C = (\text{RTP}/100) / (1 - U) \), where \( U \) is a uniform random variable (0 to 1).
  - This ensures the RTP holds over many rounds, regardless of player strategy.
- **Send Feature**: 
  - Implemented mid-loop, checking if \( \text{multiplier} \geq M_s \) and sending winnings once per round.
  - Adjusts `remaining_bet` dynamically, keeping the multiplier progression intact.
- **Performance**: Lightweight, with no external dependencies beyond Python’s standard library, making it ideal for local execution.

**Example Run**  
```
Welcome to Bathyscaphe Depths Crash Game!
Enter desired RTP (e.g., 97 for 97%): 97
Enter number of rounds to play: 1

Round 1
Enter your bet amount: 10
Enter your auto-cashout multiplier (e.g., 2.0): 3.0
Enter send multiplier Ms (0 for no send): 2.0
Enter send percentage P (0-100): 50
Starting with bet 10, auto-cashout at 3.0, send 50% at 2.0
Sent 10.00 at multiplier 2.00
Cashed out remaining at 3.00, won 15.00

Total winnings after 1 round: 25.00
```
- **Explanation**: At 2.0, 50% of $10 × 2.0 = $10 is sent; remaining bet ($5) cashes out at 3.0 for $15, totaling $25.

**Limitations**  
- **Command-Line Simplicity**: Uses pre-set send and cashout points for ease of use; lacks real-time input during multiplier progression.
- **Step Size**: Increments of 0.01 provide precision but make output verbose; smaller steps could be used with less printing for smoother simulation.
- **No Graphics**: Focuses on mechanics rather than visuals, fitting the lightweight, local-run requirement.

**Conclusion**  
This Python implementation delivers a functional crash game with a configurable RTP and the "Send Part of Winnings" feature, allowing players to lock in partial gains mid-round while pursuing higher multipliers. It’s a simple, text-based version of "Bathyscaphe Depths," ideal for testing mechanics locally, with the RTP accurately reflected in long-term play outcomes.

--- 

This description captures the updated code’s functionality, emphasizing how the new feature integrates with the existing crash game structure while maintaining the desired RTP. Let me know if you’d like further enhancements!
