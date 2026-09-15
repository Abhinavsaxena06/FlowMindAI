import {
  useMemo,
} from "react";

const nodes = [
  {
    id: "A",
    x: 50,
    y: 50,
    status: "high",
    label: "Junction A",
  },
  {
    id: "B",
    x: 25,
    y: 25,
    status: "normal",
    label: "Junction B",
  },
  {
    id: "C",
    x: 75,
    y: 25,
    status: "moderate",
    label: "Junction C",
  },
  {
    id: "D",
    x: 75,
    y: 75,
    status: "normal",
    label: "Junction D",
  },
  {
    id: "E",
    x: 25,
    y: 75,
    status: "moderate",
    label: "Junction E",
  },
];

const edges = [
  ["A", "B"],
  ["A", "C"],
  ["A", "D"],
  ["A", "E"],
  ["B", "C"],
  ["E", "D"],
];

export default function NetworkGraph({
  selected,
  onSelect,
}) {
  const nodeMap =
    useMemo(() => {
      return Object.fromEntries(
        nodes.map(
          (node) => [
            node.id,
            node,
          ]
        )
      );
    }, []);

  return (
    <div className="network-graph">

      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
      >

        {edges.map(
          ([from, to]) => {
            const a =
              nodeMap[from];

            const b =
              nodeMap[to];

            return (
              <line
                key={`${from}-${to}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                className="network-edge"
              />
            );
          }
        )}

      </svg>

      <div className="network-nodes">

        {nodes.map(
          (node) => (
            <button
              key={node.id}
              className={`network-node ${
                node.status
              } ${
                selected === node.id
                  ? "selected"
                  : ""
              }`}
              style={{
                left: `${node.x}%`,
                top: `${node.y}%`,
              }}
              onClick={() =>
                onSelect(node.id)
              }
            >
              <span />
              <strong>
                {node.id}
              </strong>
            </button>
          )
        )}

      </div>

      <div className="network-legend">

        <span>
          <i className="normal" />
          Normal
        </span>

        <span>
          <i className="moderate" />
          Moderate
        </span>

        <span>
          <i className="high" />
          Congested
        </span>

      </div>

    </div>
  );
}