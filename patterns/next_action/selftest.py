import statistics
from . import decide, state_to_text
from validate import CASES   # the 16 fresh cases from Step 7

if __name__ == "__main__":
    decide(state_to_text(CASES[0][1]))  # warm-up
    ok_n, lat = 0, []
    for label, state, ok in CASES:
        d = decide(state_to_text(state))
        good = d.choice in ok
        ok_n += good
        lat.append(d.latency_ms)
        print(f'{"OK " if good else "BAD"} {"ASK" if d.escalate else "ACT"} {label:38} -> {d.choice:10} conf={d.confidence:.2f} {d.latency_ms:5.0f} ms')
    print(f"\naccuracy: {ok_n}/{len(CASES)}   median latency: {statistics.median(lat):.0f} ms")
