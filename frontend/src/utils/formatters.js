export function number(value, digits = 0) {
  const parsed = Number(value);

  if (!Number.isFinite(parsed)) {
    return "—";
  }

  return parsed.toFixed(digits);
}

export function percentage(value, digits = 0) {
  const parsed = Number(value);

  if (!Number.isFinite(parsed)) {
    return "—";
  }

  return `${parsed.toFixed(digits)}%`;
}

export function speed(value) {
  const parsed = Number(value);

  if (!Number.isFinite(parsed)) {
    return "—";
  }

  return `${parsed.toFixed(1)} km/h`;
}

export function timeAgo(timestamp) {
  if (!timestamp) {
    return "No recent update";
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "Recently";
  }

  const seconds = Math.floor(
    (Date.now() - date.getTime()) / 1000
  );

  if (seconds < 10) {
    return "Just now";
  }

  if (seconds < 60) {
    return `${seconds}s ago`;
  }

  const minutes = Math.floor(seconds / 60);

  if (minutes < 60) {
    return `${minutes}m ago`;
  }

  return `${Math.floor(minutes / 60)}h ago`;
}