class TwinJunction:

    APPROACHES = [
        "north",
        "east",
        "south",
        "west",
    ]

    def __init__(
        self,
        initial_phase="north",
        primary_green_duration=10,
        secondary_green_duration=10,
        yellow_duration=3,
        all_red_duration=1,
    ):
        if initial_phase not in self.APPROACHES:
            initial_phase = "north"

        self.current_phase = initial_phase

        self.primary_phase = initial_phase

        self.primary_green_duration = float(
            primary_green_duration
        )

        self.secondary_green_duration = float(
            secondary_green_duration
        )

        self.yellow_duration = float(
            yellow_duration
        )

        self.all_red_duration = float(
            all_red_duration
        )

        self.phase_elapsed = 0.0

        self.signal_state = "GREEN"

        self.time = 0.0

        self.phase_index = self.APPROACHES.index(
            initial_phase
        )

    # ---------------------------------------------------------
    # STRATEGY CONFIGURATION
    # ---------------------------------------------------------

    def configure_strategy(
        self,
        primary_phase,
        primary_green_duration,
        secondary_green_duration=10,
    ):

        if primary_phase not in self.APPROACHES:
            primary_phase = "north"

        self.primary_phase = primary_phase

        self.primary_green_duration = max(
            5.0,
            float(primary_green_duration)
        )

        self.secondary_green_duration = max(
            5.0,
            float(secondary_green_duration)
        )

        self.current_phase = primary_phase

        self.phase_index = self.APPROACHES.index(
            primary_phase
        )

        self.phase_elapsed = 0.0

        self.signal_state = "GREEN"

    # ---------------------------------------------------------
    # MANUAL PHASE
    # ---------------------------------------------------------

    def set_phase(self, phase):

        if phase not in self.APPROACHES:
            return

        self.current_phase = phase

        self.phase_index = self.APPROACHES.index(
            phase
        )

        self.phase_elapsed = 0.0

        self.signal_state = "GREEN"

    # ---------------------------------------------------------
    # CURRENT PHASE
    # ---------------------------------------------------------

    def get_active_phase(self):

        return self.current_phase

    # ---------------------------------------------------------
    # GREEN CHECK
    # ---------------------------------------------------------

    def is_green(self, approach):

        return (
            self.signal_state == "GREEN"
            and approach == self.current_phase
        )

    # ---------------------------------------------------------
    # YELLOW CHECK
    # ---------------------------------------------------------

    def is_yellow(self, approach):

        return (
            self.signal_state == "YELLOW"
            and approach == self.current_phase
        )

    # ---------------------------------------------------------
    # ALL RED
    # ---------------------------------------------------------

    def is_all_red(self):

        return self.signal_state == "ALL_RED"

    # ---------------------------------------------------------
    # CURRENT GREEN DURATION
    # ---------------------------------------------------------

    def get_current_green_duration(self):

        if self.current_phase == self.primary_phase:

            return self.primary_green_duration

        return self.secondary_green_duration

    # ---------------------------------------------------------
    # ADVANCE SIGNAL
    # ---------------------------------------------------------

    def advance(self, seconds=1.0):

        seconds = float(seconds)

        self.time += seconds

        self.phase_elapsed += seconds

        # -----------------------------------------------------
        # GREEN
        # -----------------------------------------------------

        if self.signal_state == "GREEN":

            green_duration = (
                self.get_current_green_duration()
            )

            if self.phase_elapsed >= green_duration:

                self.signal_state = "YELLOW"

                self.phase_elapsed = 0.0

        # -----------------------------------------------------
        # YELLOW
        # -----------------------------------------------------

        elif self.signal_state == "YELLOW":

            if (
                self.phase_elapsed
                >= self.yellow_duration
            ):

                self.signal_state = "ALL_RED"

                self.phase_elapsed = 0.0

        # -----------------------------------------------------
        # ALL RED
        # -----------------------------------------------------

        elif self.signal_state == "ALL_RED":

            if (
                self.phase_elapsed
                >= self.all_red_duration
            ):

                self.phase_index += 1

                if (
                    self.phase_index
                    >= len(self.APPROACHES)
                ):

                    self.phase_index = 0

                self.current_phase = (
                    self.APPROACHES[
                        self.phase_index
                    ]
                )

                self.signal_state = "GREEN"

                self.phase_elapsed = 0.0

    # ---------------------------------------------------------
    # STATE
    # ---------------------------------------------------------

    def get_state(self):

        return {
            "current_phase": self.current_phase,

            "signal_state": self.signal_state,

            "phase_elapsed": round(
                self.phase_elapsed,
                2
            ),

            "current_green_duration": round(
                self.get_current_green_duration(),
                2
            ),

            "primary_phase": self.primary_phase,

            "primary_green_duration": round(
                self.primary_green_duration,
                2
            ),

            "secondary_green_duration": round(
                self.secondary_green_duration,
                2
            ),

            "yellow_duration": round(
                self.yellow_duration,
                2
            ),

            "all_red_duration": round(
                self.all_red_duration,
                2
            ),

            "time": round(
                self.time,
                2
            ),
        }