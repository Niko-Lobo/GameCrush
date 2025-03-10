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


# Welcome message
print("Welcome to Bathyscaphe Depths Crash Game!")

# Get game settings
rtp = float(input("Enter desired RTP (e.g., 97 for 97%): "))
num_rounds = int(input("Enter number of rounds to play: "))
total_winnings = 0

# Main game loop
for round_num in range(1, num_rounds + 1):
    print(f"\nRound {round_num}")

    # Get player inputs
    bet = float(input("Enter your bet amount: "))
    M = float(input("Enter your auto-cashout multiplier (e.g., 2.0): "))
    send_multiplier = float(input("Enter send multiplier Ms (0 for no send): "))
    if send_multiplier > 0:
        send_percentage = float(input("Enter send percentage P (0-100): "))
    else:
        send_percentage = 0

    # Basic input validation
    if M < 1.0:
        print("Auto-cashout must be at least 1.0")
        continue
    if send_multiplier > 0 and (send_percentage <= 0 or send_percentage > 100):
        print("Send percentage must be between 0 and 100")
        continue

    # Generate crash point
    C = generate_crash_point(rtp)

    # Initialize game state
    multiplier = 1.00
    step = 0.01  # Small step for precision
    sent = False
    cashed_out = False
    original_bet = bet
    remaining_bet = bet

    print(
        f"Starting with bet {bet}, auto-cashout at {M}, send {send_percentage}% at {send_multiplier if send_multiplier > 0 else 'N/A'}")

    # Simulate multiplier increase
    while multiplier < C and not cashed_out:
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
print(f"\nTotal winnings after {num_rounds} rounds: {total_winnings:.2f}")