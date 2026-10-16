import statistics
import test_decision
from test_decision import decide
from calibrate import CASES
from calibrate_text import to_text

NEW_ACTIONS = {
    "work": "Do your job. Choose this when the villager is rested and not hungry during working hours, from morning to late afternoon.",
    "eat": "Get food or a drink. Choose this when the villager is hungry or starving, at any time of day.",
    "sleep": "Go to bed or rest. Choose this when the villager is tired or exhausted, or it is the middle of the night.",
    "socialize": "Talk with other villagers who are nearby. Choose this when others are nearby and the villager is lonely or cheerful with free time.",
    "wander": "Stroll around aimlessly. Choose this only when nothing else is needed and nobody is nearby to talk to.",
    "trade": "Buy or sell goods at the market. Choose this when the villager is carrying goods to sell.",
}
test_decision.QUESTION["next_action"]["criteria"] = NEW_ACTIONS

if __name__ == "__main__":
    decide(to_text(CASES[0][1]))  # warm-up
    rows = []
    for label, state, ok in CASES:
        ans, ms = decide(to_text(state))
        good = ans["choice"] in ok
        rows.append((ans["confidence"], good))
        print(f'{"OK " if good else "BAD"} {label:40} -> {ans["choice"]:10} conf={ans["confidence"]:.2f}  {ms:5.0f} ms')
    right = [c for c, g in rows if g]; wrong = [c for c, g in rows if not g]
    print(f"\naccuracy: {len(right)}/{len(rows)}")
    if right: print(f"mean confidence when right: {statistics.mean(right):.2f}")
    if wrong: print(f"mean confidence when wrong: {statistics.mean(wrong):.2f}")
