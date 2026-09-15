export default function PredictionTimeline({
  current = 0,
  thirty = 0,
  sixty = 0,
}) {
  const items = [
    {
      label: "NOW",
      value: current,
    },
    {
      label: "+30 SEC",
      value: thirty,
    },
    {
      label: "+60 SEC",
      value: sixty,
    },
  ];

  return (
    <div className="prediction-timeline">

      {items.map(
        (item, index) => (
          <div
            className="timeline-item"
            key={item.label}
          >

            <div className="timeline-label">
              {item.label}
            </div>

            <div className="timeline-value">
              {Number(
                item.value
              ).toFixed(0)}
              <span>%</span>
            </div>

            <div className="timeline-track">
              <span
                style={{
                  width: `${Math.min(
                    100,
                    Math.max(
                      0,
                      item.value
                    )
                  )}%`,
                }}
              />
            </div>

            {index <
              items.length - 1 && (
              <div className="timeline-line" />
            )}

          </div>
        )
      )}

    </div>
  );
}