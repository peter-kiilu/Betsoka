# ⚽ BETSOKA — AI Football Match Outcome Prediction System

A production-grade full-stack application leveraging machine learning to predict football match outcomes. Built with **FastAPI** backend and **React** frontend, featuring real-time predictions and comprehensive analytics.

---

## ⚠️ Disclaimer

**This system is designed for research and educational purposes only.**

- The predictions are generated using synthetic data and statistical models
- **NOT intended for gambling or betting purposes**
- We assume **NO responsibility** for any financial decisions made based on these predictions
- All match data is algorithmically generated for demonstration purposes
- Use at your own risk

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**

```bash
pip install numpy pandas scikit-learn tensorflow joblib fastapi uvicorn pydantic
```

2. **Start the API server:**

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API documentation available at: **http://localhost:8000/docs**

### Frontend Setup

1. **Install Node dependencies:**

```bash
cd frontend
npm install
```

2. **Start the development server:**

```bash
npm run dev
```

Application available at: **http://localhost:5173**

---

## 🏗️ Architecture

```
BETSOKA/
├── api/                        # FastAPI REST API
│   ├── main.py                 # Application entry point & CORS configuration
│   └── routes.py               # API endpoints (/generate, /train, /predict, /status)
│
├── core/                       # Machine Learning Core
│   ├── config.py               # Model hyperparameters & feature definitions
│   ├── data_processing.py      # Data generation & preprocessing pipeline
│   └── services.py             # Model training, evaluation & inference
│
├── frontend/                   # React Application
│   ├── src/
│   │   ├── pages/              # Dashboard, Predictions, Analytics, About
│   │   ├── components/         # Reusable UI components
│   │   ├── context/            # Global state management
│   │   ├── data/               # Team data & fixtures
│   │   └── api.js              # API client (Axios)
│   └── public/
│       └── logos/              # Premier League team badges
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
└── README.md
```

---

## 🧠 Machine Learning Models

The system implements three distinct classification models for comparative analysis:

| Model                | Architecture      | Configuration                   | Use Case             |
| -------------------- | ----------------- | ------------------------------- | -------------------- |
| Logistic Regression  | Linear Classifier | Multinomial, L-BFGS solver      | Baseline performance |
| Random Forest        | Ensemble Learning | 150 estimators, max_depth=12    | Feature importance   |
| Neural Network (ANN) | Deep Learning     | 64→32→16 MLP with dropout (0.3) | Non-linear patterns  |

### Model Features

Each model is trained on 12 engineered features:

- Team strength metrics (home/away)
- Recent form indicators
- Goal-scoring statistics
- Shot accuracy
- Possession differential
- Home advantage factor
- Head-to-head historical performance
- Goal difference trends

---

## 📊 Features

### Dashboard

- Real-time match predictions for Premier League fixtures
- Interactive matchday navigation
- Team-specific analytics with official badges
- Click-through head-to-head history

### Predictions

- Custom match prediction with adjustable parameters
- Multi-model comparison
- Probability distribution visualization
- Confidence scoring

### Analytics

- Model performance metrics (accuracy, precision, recall, F1)
- Confusion matrices
- Feature importance analysis
- Interactive charts (Recharts)

### System Management

- Synthetic data generation (500-5000 matches)
- One-click model training
- Real-time status monitoring
- API health checks

---

## 🎯 Usage Workflow

1. **Initialize Data**: Generate synthetic match dataset via sidebar controls
2. **Train Models**: Execute training pipeline for all three models
3. **Make Predictions**: Navigate to Predictions page for custom match analysis
4. **Review Analytics**: Examine model performance and feature importance
5. **Explore Insights**: View detailed statistics and historical comparisons

---

## 🔧 Technical Stack

**Backend:**

- FastAPI (REST API framework)
- scikit-learn (ML models)
- TensorFlow/Keras (Neural networks)
- Pandas/NumPy (Data processing)
- Pydantic (Data validation)

**Frontend:**

- React 18
- Vite (Build tool)
- React Router (Navigation)
- Recharts (Data visualization)
- Axios (HTTP client)
- Lucide React (Icons)

**Styling:**

- Custom CSS (SofaScore-inspired dark theme)
- Responsive design (mobile-first)
- Glassmorphism effects

---

## 📝 API Endpoints

| Endpoint        | Method | Description                         |
| --------------- | ------ | ----------------------------------- |
| `/api/status`   | GET    | System health & model status        |
| `/api/features` | GET    | Feature definitions for UI forms    |
| `/api/generate` | POST   | Generate synthetic match data       |
| `/api/train`    | POST   | Train all models & return metrics   |
| `/api/predict`  | POST   | Predict match outcome with features |

---

## 🔒 Data & Privacy

- All match data is **synthetically generated** using probabilistic models
- No real match data or external APIs are used
- No user data is collected or stored
- All processing occurs locally

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 🙏 Acknowledgments

- Premier League team badges used for educational demonstration
- UI design inspired by SofaScore
- Built with modern web technologies and machine learning frameworks

---

**Remember:** This system is for educational and research purposes only. Do not use for gambling or betting activities.
