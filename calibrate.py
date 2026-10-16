import statistics
from test_decision import decide

# (description, state, acceptable answers)
CASES = [
    ("hungry baker, noon", {"name": "Mira", "job": "baker", "time": "12:30", "hunger": 9, "energy": 7, "mood": "cheerful", "nearby": [], "last_action": "work"}, {"eat"}),
    ("exhausted farmer, midnight", {"name": "Tomas", "job": "farmer", "time": "23:50", "hunger": 2, "energy": 1, "mood": "tired", "nearby": [], "last_action": "work"}, {"sleep"}),
    ("lonely bard, friends nearby", {"name": "Lena", "job": "bard", "time": "20:15", "hunger": 3, "energy": 8, "mood": "lonely", "nearby": ["Mira", "Tomas"], "last_action": "wander"}, {"socialize"}),
    ("fed, rested baker, morning", {"name": "Mira", "job": "baker", "time": "09:00", "hunger": 2, "energy": 9, "mood": "calm", "nearby": [], "last_action": "sleep"}, {"work"}),
    ("merchant with full pack, market open", {"name": "Odo", "job": "merchant", "time": "10:30", "hunger": 2, "energy": 8, "mood": "eager", "nearby": [], "carrying": "full pack of goods", "last_action": "wander"}, {"trade"}),
    ("retired, fed and rested, midday", {"name": "Old Bram", "job": "retired", "time": "13:00", "hunger": 1, "energy": 8, "mood": "relaxed", "nearby": [], "last_action": "sleep"}, {"wander", "socialize"}),
    ("starving tavern keeper, evening", {"name": "Greta", "job": "tavern keeper", "time": "19:00", "hunger": 10, "energy": 6, "mood": "grumpy", "nearby": [], "last_action": "work"}, {"eat"}),
    ("sick and drained, afternoon", {"name": "Finn", "job": "forger", "time": "15:00", "hunger": 3, "energy": 0, "mood": "sick", "nearby": [], "last_action": "work"}, {"sleep"}),
    ("rested farmer at dawn", {"name": "Tomas", "job": "farmer", "time": "06:00", "hunger": 3, "energy": 10, "mood": "determined", "nearby": [], "last_action": "sleep"}, {"work"}),
    ("cheerful, fed, friends nearby, evening", {"name": "Pip", "job": "student", "time": "20:00", "hunger": 1, "energy": 9, "mood": "cheerful", "nearby": ["Lena", "Odo"], "last_action": "wander"}, {"socialize"}),
    ("hungry merchant with goods", {"name": "Odo", "job": "merchant", "time": "11:00", "hunger": 8, "energy": 7, "mood": "eager", "nearby": [], "carrying": "full pack of goods", "last_action": "wander"}, {"eat", "trade"}),
    ("blacksmith at 2am", {"name": "Hale", "job": "blacksmith", "time": "02:00", "hunger": 1, "energy": 5, "mood": "calm", "nearby": [], "last_action": "work"}, {"sleep"}),
]

if __name__ == "__main__":
    decide(CASES[0][1])  # warm-up, not counted
    rows, lat = [], []
    for label, state, ok in CASES:
        ans, ms = decide(state)
        good = ans["choice"] in ok
        rows.append((label, ans["choice"], ans["confidence"], good))
        lat.append(ms)
        print(f'{"OK " if good else "BAD"} {label:40} -> {ans["choice"]:10} conf={ans["confidence"]:.2f}  {ms:5.0f} ms')
    right = [c for _, _, c, g in rows if g]
    wrong = [c for _, _, c, g in rows if not g]
    print(f"\naccuracy: {len(right)}/{len(rows)}")
    if right: print(f"mean confidence when right: {statistics.mean(right):.2f} (min {min(right):.2f})")
    if wrong: print(f"mean confidence when wrong: {statistics.mean(wrong):.2f} (max {max(wrong):.2f})")
    print(f"median latency: {statistics.median(lat):.0f} ms")
