export function normalizeTrafficState(raw = {}) {
  const lanes =
    raw.lane_counts ||
    raw.lanes ||
    {};

  return {
    totalVehicles:
      Number(
        raw.total_vehicles ??
        raw.vehicle_count ??
        0
      ),

    queueCount:
      Number(
        raw.queue_count ??
        raw.queue_length ??
        0
      ),

    averageSpeed:
      Number(
        raw.average_speed ??
        raw.avg_speed ??
        0
      ),

    density:
      Number(
        raw.density ??
        0
      ),

    congestionScore:
      Number(
        raw.congestion_score ??
        raw.congestion ??
        0
      ),

    trafficStatus:
      raw.traffic_status ||
      raw.status ||
      "UNKNOWN",

    laneCounts: {
      north: Number(
        lanes.north ?? 0
      ),

      east: Number(
        lanes.east ?? 0
      ),

      south: Number(
        lanes.south ?? 0
      ),

      west: Number(
        lanes.west ?? 0
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