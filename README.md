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
