import random
import statistics


def generate_crash_point(rtp, mode="Normal"):
    """
    Generate a random crash point based on input RTP.
    For Additional MAX, scale crash points to balance higher cost and meta-multipliers.
    """
    u = random.uniform(0, 1)
    if mode == "Additional MAX":
        scale_factor = 0.5  # Increased to 0.5 to reduce early crashes
        if u < 1 - (rtp / 100) * scale_factor:
            return 1.0
        else:
            return min((rtp / 100) * scale_factor / (1 - u), 50000)
    else:
        # Standard distribution for Normal and Additional
        if u < 1 - (rtp / 100):
            return 1.0
        else:
            return min((rtp / 100) / (1 - u), 50000)


def generate_meta_multiplier():
    """Generate a random meta-multiplier between 2x and 20x."""
    return random.randint(2, 20)


def classify_volatility(hit_rate, sd):
    """Classify volatility based on hit rate and standard deviation."""
    if hit_rate < 20 and sd > 1000:
        return "High"
    elif 20 <= hit_rate <= 40 or (sd > 500 and hit_rate < 50):
        return "Medium"
    else:
        return "Low"


# Welcome message
print("Welcome to Knight's Ascent RTP Simulation!")

# Get user inputs
rtp = float(input("Enter desired RTP (e.g., 95 for 95%): "))
base_bet = float(input("Enter standard bet amount (e.g., 1.0): "))
num_rounds = int(input("Enter number of rounds to simulate: "))

# Initialize tracking variables by mode
stats = {
    "Normal": {"rounds": 0, "total_spent": 0, "total_winnings": 0, "payouts": [], "hits": 0, "max_wins": 0},
    "Additional": {"rounds": 0, "total_spent": 0, "total_winnings": 0, "payouts": [], "hits": 0, "max_wins": 0},
    "Additional MAX": {"rounds": 0, "total_spent": 0, "total_winnings": 0, "payouts": [], "hits": 0, "max_wins": 0}
}

# Run simulation for specified number of rounds
for round_num in range(1, num_rounds + 1):
    # Randomly select game mode (equal probability)
    mode = random.choice(["Normal", "Additional", "Additional MAX"])
    bet_multiplier = {"Normal": 1, "Additional": 150, "Additional MAX": 300}[mode]
    bet = base_bet * bet_multiplier
    cashout_multiplier = random.uniform(1.1, 50.0)
    crash_point = generate_crash_point(rtp, mode)
    meta_multipliers = [10] if mode == "Additional MAX" else []

    multiplier = 1.0
    step = 0.1
    while multiplier < cashout_multiplier and multiplier < crash_point:
        if mode in ["Additional", "Additional MAX"] and random.random() < 0.05:
            meta_multipliers.append(generate_meta_multiplier())
        multiplier += step

    if multiplier >= crash_point:
        payout = 0
        result = f"Round {round_num} ({mode}): Bet = {bet:.2f}, Crash at {crash_point:.1f}x, Payout = {payout:.2f}"
    else:
        total_meta = sum(meta_multipliers) / 100 if meta_multipliers else 1  # Sum divided by 100
        payout = bet * cashout_multiplier * total_meta
        if payout >= base_bet * 50000:
            payout = base_bet * 50000
            stats[mode]["max_wins"] += 1
        stats[mode]["hits"] += 1
        meta_str = f", Meta-Multipliers = {'x' + ', x'.join(map(str, meta_multipliers))}" if meta_multipliers else ""
        result = f"Round {round_num} ({mode}): Bet = {bet:.2f}, Cashout at {cashout_multiplier:.1f}x{meta_str}, Payout = {payout:.2f}"

    print(result)
    stats[mode]["rounds"] += 1
    stats[mode]["total_spent"] += bet
    stats[mode]["total_winnings"] += payout
    stats[mode]["payouts"].append(payout)

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
print(f"Max Win Rate: {overall_max_win_rate:.2f}%")
print(f"Volatility: {overall_volatility}")

# Display mode-specific results
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
    print(f"Max Win Rate: {mode_max_win_rate:.2f}%")
    print(f"Volatility: {mode_volatility}")