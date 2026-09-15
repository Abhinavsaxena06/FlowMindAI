import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getPrediction,
} from "../services/api";

export default function usePrediction() {
  const [
    prediction,
    setPrediction,
  ] = useState(null);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState(null);

  const refresh = useCallback(
    async () => {
      try {
        const data =
          await getPrediction();

        setPrediction(data);
        setError(null);
      } catch (err) {
        setError(
          err.message ||
          "Prediction unavailable"
        );
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    refresh();

    const timer =
      setInterval(
        refresh,
        15000
      );

    return () => {
      clearInterval(timer);
    };
  }, [refresh]);

  return {
    prediction,
    loading,
    error,
    refresh,
  };
}