import { useEffect, useRef, useState } from "react";
import {
  Ambulance,
  Car,
  Pause,
  Play,
  RotateCcw,
  Settings2,
  TrafficCone,
  Zap,
} from "lucide-react";

const LANES = ["north", "east", "south", "west"];

const INITIAL_SIGNALS = {
  north: "green",
  east: "red",
  south: "red",
  west: "red",
};

const CENTER = { x: 50, y: 50 };

const ROAD = {
  north: {
    spawn: { x: 47.5, y: -8 },
    stop: { x: 47.5, y: 32 },
    entry: { x: 47.5, y: 38 },
    angle: -90,
  },

  east: {
    spawn: { x: 108, y: 47.5 },
    stop: { x: 68, y: 47.5 },
    entry: { x: 62, y: 47.5 },
    angle: 0,
  },

  south: {
    spawn: { x: 52.5, y: 108 },
    stop: { x: 52.5, y: 68 },
    entry: { x: 52.5, y: 62 },
    angle: 90,
  },

  west: {
    spawn: { x: -8, y: 52.5 },
    stop: { x: 32, y: 52.5 },
    entry: { x: 38, y: 52.5 },
    angle: 180,
  },
};

const EXIT_POINTS = {
  north: {
    x: 52.5,
    y: -8,
  },

  east: {
    x: 108,
    y: 52.5,
  },

  south: {
    x: 47.5,
    y: 108,
  },

  west: {
    x: -8,
    y: 47.5,
  },
};

const VEHICLE_CONFIG = {
  car: {
    width: 8,
    height: 4.5,
    maxSpeed: 0.085,
    acceleration: 0.004,
    braking: 0.009,
    className: "car",
  },

  truck: {
    width: 10,
    height: 5,
    maxSpeed: 0.055,
    acceleration: 0.003,
    braking: 0.008,
    className: "truck",
  },

  bike: {
    width: 5.5,
    height: 3,
    maxSpeed: 0.11,
    acceleration: 0.006,
    braking: 0.012,
    className: "bike",
  },
};

function randomType() {
  const value = Math.random();

  if (value < 0.72) {
    return "car";
  }

  if (value < 0.9) {
    return "bike";
  }

  return "truck";
}

function nextLane(direction) {
  const index = LANES.indexOf(direction);

  return LANES[
    (index + 1) % LANES.length
  ];
}

function oppositeLane(direction) {
  const index = LANES.indexOf(direction);

  return LANES[
    (index + 2) % LANES.length
  ];
}

function getSpawnPosition(direction, offset) {
  const road = ROAD[direction];

  if (
    direction === "north" ||
    direction === "south"
  ) {
    return {
      x: road.spawn.x,
      y:
        direction === "north"
          ? road.spawn.y - offset
          : road.spawn.y + offset,
    };
  }

  return {
    x:
      direction === "west"
        ? road.spawn.x - offset
        : road.spawn.x + offset,
    y: road.spawn.y,
  };
}

function createVehicle(
  direction,
  offset = 0
) {
  const type = randomType();
  const config = VEHICLE_CONFIG[type];

  const destinationOptions = [
    nextLane(direction),
    oppositeLane(direction),
    LANES[
      (LANES.indexOf(direction) + 3) %
        LANES.length
    ],
  ];

  const destination =
    destinationOptions[
      Math.floor(
        Math.random() *
          destinationOptions.length
      )
    ];

  const position =
    getSpawnPosition(
      direction,
      offset
    );

  return {
    id:
      `${direction}-${Date.now()}-${Math.random()}`,

    direction,

    destination,

    type,

    x: position.x,
    y: position.y,

    speed:
      config.maxSpeed *
      (0.65 + Math.random() * 0.25),

    maxSpeed:
      config.maxSpeed *
      (0.9 + Math.random() * 0.15),

    acceleration:
      config.acceleration,

    braking:
      config.braking,

    state: "approaching",

    distance: 0,

    pathDistance: 0,

    routeStarted: false,

    angle: ROAD[direction].angle,

    turnProgress: 0,

    waitTime: 0,
  };
}

