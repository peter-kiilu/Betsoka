# ⚽ BETSOKA — AI Football Match Outcome Prediction

A full-stack academic demo system: **FastAPI** backend with ML models + **React** frontend inspired by SofaScore.

> **University class assignment** — no real-world data, no APIs, fully self-contained.

---

## Quick Start

### 1. Install Backend Dependencies

```bash
pip install numpy pandas scikit-learn tensorflow joblib fastapi uvicorn pydantic
```

### 2. Start the Backend (from project root)

```bash
cd d:\Betsoka
python -m uvicorn api.main:app --reload --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Start the Frontend (in a second terminal)

```bash
cd d:\Betsoka\frontend
npm run dev
```

Opens at: [http://localhost:5173](http://localhost:5173)

---

## 🏗 Project Structure

```
├── api/                     # FastAPI REST backend
│   ├── main.py              # App entry + CORS
│   └── routes.py            # /generate, /train, /predict, /status, /features
│
├── core/                    # ML business logic
│   ├── config.py            # Feature schemas, model params, theme
│   ├── data_processing.py   # Synthetic data gen & preprocessing
│   └── services.py          # Training, evaluation, prediction
│
├── frontend/                # React / Vite UI
│   └── src/
│       ├── pages/           # Dashboard, Predictions, Analytics, About
│       ├── components/      # Sidebar
│       ├── context/         # Global state (AppContext)
│       └── api.js           # Axios client
│
├── requirements.txt
├── .env
└── README.md
```

## 🧠 Models

| Model                | Type          | Description               |
| -------------------- | ------------- | ------------------------- |
| Logistic Regression  | Linear        | Multinomial baseline      |
| Random Forest        | Ensemble      | 150 trees, max_depth=12   |
| Neural Network (ANN) | Deep Learning | 64→32→16 MLP with dropout |

## 🎓 Demo Flow

1. Click **Generate Data** in the sidebar
2. Click **Train Models**
3. Go to **Predictions** to predict custom matches
4. Explore **Analytics** for charts & confusion matrices
5. Visit **About** for academic context

---

_Built for educational purposes only. All data is synthetic._
