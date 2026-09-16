import {
  useCallback,
  useEffect,
  useState,
} from "react";

const defaultState = {
  requestPending: false,
  pedestriansWaiting: 2,
  pedestriansCrossing: 0,
  signalState: "WAIT",
  countdown: 0,
  crossingActive: false,
  safetyStatus: "SAFE",
  vehicleSignal: "RED",
};

export default function usePedestrianSafety(vehicleSignal = "RED") {
  const [state, setState] = useState(defaultState);

  useEffect(() => {
    const normalized = (vehicleSignal || "RED").toUpperCase();

    setState((previous) => ({
      ...previous,
      vehicleSignal: normalized,
    }));
  }, [vehicleSignal]);

  const requestCrossing = useCallback(() => {
    const normalized = (vehicleSignal || "RED").toUpperCase();
    const safeToStart = normalized !== "GREEN" && normalized !== "YELLOW";

    setState((previous) => {
      const nextState = {
        ...previous,
        requestPending: true,
        pedestriansWaiting: Math.max(previous.pedestriansWaiting, 1),
        vehicleSignal: normalized,
      };

      if (!safeToStart) {
        return {
          ...nextState,
          signalState: "STOP",
          safetyStatus: "BLOCKED",
          countdown: 0,
          crossingActive: false,
        };
      }

      return {
        ...nextState,
        signalState: "WAIT",
        safetyStatus: "SAFE",
        countdown: 0,
        crossingActive: false,
      };
    });
  }, [vehicleSignal]);

  useEffect(() => {
    if (!state.requestPending || state.crossingActive) {
      return undefined;
    }

    const timer = setTimeout(() => {
      setState((previous) => {
        if (!previous.requestPending || previous.crossingActive) {
          return previous;
        }

        const normalized = (vehicleSignal || "RED").toUpperCase();
        const isSafe = normalized !== "GREEN" && normalized !== "YELLOW";

        if (!isSafe) {
          return {
            ...previous,
            requestPending: false,
            signalState: "STOP",
            safetyStatus: "BLOCKED",
            countdown: 0,
            crossingActive: false,
          };
        }

        return {
          ...previous,
          requestPending: false,
          pedestriansWaiting: Math.max(previous.pedestriansWaiting - 1, 0),
          pedestriansCrossing: 1,
          crossingActive: true,
          signalState: "WALK",
          safetyStatus: "CLEAR",
          countdown: 12,
        };
      });
    }, 1200);

    return () => clearTimeout(timer);
  }, [state.requestPending, state.crossingActive, vehicleSignal]);

  useEffect(() => {
    if (!state.crossingActive) {
      return undefined;
    }

    const timer = setInterval(() => {
      setState((previous) => {
        if (!previous.crossingActive) {
          return previous;
        }

        if (previous.countdown <= 1) {
          return {
            ...previous,
            crossingActive: false,
            pedestriansCrossing: 0,
            signalState: "STOP",
            safetyStatus: "SAFE",
            countdown: 0,
            vehicleSignal: "GREEN",
          };
        }

        return {
          ...previous,
          countdown: previous.countdown - 1,
          signalState:
            previous.countdown <= 3 ? "COUNTDOWN" : "WALK",
        };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [state.crossingActive]);

  const resetCrossing = useCallback(() => {
    setState((previous) => ({
      ...previous,
      requestPending: false,
      pedestriansWaiting: 0,
      pedestriansCrossing: 0,
      signalState: "STOP",
      countdown: 0,
      crossingActive: false,
      safetyStatus: "SAFE",
    }));
  }, []);

  return {
    ...state,
    requestCrossing,
    resetCrossing,
  };
}
