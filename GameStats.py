import random
import statistics

# Function to generate crash point based on RTP
def generate_crash_point(rtp):
    u = random.random()
    if u < 1 - (rtp / 100):
        return 1.0
    else:
        return (rtp / 100) / (1 - u)

# Function to calculate fireproof cost
def calculate_fireproof_cost(bet, M_f, rtp):
    probability = (rtp / 100) / M_f
    return bet * M_f * probability

# Welcome message
print("Welcome to Bathyscaphe Depths RTP Simulation!")

# Get user inputs
rtp = float(input("Enter desired RTP (e.g., 97 for 97%): "))
num_cycles = int(input("Enter number of cycles to simulate: "))

# Initialize tracking variables
total_spent = 0
total_winnings = 0
payouts = []  # List to store all payouts
max_win = 0   # Tracks maximum won
max_potential_win = 0  # Tracks maximum potential win
bet = 1.0     # Fixed bet amount for simplicity

# Run the simulation
for cycle in range(num_cycles):
    # Random game parameters
    M = random.uniform(1.1, 10.0)  # Auto-cashout multiplier
    send_multiplier = random.uniform(1.1, M) if random.random() < 0.5 else 0
    send_percentage = random.uniform(0, 100) if send_multiplier > 0 else 0
    M_f = random.uniform(1.1, 3.0) if random.random() < 0.5 else 0
    fireproof_cost = calculate_fireproof_cost(bet, M_f, rtp) if M_f > 0 else 0

    # Update total spent
    total_spent += bet + fireproof_cost

    # Generate crash point
    C = generate_crash_point(rtp)

    # Calculate payouts
    fireproof_payout = bet * M_f if M_f > 0 and C >= M_f else 0
    if send_multiplier > 0 and C >= send_multiplier:
        send_amount = (send_percentage / 100) * bet * send_multiplier
        remaining_bet = (1 - send_percentage / 100) * bet
    else:
        send_amount = 0
        remaining_bet = bet
    payout = remaining_bet * M if C >= M else 0

    # Total payout for this cycle, capped at 11000x bet
    cycle_payout = min(fireproof_payout + send_amount + payout, 11000 * bet)
    payouts.append(cycle_payout)

    # Update maximum win
    if cycle_payout > max_win:
        max_win = cycle_payout

    # Update maximum potential win (capped at 11000x)
    potential_win = min(bet * C, 11000 * bet)
    if potential_win > max_potential_win:
        max_potential_win = potential_win

    # Update total winnings
    total_winnings += cycle_payout

# Calculate statistics
average_win = statistics.mean(payouts) if payouts else 0
std_dev = statistics.stdev(payouts) if len(payouts) > 1 else 0
achieved_rtp = (total_winnings / total_spent) * 100 if total_spent > 0 else 0

# Display results
print(f"\nSimulation Complete")
print(f"Total cycles: {num_cycles}")
print(f"Total spent: {total_spent:.2f}")
print(f"Total winnings: {total_winnings:.2f}")
print(f"Achieved RTP: {achieved_rtp:.2f}% (Target RTP: {rtp}%)")
print(f"Maximum won: {max_win:.2f}")
print(f"Maximum potential win: {max_potential_win:.2f}")
print(f"Mathematical expectation (RTP): {achieved_rtp:.2f}%")
print(f"Average win: {average_win:.2f}")
print(f"Standard deviation: {std_dev:.2f}")