import random
import numpy as np
import matplotlib.pyplot as plt


def create_transition_matrix(multipliers, crash_prob, cashout_prob):
    """Build the Markov Chain transition matrix."""
    n = len(multipliers)
    P = np.zeros((n + 2, n + 2))  # Rows/cols: multipliers + crash + cashout
    for i in range(n):
        if i < n - 1:
            P[i, i + 1] = 1 - crash_prob - cashout_prob  # Continue
        P[i, n] = crash_prob  # Crash
        P[i, n + 1] = cashout_prob  # Cashout
    P[n, n] = 1  # Crash is absorbing
    P[n + 1, n + 1] = 1  # Cashout is absorbing
    return P


def compute_expected_payout(P, multipliers, bet, meta_multipliers=None):
    """Calculate expected payout from the transition matrix."""
    n = len(multipliers)
    Q = P[:n, :n]  # Transient state transitions
    R = P[:n, n:]  # To absorbing states
    I = np.eye(n)
    N = np.linalg.inv(I - Q)  # Fundamental matrix
    B = N @ R  # Absorption probabilities

    expected = 0
    for i in range(n):
        if meta_multipliers and i in meta_multipliers:
            meta_sum = sum(meta_multipliers[i]) if meta_multipliers[i] else 0
            payout = bet * multipliers[i] * (1 + meta_sum)
        else:
            payout = bet * multipliers[i]
        expected += B[i, 1] * min(payout, bet * 50000)  # Cashout payout, capped
    return expected


def simulate_round(multipliers, P, bet, mode, meta_prob=0.05):
    """Simulate one round using the Markov Chain."""
    state = 0  # Start at 1.0x
    meta_multipliers = [1] if mode == "Additional MAX" else []  # Guaranteed 1x for MAX

    while state < len(multipliers):
        r = random.uniform(0, 1)
        if r < P[state, len(multipliers)]:  # Crash
            return 0
        elif r < P[state, len(multipliers)] + P[state, len(multipliers) + 1]:  # Cashout
            meta_sum = sum(meta_multipliers)
            payout = bet * multipliers[state] * (1 + meta_sum)
            return min(payout, bet * 50000)
        else:  # Continue
            if mode in ["Additional", "Additional MAX"] and random.random() < meta_prob:
                meta_multipliers.append(random.uniform(1.0, 5.0))  # Increased range
            state += 1
    return bet * multipliers[-1] * (1 + sum(meta_multipliers))  # Max multiplier if reached


# Welcome message
print("Welcome to Knight's Ascent RTP Simulation with Markov Chains!")

# Get user inputs
rtp = float(input("Enter desired RTP (e.g., 95 for 95%): "))
base_bet = float(input("Enter standard bet amount (e.g., 1.0): "))
num_rounds = int(input("Enter number of rounds to simulate: "))

# Define multipliers and mode-specific parameters
multipliers = [1.0 + 0.1 * i for i in range(491)]  # 1.0 to 50.0
modes = ["Normal", "Additional", "Additional MAX"]
bet_multipliers = {"Normal": 1, "Additional": 150, "Additional MAX": 300}
initial_crash_probs = {"Normal": 0.0118, "Additional": 0.0105, "Additional MAX": 0.0050}
cashout_prob = 0.02  # Fixed for simplicity

# Tune crash probabilities to achieve 95% RTP for each mode
crash_probs = {}
for mode in modes:
    crash_prob = initial_crash_probs[mode]
    bet = base_bet * bet_multipliers[mode]
    P = create_transition_matrix(multipliers, crash_prob, cashout_prob)
    expected = compute_expected_payout(P, multipliers, bet)
    target_payout = bet * (rtp / 100)

    while abs(expected - target_payout) > 0.01:
        if expected > target_payout:
            crash_prob += 0.0001
        else:
            crash_prob -= 0.0001
        P = create_transition_matrix(multipliers, crash_prob, cashout_prob)
        expected = compute_expected_payout(P, multipliers, bet)
    crash_probs[mode] = crash_prob
    print(f"{mode} Mode: Adjusted Crash Prob = {crash_prob:.4f}, Expected RTP = {expected / bet:.2%}")

# Initialize stats
stats = {mode: {"rounds": 0, "total_spent": 0, "total_winnings": 0, "payouts": [], "hits": 0, "max_wins": 0} for mode in
         modes}

