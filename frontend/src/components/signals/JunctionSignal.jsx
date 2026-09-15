import SignalLight from "./SignalLight";

export default function JunctionSignal({
  direction,
  state,
  seconds,
}) {
  return (
    <div className="junction-signal">

      <div>
        <span className="eyebrow">
          APPROACH
        </span>

        <h3>
          {direction}
        </h3>
      </div>

      <SignalLight
        state={state}
      />

      <div className="signal-countdown">
        <strong>
          {seconds}
        </strong>

        <span>
          seconds
        </span>
      </div>

    </div>
  );
}