export default function SignalLight({
  state = "RED",
}) {
  const active =
    state.toLowerCase();

  return (
    <div className="traffic-light">

      <span
        className={`light red ${
          active === "red"
            ? "active"
            : ""
        }`}
      />

      <span
        className={`light yellow ${
          active === "yellow"
            ? "active"
            : ""
        }`}
      />

      <span
        className={`light green ${
          active === "green"
            ? "active"
            : ""
        }`}
      />

    </div>
  );
}