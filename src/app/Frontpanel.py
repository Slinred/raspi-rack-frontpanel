import time
import logging

from Constants import Constants
from services.StatusScreenService import StatusScreenService
from status_screen.BootScreen import BootScreen
from status_screen.MainStatusScreen import MainStatusScreen
from status_screen.SysStatusScreen import SysStatusScreen
from status_screen.SvcStatusScreen import SvcStatusScreen


class Frontpanel:
    """
    @brief  This is the main class encapsulating all functionality of the frontpanel
    """

    def __init__(self, configFile: str):
        logging.basicConfig(level=logging.DEBUG)

    def start(self):
        status_screen_svc = StatusScreenService(1, 0x3C, Constants.SCREEN_SIZE)
        status_screen_svc.add_screen(BootScreen(), is_boot_screen=True)
        status_screen_svc.add_screen(MainStatusScreen())
        status_screen_svc.add_screen(SysStatusScreen())
        status_screen_svc.add_screen(
            SvcStatusScreen(
                [
                    ("systemd-networkd", "networkd"),
                    "ssh",
                    ("systemd-resolved", "resolved"),
                ]
            )
        )

        try:
            status_screen_svc.start()
            while True:
                time.sleep(1)
        except:
            status_screen_svc.wait_stop()


if __name__ == "__main__":
    Frontpanel("").start()
