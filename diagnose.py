import statistics
import test_decision
from test_decision import decide
from validate import CASES
from calibrate_text import to_text

def margin(ans):
    p = sorted(ans["probabilities"].values(), reverse=True)
    return p[0] - p[1]

print("PART A: confidence vs margin (gap between top two options)")
right_m, wrong_m = [], []
for label, state, ok in CASES:
    ans, _ = decide(to_text(state))
    good = ans["choice"] in ok
    m = margin(ans)
    (right_m if good else wrong_m).append(m)
    print(f'{"OK " if good else "BAD"} {label:38} -> {ans["choice"]:10} conf={ans["confidence"]:.2f} margin={m:.2f}')
print(f"mean margin when right: {statistics.mean(right_m):.2f} (min {min(right_m):.2f})")
print(f"mean margin when wrong: {statistics.mean(wrong_m):.2f} (max {max(wrong_m):.2f})")

print("\nPART B: why does trade fail?")
trade_cases = [c for c in CASES if c[0] in ("fishmonger with fresh fish", "merchant with cart of goods")]
original_trade = test_decision.QUESTION["next_action"]["criteria"]["trade"]
new_trade = ("Go to the market to sell goods. Choose this whenever the villager is carrying "
             "goods such as fish, cloth, spices or produce, during market hours (morning to late afternoon).")

def run(tag, desc, extra):
    test_decision.QUESTION["next_action"]["criteria"]["trade"] = desc
    for label, state, ok in trade_cases:
        text = to_text(state) + extra.format(name=state["name"])
        ans, _ = decide(text)
        top = sorted(ans["probabilities"].items(), key=lambda kv: -kv[1])[:3]
        print(f'{tag:34} {label:30} -> {ans["choice"]:8} conf={ans["confidence"]:.2f} top3={[(k, round(v, 2)) for k, v in top]}')

run("baseline", original_trade, "")
run("state says wants to sell at market", original_trade, " {name} wants to sell it at the market.")
run("stronger trade description", new_trade, "")
run("both changes", new_trade, " {name} wants to sell it at the market.")
