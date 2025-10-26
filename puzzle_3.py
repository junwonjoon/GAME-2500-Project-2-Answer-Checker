import time
import json
import os
from pathlib import Path
import streamlit as st

st.title("Filling Maker")

# ---------- Persistence helpers ----------
LOCK_FILE = Path("lock_state.json")

def load_lock() -> float:
    """Return UNIX timestamp when lock expires (0 if none)."""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, "r") as f:
                data = json.load(f)
            return float(data.get("lock_until", 0))
        except Exception:
            return 0.0
    return 0.0

def save_lock(lock_until: float) -> None:
    """Persist lock expiration timestamp."""
    tmp = LOCK_FILE.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump({"lock_until": lock_until}, f)
    os.replace(tmp, LOCK_FILE)  # atomic write on most OSes

# ---------- Session init ----------
if "lock_until" not in st.session_state:
    st.session_state["lock_until"] = 0.0

# Read persisted lock & keep the stricter one (disk survives refresh)
persisted = load_lock()
now = time.time()
effective_lock_until = max(st.session_state["lock_until"], persisted)
st.session_state["lock_until"] = effective_lock_until  # unify view

remaining = max(0, int(effective_lock_until - now))
locked = remaining > 0

# ---------- Input ----------
st.header("Press Enter After Typing!")
user_ans = st.text_input(
    "Enter a 4 digit number to cook fillings", max_chars=4
)
if len(user_ans) != 0:
    st.write(f"Is your answer: {user_ans}?")

# ---------- Submit (only locks on wrong answer) ----------
if st.button("Check", disabled=locked):
    if user_ans == "0129":
        st.success("You earned Filling! Tell the operator to give you the card!")
        # Clear any existing lock
        st.session_state["lock_until"] = 0.0
        save_lock(0.0)
    else:
        st.error("❌ Wrong Attempt! Locked for 30 seconds.")
        lock_until = time.time() + 30
        st.session_state["lock_until"] = lock_until
        save_lock(lock_until)
        remaining = 30
        locked = True

# ---------- Live countdown (decrements every second) ----------
if locked:
    msg = st.empty()
    # Keep updating until the lock expires (survives refresh because of disk)
    while True:
        now = time.time()
        effective_lock_until = max(st.session_state["lock_until"], load_lock())
        remaining = int(effective_lock_until - now)
        if remaining <= 0:
            # Unlock and refresh UI
            st.session_state["lock_until"] = 0.0
            save_lock(0.0)
            st.rerun()
        msg.warning(f"Try again in {remaining} seconds.")
        time.sleep(1)
