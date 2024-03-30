from io import BufferedReader
from typing import Dict, List, Tuple, Optional
import os
import array
import struct
import logging
from fcntl import ioctl


_LOGGER = logging.getLogger(__name__)


class _EventType:
    INIT = 0x80
    BUTTON = 0x01
    AXIS = 0x02


_AXIS_NORMALIZATION_FACTOR = 32767.0

# Event format string
_EVENT_FORMAT = "IhBB"


class IoctlJoystick(object):
    """
    An interface to interact with a physical joystick device via the ioctl system calls.

    This class allows initialization of the joystick, querying available buttons and axes,
    and polling for button and axis events. It uses ioctl system calls to communicate with
    the joystick device and retrieve information about its capabilities.

    Args:
        dev_fn (str): The path to the joystick device file (default: '/dev/input/js0').

    Attributes:
        axis_states (dict): The current states of the joystick axes.
        button_states (dict): The current states of the joystick buttons.
        axis_names (dict): The names of the joystick axes.
        button_names (dict): The names of the joystick buttons.
        axis_map (list): The mapping of axis indices to axis names.
        button_map (list): The mapping of button indices to button names.
        js_dev (file): The file object representing the joystick device.
        dev_fn (str): The path to the joystick device file.

    Methods:
        init(): Initialize the connection to the joystick device and map buttons and axes.
        show_map(): Display the available buttons and axes of the joystick.
        poll(): Query the state of the joystick and return any button or axis events.
    """

    def __init__(self, dev_fn="/dev/input/js0"):
        self.axis_states: Dict = {}
        self.button_states: Dict = {}
        self.axis_names: Dict = {}
        self.button_names: Dict = {}
        self.axis_map: List = []
        self.button_map: List = []
        self.js_dev: Optional[BufferedReader] = None
        self.dev_fn: str = dev_fn

    def init(self):
        """
        Query available buttons and axes given
        a path in the linux device tree.
        """
        self.js_dev = self._open_device()

        self._get_device_name(self.js_dev)
        self._get_num_axes(self.js_dev)
        self._get_num_buttons(self.js_dev)
        self._get_axis_map(self.js_dev)
        self._get_button_map(self.js_dev)

        return True

    def _open_device(self) -> BufferedReader:
        """Open the joystick device file."""
        if not os.path.exists(self.dev_fn):
            raise ValueError(f"{self.dev_fn} is missing")

        # Open the joystick device
        _LOGGER.info(f"Opening {self.dev_fn}...")
        return open(self.dev_fn, "rb")

    def _get_device_name(self, js_dev: BufferedReader):
        # Get the device name.
        # JSIOCGNAME stands for "Joystick IO Control Get Name".
        # It is the name of the ioctl command used to retrieve the device name of the joystick.
        buf_size = 64
        buf = array.array("B", [0] * buf_size)
        ioctl_dev_name = 0x80006A13  # JSIOCGNAME
        ioctl_dev_name_arg = 0x10000 * buf_size
        ioctl(js_dev, ioctl_dev_name + ioctl_dev_name_arg, buf)
        self.js_name = buf.tobytes().decode("utf-8")
        _LOGGER.info(f"Device name: {self.js_name}")

    def _get_num_axes(self, js_dev: BufferedReader):
        # Get number of axes
        # JSIOCGAXES stands for "Joystick IO Control Get Axes".
        # It is the name of the ioctl command used to retrieve the number of axes supported by the joystick.
        ioctl_axes = 0x80016A11  # JSIOCGAXES
        buf = array.array("B", [0])
        ioctl(js_dev, ioctl_axes, buf)
        self.num_axes = buf[0]

    def _get_num_buttons(self, js_dev: BufferedReader):
        # Get number of buttons
        # JSIOCGBUTTONS stands for "Joystick IO Control Get Buttons".
        # It is the name of the ioctl command used to retrieve the number of buttons supported by the joystick.
        ioctl_buttons = 0x80016A12  # JSIOCGBUTTONS
        buf = array.array("B", [0])
        ioctl(js_dev, ioctl_buttons, buf)
        self.num_buttons = buf[0]

    def _get_axis_map(self, js_dev: BufferedReader):
        # Get the axis map
        # JSIOCGAXMAP stands for "Joystick IO Control Get Axis Map".
        # It is the name of the ioctl command used to retrieve the axis map of the joystick.
        ioctl_ax_map = 0x80406A32  # JSIOCGAXMAP
        ax_map_size = 0x40
        buf = array.array("B", [0] * ax_map_size)
        ioctl(js_dev, ioctl_ax_map, buf)
        for axis in buf[: self.num_axes]:
            axis_name = self.axis_names.get(axis, f"unknown(0x{axis:02x})")
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0

    def _get_button_map(self, js_dev: BufferedReader):
        # Get the button map
        # JSIOCGBTNMAP stands for "Joystick IO Control Get Button Map".
        # It is the name of the ioctl command used to retrieve the button map of the joystick.
        ioctl_btn_map = 0x80406A34  # JSIOCGBTNMAP
        btn_map_size = 200
        buf = array.array("H", [0] * btn_map_size)
        ioctl(js_dev, ioctl_btn_map, buf)
        for btn in buf[: self.num_buttons]:
            btn_name = self.button_names.get(btn, f"unknown(0x{btn:03x})")
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0
            _LOGGER.debug(f"Button: 0x{btn:03x}, Name: {btn_name}")

    def show_map(self):
        """
        list the buttons and axis found on this joystick
        """
        print("%d axes found: %s" % (self.num_axes, ", ".join(self.axis_map)))
        print("%d buttons found: %s" % (self.num_buttons, ", ".join(self.button_map)))

    def poll(
        self,
    ) -> Tuple[Optional[str], Optional[int], Optional[str], Optional[float]]:
        """
        Query the state of the joystick.

        Returns:
            tuple: A tuple containing the following elements:
                - button (str): The name of the button that was pressed, if any.
                - button_state (int): The state of the button (None: no change, 1: pressed, 0: released).
                - axis (str): The name of the axis that was moved, if any.
                - axis_val (float): The value of the axis, ranging from -1 to +1.
        """
        button: Optional[str] = None
        button_state: Optional[int] = None
        axis: Optional[str] = None
        axis_val: Optional[float] = None

        if self.js_dev is None:
            raise ValueError("Joystick device is not initialized")

        # Read event from the joystick device
        event: bytes = self.js_dev.read(8)

        if event:
            _, value, event_type, number = struct.unpack(_EVENT_FORMAT, event)
            _: int
            value: int
            event_type: int
            number: int

            if event_type & _EventType.INIT:
                # Ignore initialization event
                return button, button_state, axis, axis_val

            if event_type & _EventType.BUTTON:
                # Button event
                button = self.button_map[number]
                if button:
                    self.button_states[button] = value
                    button_state = value
                    _LOGGER.debug(f"Button: {button}, State: {value}")

            if event_type & _EventType.AXIS:
                # Axis event
                axis = self.axis_map[number]
                if axis:
                    axis_val = value / _AXIS_NORMALIZATION_FACTOR
                    self.axis_states[axis] = axis_val
                    _LOGGER.debug(f"Axis: {axis}, Value: {axis_val:.3f}")

        return button, button_state, axis, axis_val


if __name__ == "__main__":
    joystick = IoctlJoystick()
    joystick.init()
    joystick.show_map()

    while True:
        button, button_state, axis, axis_val = joystick.poll()
        if button:
            print(f"Button: {button}, State: {button_state}")
        if axis:
            print(f"Axis: {axis}, Value: {axis_val:.3f}")
