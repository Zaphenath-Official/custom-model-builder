
# 🚀 Autonomous Multi-Model Tournament AutoML Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![Backend](https://img.shields.io/badge/Backend-Flask%20%2F%20ThreadPool-orange?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-Supabase%20%2F%20PostgreSQL-green?style=for-the-badge&logo=supabase)](https://supabase.com)

An autonomous, distributed machine learning engine designed to handle end-to-end model creation directly through an intuitive user dashboard. The system ingests arbitrary user-uploaded tabular datasets, profiles targets and features dynamically, and executes a multi-model validation tournament using state-of-the-art gradient boosters and tree ensembles. Winning artifacts are serialized, securely committed to remote object storage, and spun up instantly with an isolated public inference API gateway endpoint.

---

## 📺 Application Architecture Overview

```text
 ┌──────────────────────┐      CSV Stream      ┌─────────────────────────┐
 │  Vercel React App    │ ───────────────────> │  Flask Backend Engine   │
 │                      │                      │ (ThreadPool Execution)  │
 │  ┌────────────────┐  │ <─────────────────── │                         │
 │  │ Live Jobs Sync │  │   Polling Status     └─────────────────────────┘
 │  └────────────────┘  │                                │         │
 └──────────────────────┘                    Metadata    │         │ Model Artifacts
            ▲                                 & Logs     ▼         ▼
            │                                      ┌──────────┐┌───────────────┐
            └───────────────────────────────────── │ Supabase ││ Object Cloud  │
                       Session/JWT                 │ Database ││ Storage       │
                                                   └──────────┘└───────────────┘

```

---

## 🚀 Core Engine Capabilities

### 1. Multi-Model Pipeline Tournaments

The pipeline bypasses structural boilerplate by dynamically executing competitive feature matching across the highest-performing machine learning frameworks simultaneously:

* **Gradient Boosters:** `LightGBM` (Light Gradient Boosting Machine) & `XGBoost` (eXtreme Gradient Boosting).
* **High-Cardinality Categorical Engines:** `CatBoost` (Categorical Boosting).
* **Bagging Baseline Ensembles:** `RandomForest` (Regressor / Classifier variants).

### 2. Multi-Threaded Asynchronous Execution Engine

To prevent blocking incoming I/O operations and bypass standard free-tier timeout thresholds, the core engine leverages an isolated `ThreadPoolExecutor` cluster. When a user submits a training payload:

1. The incoming multi-part file stream is stored as an in-memory binary vector.
2. An asynchronous worker thread is checked out to execute profiling, processing, and optimization passes cleanly outside the main HTTP thread framework.
3. The client receives an immediate `202 Accepted` response alongside a unique `job_id`, unlocking real-time interface step-tracking polling.

### 3. Integrated Microsecond Termination Vectors

High-dimensional datasets or extensive iteration hyperparameter trees can block engine resources if misconfigured. The backend handles this gracefully using a memory-isolated cancellation matrix (`cancelled_jobs`). The tournament evaluation engine continuously verifies cancellation tracking metrics at key operational boundaries. If a user triggers a cancellation from the frontend modal, the loop terminates execution immediately, flushes working memory caches, cleans up isolated local artifacts, and updates downstream database states cleanly.

---

## 📦 API Payload Reference

### Model Ingestion & Training Pipeline

To register a job tracking row inside the database layer and dispatch an async training thread loop, issue a **POST** request using a `multipart/form-data` encoding payload structure:

* **Endpoint:** `/targets-features-train`
* **Form Parameters:**
* `file`: `[Binary Blob / .csv]`
* `targets`: `price`
* `features`: `year`
* `features`: `odometer`
* `features`: `condition`
* `model_name`: `Vehicle_Valuation_Production_v1`
* `user_id`: `[Supabase UUID User Context Key]`



#### Response Receipt (`202 Accepted`)

```json
{
  "status": "pending",
  "job_id": 418,
  "message": "Model training pipeline queued successfully!"
}

```

### Production Live Inference API Gateway

Once the tournament establishes a winning architecture, the backend produces an active deployment record containing an immutable authentication signature token. Issue a secure tokenized call to perform instant predictions:

* **Endpoint:** `/v1/predict`
* **Headers:** `Authorization: Bearer sk_engine_4a6f7b...`

#### Request Input Body Matrix (`application/json`)

```json
{
  "year": 2018,
  "odometer": 45000,
  "condition": "excellent"
}

```

#### Response Payload Matrix (`200 OK`)

```json
{
  "status": "success",
  "model_name": "Vehicle_Valuation_Production_v1",
  "prediction": 26450.82
}

```

---

## 🗂️ Project Directory Topology

```text
├── adapters/
│   └── storage.py                 # Supabase Storage Adapter pipeline abstraction
├── services/
│   └── supabase_service.py        # Database communication wrapper and API key validator
├── models/                        # Thread-isolated local training buffers (auto-cleaned)
├── index.py                       # Main Flask Application Engine & API Router Gateway
├── App.jsx                        # React Frontend Core with Multi-Step Wizard and Inference Forms
├── App.css                        # Modern CSS Variables & Responsive Workspace Layout Configurations
├── package.json                   # Client-side node package environment dependencies
└── .env                           # Protected Production Environment Tokens

```

---

## 🛠️ Step-by-Step Installation & Local Setup

### 1. Backend Service Configuration

Clone your repository and navigate to your backend runtime path:

```bash
# Setup clean Python Virtual Environment wrapper
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install exact requirements vectors
pip install flask flask-cors pandas numpy scikit-learn lightgbm xgboost catboost python-dotenv joblib supabase

```

Create a production-ready `.env` file within the root execution layer:

```env
SUPABASE_URL=[https://your-project-id.supabase.co](https://your-project-id.supabase.co)
SUPABASE_KEY=your-supabase-service-role-key
SMTP_EMAIL=your-verification-system@gmail.com
SMTP_PASSWORD=your-secure-app-password

```

Run the local cluster server link:

```bash
python index.py

```

### 2. Frontend Workspace Client Setup

Open a separate shell and enter the client dashboard folder directory:

```bash
# Install node packages
npm install

# Run development mode compiler
npm run dev

```

---

## 🛡️ Production Verification Checks

* **Isolated Column Transformation:** Categorical elements are automatically extracted, injected with constant indicators to safely capture missing string patterns, and fed to safe ordinal encoders. Continuous real values are scaled using global z-score normalization vectors (`StandardScaler`).
* **Cross-Origin Configuration (CORS):** The Flask infrastructure is bundled with explicit wildcard acceptance matrices to prevent security handshake execution blocks when talking directly to cloud-deployed edge layers like Vercel.

```

```
