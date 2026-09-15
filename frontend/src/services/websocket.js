const HTTP_API =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const WS_API = HTTP_API
  .replace("https://", "wss://")
  .replace("http://", "ws://");

export function createTrafficSocket({
  onMessage,
  onOpen,
  onClose,
  onError,
}) {
  const socket = new WebSocket(
    `${WS_API}/ws/traffic`
  );

  socket.onopen = () => {
    if (onOpen) {
      onOpen();
    }
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (onMessage) {
        onMessage(data);
      }
    } catch {
      console.warn(
        "Invalid WebSocket message"
      );
    }
  };

  socket.onerror = (error) => {
    if (onError) {
      onError(error);
    }
  };

  socket.onclose = () => {
    if (onClose) {
      onClose();
    }
  };

  return socket;
}