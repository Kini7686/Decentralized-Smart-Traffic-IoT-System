import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple

import pandas as pd
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ============================
# AES-256-GCM Encryption Layer
# ============================
class AESCipher:
    """
    Symmetric cipher using a fixed 'police' key.

    NOTE: In production, POLICE_KEY_HEX must be set via environment variable
    and NEVER hard-coded or committed to Git.
    """

    def __init__(self):
        # Load fixed police key from environment (recommended)
        police_key_hex = os.getenv("POLICE_KEY_HEX")

        if police_key_hex:
            key = bytes.fromhex(police_key_hex)
        else:
            # Demo fallback (for your local testing only)
            # 32 bytes (256 bits) hex string
            key = bytes.fromhex(
                "00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF"
            )

        if len(key) != 32:
            raise ValueError("POLICE_KEY must be 32 bytes (256-bit)")

        self.key = key
        self.aes = AESGCM(self.key)

    def encrypt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        Encrypt a Python dict using AES-256-GCM.
        Returns (nonce_hex, ciphertext_hex).
        """
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        plaintext = json.dumps(data).encode("utf-8")
        ct = self.aes.encrypt(nonce, plaintext, None)
        return nonce.hex(), ct.hex()

    def decrypt(self, nonce_hex: str, ciphertext_hex: str) -> Dict[str, Any]:
        """
        Decrypt a previously-encrypted payload.
        """
        nonce = bytes.fromhex(nonce_hex)
        ct = bytes.fromhex(ciphertext_hex)
        pt = self.aes.decrypt(nonce, ct, None)
        return json.loads(pt.decode("utf-8"))


# ============================
# Blockchain Data Structures
# ============================
class Block:
    def __init__(self, index: int, timestamp: str, data: Any, prev_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data          # list/dict of transactions
        self.prev_hash = prev_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_data = json.dumps(self.__dict__, sort_keys=True, default=str).encode()
        return hashlib.sha256(block_data).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_tx: List[Dict[str, Any]] = []
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={"msg": "Genesis Block"},
            prev_hash="0",
        )
        self.chain.append(genesis)

    def add_tx(self, tx: Dict[str, Any]):
        self.current_tx.append(tx)

    def mine(self) -> Block:
        prev = self.chain[-1]
        new_block = Block(
            index=prev.index + 1,
            timestamp=datetime.utcnow().isoformat(),
            data=self.current_tx.copy(),
            prev_hash=prev.hash,
        )
        self.chain.append(new_block)
        self.current_tx.clear()
        return new_block


# ============================
# Smart-contract-style Logic
# ============================
def toll(event: Dict[str, Any]) -> float:
    """
    Simple dynamic toll based on congestion (0–1).
    """
    congestion = float(event.get("congestion", 0.5))
    base = 1.0
    dynamic = congestion * 2.0
    return round(base + dynamic, 2)


def route(event: Dict[str, Any]) -> str:
    """
    Choose route based on congestion.
    """
    congestion = float(event.get("congestion", 0.5))
    if congestion < 0.4:
        return "FASTEST"
    if congestion < 0.8:
        return "ALTERNATE_1"
    return "ALTERNATE_2"


# ============================
# Real US Traffic Dataset
# ============================
def load_vehicle_dataset(path: str = "us_traffic_data.csv") -> pd.DataFrame:
    """
    Load real US traffic data from CSV.

    Expected columns (you can extend as needed):
      plate, phone, email, entry_point, exit_point,
      entry_time, exit_time, speed_kmph, speed_limit_kmph
    """
    df = pd.read_csv(path)
    return df


def build_event_from_row(row: pd.Series) -> Dict[str, Any]:
    """
    Convert a dataset row into an IoT 'event' the system can process.
    """
    speed = float(row["speed_kmph"])
    limit = float(row["speed_limit_kmph"])

    # Congestion estimate
    congestion = round(min(1.0, max(0.1, speed / max(1.0, limit))), 2)

    # Travel time (optional, if columns exist)
    travel_minutes = None
    if "entry_time" in row and "exit_time" in row:
        try:
            t_in = datetime.fromisoformat(str(row["entry_time"]))
            t_out = datetime.fromisoformat(str(row["exit_time"]))
            travel_minutes = round((t_out - t_in).total_seconds() / 60.0, 1)
        except Exception:
            travel_minutes = None

    event = {
        "vehicle": row.get("plate"),
        "phone": row.get("phone"),
        "email": row.get("email"),
        "entry_point": row.get("entry_point"),
        "exit_point": row.get("exit_point"),
        "entry_time": str(row.get("entry_time")),
        "exit_time": str(row.get("exit_time")),
        "speed": round(speed, 2),
        "speed_limit": round(limit, 2),
        "congestion": congestion,
        "travel_time_min": travel_minutes,
    }
    return event


def evaluate_decision(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Algorithm for decision making + correctness check.

    - Computes toll & route.
    - Checks if driver is overspeeding.
    """
    speed = float(event.get("speed", 0.0))
    limit = float(event.get("speed_limit", 0.0))

    overspeed = speed > limit
    decision_correct = not overspeed  # simple rule

    decision = {
        "toll": toll(event),
        "route": route(event),
        "overspeed": overspeed,
        "decision_correct": decision_correct,
        "comment": (
            "Safe driving, decision OK."
            if decision_correct
            else "Overspeed detected. Driver must confirm or reject guidance."
        ),
    }
    return decision
