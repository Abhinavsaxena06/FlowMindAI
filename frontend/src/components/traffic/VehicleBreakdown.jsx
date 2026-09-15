const types = [
  {
    name: "Cars",
    value: 0,
  },
  {
    name: "Motorcycles",
    value: 0,
  },
  {
    name: "Buses",
    value: 0,
  },
  {
    name: "Trucks",
    value: 0,
  },
];

export default function VehicleBreakdown({
  data = {},
}) {
  const values =
    types.map(
      (item) => ({
        ...item,
        value:
          Number(
            data[
              item.name
                .toLowerCase()
            ] ??
            item.value
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
    <div className="panel">

      <div className="panel-header">

        <div>
          <div className="eyebrow">
            PERCEPTION
          </div>

          <h2>
            Vehicle mix
          </h2>
        </div>

        <strong>
          {total}
        </strong>

      </div>

      <div className="vehicle-list">

        {values.map(
          (item) => (
            <div
              className="vehicle-row"
              key={item.name}
            >

              <span>
                {item.name}
              </span>

              <div className="vehicle-value">
                <div>
                  <span
                    style={{
                      width: `${
                        total
                          ? (
                              item.value /
                              total
                            ) *
                            100
                          : 0
                      }%`,
                    }}
                  />
                </div>

                <strong>
                  {item.value}
                </strong>
              </div>

            </div>
          )
        )}

      </div>

    </div>
  );
}