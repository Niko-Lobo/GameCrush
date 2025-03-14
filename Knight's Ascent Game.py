import random
import time


def generate_crash_point(rtp, mode="Normal"):
    """
    Generate a random crash point based on RTP (97%).
    For Additional MAX, scale down to balance higher cost and meta-multipliers.
    """
    u = random.random()
    if mode == "Additional MAX":
        # Scale crash point to balance 300x cost and guaranteed 10x meta-multiplier
        # Adjusted to maintain RTP of 97% over 300x bet
        scale_factor = 0.03233  # Approx 1/30.9 to offset 300x cost and ~10x meta-multiplier
        if u < 1 - (rtp / 100) * scale_factor:
            return 1.0
        else:
            return min((rtp / 100) * scale_factor / (1 - u), 50000)
    else:
        # Normal and Additional modes use standard distribution
        if u < 1 - (rtp / 100):
            return 1.0
        else:
            return min((rtp / 100) / (1 - u), 50000)


def generate_meta_multiplier():
    """Generate a random meta-multiplier between 2x and 100x."""
    return random.randint(2, 100)


# Welcome message
print("Welcome to Knight's Ascent!")

# Set RTP (fixed for simplicity)
rtp = 97.0  # 97% RTP

# Choose game mode
print("\nChoose your game mode:")
print("1. Normal (1x bet, max win 50,000x)")
print("2. Additional (150x bet, chance for meta-multipliers)")
print("3. Additional MAX (300x bet, guaranteed 10x meta-multiplier + more)")
mode_choice = int(input("Enter mode (1-3): "))

# Set bet and mode-specific costs
base_bet = float(input("Enter your base bet amount (e.g., 1.0): "))
if mode_choice == 1:
    mode = "Normal"
    bet_multiplier = 1
elif mode_choice == 2:
    mode = "Additional"
    bet_multiplier = 150
elif mode_choice == 3:
    mode = "Additional MAX"
    bet_multiplier = 300
else:
    print("Invalid mode, defaulting to Normal")
    mode = "Normal"
    bet_multiplier = 1

bet = base_bet * bet_multiplier
print(f"\nMode: {mode}, Total Bet: {bet:.2f}")

# Generate crash point based on mode
crash_point = generate_crash_point(rtp, mode)

# Initialize game state
multiplier = 1.0
step = 0.1
meta_multipliers = []
if mode == "Additional MAX":
    meta_multipliers.append(10)  # Guaranteed 10x at start
running = True

print("The knight begins climbing the tower... Press 'c' to cash out, or wait!")

# Game loop
while running:
    print(f"Current Multiplier: {multiplier:.1f}x")

    # Chance to get a meta-multiplier in Additional modes
    if mode in ["Additional", "Additional MAX"] and random.random() < 0.1:  # 10% chance per step
        new_meta = generate_meta_multiplier()
        meta_multipliers.append(new_meta)
        print(f"Collected Meta-Multiplier: x{new_meta}")

    # Check for crash
    if multiplier >= crash_point:
        print(f"\nThe tower collapses at {crash_point:.1f}x! You lose.")
        total_win = 0
        running = False
    else:
        # Player input to cash out
        choice = input("Press 'c' to cash out, or Enter to continue: ").lower()
        if choice == 'c':
            total_meta = 1
            for m in meta_multipliers:
                total_meta *= m
            total_win = bet * multiplier * total_meta
   #         total_win = min(total_win, base_bet * 50000)  # Cap at 50,000x base bet
            print(f"\nCashed out at {multiplier:.1f}x!")
            if meta_multipliers:
                print(f"Meta-Multipliers: {', '.join(f'x{m}' for m in meta_multipliers)}")
                print(f"Total Multiplier: {multiplier:.1f} * {total_meta} = {multiplier * total_meta:.1f}x")
            print(f"Total Win: {total_win:.2f}")
            running = False
        else:
            multiplier += step
            time.sleep(0.1)  # Simulate real-time progression

# End of game
print(f"\nGame Over!")