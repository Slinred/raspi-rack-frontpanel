import socket
import psutil

from PIL import ImageFont
from status_screen.StatusScreenBase import StatusScreenBase, Image, ImageDraw
from Constants import Constants


class MainStatusScreen(StatusScreenBase):
    def __init__(self, display_time_s=10):
        super().__init__(
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, display_time_s
        )

    def __render__(self):
        def get_ipv4_address(interface_name):
            addrs = psutil.net_if_addrs()  # Get all network interface addresses
            if interface_name in addrs:
                for addr in addrs[interface_name]:
                    if addr.family.name == "AF_INET":  # Check for IPv4
                        return addr.address
            return "?.?.?.?"  # Return None if no IPv4 address found

        line_count = 2
        image, draw = self.__create_image__()
        with self.__thread_lock__:
            try:
                font = ImageFont.truetype(
                    Constants.DEFAULT_FONT,
                    size=Constants.SCREEN_TEXT_CONFIG[line_count]["FONT_SIZE"],
                )
            except:
                font = ImageFont.load_default(
                    size=Constants.SCREEN_TEXT_CONFIG[line_count]["FONT_SIZE"]
                )

        draw.rectangle(
            [0, 0, self.__width__ - 1, self.__height__ - 1], fill=0, outline=1
        )

        draw.text(
            (self.__hcenter_text__(socket.gethostname(), draw), 2),
            socket.gethostname(),
            font=font,
            fill=1,
        )

        ip = get_ipv4_address("eth0")
        draw.text(
            (
                self.__hcenter_text__(ip, draw),
                (
                    2
                    + Constants.SCREEN_TEXT_CONFIG[line_count]["FONT_SIZE"]
                    + Constants.SCREEN_TEXT_CONFIG[line_count]["HSPACE"]
                ),
            ),
            ip,
            font=font,
            fill=1,
        )

        self.__images__.put(image, block=True)
