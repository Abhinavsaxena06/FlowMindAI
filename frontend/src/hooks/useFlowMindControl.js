import {
  useEffect,
  useState,
} from "react";

import {
  getTrafficState,
  getTrafficForecast,
  getTrafficRecommendation,
  getTrafficResult,
  startTraffic,
} from "../services/api";


export default function useFlowMindControl() {

  const [
    state,
    setState,
  ] = useState(null);


  const [
    forecast,
    setForecast,
  ] = useState(null);


  const [
    recommendation,
    setRecommendation,
  ] = useState(null);


  const [
    result,
    setResult,
  ] = useState(null);


  const [
    connected,
    setConnected,
  ] = useState(false);


  useEffect(() => {

    let mounted = true;
    startTraffic().catch(() => {});


    async function load() {

      try {

        const [
          trafficState,
          trafficForecast,
          trafficRecommendation,
          trafficResult,
        ] = await Promise.all([
          getTrafficState(),
          getTrafficForecast(),
          getTrafficRecommendation(),
          getTrafficResult(),
        ]);


        if (!mounted) {
          return;
        }


        setState(
          trafficState?.status === "waiting"
            ? null
            : trafficState
        );


        setForecast(
          trafficForecast?.status === "warming_up"
            ? null
            : trafficForecast
        );


        setRecommendation(
          trafficRecommendation?.status === "warming_up"
            ? null
            : trafficRecommendation
        );


        setResult(
          trafficResult?.status === "waiting"
            ? null
            : trafficResult
        );


        setConnected(true);

      } catch {

        if (mounted) {
          setConnected(false);
        }

      }
    }


    load();


    const timer =
      setInterval(
        load,
        1500
      );


    return () => {

      mounted = false;

      clearInterval(
        timer
      );

    };

  }, []);


  return {
    state,
    forecast,
    recommendation,
    result,
    connected,
  };
}