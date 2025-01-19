import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from status_screen.StatusScreenBase import StatusScreenBase, threading
from services.ServiceBase import ServiceBase


class StatusScreenService(ServiceBase):
    """
    @brief  This class serves the display via I2C and is updating the display with the different screens
    """

    I2C_ADDRESS_RANGE = (0x00, 0x7F)
    DEVICE_ROTATION_RANGE = (0, 359)

    ITERATION_INTERVAL = 0.1

    def __init__(
        self,
        i2c_port_id: int,
        i2c_address: int,
        size: tuple[int, int],
        rotation: int = 0,
    ):
        if not isinstance(i2c_port_id, int):
            raise TypeError("i2c_port_id must be of type int")
        if (
            not isinstance(i2c_address, int)
            or i2c_address < self.I2C_ADDRESS_RANGE[0]
            or i2c_address > self.I2C_ADDRESS_RANGE[1]
        ):
            raise TypeError(
                f"i2c_address must be of type int and in the range of {'-'.join(self.I2C_ADDRESS_RANGE)}"
            )
        if not isinstance(size, tuple) or any(
            not isinstance(size_elem, int) for size_elem in size
        ):
            raise TypeError("i2c_port_id must be of type tuple[int, int]")
        if not isinstance(rotation, int) or (
            rotation < self.DEVICE_ROTATION_RANGE[0]
            or rotation > self.DEVICE_ROTATION_RANGE[1]
        ):
            raise TypeError(
                f"rotation must be of type int and in the range of {'-'.join(self.DEVICE_ROTATION_RANGE)}"
            )

        super().__init__("Status screen service")

        try:
            self._device = ssd1306(
                i2c(port=i2c_port_id, address=i2c_address),
                width=size[0],
                height=size[1],
                rotate=rotation,
            )
        except:
            raise Exception("Failed to initilize display device!")

        self._lock = threading.Lock()

        self._update_screen = threading.Event()
        self._screens = list[StatusScreenBase]()
        self._bootscreen = None
        self._screen = None

        self._device.hide()

    def add_screen(self, screen: StatusScreenBase, is_boot_screen: bool = False):
        if is_boot_screen:
            self._bootscreen = screen
        else:
            self._screens.append(screen)

    def get_screens(self) -> list[StatusScreenBase]:
        return self._screens

    def __main__(self):
        self._device.show()
        self._device.contrast(1)
        self._device.clear()

        with self._lock:
            if len(self._screens) == 0 and not isinstance(
                self._bootscreen, StatusScreenBase
            ):
                return

        screen_idx = 0
        if isinstance(self._bootscreen, StatusScreenBase):
            screen_idx = -1
            next_screen_idx = 0
            self._bootscreen.render()
        self._screens[0].render()

        display_thread = None
        self._update_screen.set()  # trigger initial redraw of screen
        while self.__running__.is_set():
            if self._update_screen.is_set():
                self._update_screen.clear()
                if isinstance(display_thread, threading.Thread):
                    display_thread.join()

                if screen_idx >= 0:
                    # first trigger rendering of next screen
                    next_screen_idx = (screen_idx + 1) % len(self._screens)

                with self._lock:
                    self._screens[next_screen_idx].render()

                    # now display the actual screen
                    self._screen = (
                        self._screens[screen_idx]
                        if screen_idx >= 0
                        else self._bootscreen
                    )

                screen_idx = (
                    ((screen_idx + 1) % len(self._screens)) if screen_idx >= 0 else 0
                )

                display_thread = threading.Thread(
                    target=self._display_screen,
                    name=f"{self.__class__.__name__}-Display",
                )
                display_thread.start()

            time.sleep(self.ITERATION_INTERVAL)

        self._device.clear()
        self._device.hide()

    def _display_screen(self):
        if not isinstance(self._screen, StatusScreenBase):
            return

        with self._lock:
            display_time = self._screen.get_display_time()
        start_time = time.time()
        while (display_time == 0) or ((time.time() - start_time) < display_time):
            with self._lock:
                if (display_time == 0) and self._screen.is_done():
                    break
                self._screen.render()
                self._device.display(self._screen.get_image())

            time.sleep(self._screen.get_redraw_interval())

        self._update_screen.set()
        return
