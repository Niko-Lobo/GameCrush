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
print("Welcome to Bathyscaphe Depths Crash Game!")

# Get game settings
rtp = float(input("Enter desired RTP (e.g., 97 for 97%): "))
num_rounds = int(input("Enter number of rounds to play: "))
total_winnings = 0
total_spent = 0

# Main game loop
for round_num in range(1, num_rounds + 1):
    print(f"\nRound {round_num}")

    # Get player inputs
    bet = float(input("Enter your bet amount: "))
    M = float(input("Enter your auto-cashout multiplier (e.g., 3.0): "))
    send_multiplier = float(input("Enter send multiplier Ms (0 for no send): "))
    if send_multiplier > 0:
        send_percentage = float(input("Enter send percentage P (0-100): "))
    else:
        send_percentage = 0
    fireproof_choice = input("Buy fireproof level? (y/n): ").lower()
    if fireproof_choice == 'y':
        M_f = float(input("Enter fireproof multiplier Mf (e.g., 1.5): "))
    else:
        M_f = 0

    # Basic input validation
    if M < 1.0:
        print("Auto-cashout must be at least 1.0")
        continue
    if send_multiplier > 0 and (send_percentage <= 0 or send_percentage > 100):
        print("Send percentage must be between 0 and 100")
        continue
    if M_f > 0 and M_f < 1.0:
        print("Fireproof multiplier must be at least 1.0")
        continue

    # Calculate fireproof cost if applicable
    fireproof_cost = 0
    if M_f > 0:
        fireproof_cost = calculate_fireproof_cost(bet, M_f, rtp)
        print(f"Fireproof level at {M_f:.2f} costs {fireproof_cost:.2f}")

    # Generate crash point
    C = generate_crash_point(rtp)

    # Initialize game state
    multiplier = 1.00
    step = 0.01  # Small step for precision
    sent = False
    cashed_out = False
    fireproof_reached = False
    original_bet = bet
    remaining_bet = bet

    total_spent += bet + fireproof_cost

    print(
        f"Starting with bet {bet}, auto-cashout at {M}, send {send_percentage}% at {send_multiplier if send_multiplier > 0 else 'N/A'}, fireproof at {M_f if M_f > 0 else 'N/A'}")

    # Simulate multiplier increase
    while multiplier < C and not cashed_out:
        # Fireproof level check
        if M_f > 0 and multiplier >= M_f and not fireproof_reached:
            fireproof_payout = original_bet * M_f
            total_winnings += fireproof_payout
            fireproof_reached = True
            print(f"Fireproof level reached at {M_f:.2f}, secured {fireproof_payout:.2f}")

        # Send action
        if send_multiplier > 0 and multiplier >= send_multiplier and not sent:
            send_amount = (send_percentage / 100) * original_bet * multiplier
            total_winnings += send_amount
            remaining_bet = (1 - send_percentage / 100) * original_bet
            sent = True
            print(f"Sent {send_amount:.2f} at multiplier {multiplier:.2f}")

        # Auto-cashout
        if multiplier >= M:
            payout = remaining_bet * multiplier
            total_winnings += payout
            cashed_out = True
            print(f"Cashed out remaining at {multiplier:.2f}, won {payout:.2f}")

        multiplier += step

    # Handle crash
    if not cashed_out:
        print(f"Crashed at {C:.2f}, lost remaining bet {remaining_bet:.2f}")

# Final results
print(f"\nTotal spent: {total_spent:.2f}")
print(f"Total winnings after {num_rounds} rounds: {total_winnings:.2f}")
print(f"Net result: {total_winnings - total_spent:.2f}")