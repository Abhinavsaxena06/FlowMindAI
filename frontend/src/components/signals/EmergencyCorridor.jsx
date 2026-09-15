import {
  Ambulance,
  ShieldCheck,
  Siren,
} from "lucide-react";

export default function EmergencyCorridor() {
  return (
    <div className="emergency-card">

      <div className="emergency-header">

        <div className="emergency-title">
          <Siren size={19} />

          <div>
            <div className="eyebrow">
              EMERGENCY PRIORITY
            </div>

            <h2>
              Green corridor
            </h2>
          </div>
        </div>

        <span className="badge danger">
          STANDBY
        </span>

      </div>

      <div className="ambulance-info">

        <Ambulance size={27} />

        <div>
          <strong>
            Authorized emergency route
          </strong>

          <span>
            Junction A → B → C → Hospital
          </span>
        </div>

      </div>

      <div className="safety-checks">

        <div>
          <ShieldCheck size={15} />
          Conflict checks
        </div>

        <div>
          <ShieldCheck size={15} />
          Yellow clearance
        </div>

        <div>
          <ShieldCheck size={15} />
          Manual override
        </div>

      </div>

      <button className="danger-button">
        Activate emergency workflow
      </button>

    </div>
  );
}