function createInitialVehicles() {
  const vehicles = [];

  LANES.forEach((lane) => {
    for (let i = 0; i < 7; i++) {
      vehicles.push(
        createVehicle(
          lane,
          i * 8
        )
      );
    }
  });

  return vehicles;
}

function lerp(a, b, t) {
  return (
    a +
    (b - a) * t
  );
}

function lerpPoint(a, b, t) {
  return {
    x: lerp(a.x, b.x, t),
    y: lerp(a.y, b.y, t),
  };
}

function normalizeAngle(angle) {
  while (angle > 180) {
    angle -= 360;
  }

  while (angle < -180) {
    angle += 360;
  }

  return angle;
}

function clockwiseDifference(
  start,
  end
) {
  let difference =
    end - start;

  while (difference < 0) {
    difference += 360;
  }

  while (difference >= 360) {
    difference -= 360;
  }

  return difference;
}

function getEntryAngle(direction) {
  return ROAD[direction].angle;
}

function getDestinationAngle(
  direction
) {
  return ROAD[direction].angle;
}

function getRoundaboutPoint(
  angle
) {
  const radius = 14.5;

  const radians =
    (angle * Math.PI) / 180;

  return {
    x:
      CENTER.x +
      Math.cos(radians) *
        radius,

    y:
      CENTER.y +
      Math.sin(radians) *
        radius,
  };
}

function getRoutePoint(
  vehicle
) {
  const direction =
    vehicle.direction;

  const destination =
    vehicle.destination;

  if (
    vehicle.state ===
    "approaching"
  ) {
    const road =
      ROAD[direction];

    return {
      x: vehicle.x,
      y: vehicle.y,
      rotation:
        direction === "north"
          ? 180
          : direction === "south"
            ? 0
            : direction === "east"
              ? 270
              : 90,
    };
  }

  if (
    vehicle.state ===
    "roundabout"
  ) {
    const point =
      getRoundaboutPoint(
        vehicle.angle
      );

    return {
      x: point.x,
      y: point.y,
      rotation:
        vehicle.angle + 90,
    };
  }

  const entry =
    getRoundaboutPoint(
      getDestinationAngle(
        destination
      )
    );

  const exit =
    EXIT_POINTS[destination];

  const t =
    Math.max(
      0,
      Math.min(
        1,
        vehicle.turnProgress
      )
    );

  const point =
    lerpPoint(
      entry,
      exit,
      t
    );

  const rotation =
    destination === "north"
      ? 180
      : destination === "south"
        ? 0
        : destination === "east"
          ? 270
          : 90;

  return {
    x: point.x,
    y: point.y,
    rotation,
  };
}

function distance(
  a,
  b
) {
  const dx =
    a.x - b.x;

  const dy =
    a.y - b.y;

  return Math.sqrt(
    dx * dx + dy * dy
  );
}

function getVehicleGap(
  vehicle,
  other
) {
  const config =
    VEHICLE_CONFIG[
      vehicle.type
    ];

  const otherConfig =
    VEHICLE_CONFIG[
      other.type
    ];

  return (
    3 +
    config.height / 2 +
    otherConfig.height / 2
  );
}

function isAhead(
  vehicle,
  other
) {
  if (
    vehicle.direction !==
    other.direction
  ) {
    return false;
  }

  if (
    vehicle.state !==
    "approaching" ||
    other.state !==
    "approaching"
  ) {
    return false;
  }

  if (
    vehicle.direction ===
    "north"
  ) {
    return (
      other.y >
      vehicle.y
    );
  }

  if (
    vehicle.direction ===
    "south"
  ) {
    return (
      other.y <
      vehicle.y
    );
  }

  if (
    vehicle.direction ===
    "east"
  ) {
    return (
      other.x <
      vehicle.x
    );
  }

  return (
    other.x >
    vehicle.x
  );
}

function getLeader(
  vehicle,
  vehicles
) {
  let leader = null;
  let bestDistance =
    Infinity;

  vehicles.forEach(
    (other) => {
      if (
        other.id ===
        vehicle.id
      ) {
        return;
      }

      if (
        !isAhead(
          vehicle,
          other
        )
      ) {
        return;
      }

      const gap =
        distance(
          vehicle,
          other
        );

      if (
        gap <
        bestDistance
      ) {
        bestDistance =
          gap;

        leader =
          other;
      }
    }
  );

  return leader;
}

