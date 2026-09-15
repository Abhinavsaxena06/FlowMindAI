const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, options.timeout || 8000);

  try {
    const response = await fetch(
      `${API_BASE}${path}`,
      {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
        },
        signal: controller.signal,
      }
    );

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status}`
      );
    }

    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

export async function getTrafficCurrent() {
  return request("/api/traffic/current");
}

export async function getTrafficHistory(limit = 30) {
  return request(
    `/api/traffic/history?limit=${limit}`
  );
}

export async function getPrediction() {
  return request("/api/prediction/");
}

export async function getHealth() {
  return request("/api/health");
}

export async function getSignals() {
  try {
    return await request("/api/signals/");
  } catch {
    return null;
  }
}

export async function getNetwork() {
  try {
    return await request("/api/network/");
  } catch {
    return null;
  }
}

export async function getSimulation() {
  try {
    return await request("/api/simulation/");
  } catch {
    return null;
  }
}

export { API_BASE };