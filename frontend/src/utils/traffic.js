export function normalizeTrafficState(raw = {}) {
  const lanes =
    raw.lane_counts ||
    raw.lanes ||
    {};

  const signal =
    raw.signal ||
    raw.signal_state ||
    {};

  const totals = raw.overall || {};

  const currentVehicles = Number(
    raw.current_vehicles ??
      raw.total_vehicles ??
      raw.vehicle_count ??
      totals.total_vehicles ??
      0
  );

  return {
    currentVehicles,

    totalVehicles: currentVehicles,

    totalSpawned:
      Number(
        raw.total_spawned ??
        raw.spawned_vehicles ??
        0
      ),

    passedVehicles:
      Number(
        raw.passed_vehicles ??
        raw.total_passed ??
        raw.passed ??
        0
      ),

    waitingVehicles:
      Number(
        raw.waiting_vehicles ??
        raw.waiting ??
        raw.queue_count ??
        raw.queue_length ??
        0
      ),

    queueCount:
      Number(
        raw.queue_count ??
        raw.queue_length ??
        raw.total_queue ??
        raw.waiting_vehicles ??
        0
      ),

    averageSpeed:
      Number(
        raw.average_speed ??
        raw.avg_speed ??
        totals.average_speed ??
        0
      ),

    density:
      Number(
        raw.density ??
        raw.overall_density ??
        totals.overall_density ??
        0
      ),

    congestionScore:
      Number(
        raw.congestion_score ??
        raw.congestion ??
        totals.congestion_score ??
        0
      ),

    congestionLevel:
      raw.congestion_level ||
      raw.traffic_status ||
      raw.status ||
      "UNKNOWN",

    trafficStatus:
      raw.traffic_status ||
      raw.status ||
      raw.congestion_level ||
      "UNKNOWN",

    signalState:
      signal.current_phase ||
      signal.phase_name ||
      signal.state ||
      "UNKNOWN",

    signalRemainingSeconds:
      Number(
        signal.remaining_seconds ??
        signal.remaining ??
        0
      ),

    activeDirection:
      signal.active_direction ||
      signal.direction ||
      "UNKNOWN",

    laneCounts: {
      north: Number(
        lanes.north ??
          lanes.north?.vehicle_count ??
          0
      ),

      east: Number(
        lanes.east ??
          lanes.east?.vehicle_count ??
          0
      ),

      south: Number(
        lanes.south ??
          lanes.south?.vehicle_count ??
          0
      ),

      west: Number(
        lanes.west ??
          lanes.west?.vehicle_count ??
          0
      ),
    },

    timestamp:
      raw.timestamp ||
      raw.video_time_seconds ||
      new Date().toISOString(),

    raw,
  };
}

export function statusTone(status = "") {
  const value = status.toLowerCase();

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

export function congestionTone(score) {
  const value = Number(score);

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