import { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
import * as api from '../api';

const AppContext = createContext();

export function AppProvider({ children }) {
  const initialized = useRef(false);
  const [status, setStatus] = useState({ data_loaded: false, models_trained: false, data_rows: 0 });
  const [trainingResults, setTrainingResults] = useState(null);
  const [loading, setLoading] = useState({ generate: false, train: false, predict: false });
  const [toast, setToast] = useState(null);

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  }, []);

  const generateData = useCallback(async (n) => {
    setLoading(l => ({ ...l, generate: true }));
    try {
      const { data } = await api.generateData(n);
      setStatus({ data_loaded: true, models_trained: false, data_rows: data.rows });
      setTrainingResults(null);
      showToast(`Generated ${data.rows.toLocaleString()} matches`);
      return data;
    } catch (e) {
      showToast(e.response?.data?.detail || 'Failed to generate data', 'error');
    } finally {
      setLoading(l => ({ ...l, generate: false }));
    }
  }, [showToast]);

  const trainModels = useCallback(async () => {
    setLoading(l => ({ ...l, train: true }));
    try {
      const { data } = await api.trainModels();
      setTrainingResults(data);
      setStatus(s => ({ ...s, models_trained: true }));
      showToast('All models trained successfully');
      return data;
    } catch (e) {
      showToast(e.response?.data?.detail || 'Failed to train models', 'error');
    } finally {
      setLoading(l => ({ ...l, train: false }));
    }
  }, [showToast]);

  const predict = useCallback(async (payload) => {
    setLoading(l => ({ ...l, predict: true }));
    try {
      const { data } = await api.predictOutcome(payload);
      return data;
    } catch (e) {
      showToast(e.response?.data?.detail || 'Prediction failed', 'error');
    } finally {
      setLoading(l => ({ ...l, predict: false }));
    }
  }, [showToast]);

  // Auto-initialize: generate data + train models on first visit
  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    const autoInit = async () => {
      setLoading(l => ({ ...l, generate: true }));
      try {
        const { data: genData } = await api.generateData(2000);
        setStatus({ data_loaded: true, models_trained: false, data_rows: genData.rows });

        setLoading(l => ({ ...l, generate: false, train: true }));
        const { data: trainData } = await api.trainModels();
        setTrainingResults(trainData);
        setStatus(s => ({ ...s, models_trained: true }));
        showToast('System ready — data generated & models trained');
      } catch {
        // Backend may not be up yet — user can init manually via sidebar
      } finally {
        setLoading({ generate: false, train: false, predict: false });
      }
    };
    autoInit();
  }, [showToast]);

  return (
    <AppContext.Provider value={{ status, trainingResults, loading, toast, generateData, trainModels, predict, showToast }}>
      {children}
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}
    </AppContext.Provider>
  );
}

export const useApp = () => useContext(AppContext);