function moveTowards(
  current,
  target,
  amount
) {
  if (
    current < target
  ) {
    return Math.min(
      current + amount,
      target
    );
  }

  return Math.max(
    current - amount,
    target
  );
}

function updateApproachingVehicle(
  vehicle,
  vehicles,
  signals,
  multiplier
) {
  const road =
    ROAD[
      vehicle.direction
    ];

  const leader =
    getLeader(
      vehicle,
      vehicles
    );

  let targetSpeed =
    vehicle.maxSpeed;

  const stopDistance =
    distance(
      vehicle,
      road.stop
    );

  const signal =
    signals[
      vehicle.direction
    ];

  /*
   * RED LIGHT
   *
   * Slow down before the stop
   * line rather than instantly
   * freezing the vehicle.
   */
  if (
    signal !== "green" &&
    stopDistance < 14
  ) {
    targetSpeed = 0;
  }

  /*
   * VEHICLE AHEAD
   */
  if (leader) {
    const gap =
      distance(
        vehicle,
        leader
      );

    const requiredGap =
      getVehicleGap(
        vehicle,
        leader
      );

    if (
      gap <
      requiredGap + 8
    ) {
      targetSpeed =
        Math.min(
          targetSpeed,
          vehicle.maxSpeed *
            Math.max(
              0,
              (
                gap -
                requiredGap
              ) / 8
            )
        );
    }
  }

  /*
   * Smooth acceleration
   */
  if (
    vehicle.speed <
    targetSpeed
  ) {
    vehicle.speed =
      Math.min(
        vehicle.speed +
          vehicle.acceleration *
            multiplier,
        targetSpeed
      );
  }

  /*
   * Smooth braking
   */
  if (
    vehicle.speed >
    targetSpeed
  ) {
    vehicle.speed =
      Math.max(
        vehicle.speed -
          vehicle.braking *
            multiplier,
        targetSpeed
      );
  }

  /*
   * Move along the road
   */
  if (
    vehicle.speed >
    0.001
  ) {
    if (
      vehicle.direction ===
      "north"
    ) {
      vehicle.y +=
        vehicle.speed *
        multiplier;
    }

    if (
      vehicle.direction ===
      "south"
    ) {
      vehicle.y -=
        vehicle.speed *
        multiplier;
    }

    if (
      vehicle.direction ===
      "east"
    ) {
      vehicle.x -=
        vehicle.speed *
        multiplier;
    }

    if (
      vehicle.direction ===
      "west"
    ) {
      vehicle.x +=
        vehicle.speed *
        multiplier;
    }
  }

  /*
   * Enter roundabout once
   * the car reaches the entry.
   */
  const reachedEntry =
    (
      vehicle.direction ===
        "north" &&
      vehicle.y >=
        road.entry.y
    ) ||
    (
      vehicle.direction ===
        "south" &&
      vehicle.y <=
        road.entry.y
    ) ||
    (
      vehicle.direction ===
        "east" &&
      vehicle.x <=
        road.entry.x
    ) ||
    (
      vehicle.direction ===
        "west" &&
      vehicle.x >=
        road.entry.x
    );

  if (
    reachedEntry &&
    signal === "green"
  ) {
    vehicle.state =
      "roundabout";

    vehicle.angle =
      getEntryAngle(
        vehicle.direction
      );

    vehicle.routeStarted =
      true;

    const entryPoint =
      getRoundaboutPoint(
        vehicle.angle
      );

    vehicle.x =
      entryPoint.x;

    vehicle.y =
      entryPoint.y;
  }
}

