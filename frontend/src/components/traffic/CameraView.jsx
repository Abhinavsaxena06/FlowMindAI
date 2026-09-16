import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  Camera,
  Maximize2,
  Video,
} from "lucide-react";

export default function CameraView({
  source,
}) {
  const screenRef = useRef(null);
  const [frameUrl, setFrameUrl] = useState(source);
  const [fullscreen, setFullscreen] =
    useState(false);

  useEffect(() => {
    if (!source) {
      return;
    }

    let active = true;

    const updateFrame = () => {
      if (!active) {
        return;
      }

      setFrameUrl(
        `${source}${
          source.includes("?")
            ? "&"
            : "?"
        }t=${Date.now()}`
      );
    };

    updateFrame();

    const timer = setInterval(
      updateFrame,
      1000
    );

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [source]);

  const handleFullscreen = async () => {
    if (!screenRef.current) {
      return;
    }

    try {
      if (
        !document.fullscreenElement
      ) {
        await screenRef.current.requestFullscreen();
        setFullscreen(true);
      } else {
        await document.exitFullscreen();
        setFullscreen(false);
      }
    } catch (error) {
      console.error(
        "Fullscreen failed:",
        error
      );
    }
  };

  useEffect(() => {
    const handleChange = () => {
      setFullscreen(
        Boolean(
          document.fullscreenElement
        )
      );
    };

    document.addEventListener(
      "fullscreenchange",
      handleChange
    );

    return () => {
      document.removeEventListener(
        "fullscreenchange",
        handleChange
      );
    };
  }, []);

  return (
    <div className="camera-panel">
      <div className="camera-header">
        <div className="camera-title">
          <Camera size={17} />

          <div>
            <strong>
              Junction A
            </strong>

            <span>
              Camera 01
            </span>
          </div>
        </div>

        <div className="camera-live">
          <span className="status-dot live" />
          LIVE
        </div>
      </div>

      <div
        className={`camera-screen ${
          fullscreen
            ? "camera-fullscreen-mode"
            : ""
        }`}
        ref={screenRef}
      >
        {frameUrl ? (
          <img
            src={frameUrl}
            alt="Live traffic camera feed"
            className="camera-feed"
          />
        ) : (
          <div className="camera-placeholder">
            <Video size={36} />

            <strong>
              Camera stream
            </strong>

            <span>
              Live perception feed will
              appear here
            </span>
          </div>
        )}

        <div className="camera-overlay">
          <span>FLOWMIND</span>
          <span>AI VISION</span>
        </div>

        <button
          className="camera-fullscreen"
          onClick={handleFullscreen}
          type="button"
          aria-label={
            fullscreen
              ? "Exit fullscreen"
              : "Open fullscreen"
          }
        >
          <Maximize2 size={17} />
        </button>
      </div>
    </div>
  );
}