# Run simulation
for round_num in range(1, num_rounds + 1):
    mode = random.choice(modes)
    bet = base_bet * bet_multipliers[mode]
    P = create_transition_matrix(multipliers, crash_probs[mode], cashout_prob)
    payout = simulate_round(multipliers, P, bet, mode)

    result = f"Round {round_num} ({mode}): Bet = {bet:.2f}, Payout = {payout:.2f}"
    print(result)

    stats[mode]["rounds"] += 1
    stats[mode]["total_spent"] += bet
    stats[mode]["total_winnings"] += payout
    stats[mode]["payouts"].append(payout)
    if payout > 0:
        stats[mode]["hits"] += 1
    if payout >= base_bet * 50000:
        stats[mode]["max_wins"] += 1

# Overall statistics
total_spent = sum(stats[m]["total_spent"] for m in stats)
total_winnings = sum(stats[m]["total_winnings"] for m in stats)
overall_rtp = (total_winnings / total_spent) * 100 if total_spent > 0 else 0
overall_payouts = [p for m in stats for p in stats[m]["payouts"]]
overall_mean = statistics.mean(overall_payouts) if overall_payouts else 0
overall_sd = statistics.stdev(overall_payouts) if len(overall_payouts) > 1 else 0
overall_variance = overall_sd ** 2
overall_hits = sum(stats[m]["hits"] for m in stats)
overall_hit_rate = (overall_hits / num_rounds) * 100
overall_max_wins = sum(stats[m]["max_wins"] for m in stats)
overall_max_win_rate = (overall_max_wins / num_rounds) * 100
overall_volatility = classify_volatility(overall_hit_rate, overall_sd)

# Display overall results
print("\n**Overall Simulation Results**")
print(f"Total rounds: {num_rounds}")
print(f"Total spent: {total_spent:.2f}")
print(f"Total winnings: {total_winnings:.2f}")
print(f"RTP: {overall_rtp:.2f}% (Target: {rtp}%)")
print(f"Mean Payout: {overall_mean:.2f}")
print(f"Standard Deviation: {overall_sd:.2f}")
print(f"Variance: {overall_variance:.2f}")
print(f"Hit Rate: {overall_hit_rate:.2f}%")
print(f"Max Wins: {overall_max_wins}")
print(f"Max Win Rate: {overall_max_win_rate:.2f}%")
print(f"Volatility: {overall_volatility}")

# Display mode-specific results and generate histograms
for mode in stats:
    s = stats[mode]
    mode_rtp = (s["total_winnings"] / s["total_spent"]) * 100 if s["total_spent"] > 0 else 0
    mode_mean = statistics.mean(s["payouts"]) if s["payouts"] else 0
    mode_sd = statistics.stdev(s["payouts"]) if len(s["payouts"]) > 1 else 0
    mode_variance = mode_sd ** 2
    mode_hit_rate = (s["hits"] / s["rounds"]) * 100 if s["rounds"] > 0 else 0
    mode_max_win_rate = (s["max_wins"] / s["rounds"]) * 100 if s["rounds"] > 0 else 0
    mode_volatility = classify_volatility(mode_hit_rate, mode_sd)

    print(f"\n**{mode} Mode Results**")
    print(f"Rounds: {s['rounds']}")
    print(f"Total bets: {s['total_spent']:.2f}")
    print(f"Total wins: {s['total_winnings']:.2f}")
    print(f"RTP: {mode_rtp:.2f}%")
    print(f"Mean Payout: {mode_mean:.2f}")
    print(f"Standard Deviation: {mode_sd:.2f}")
    print(f"Variance: {mode_variance:.2f}")
    print(f"Hit Rate: {mode_hit_rate:.2f}%")
    print(f"Max Wins: {s['max_wins']}")
    print(f"Max Win Rate: {mode_max_win_rate:.2f}%")
    print(f"Volatility: {mode_volatility}")

    # Generate histogram with logarithmic y-scale
    plt.figure(figsize=(8, 6))
    plt.hist(s["payouts"], bins=50, color='skyblue', edgecolor='black')
    plt.yscale('log')  # Logarithmic scale for y-axis
    plt.title(f"Payout Distribution for {mode} Mode (Log Scale)")
    plt.xlabel("Payout")
    plt.ylabel("Frequency (Log Scale)")
    plt.grid(True, alpha=0.3)
    plt.show()
