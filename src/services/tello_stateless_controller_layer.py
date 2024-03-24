class TelloControllerStatelessLayer:

    def get_state(self) -> TelloControlState:
        self.pygame_connector.get_events()

        left_right_velocity = 0
        forward_backward_velocity = 0
        up_down_velocity = 0
        yaw_velocity = 0

        for i in range(self.joystick.get_numaxes()):
            val = self.joystick.get_axis(i)
            if abs(val) < self.dead_zone:
                val = 0.0
            if self.axis_states[i] != val and i in self.axis_ids:
                axis = self.axis_ids[i]
                self.axis_states[i] = val
                logging.debug("axis: %s val: %f" % (axis, val))

                if axis == "left_right":
                    left_right_velocity = int(val * 100)
                elif axis == "forward_backward":
                    forward_backward_velocity = int(val * 100)
                elif axis == "up_down":
                    up_down_velocity = int(val * 100)
                elif axis == "yaw":
                    yaw_velocity = int(val * 100)

        for i in range(self.joystick.get_numbuttons()):
            state = bool(self.joystick.get_button(i))
            if self.button_states[i] != state:
                if i not in self.button_ids:
                    LOGGER.info(f"button: {i}")
                    continue
                button = self.button_ids[i]
                self.button_states[i] = state
                LOGGER.info("button: %s state: %d" % (button, state))

        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            horz, vert = hat
            iBtn = self.joystick.get_numbuttons() + (i * 4)
            states = (horz == -1, horz == 1, vert == -1, vert == 1)
            for state in states:
                state = bool(state)
                if self.button_states[iBtn] != state:
                    if iBtn not in self.button_ids:
                        LOGGER.info(f"button: {iBtn}")
                        continue
                    button = self.button_ids[iBtn]
                    self.button_states[iBtn] = state
                    LOGGER.info("button: %s state: %d" % (button, state))
                iBtn += 1

        pressed_button_ids = [
            index
            for index, is_pressed_state in enumerate(self.button_states)
            if is_pressed_state
        ]
        if LOGGER.level == logging.DEBUG:
            LOGGER.debug(
                f"Axis {list(zip(self.AXIS_NAMES.values() ,self.axis_ids, self.axis_states))}"
            )
            LOGGER.debug(
                f"Buttons {list(zip(self.BUTTON_NAMES.values(), self.button_ids, self.button_states))}"
            )
            LOGGER.debug(
                f"Pressed Buttons { [ v for k,v in self.BUTTON_NAMES.items() if k in pressed_button_ids ]}"
            )
        return TelloControlState(
            left_right_velocity=left_right_velocity,
            forward_backward_velocity=forward_backward_velocity,
            up_down_velocity=up_down_velocity,
            yaw_velocity=yaw_velocity,
            speed=50,
            take_off=False,
        )
