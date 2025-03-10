import random


def generate_crash_point(rtp):
    """
    Generate a random crash point based on the desired RTP.
    - If U < 1 - (RTP/100), crash at 1.0.
    - Otherwise, C = (RTP/100) / (1 - U).
    """
    u = random.random()
    if u < 1 - (rtp / 100):
        return 1.0
    else:
        return (rtp / 100) / (1 - u)


def calculate_fireproof_cost(bet, M_f, rtp):
    """Calculate cost of fireproof level to maintain RTP."""
    probability = (rtp / 100) / M_f
    return bet * M_f * probability


# Welcome message
print("Welcome to Bathyscaphe Depths RTP Simulation!")

# Get simulation settings from user
rtp = float(input("Enter desired RTP (e.g., 97 for 97%): "))
num_cycles = int(input("Enter number of cycles to simulate: "))

# Initialize totals
total_spent = 0
total_winnings = 0

# Fixed bet amount for simplicity
bet = 1.0

# Run simulation for specified number of cycles
for cycle in range(num_cycles):
    # Generate random game parameters
    M = random.uniform(1.1, 10.0)  # Auto-cashout multiplier between 1.1 and 10.0
    if random.random() < 0.5:  # 50% chance to use send feature
        send_multiplier = random.uniform(1.1, M)  # Send multiplier between 1.1 and M
        send_percentage = random.uniform(0, 100)  # Send percentage between 0% and 100%
    else:
        send_multiplier = 0
        send_percentage = 0
    if random.random() < 0.5:  # 50% chance to buy fireproof
        M_f = random.uniform(1.1, 3.0)  # Fireproof multiplier between 1.1 and 3.0
        fireproof_cost = calculate_fireproof_cost(bet, M_f, rtp)
    else:
        M_f = 0
        fireproof_cost = 0

    # Accumulate total spent (bet + fireproof cost if applicable)
    total_spent += bet + fireproof_cost

    # Generate crash point
    C = generate_crash_point(rtp)

    # Calculate winnings
    fireproof_payout = bet * M_f if M_f > 0 and C >= M_f else 0
    if send_multiplier > 0 and C >= send_multiplier:
        send_amount = (send_percentage / 100) * bet * send_multiplier
        remaining_bet = (1 - send_percentage / 100) * bet
    else:
        send_amount = 0
        remaining_bet = bet
    if C >= M:
        payout = remaining_bet * M
    else:
        payout = 0

    # Accumulate total winnings
    total_winnings += fireproof_payout + send_amount + payout

# Calculate achieved RTP
achieved_rtp = (total_winnings / total_spent) * 100 if total_spent > 0 else 0

# Display statistics
print(f"\nSimulation Complete")
print(f"Total cycles: {num_cycles}")
print(f"Total spent: {total_spent:.2f}")
print(f"Total winnings: {total_winnings:.2f}")
print(f"Achieved RTP: {achieved_rtp:.2f}% (Target RTP: {rtp}%)")