function updateRoundaboutVehicle(
  vehicle,
  multiplier
) {
  const targetAngle =
    getDestinationAngle(
      vehicle.destination
    );

  const currentAngle =
    vehicle.angle;

  const difference =
    clockwiseDifference(
      currentAngle,
      targetAngle
    );

  /*
   * Never make a vehicle
   * perform a full circle unless
   * the route actually requires it.
   */
  if (
    difference < 8
  ) {
    vehicle.state =
      "exiting";

    vehicle.turnProgress =
      0;

    return;
  }

  /*
   * Smooth circular motion.
   */
  const turnSpeed =
    1.35 *
    multiplier;

  vehicle.angle +=
    turnSpeed;

  if (
    vehicle.angle >=
    360
  ) {
    vehicle.angle -=
      360;
  }

  const point =
    getRoundaboutPoint(
      vehicle.angle
    );

  vehicle.x =
    point.x;

  vehicle.y =
    point.y;
}

function updateExitingVehicle(
  vehicle,
  multiplier
) {
  vehicle.turnProgress =
    Math.min(
      1,
      vehicle.turnProgress +
        0.018 *
        multiplier
    );

  const position =
    getRoutePoint(
      vehicle
    );

  vehicle.x =
    position.x;

  vehicle.y =
    position.y;

  /*
   * When the car reaches
   * the outside of the road,
   * respawn it naturally at
   * the back of its original lane.
   */
  if (
    vehicle.turnProgress >=
    1
  ) {
    return true;
  }

  return false;
}

function updateAmbulance(
  ambulance,
  multiplier
) {
  const road =
    ROAD[
      ambulance.direction
    ];

  const next = {
    ...ambulance,
  };

  if (
    next.state ===
    "approaching"
  ) {
    const dx =
      road.entry.x -
      next.x;

    const dy =
      road.entry.y -
      next.y;

    const distanceToEntry =
      Math.sqrt(
        dx * dx +
        dy * dy
      );

    if (
      distanceToEntry >
      2
    ) {
      const speed =
        0.18 *
        multiplier;

      if (
        Math.abs(dx) >
        Math.abs(dy)
      ) {
        next.x +=
          Math.sign(dx) *
          speed;
      } else {
        next.y +=
          Math.sign(dy) *
          speed;
      }
    } else {
      next.state =
        "roundabout";

      next.angle =
        getEntryAngle(
          ambulance.direction
        );
    }

    return next;
  }

  if (
    next.state ===
    "roundabout"
  ) {
    const destination =
      oppositeLane(
        ambulance.direction
      );

    const target =
      getDestinationAngle(
        destination
      );

    const difference =
      clockwiseDifference(
        next.angle,
        target
      );

    if (
      difference < 7
    ) {
      next.state =
        "exiting";

      next.turnProgress =
        0;

      next.destination =
        destination;

      return next;
    }

    next.angle +=
      2.7 *
      multiplier;

    if (
      next.angle >=
      360
    ) {
      next.angle -=
        360;
    }

    const point =
      getRoundaboutPoint(
        next.angle
      );

    next.x =
      point.x;

    next.y =
      point.y;

    return next;
  }

  next.turnProgress =
    Math.min(
      1,
      next.turnProgress +
        0.035 *
        multiplier
    );

  const position =
    getRoutePoint(
      next
    );

  next.x =
    position.x;

  next.y =
    position.y;

  if (
    next.turnProgress >=
    1
  ) {
    return null;
  }

  return next;
}

