import {
  useState,
} from "react";

import NetworkGraph from "../components/network/NetworkGraph";
import JunctionDetails from "../components/network/JunctionDetails";

export default function NetworkView() {
  const [
    selected,
    setSelected,
  ] = useState("A");

  return (
    <div className="page">

      <section className="page-heading">

        <div>
          <div className="eyebrow">
            NETWORK INTELLIGENCE
          </div>

          <h1>
            Traffic network
          </h1>

          <p>
            Understand congestion propagation
            across connected intersections.
          </p>
        </div>

        <span className="badge success">
          5 JUNCTIONS
        </span>

      </section>

      <div className="network-layout">

        <div className="panel network-panel">

          <div className="panel-header">

            <div>
              <div className="eyebrow">
                DIGITAL NETWORK
              </div>

              <h2>
                Live junction graph
              </h2>
            </div>

          </div>

          <NetworkGraph
            selected={selected}
            onSelect={setSelected}
          />

        </div>

        <JunctionDetails
          junction={selected}
        />

      </div>

    </div>
  );
}