# Decentralized Smart Traffic IoT System

A secure, AI-powered **Smart Traffic Management System** that integrates IoT vehicle data, decision intelligence, AES-256 encryption, and blockchain-based logging. Built with Streamlit for an interactive dashboard experience.

The system simulates real-time traffic monitoring, driver behavior analysis (including overspeed detection), and secure enforcement using decentralized technology—ideal for IoT and blockchain coursework or demonstrations.

---

## Features

| Feature | Description |
|---------|-------------|
| **Real IoT Traffic Dataset** | Processes vehicle records from CSV with plate, speed, entry/exit points, timestamps |
| **AI Decision Engine** | Dynamic toll calculation, optimal route suggestion, overspeed detection |
| **Driver Validation** | Confirm / Reject workflow for overspeed cases; auto-approval for safe drivers |
| **AES-256-GCM Encryption** | Full payload encryption before storage—only authorized users can decrypt |
| **Custom Blockchain Ledger** | Immutable, tamper-resistant transaction history with block mining |
| **Rejected Guidance System** | Separate storage for rejected cases; accessible to traffic police for review |
| **Interactive Dashboard** | Streamlit UI with tabs for Control Panel, Blockchain Ledger, and Rejected Guidance |

---

## System Architecture

```
IoT Dataset (CSV)
       ↓
   Load & Parse
       ↓
  AI Decision Engine (Toll, Route, Overspeed)
       ↓
   Driver Response (Confirm / Reject / Auto-Safe)
       ↓
  AES-256-GCM Encryption
       ↓
  ┌─────────────────────────────────────┐
  │ CONFIRMED / AUTO_SAFE → Blockchain   │
  │ REJECTED → Rejected Guidance Tab     │
  └─────────────────────────────────────┘
       ↓
  Police / Admin Decryption (authorized access)
```

---

## Project Structure

```
.
├── app.py              # Streamlit frontend & UI
├── backend.py          # Blockchain, encryption, AI decision logic
├── generate_dataset.py # Script to generate us_traffic_data.csv
├── us_traffic_data.csv # Sample IoT traffic dataset (500 records)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Technologies Used

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.8+ |
| **Encryption** | AES-256-GCM (via `cryptography`) |
| **Blockchain** | Custom Python blockchain (SHA-256, linked blocks) |
| **Data Processing** | Pandas |
| **Dataset** | CSV (US traffic simulation) |

---

## Functional Modules

### 1. IoT Data Loader
- Loads traffic data from `us_traffic_data.csv`
- Converts rows into structured events (vehicle, speed, limits, congestion, etc.)

### 2. Decision Engine
- **Toll**: Dynamic toll based on congestion (base + congestion factor)
- **Route**: Chooses FASTEST, ALTERNATE_1, or ALTERNATE_2 based on congestion
- **Overspeed**: Detects when `speed_kmph > speed_limit_kmph`

### 3. Driver Validation
- **Auto-Safe**: No overspeed → system auto-approves
- **Confirm / Reject**: Overspeed detected → driver must confirm or reject guidance

### 4. Secure Encryption
- AES-256-GCM symmetric encryption
- Encrypts full payload (event + decision + driver_response) before storage
- Key via `POLICE_KEY_HEX` environment variable (32-byte hex string)

### 5. Blockchain Ledger
- Genesis block + chained blocks
- Stores confirmed transactions with block mining
- SHA-256 hashing for tamper resistance

### 6. Rejected Guidance
- Rejected cases stored separately (not on blockchain)
- Visible in a dedicated tab for traffic police
- Supports full decryption for authorized users

---

## Security Model

| Layer | Implementation |
|-------|----------------|
| **Encryption** | AES-256-GCM with 96-bit nonce; fixed police key via env |
| **Blockchain** | SHA-256 hashing; linked block structure; immutable records |
| **Privacy** | Sensitive data encrypted; decryption only for authorized access |

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kini7686/Decentralized-Smart-Traffic-IoT-System
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Set encryption key

For production, set the police decryption key:

```bash
# Windows (PowerShell)
$env:POLICE_KEY_HEX="00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF"

# Windows (CMD) / macOS / Linux
set POLICE_KEY_HEX=00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF
```

> If not set, a demo key is used for local testing.

### 5. Run the application

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

---

## Usage Workflow

1. **Load IoT Data** — Use the slider to select a vehicle trip record, then click *Load IoT Event*.
2. **Run Decision Engine** — Click *Decision Engine* to compute toll, route, and overspeed status.
3. **Driver Response** — For overspeed cases, click *Confirm* or *Reject*; safe drivers are auto-approved.
4. **Secure Logging** — Click *Encrypt & Save Transaction* to encrypt and store (blockchain or rejected list).
5. **Mine Block** — Click *Mine Block* to finalize pending transactions into a new block.
6. **View Ledger** — Use the *Blockchain Ledger* tab to inspect blocks and decrypt transactions.
7. **Rejected Cases** — Use the *Rejected Guidance* tab to review and decrypt rejected cases.

---

## Generating New Dataset

To regenerate or customize the traffic dataset:

```bash
python generate_dataset.py
```

This creates `us_traffic_data.csv` with 500 records including:
- Plate, phone, email
- Entry/exit points (NYC & US highway locations)
- Entry/exit timestamps
- Speed (km/h) and speed limit (km/h)

---

## Dataset Schema

| Column | Description |
|--------|-------------|
| `plate` | Vehicle plate (e.g., NY-ABC1234) |
| `phone` | Driver phone (e.g., +1-212-555-1234) |
| `email` | Driver email |
| `entry_point` | Entry location |
| `exit_point` | Exit location |
| `entry_time` | ISO timestamp |
| `exit_time` | ISO timestamp |
| `speed_kmph` | Actual speed (km/h) |
| `speed_limit_kmph` | Speed limit (km/h) |

---

## License

MIT (or your preferred license)
