import streamlit as st
from backend import (
    AESCipher,
    Blockchain,
    load_vehicle_dataset,
    build_event_from_row,
    evaluate_decision,
)

# ---------- PAGE CONFIG & CSS ----------

st.set_page_config(page_title="Smart Traffic IoT System", page_icon="🚦", layout="wide")

st.markdown(
    """
<style>
.stApp { background: #0b0f19; color: #ffffff; }
.main-title { font-size: 32px; font-weight: 800; }
.subtext { font-size: 14px; color: #aeb4c6; }
.section-header { font-size: 18px; font-weight: 700; margin-top: 1.5rem; color: #93c5fd; }
.metric-badge { border-radius: 20px; padding: 5px 12px; font-size: 13px; font-weight: 600; }
.safe { background: #14532d; color: #86efac; }
.unsafe { background: #7f1d1d; color: #fecaca; }
.overspeed-banner {
    background:#991b1b;
    padding:12px;
    font-size:16px;
    font-weight:700;
    border-radius:8px;
    margin-top:10px;
    margin-bottom:4px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🚦 Decentralized Smart Traffic IoT System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtext">Real vehicle IoT data → AI decisions → Driver validation → Blockchain security</div>',
    unsafe_allow_html=True,
)
st.write("")

# ---------- SESSION STATE INIT ----------

if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()
if "cipher" not in st.session_state:
    st.session_state.cipher = AESCipher()
if "current_event" not in st.session_state:
    st.session_state.current_event = None
if "current_decision" not in st.session_state:
    st.session_state.current_decision = None
if "driver_response" not in st.session_state:
    st.session_state.driver_response = None
if "rejected_cases" not in st.session_state:
    # list of dicts: {nonce, ciphertext, vehicle, exit_point}
    st.session_state.rejected_cases = []

tab_control, tab_ledger, tab_rejected = st.tabs(
    ["🎛 Control Panel", "📦 Blockchain Ledger", "🚨 Rejected Guidance"]
)

# ---------- CONTROL PANEL TAB ----------

with tab_control:
    # Step 1 – Load Data (IoT)
    st.markdown(
        '<div class="section-header">1️⃣ Load IoT Data from Dataset</div>',
        unsafe_allow_html=True,
    )

    df = None
    try:
        df = load_vehicle_dataset()
        st.caption(f"Loaded dataset with {len(df)} records")
    except Exception as e:
        st.error(f"Error loading dataset: {e}")

    if df is not None:
        idx = st.slider("Select Vehicle Trip Record", 0, len(df) - 1, 0)

        if st.button("Load IoT Event"):
            st.session_state.current_event = build_event_from_row(df.iloc[idx])
            st.session_state.current_decision = None
            st.session_state.driver_response = None
            st.success("IoT event loaded!")

    if st.session_state.current_event:
        st.json(st.session_state.current_event)

    # Step 2 – Decision Engine
    st.markdown(
        '<div class="section-header">2️⃣ Run Decision Engine</div>',
        unsafe_allow_html=True,
    )

    if st.button("Decision Engine"):
        if not st.session_state.current_event:
            st.warning("Load an IoT event first!")
        else:
            st.session_state.current_decision = evaluate_decision(
                st.session_state.current_event
            )
            st.session_state.driver_response = None
            st.success("Decision generated!")

    if st.session_state.current_decision:
        dec = st.session_state.current_decision

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Toll", dec["toll"])
        col2.metric("📍 Route", dec["route"])
        col3.metric("⚠ Overspeed", "YES" if dec["overspeed"] else "NO")

        if dec["overspeed"]:
            st.markdown(
                '<div class="overspeed-banner">⚠️ OVERSPEED DETECTED — DRIVER ACTION REQUIRED</div>',
                unsafe_allow_html=True,
            )

        safe = dec["decision_correct"]
        st.markdown(
            f'<span class="metric-badge {"safe" if safe else "unsafe"}">'
            f'{"Decision Safe" if safe else "Driver action required"}'
            "</span>",
            unsafe_allow_html=True,
        )
        st.caption(dec["comment"])

    # Step 3 – Driver Response
    st.markdown(
        '<div class="section-header">3️⃣ Driver Response</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.current_decision:
        st.info("Run decision engine first!")
    else:
        dec = st.session_state.current_decision
        if not dec["overspeed"]:
            st.success("No overspeed detected — system auto-approved.")
            st.session_state.driver_response = "AUTO_SAFE"
        else:
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✔ Confirm Guidance"):
                    st.session_state.driver_response = "CONFIRMED"
            with col_no:
                if st.button("❌ Reject Guidance"):
                    st.session_state.driver_response = "REJECTED"

    # Response status
    if st.session_state.driver_response == "CONFIRMED":
        st.success("Driver CONFIRMED guidance")
    elif st.session_state.driver_response == "REJECTED":
        st.error("Driver REJECTED guidance")
    elif st.session_state.driver_response == "AUTO_SAFE":
        st.info("System auto-approved (safe driving)")

    # Step 4 – Secure + Add / Store
    st.markdown(
        '<div class="section-header">4️⃣ Secure Logging</div>',
        unsafe_allow_html=True,
    )

    if st.button("🧾 Encrypt & Save Transaction"):
        if not st.session_state.driver_response:
            st.warning("Get driver confirmation/rejection first!")
        else:
            payload = {
                "event": st.session_state.current_event,
                "decision": st.session_state.current_decision,
                "driver_response": st.session_state.driver_response,
            }

            nonce_hex, ciphertext_hex = st.session_state.cipher.encrypt(payload)

            # Minimal metadata for quick viewing (no need to decrypt for this)
            meta_vehicle = (
                st.session_state.current_event.get("vehicle")
                if st.session_state.current_event
                else None
            )
            meta_exit = (
                st.session_state.current_event.get("exit_point")
                if st.session_state.current_event
                else None
            )

            tx = {
                "nonce": nonce_hex,
                "ciphertext": ciphertext_hex,
                "driver_response": st.session_state.driver_response,
                "vehicle": meta_vehicle,
                "exit_point": meta_exit,
            }

            if st.session_state.driver_response == "REJECTED":
                # ❌ Rejected guidance → NOT on blockchain; only Rejected tab
                st.session_state.rejected_cases.append(tx)
                st.error(
                    "Rejected guidance stored ONLY in 'Rejected Guidance' tab (not on blockchain)."
                )
            else:
                # ✅ Confirmed / AUTO_SAFE → goes to blockchain
                st.session_state.bc.add_tx(tx)
                st.success("Transaction added to pending blockchain block!")

    if st.button("⛓ Mine Block"):
        if not st.session_state.bc.current_tx:
            st.warning("No pending transactions to mine!")
        else:
            block = st.session_state.bc.mine()
            st.success(f"Block #{block.index} successfully mined!")


# ---------- BLOCKCHAIN LEDGER TAB ----------

with tab_ledger:
    st.markdown('<div class="section-header">📦 Blockchain Ledger</div>', unsafe_allow_html=True)

    for blk in st.session_state.bc.chain[::-1]:
        with st.expander(f"Block #{blk.index} | {blk.timestamp}"):

            st.write("📌 Block Metadata")
            st.json({"hash": blk.hash, "prev_hash": blk.prev_hash})

            st.write("📦 Transactions")
            for t_i, tx in enumerate(blk.data):
                with st.container():
                    if isinstance(tx, dict) and "ciphertext" in tx:
                        vehicle = tx.get("vehicle", "N/A")
                        st.markdown(f"**TX #{t_i+1}** — Vehicle: `{vehicle}`")
                    else:
                        # This is the genesis block or other header object
                        st.json(tx)
                        continue


                    # Show raw blockchain TX metadata
                    st.json({
                        "nonce": tx["nonce"],
                        "ciphertext": tx["ciphertext"],
                        "driver_response": tx.get("driver_response"),
                    })

                    # Decrypt button
                    if st.button(f"🔓 Decrypt TX #{t_i+1} in Block {blk.index}", key=f"ledger_decrypt_{blk.index}_{t_i}"):
                        try:
                            decrypted = st.session_state.cipher.decrypt(
                                tx["nonce"], tx["ciphertext"]
                            )

                            st.success("Decrypted Full Transaction:")
                            st.json(decrypted)

                        except Exception as e:
                            st.error(f"❌ Decryption failed: {e}")



# ---------- REJECTED GUIDANCE TAB ----------

with tab_rejected:
    st.markdown(
        '<div class="section-header">🚨 Rejected Guidance Cases</div>',
        unsafe_allow_html=True,
    )

    cases = st.session_state.rejected_cases
    if not cases:
        st.info("No rejected cases yet.")
    else:
        for i, case in enumerate(cases[::-1]):
            vehicle = case.get("vehicle", "Unknown")
            exit_point = case.get("exit_point", "Unknown")

            with st.expander(f"🚫 Case #{i+1} — Vehicle: {vehicle}"):
                # Big highlighted vehicle banner
                st.markdown(
                    f"""
                    <div style="
                        background:#8B0000;
                        padding:12px;
                        border-radius:8px;
                        font-size:20px;
                        font-weight:800;
                        color:#FFD700;
                        text-align:center;">
                        🚙 Vehicle Plate: {vehicle}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Highlight exit point
                st.markdown(
                    f"""
                    <div style="
                        background:#6b5f12;
                        padding:10px;
                        margin-top:10px;
                        border-radius:8px;
                        font-size:16px;">
                        🛣 Last Exit Point: <strong>{exit_point}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Rejected banner
                st.markdown(
                    """
                    <div style="
                        background:#4C0000;
                        padding:10px;
                        margin-top:10px;
                        border-radius:8px;
                        font-size:16px;
                        color:#FFB3B3;">
                        ❌ Driver REJECTED guidance — Share with traffic police.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Decrypt button for police/authorized users
                if st.button(
                    f"🔓 Decrypt full case #{i+1}", key=f"decrypt_case_{i+1}"
                ):
                    try:
                        decrypted = st.session_state.cipher.decrypt(
                            case["nonce"], case["ciphertext"]
                        )
                        st.success("Decrypted case payload:")
                        st.json(decrypted)
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")

                # For debugging / auditing, you can also show raw encrypted record:
                if st.checkbox(f"Show raw encrypted record #{i+1}", key=f"raw_case_{i+1}"):
                    st.json(case)   