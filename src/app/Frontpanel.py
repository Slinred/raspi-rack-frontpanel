import sys
import time
import logging

from Constants import Constants
from services.StatusScreenService import StatusScreenService
from status_screen.BootScreen import BootScreen
from status_screen.StatusScreenBase import StatusScreenBase
from status_screen.MainStatusScreen import MainStatusScreen
from status_screen.SysStatusScreen import SysStatusScreen
from status_screen.SvcStatusScreen import SvcStatusScreen


class Frontpanel:
    """
    @brief  This is the main class encapsulating all functionality of the frontpanel
    """

    def __init__(self, configFile: str):
        log_level = logging.DEBUG

        logging.basicConfig(
            format="%(asctime)s - %(name)-20s - %(levelname)s - %(funcName)s: %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            level=log_level,
            handlers=[logging.StreamHandler(sys.stdout)],
            force=True,
        )

        self._logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        self._logger.info("Starting...")

        self._logger.debug("Initiliazing status screen service...")
        status_screen_svc = StatusScreenService(1, 0x3C, Constants.SCREEN_SIZE)
        self._logger.debug("Initializing boot screen...")
        status_screen_svc.add_screen(BootScreen(), is_boot_screen=True)

        screens = [
            MainStatusScreen(),
            SysStatusScreen(),
            SvcStatusScreen(
                [
                    ("systemd-networkd", "networkd"),
                    "ssh",
                    ("systemd-resolved", "resolved"),
                ]
            ),
        ]

        for screen in screens:
            screen: StatusScreenBase
            self._logger.debug(f"Initializing {screen.__class__.__name__}...")
            status_screen_svc.add_screen(screen)

        try:
            status_screen_svc.start()
            while True:
                time.sleep(1)
        except:
            status_screen_svc.wait_stop()

        self._logger.info(f"stopped!")


if __name__ == "__main__":
    Frontpanel("").start()
