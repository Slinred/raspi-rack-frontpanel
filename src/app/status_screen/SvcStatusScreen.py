import psutil
import subprocess
from PIL import ImageFont

from status_screen.StatusScreenBase import StatusScreenBase, Image, ImageDraw
from Constants import Constants


class SvcStatusScreen(StatusScreenBase):
    REDRAW_INTERVAL = 1

    def __init__(self, services: list[str | tuple[str, str]], display_time_s=10):
        super().__init__(
            Constants.SCREEN_WIDTH,
            Constants.SCREEN_HEIGHT,
            display_time_s,
            self.REDRAW_INTERVAL,
        )
        psutil.cpu_percent()

        self._services = services
        self._svc_idx = 0

    def __render__(self):
        def get_service_status(service_name):
            try:
                # Run the systemctl status command
                result = subprocess.run(
                    ["systemctl", "is-active", service_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                # Check the result
                return result.stdout.strip()
            except Exception as e:
                return f"Error while checking status: {str(e)}"

        line_count = len(self._services) if len(self._services) < 4 else 3

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

        lines = []
        for _ in range(line_count):
            service = self._services[self._svc_idx]
            if isinstance(service, tuple):
                service_name = service[0]
                display_name = service[1]
            else:
                service_name = display_name = service
            lines.append(f"{display_name}: {get_service_status(service_name)}")
            self._svc_idx = (self._svc_idx + 1) % len(self._services)

        draw.multiline_text(
            (Constants.DEFAULT_VSPACE, Constants.DEFAULT_HSPACE),
            "\n".join(lines),
            spacing=Constants.SCREEN_TEXT_CONFIG[line_count]["HSPACE"],
            font=font,
            fill=1,
        )

        self.__images__.put(image, block=True)
