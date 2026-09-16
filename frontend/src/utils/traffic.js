const LANES = [
  "north",
  "east",
  "south",
  "west",
];


function number(
  value,
  fallback = 0
) {
  const parsed =
    Number(value);

  return Number.isFinite(parsed)
    ? parsed
    : fallback;
}


function getApproaches(
  raw
) {
  if (
    raw &&
    raw.approaches &&
    typeof raw.approaches === "object"
  ) {
    return raw.approaches;
  }

  return {};
}


export function normalizeTrafficState(
  raw = {}
) {

  const approaches =
    getApproaches(raw);

  const hasApproaches =
    Object.keys(
      approaches
    ).length > 0;


  let currentVehicles =
    number(
      raw.current_vehicles ??
      raw.total_vehicles ??
      raw.vehicle_count,
      0
    );


  let queueCount =
    number(
      raw.queue_count ??
      raw.queue_length,
      0
    );


  let waitingVehicles =
    number(
      raw.waiting_vehicles ??
      raw.waiting ??
      raw.queue_count ??
      raw.queue_length,
      0
    );


  let averageSpeed =
    number(
      raw.average_speed ??
      raw.avg_speed,
      0
    );


  let density =
    number(
      raw.density,
      0
    );


  const laneCounts = {
    north: 0,
    east: 0,
    south: 0,
    west: 0,
  };


  if (hasApproaches) {

    let totalSpeed =
      0;

    let totalDensity =
      0;

    let totalVehicles =
      0;

    let totalQueue =
      0;

    let totalStopped =
      0;


    LANES.forEach(
      (lane) => {

        const data =
          approaches[lane] ||
          {};

        const vehicles =
          number(
            data.vehicles ??
            data.vehicle_count,
            0
          );

        const queue =
          number(
            data.queue ??
            data.queue_length,
            0
          );

        const stopped =
          number(
            data.stopped,
            0
          );

        const speed =
          number(
            data.avg_speed_kmh ??
            data.average_speed,
            0
          );

        const laneDensity =
          number(
            data.density,
            0
          );


        laneCounts[lane] =
          vehicles;

        totalVehicles +=
          vehicles;

        totalQueue +=
          queue;

        totalStopped +=
          stopped;

        totalSpeed +=
          vehicles * speed;

        totalDensity +=
          laneDensity;
      }
    );


    currentVehicles =
      totalVehicles;

    queueCount =
      totalQueue;

    waitingVehicles =
      totalQueue;

    averageSpeed =
      totalVehicles > 0
        ? totalSpeed /
          totalVehicles
        : 0;

    density =
      totalDensity / 4;
  }


  let congestionScore =
    number(
      raw.congestion_score ??
      raw.congestion,
      0
    );


  // Backend state uses density 0..1.
  // Dashboard uses congestion 0..100.
  if (
    congestionScore <= 1 &&
    congestionScore > 0
  ) {
    congestionScore *= 100;
  }


  if (
    congestionScore === 0 &&
    (
      currentVehicles > 0 ||
      queueCount > 0
    )
  ) {

    const densityScore =
      Math.min(
        density,
        1
      ) * 45;

    const queueScore =
      Math.min(
        queueCount / 20,
        1
      ) * 35;

    const waitingScore =
      Math.min(
        waitingVehicles / 20,
        1
      ) * 20;

    congestionScore =
      Math.min(
        100,
        Math.round(
          densityScore +
          queueScore +
          waitingScore
        )
      );
  }


  let trafficStatus =
    raw.traffic_status ||
    raw.status ||
    raw.congestion_level;


  if (!trafficStatus) {

    if (
      congestionScore >= 80
    ) {
      trafficStatus =
        "CRITICAL";

    } else if (
      congestionScore >= 60
    ) {
      trafficStatus =
        "HIGH";

    } else if (
      congestionScore >= 35
    ) {
      trafficStatus =
        "MODERATE";

    } else {
      trafficStatus =
        "NORMAL";
    }
  }


  return {

    currentVehicles,

    totalVehicles:
      currentVehicles,

    totalSpawned:
      number(
        raw.total_spawned,
        0
      ),

    passedVehicles:
      number(
        raw.passed_vehicles ??
        raw.total_passed ??
        raw.passed,
        0
      ),

    waitingVehicles,

    queueCount,

    averageSpeed,

    density,

    congestionScore,

    congestionLevel:
      trafficStatus,

    trafficStatus,

    signalState:
      raw.signal_state ||
      raw.signal?.current_phase ||
      "UNKNOWN",

    signalRemainingSeconds:
      number(
        raw.signal?.remaining_seconds,
        0
      ),

    activeDirection:
      raw.active_direction ||
      raw.signal?.active_direction ||
      "UNKNOWN",

    laneCounts,

    timestamp:
      raw.timestamp ||
      new Date().toISOString(),

    approaches,

    raw,
  };
}


export function statusTone(
  status = ""
) {

  const value =
    String(status)
      .toLowerCase();

  if (
    value.includes("critical") ||
    value.includes("severe")
  ) {
    return "critical";
  }

  if (
    value.includes("high") ||
    value.includes("heavy")
  ) {
    return "high";
  }

  if (
    value.includes("moderate") ||
    value.includes("medium")
  ) {
    return "moderate";
  }

  return "normal";
}


export function congestionTone(
  score
) {

  const value =
    Number(score);

  if (value >= 80) {
    return "critical";
  }

  if (value >= 60) {
    return "high";
  }

  if (value >= 35) {
    return "moderate";
  }

  return "normal";
}