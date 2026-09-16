import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getTrafficState,
} from "../services/api";

import {
  normalizeTrafficState,
} from "../utils/traffic";


export default function useTrafficState() {

  const [
    traffic,
    setTraffic,
  ] = useState(null);


  const [
    loading,
    setLoading,
  ] = useState(true);


  const [
    error,
    setError,
  ] = useState(null);


  const [
    connected,
    setConnected,
  ] = useState(false);


  const fetchState =
    useCallback(
      async () => {

        try {

          const data =
            await getTrafficState();

          if (
            data?.status ===
            "waiting"
          ) {
            return;
          }

          setTraffic(
            normalizeTrafficState(
              data
            )
          );

          setConnected(true);
          setError(null);

        } catch (err) {

          setConnected(false);

          setError(
            err.message ||
            "Unable to load traffic data"
          );

        } finally {

          setLoading(false);
        }
      },
      []
    );


  useEffect(() => {

    fetchState();

    const timer =
      setInterval(
        fetchState,
        1000
      );

    return () =>
      clearInterval(timer);

  }, [fetchState]);


  return {
    traffic,
    loading,
    error,
    connected,
    refresh: fetchState,
  };
}