export default function Simulation() {
  const [
    running,
    setRunning,
  ] = useState(true);

  const [
    signals,
    setSignals,
  ] = useState(
    INITIAL_SIGNALS
  );

  const [
    vehicles,
    setVehicles,
  ] = useState(
    createInitialVehicles
  );

  const [
    selectedLane,
    setSelectedLane,
  ] = useState(
    "north"
  );

  const [
    simulationSpeed,
    setSimulationSpeed,
  ] = useState(1);

  const [
    ambulance,
    setAmbulance,
  ] = useState(null);

  const runningRef =
    useRef(true);

  const signalsRef =
    useRef(INITIAL_SIGNALS);

  const speedRef =
    useRef(1);

  const ambulanceRef =
    useRef(null);

  const previousSignalsRef =
    useRef(
      INITIAL_SIGNALS
    );

  useEffect(() => {
    runningRef.current =
      running;
  }, [running]);

  useEffect(() => {
    signalsRef.current =
      signals;
  }, [signals]);

  useEffect(() => {
    speedRef.current =
      simulationSpeed;
  }, [simulationSpeed]);

  useEffect(() => {
    ambulanceRef.current =
      ambulance;
  }, [ambulance]);

  useEffect(() => {
    let frame;

    let previous =
      performance.now();

    function loop(now) {
      const delta =
        Math.min(
          now - previous,
          35
        );

      previous = now;

      if (
        runningRef.current
      ) {
        const multiplier =
          (delta / 16.67) *
          speedRef.current;

        setVehicles(
          (current) => {
            const updated =
              current.map(
                (vehicle) => ({
                  ...vehicle,
                })
              );

            updated.forEach(
              (vehicle) => {
                if (
                  vehicle.state ===
                  "approaching"
                ) {
                  updateApproachingVehicle(
                    vehicle,
                    updated,
                    signalsRef.current,
                    multiplier
                  );
                }

                else if (
                  vehicle.state ===
                  "roundabout"
                ) {
                  updateRoundaboutVehicle(
                    vehicle,
                    multiplier
                  );
                }
              }
            );

            const finalVehicles =
              [];

            updated.forEach(
              (vehicle) => {
                if (
                  vehicle.state ===
                  "exiting"
                ) {
                  const finished =
                    updateExitingVehicle(
                      vehicle,
                      multiplier
                    );

                  if (
                    finished
                  ) {
                    finalVehicles.push(
                      createVehicle(
                        vehicle.direction,
                        0
                      )
                    );

                    return;
                  }
                }

                finalVehicles.push(
                  vehicle
                );
              }
            );

            return finalVehicles;
          }
        );

        if (
          ambulanceRef.current
        ) {
          const nextAmbulance =
            updateAmbulance(
              ambulanceRef.current,
              multiplier
            );

          setAmbulance(
            nextAmbulance
          );

          ambulanceRef.current =
            nextAmbulance;
        }
      }

      frame =
        requestAnimationFrame(
          loop
        );
    }

    frame =
      requestAnimationFrame(
        loop
      );

    return () => {
      cancelAnimationFrame(
        frame
      );
    };
  }, []);

  function giveGreen(
    lane
  ) {
    if (
      ambulanceRef.current
    ) {
      return;
    }

    previousSignalsRef.current =
      signalsRef.current;

    const next = {};

    LANES.forEach(
      (currentLane) => {
        next[currentLane] =
          currentLane === lane
            ? "green"
            : "red";
      }
    );

    setSignals(next);
    setSelectedLane(lane);
  }

  function dispatchAmbulance() {
    if (
      ambulanceRef.current
    ) {
      return;
    }

    previousSignalsRef.current =
      signalsRef.current;

    const next = {};

    LANES.forEach(
      (lane) => {
        next[lane] =
          lane === selectedLane
            ? "green"
            : "red";
      }
    );

    setSignals(next);

    const spawn =
      ROAD[
        selectedLane
      ].spawn;

    const newAmbulance = {
      direction:
        selectedLane,

      destination:
        oppositeLane(
          selectedLane
        ),

      state:
        "approaching",

      x: spawn.x,

      y: spawn.y,

      angle:
        getEntryAngle(
          selectedLane
        ),

      turnProgress: 0,
    };

    setAmbulance(
      newAmbulance
    );

    ambulanceRef.current =
      newAmbulance;
  }

  function cancelEmergency() {
    setAmbulance(null);

    ambulanceRef.current =
      null;

    setSignals(
      previousSignalsRef.current
    );
  }

  function resetSimulation() {
    const initial =
      createInitialVehicles();

    setVehicles(initial);

    setSignals(
      INITIAL_SIGNALS
    );

    signalsRef.current =
      INITIAL_SIGNALS;

    setSelectedLane(
      "north"
    );

    setAmbulance(null);

    ambulanceRef.current =
      null;

    setSimulationSpeed(1);

    speedRef.current = 1;

    setRunning(true);
  }

  const vehicleCount =
    vehicles.length;

  const waitingVehicles =
    vehicles.filter(
      (vehicle) =>
        vehicle.state ===
          "approaching" &&
        vehicle.speed <
          0.015
    ).length;

  return (
    <div className="page simulation-page">

      <section className="page-heading">

        <div>
          <div className="eyebrow">
            DIGITAL TWIN · SIGNAL LAB
          </div>

          <h1>
            Intersection simulation
          </h1>

          <p>
            Test traffic signal strategies
            before deploying them to the
            real intersection.
          </p>
        </div>

        <div
          className={
            ambulance
              ? "simulation-state emergency"
              : "simulation-state"
          }
        >
          <span className="status-dot live" />

          {ambulance
            ? "EMERGENCY PRIORITY"
            : running
              ? "SIMULATION RUNNING"
              : "SIMULATION PAUSED"}
        </div>

      </section>

      <div className="simulation-layout">

        <section className="panel simulation-card">

          <div className="simulation-toolbar">

            <div className="toolbar-title">
              <TrafficCone
                size={18}
              />

              <span>
                JUNCTION A · DIGITAL TWIN
              </span>
            </div>

            <div className="toolbar-actions">

              <div className="simulation-stat">
                <Car size={14} />
                {vehicleCount}
              </div>

              <div className="simulation-stat">
                Waiting {waitingVehicles}
              </div>

              <button
                className="ghost-button"
                onClick={() =>
                  setRunning(
                    (value) =>
                      !value
                  )
                }
              >
                {running ? (
                  <Pause
                    size={15}
                  />
                ) : (
                  <Play
                    size={15}
                  />
                )}

                {running
                  ? "Pause"
                  : "Run"}
              </button>

              <button
                className="ghost-button"
                onClick={
                  resetSimulation
                }
              >
                <RotateCcw
                  size={15}
                />

                Reset
              </button>

            </div>

          </div>

          <div className="roundabout-stage">

            <div className="road road-north" />
            <div className="road road-south" />
            <div className="road road-east" />
            <div className="road road-west" />

            <div className="lane-mark north-mark" />
            <div className="lane-mark south-mark" />
            <div className="lane-mark east-mark" />
            <div className="lane-mark west-mark" />

            <div className="roundabout-ring">

              <div className="roundabout-inner">

                <strong>
                  JUNCTION A
                </strong>

                <span>
                  DIGITAL TWIN
                </span>

              </div>

            </div>

            {LANES.map(
              (lane) => (
                <TrafficLight
                  key={lane}
                  direction={lane}
                  state={
                    signals[lane]
                  }
                  disabled={
                    Boolean(ambulance)
                  }
                  onClick={() =>
                    setSelectedLane(
                      lane
                    )
                  }
                />
              )
            )}

            {vehicles.map(
              (vehicle) => {
                const position =
                  getRoutePoint(
                    vehicle
                  );

                return (
                  <Vehicle
                    key={
                      vehicle.id
                    }
                    vehicle={
                      vehicle
                    }
                    position={
                      position
                    }
                  />
                );
              }
            )}

            {ambulance && (
              <AmbulanceVehicle
                ambulance={
                  ambulance
                }
              />
            )}

          </div>

          <div className="simulation-legend">

            <span>
              <i className="legend-dot green" />
              Moving
            </span>

            <span>
              <i className="legend-dot red" />
              Waiting
            </span>

            <span>
              <i className="legend-dot ambulance" />
              Emergency
            </span>

            <span className="legend-note">
              Vehicles accelerate, brake and
              maintain following distance.
            </span>

          </div>

        </section>

        <aside className="simulation-controls">

          <section className="control-panel">

            <div className="control-title">
              <Settings2
                size={17}
              />

              Signal control
            </div>

            <p className="control-help">
              Choose an approach and
              give it priority.
            </p>

            <div className="lane-controls">

              {LANES.map(
                (lane) => (
                  <button
                    key={lane}
                    className={
                      selectedLane ===
                      lane
                        ? "lane-control selected"
                        : "lane-control"
                    }
                    onClick={() =>
                      setSelectedLane(
                        lane
                      )
                    }
                  >
                    <span
                      className={
                        signals[
                          lane
                        ] === "green"
                          ? "signal-mini green"
                          : "signal-mini"
                      }
                    />

                    <span>
                      {lane
                        .charAt(0)
                        .toUpperCase() +
                        lane.slice(1)}
                    </span>

                    <strong>
                      {
                        vehicles.filter(
                          (
                            vehicle
                          ) =>
                            vehicle.direction ===
                            lane
                        ).length
                      }
                    </strong>
                  </button>
                )
              )}

            </div>

            <button
              className="primary-button full"
              disabled={
                Boolean(ambulance)
              }
              onClick={() =>
                giveGreen(
                  selectedLane
                )
              }
            >
              <TrafficCone
                size={16}
              />

              Give{" "}
              {selectedLane} green
            </button>

          </section>

          <section className="control-panel emergency-panel">

            <div className="control-title">

              <Ambulance
                size={18}
              />

              Emergency dispatch

            </div>

            <p className="control-help">
              Give an ambulance priority
              through the selected approach.
            </p>

            {!ambulance ? (
              <button
                className="emergency-button"
                onClick={
                  dispatchAmbulance
                }
              >
                <Zap size={17} />

                Dispatch ambulance
              </button>
            ) : (
              <div className="emergency-active">

                <div>
                  <strong>
                    Ambulance active
                  </strong>

                  <span>
                    {ambulance.direction.toUpperCase()}
                    {" "}
                    approach
                  </span>
                </div>

                <button
                  className="danger-button"
                  onClick={
                    cancelEmergency
                  }
                >
                  Cancel
                </button>

              </div>
            )}

          </section>

          <section className="control-panel">

            <div className="control-title">

              <Car size={17} />

              Simulation speed

            </div>

            <div className="speed-options">

              {[0.5, 1, 1.5, 2].map(
                (speed) => (
                  <button
                    key={speed}
                    className={
                      simulationSpeed ===
                      speed
                        ? "selected"
                        : ""
                    }
                    onClick={() =>
                      setSimulationSpeed(
                        speed
                      )
                    }
                  >
                    {speed}×
                  </button>
                )
              )}

            </div>

          </section>

        </aside>

      </div>
    </div>
  );
}


