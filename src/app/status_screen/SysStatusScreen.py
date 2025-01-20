import shutil
import psutil
from PIL import ImageFont

from status_screen.StatusScreenBase import StatusScreenBase, Image, ImageDraw
from Constants import Constants


class SysStatusScreen(StatusScreenBase):
    def __init__(self, display_time_s=10):
        super().__init__(
            Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, display_time_s
        )
        psutil.cpu_percent()

        self._dirs = ["/"]
        self._dir_idx = 0

    def __render__(self):
        def get_root_filesystem_usage():
            # Get disk usage for the root filesystem
            total, used, free = shutil.disk_usage("/")

            # Convert to human-readable format (e.g., GB)
            total_gb = total / (1024**3)
            used_gb = used / (1024**3)
            free_gb = free / (1024**3)
            usage_percentage = (used / total) * 100

            return {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "usage_percentage": round(usage_percentage, 2),
            }

        line_count = 3
        lines = []
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

        lines.append(f"CPU: {psutil.cpu_percent():.1f} %")

        # Get RAM usage
        memory_info = psutil.virtual_memory()
        ram_total = memory_info.total / (1024**3)  # Convert bytes to GB
        ram_used = memory_info.used / (1024**3)  # Convert bytes to GB
        ram_usage = (ram_used / ram_total) * 100
        lines.append(f"RAM: {ram_used:.2f} / {ram_total:.2f} GB ({ram_usage:.2f} %)")

        # Get disk usage for currently displayed dir
        if len(self._dirs) > 0:
            dir = self._dirs[self._dir_idx]
            total, used, _ = shutil.disk_usage(dir)
            # Convert to human-readable format (e.g., GB)
            total_gb = total / (1024**3)
            used_gb = used / (1024**3)
            usage = (used / total) * 100
            lines.append(f"{dir}: {used_gb:.2f} / {total_gb:.2f} GB ({usage:.2f} %)")
            self._dir_idx = (self._dir_idx + 1) % len(self._dirs)

        draw.multiline_text(
            (Constants.DEFAULT_VSPACE, Constants.DEFAULT_HSPACE),
            "\n".join(lines),
            spacing=Constants.SCREEN_TEXT_CONFIG[line_count]["HSPACE"],
            font=font,
            fill=1,
        )

        self.__add_rendered_image__(image)
