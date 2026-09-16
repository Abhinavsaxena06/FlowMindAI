import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getTrafficForecast,
  getTrafficExplanation,
} from "../services/api";


function buildPrediction(
  forecast
) {

  const approaches =
    forecast?.approaches ||
    {};

  const values =
    Object.values(
      approaches
    );


  if (!values.length) {

    return {
      prediction: {
        congestion_score: 0,
      },
    };
  }


  let totalVehicles = 0;
  let totalQueue = 0;
  let totalSpeed = 0;
  let speedCount = 0;


  values.forEach(
    (item) => {

      totalVehicles +=
        Number(
          item?.predicted_vehicles ||
          0
        );

      totalQueue +=
        Number(
          item?.predicted_queue ||
          0
        );

      const speed =
        Number(
          item?.predicted_avg_speed_kmh ||
          0
        );

      if (speed > 0) {

        totalSpeed += speed;
        speedCount += 1;
      }
    }
  );


  const averageSpeed =
    speedCount > 0
      ? totalSpeed /
        speedCount
      : 0;


  const congestionScore =
    Math.min(
      100,
      Math.round(
        Math.min(
          totalVehicles / 100,
          1
        ) * 45 +

        Math.min(
          totalQueue / 40,
          1
        ) * 35 +

        (
          averageSpeed > 0
            ? Math.max(
                0,
                1 -
                averageSpeed / 50
              )
            : 0
        ) * 20
      )
    );


  return {

    prediction: {
      congestion_score:
        congestionScore,

      predicted_vehicles:
        totalVehicles,

      predicted_queue:
        totalQueue,

      predicted_average_speed:
        averageSpeed,
    },

    forecast,
  };
}


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


  const refresh =
    useCallback(
      async () => {

        try {

          const [
            forecast,
            explanationResponse,
          ] = await Promise.all([
            getTrafficForecast(),
            getTrafficExplanation(),
          ]);


          const predictionData =
            buildPrediction(
              forecast
            );


          setPrediction({
            ...predictionData,

            explanation:
              explanationResponse?.explanation ||
              null,
          });


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
        2000
      );

    return () =>
      clearInterval(timer);

  }, [refresh]);


  return {
    prediction,
    loading,
    error,
    refresh,
  };
}