/* =========================================================
   TRAFFIC LIGHT
   ========================================================= */

function TrafficLight({
  direction,
  state,
  disabled,
  onClick,
}) {
  const positionClass =
    {
      north:
        "signal-pos-north",

      east:
        "signal-pos-east",

      south:
        "signal-pos-south",

      west:
        "signal-pos-west",
    }[direction];

  return (
    <button
      className={`traffic-light ${positionClass}`}
      disabled={disabled}
      onClick={onClick}
    >
      <span
        className={
          state === "red"
            ? "on"
            : ""
        }
      />

      <span />

      <span
        className={
          state === "green"
            ? "on"
            : ""
        }
      />

      <b>
        {direction
          .charAt(0)
          .toUpperCase()}
      </b>
    </button>
  );
}


/* =========================================================
   VEHICLE
   ========================================================= */

function Vehicle({
  vehicle,
  position,
}) {
  const config =
    VEHICLE_CONFIG[
      vehicle.type
    ];

  return (
    <span
      className={`sim-vehicle ${config.className}`}
      style={{
        left: `${position.x}%`,
        top: `${position.y}%`,
        width: `${config.width}px`,
        height: `${config.height}px`,
        transform:
          `translate(-50%, -50%) rotate(${position.rotation}deg)`,
      }}
    >
      <span className="vehicle-window" />

      {vehicle.type ===
        "truck" && (
        <span className="vehicle-cargo" />
      )}

      <span className="vehicle-light front" />
      <span className="vehicle-light rear" />
    </span>
  );
}


/* =========================================================
   AMBULANCE
   ========================================================= */

function AmbulanceVehicle({
  ambulance,
}) {
  const position =
    getRoutePoint(
      ambulance
    );

  return (
    <span
      className="sim-ambulance"
      style={{
        left: `${position.x}%`,
        top: `${position.y}%`,
        transform:
          `translate(-50%, -50%) rotate(${position.rotation}deg)`,
      }}
    >
      <Ambulance size={17} />

      <span className="ambulance-light" />
    </span>
  );
}