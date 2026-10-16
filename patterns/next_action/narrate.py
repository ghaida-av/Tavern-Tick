"""Turn a game-state dict into plain English.

Lesson learned: bare numbers (hunger=9) made the model guess which way the
scale runs. Words, plus stated intent, work much better."""

def _hunger(h):
    return ("not hungry at all" if h <= 2 else "a little peckish" if h <= 5
            else "hungry" if h <= 7 else "starving")

def _energy(e):
    return ("completely exhausted" if e <= 1 else "tired" if e <= 4
            else "fairly alert" if e <= 7 else "well rested and full of energy")

def _time(t):
    h = int(t.split(":")[0])
    if h >= 22 or h < 5: return f"It is {t}, the middle of the night"
    if h < 9: return f"It is {t}, early morning"
    if h < 12: return f"It is {t}, mid-morning"
    if h < 15: return f"It is {t}, midday"
    if h < 18: return f"It is {t}, afternoon"
    return f"It is {t}, evening"

def state_to_text(s):
    n = s["name"]
    parts = [f'{n} is a {s["job"]}.', _time(s["time"]) + ".",
             f'{n} feels {s["mood"]}, is {_hunger(s["hunger"])}, and is {_energy(s["energy"])}.']
    parts.append(f'Nearby: {", ".join(s["nearby"])}.' if s["nearby"] else "Nobody else is nearby.")
    if s.get("carrying"):
        parts.append(f'{n} is carrying a {s["carrying"]}.')
        hour = int(s["time"].split(":")[0])
        if 6 <= hour < 18:  # the engine knows the market is open, so say the intent out loud
            parts.append(f"{n} wants to sell it at the market.")
    hour_now = int(s["time"].split(":")[0])
    if 8 <= hour_now < 17 and s["job"] != "retired" and s["hunger"] <= 7 and s["energy"] >= 3:
        parts.append(f"It is working hours and {n} has {s['job']} duties to do.")
    parts.append(f'Last action: {s["last_action"]}.')
    return " ".join(parts)
