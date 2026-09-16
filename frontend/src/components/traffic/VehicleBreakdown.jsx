import {
  BusFront,
  CarFront,
  Container,
  Bike,
} from "lucide-react";

const types = [
  {
    name: "Cars",
    key: "cars",
    icon: CarFront,
  },
  {
    name: "Motorcycles",
    key: "motorcycles",
    icon: Bike,
  },
  {
    name: "Buses",
    key: "buses",
    icon: BusFront,
  },
  {
    name: "Trucks",
    key: "trucks",
    icon: Container,
  },
];

export default function VehicleBreakdown({
  data = {},
}) {
  const values = types.map(
    (item) => ({
      ...item,
      value: Math.max(
        0,
        Number(
          data[item.key] ?? 0
        )
      ),
    })
  );

  const total =
    values.reduce(
      (sum, item) =>
        sum + item.value,
      0
    );

  return (
    <section className="panel vehicle-panel">
      <div className="panel-header">
        <div>
          <div className="eyebrow">
            PERCEPTION
          </div>

          <h2>Vehicle mix</h2>

          <p>
            Detected vehicle categories in the
            current traffic feed.
          </p>
        </div>

        <div className="panel-total">
          <strong>{total}</strong>
          <span>Total</span>
        </div>
      </div>

      <div className="vehicle-list">
        {values.map((item) => {
          const Icon = item.icon;

          const percentage =
            total > 0
              ? (item.value / total) * 100
              : 0;

          return (
            <div
              className="vehicle-row"
              key={item.name}
            >
              <div className="vehicle-name">
                <div className="vehicle-icon">
                  <Icon size={16} />
                </div>

                <span>
                  {item.name}
                </span>
              </div>

              <div className="vehicle-value">
                <div className="vehicle-progress">
                  <span
                    style={{
                      width: `${percentage}%`,
                    }}
                  />
                </div>

                <strong>
                  {item.value}
                </strong>

                <small>
                  {Math.round(
                    percentage
                  )}
                  %
                </small>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}