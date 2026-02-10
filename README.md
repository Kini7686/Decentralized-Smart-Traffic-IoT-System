# 🚦 Decentralized Smart Traffic IoT System with Blockchain & AI

A secure, AI-powered Smart Traffic Management System that integrates **IoT vehicle data, decision intelligence, AES-256 encryption, and blockchain-based logging** using Streamlit.

This system simulates real-time traffic monitoring, driver behavior analysis, and secure enforcement using decentralized technology.

---

## 📌 Features

- ✅ Real IoT Traffic Dataset Processing  
- ✅ AI-Based Decision Engine (Toll + Route + Overspeed Detection)  
- ✅ Driver Confirmation & Rejection Workflow  
- ✅ AES-256-GCM Encrypted Transactions  
- ✅ Custom Blockchain Ledger  
- ✅ Rejected Guidance Monitoring  
- ✅ Police/Admin Decryption Access  
- ✅ Interactive Streamlit Dashboard  

---

## 🧠 System Architecture

IoT Dataset → AI Decision Engine → Driver Response
↓
AES-256 Encryption → Blockchain Storage
↓
Police / Admin Decryption

yaml
Copy code

---

## 📂 Project Structure

smart-traffic-system/
│
├── app.py # Streamlit Frontend
├── backend.py # Blockchain, Encryption, AI Logic
├── us_traffic_data.csv # Dataset
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🛠️ Technologies Used

| Component       | Technology |
|-----------------|------------|
| Frontend        | Streamlit |
| Backend         | Python |
| Encryption      | AES-256-GCM |
| Blockchain      | Custom Python Blockchain |
| Data Processing | Pandas |
| Dataset         | CSV |

---

## 📊 Functional Modules

### 1️⃣ IoT Data Loader
- Loads real traffic data from CSV
- Converts rows into system events

### 2️⃣ Decision Engine
- Calculates dynamic toll
- Suggests optimal route
- Detects overspeed

### 3️⃣ Driver Validation
- Confirm / Reject system guidance
- Auto-approve safe drivers

### 4️⃣ Secure Encryption
- Uses AES-256-GCM
- Encrypts full payload before storage

### 5️⃣ Blockchain Ledger
- Stores confirmed transactions
- Supports block mining
- Immutable record keeping

### 6️⃣ Rejected Guidance System
- Stores rejected cases separately
- Accessible for authorities
- Supports decryption

---

## 🔐 Security Model

### Encryption
- AES-256-GCM symmetric encryption
- Fixed police key via environment variable

### Blockchain
- SHA-256 hashing
- Linked block structure
- Tamper-resistant ledger

### Privacy
- All sensitive data encrypted
- Only authorized users can decrypt

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/smart-traffic-system.git
cd smart-traffic-system