from typing import List, Tuple

INF = float("inf")


def coin_change_min_coins(coins: List[int], amount: int):
    """
    Core DP algorithm: bottom-up tabulation.
    Returns (min_coins_needed, dp_table, coin_used_table)

    coin_used_table[a] stores which coin was used to reach amount 'a'
    optimally, so we can backtrack and reconstruct the actual combination
    of coins used (not just the count).
    """
    # dp[a] = minimum coins needed to make amount a
    dp = [INF] * (amount + 1)
    dp[0] = 0

    # last_coin_used[a] = which coin denomination was used to build dp[a]
    last_coin_used = [-1] * (amount + 1)

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
                last_coin_used[a] = coin

    return dp[amount], dp, last_coin_used


def reconstruct_coins_used(amount: int, last_coin_used: List[int]) -> List[int]:
    """
    Backtracks through the last_coin_used table to reconstruct the exact
    combination of coins that make up the optimal (minimum-count) answer.
    """
    if amount == 0 or last_coin_used[amount] == -1:
        return []

    coins_used = []
    remaining = amount
    while remaining > 0:
        coin = last_coin_used[remaining]
        if coin == -1:
            # Should not happen if dp[amount] is reachable, but guard anyway
            break
        coins_used.append(coin)
        remaining -= coin
    return coins_used


def print_dp_table(dp: List[float], amount: int) -> None:
    print("\nDP Table (minimum coins needed for each amount from 0 to "
          f"{amount}):")
    print("Amount: " + "  ".join(f"{a:>3}" for a in range(amount + 1)))
    display_values = ["INF" if v == INF else str(int(v)) for v in dp]
    print("Coins : " + "  ".join(f"{v:>3}" for v in display_values))


def get_user_input():
    print("=== Coin Change Problem (Dynamic Programming - Minimum Coins) ===")
    try:
        coin_input = input(
            "Enter available coin denominations, separated by spaces "
            "(e.g. 1 5 10 20 50): "
        ).strip()
        coins = [int(c) for c in coin_input.split()]
        amount = int(input("Enter the target amount: ").strip())
    except ValueError:
        print("Invalid input.")
        return [], 0

    coins = sorted(set(c for c in coins if c > 0))
    return coins, amount


def load_sample_data() -> Tuple[List[int], int]:
    """A built-in sample dataset for quick demonstration/testing."""
    coins = [1, 5, 10, 20, 50]
    amount = 67
    return coins, amount


def main():
    print("1. Enter my own coins and amount")
    print("2. Use sample dataset (for quick testing)")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "2":
        coins, amount = load_sample_data()
    else:
        coins, amount = get_user_input()

    if not coins or amount < 0:
        print("No valid coins/amount provided. Exiting.")
        return

    if amount == 0:
        print("\nTarget amount is 0. Minimum coins needed: 0")
        return

    min_coins, dp, last_coin_used = coin_change_min_coins(coins, amount)

    print(f"\nAvailable coin denominations: {coins}")
    print(f"Target amount: {amount}")

    print_dp_table(dp, amount)

    if min_coins == INF:
        print(f"\nIt is not possible to make {amount} using the given "
              f"coin denominations.")
        return

    coins_used = reconstruct_coins_used(amount, last_coin_used)

    print(f"\nMinimum number of coins needed: {int(min_coins)}")
    print("Coins used (one possible optimal combination):")
    print("  " + " + ".join(str(c) for c in coins_used) +
          f" = {sum(coins_used)}")

    # Show a simple breakdown/count summary for clearer output formatting
    print("\nBreakdown by denomination:")
    print(f"{'Denomination':<15}{'Count':<10}")
    print("-" * 25)
    for coin in coins:
        count = coins_used.count(coin)
        if count > 0:
            print(f"{coin:<15}{count:<10}")


if __name__ == "__main__":
    main()
