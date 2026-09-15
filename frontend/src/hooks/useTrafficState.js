import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getTrafficCurrent,
} from "../services/api";

import {
  createTrafficSocket,
} from "../services/websocket";

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

  const fetchState = useCallback(
    async () => {
      try {
        const data =
          await getTrafficCurrent();

        setTraffic(
          normalizeTrafficState(data)
        );

        setError(null);
      } catch (err) {
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

    let socket;
    let reconnectTimer;
    let pollingTimer;

    const startPolling = () => {
      pollingTimer = setInterval(
        fetchState,
        5000
      );
    };

    try {
      socket = createTrafficSocket({
        onOpen: () => {
          setConnected(true);
        },

        onMessage: (data) => {
          setTraffic(
            normalizeTrafficState(data)
          );

          setError(null);
          setConnected(true);
          setLoading(false);
        },

        onClose: () => {
          setConnected(false);

          reconnectTimer =
            setTimeout(() => {
              startPolling();
            }, 1000);
        },

        onError: () => {
          setConnected(false);
        },
      });
    } catch {
      startPolling();
    }

    return () => {
      if (socket) {
        socket.close();
      }

      clearTimeout(
        reconnectTimer
      );

      clearInterval(
        pollingTimer
      );
    };
  }, [fetchState]);

  return {
    traffic,
    loading,
    error,
    connected,
    refresh: fetchState,
  };
}