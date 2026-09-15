import {
  Camera,
  Maximize2,
  Video,
} from "lucide-react";

export default function CameraView({
  source,
}) {
  return (
    <div className="camera-panel">

      <div className="camera-header">

        <div className="camera-title">
          <Camera size={17} />

          <span>
            JUNCTION A / CAMERA 01
          </span>
        </div>

        <div className="camera-live">
          <span className="status-dot live" />
          LIVE
        </div>

      </div>

      <div className="camera-screen">

        {source ? (
          <video
            src={source}
            autoPlay
            muted
            loop
            playsInline
          />
        ) : (
          <div className="camera-placeholder">

            <Video size={40} />

            <strong>
              Camera stream
            </strong>

            <span>
              Live perception feed
              will appear here
            </span>

          </div>
        )}

        <div className="camera-overlay">
          FLOWMIND AI VISION
        </div>

        <button className="camera-fullscreen">
          <Maximize2 size={17} />
        </button>

      </div>

    </div>
  );
}