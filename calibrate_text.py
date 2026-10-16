import statistics
from test_decision import decide
from calibrate import CASES

def hunger_word(h):
    return ("not hungry at all" if h <= 2 else "a little peckish" if h <= 5
            else "hungry" if h <= 7 else "starving")

def energy_word(e):
    return ("completely exhausted" if e <= 1 else "tired" if e <= 4
            else "fairly alert" if e <= 7 else "well rested and full of energy")

def time_word(t):
    h = int(t.split(":")[0])
    if h >= 22 or h < 5: return f"It is {t}, the middle of the night"
    if h < 9: return f"It is {t}, early morning"
    if h < 12: return f"It is {t}, mid-morning"
    if h < 15: return f"It is {t}, midday"
    if h < 18: return f"It is {t}, afternoon"
    return f"It is {t}, evening"

def to_text(s):
    parts = [f'{s["name"]} is a {s["job"]}.', time_word(s["time"]) + ".",
             f'{s["name"]} feels {s["mood"]}, is {hunger_word(s["hunger"])}, and is {energy_word(s["energy"])}.']
    parts.append(f'Nearby: {", ".join(s["nearby"])}.' if s["nearby"] else "Nobody else is nearby.")
    if s.get("carrying"): parts.append(f'{s["name"]} is carrying a {s["carrying"]}.')
    parts.append(f'Last action: {s["last_action"]}.')
    return " ".join(parts)

if __name__ == "__main__":
    print("example state:", to_text(CASES[0][1]), "\n")
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
