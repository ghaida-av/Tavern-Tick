import statistics
from test_decision import decide
import calibrate_v3  # applies the improved option descriptions
from calibrate_text import to_text

THRESHOLD = 0.30

def S(name, job, time, hunger, energy, mood, nearby=(), last="work", carrying=None):
    d = {"name": name, "job": job, "time": time, "hunger": hunger, "energy": energy,
         "mood": mood, "nearby": list(nearby), "last_action": last}
    if carrying: d["carrying"] = carrying
    return d

CASES = [
    ("herbalist, calm morning", S("Hilda", "herbalist", "08:30", 3, 9, "calm"), {"work"}),
    ("guard worn out at 3am", S("Rook", "guard", "03:00", 2, 2, "tired"), {"sleep"}),
    ("fishmonger with fresh fish", S("Wren", "fishmonger", "10:00", 2, 8, "eager", carrying="basket of fresh fish"), {"trade"}),
    ("weaver starving, evening", S("Cass", "weaver", "19:30", 9, 6, "irritable"), {"eat"}),
    ("bored student, two friends near", S("Dov", "student", "16:00", 1, 8, "bored", ["Pip", "Lena"], "wander"), {"socialize"}),
    ("content retiree, alone, afternoon", S("Edda", "retired", "14:00", 2, 7, "content", last="sleep"), {"wander"}),
    ("baker hungry at lunch", S("Joss", "baker", "13:30", 7, 8, "cheerful"), {"eat"}),
    ("weary farmer, late night", S("Nell", "farmer", "22:30", 1, 3, "weary"), {"sleep"}),
    ("excited bard, three people near", S("Bex", "bard", "21:00", 2, 9, "excited", ["Hale", "Greta", "Pip"], "wander"), {"socialize"}),
    ("focused smith, late morning", S("Marl", "blacksmith", "11:00", 1, 9, "focused"), {"work"}),
    ("merchant with cart of goods", S("Tilda", "merchant", "09:30", 3, 8, "hopeful", carrying="cart of cloth and spices", last="wander"), {"trade"}),
    ("innkeeper starving, dinner time", S("Ivo", "innkeeper", "17:00", 10, 5, "stressed"), {"eat"}),
    ("curious traveler, alone", S("Sol", "traveler", "15:30", 2, 9, "curious", last="wander"), {"wander"}),
    ("baker up at dawn", S("Pru", "baker", "05:30", 4, 10, "determined", last="sleep"), {"work"}),
    ("grumpy hungry AND tired (ambiguous)", S("Gus", "farmer", "12:00", 8, 3, "grumpy"), {"eat", "sleep"}),
    ("lonely retiree, one neighbor", S("Mabel", "retired", "20:30", 2, 8, "lonely", ["Bram"], "wander"), {"socialize"}),
]

if __name__ == "__main__":
    decide(to_text(CASES[0][1]))  # warm-up
    rows, lat = [], []
    for label, state, ok in CASES:
        ans, ms = decide(to_text(state))
        good = ans["choice"] in ok
        act = ans["confidence"] >= THRESHOLD
        rows.append((ans["confidence"], good, act))
        lat.append(ms)
        print(f'{"OK " if good else "BAD"} {"ACT " if act else "ASK "} {label:38} -> {ans["choice"]:10} conf={ans["confidence"]:.2f}  {ms:5.0f} ms')
    acted = [g for c, g, a in rows if a]
    asked = [g for c, g, a in rows if not a]
    print(f"\nOverall accuracy: {sum(g for _, g, _ in rows)}/{len(rows)}")
    print(f"Acted on directly (conf >= {THRESHOLD}): {len(acted)}, correct {sum(acted)}")
    print(f"Escalated to Bedrock (conf < {THRESHOLD}): {len(asked)}, of which Decider alone was wrong on {len(asked) - sum(asked)}")
    print(f"Median latency: {statistics.median(lat):.0f} ms")
