import os

from PIL import Image, ImageDraw
from status_screen.StatusScreenBase import StatusScreenBase
from Constants import Constants


class BootScreen(StatusScreenBase):

    SCREEN_PROGRESSBAR_START = (14, 14)
    REDRAW_INTERVAL = 0.1
    BOOT_TIME = 3
    SEGMENTATION = 4

    BACKGROUND_IMAGE = "_background.bmp"
    HEARTBEAT_IMAGE = "_heartbeat.bmp"

    def __init__(self, display_time_s=0):
        super().__init__(
            Constants.SCREEN_WIDTH,
            Constants.SCREEN_HEIGHT,
            display_time_s,
            self.REDRAW_INTERVAL,
        )

        self._progress = 0

        self._curimg = None

        with self.__thread_lock__:
            self._background_img = Image.open(
                os.path.join(
                    Constants.RES_DIR,
                    self.__class__.__name__.lower() + self.BACKGROUND_IMAGE,
                ),
                formats=["BMP"],
            )
            self._background_img.load()
            self._heartbeat_img = Image.open(
                os.path.join(
                    Constants.RES_DIR,
                    self.__class__.__name__.lower() + self.HEARTBEAT_IMAGE,
                ),
                formats=["BMP"],
            )
            self._heartbeat_img.load()

    def __render__(self):
        if self._progress >= 120:
            self.__done_event__.set()

        if self._progress > 100:
            self._progress += 100 / (self.BOOT_TIME / self.REDRAW_INTERVAL)
            self.__add_rendered_image__(self._curimg)
            return

        image, draw = self.__create_image__()

        for pixel in self.__get_pixels_by_color__(self._background_img):
            draw.point(pixel, 1)

        draw.line(
            [
                (
                    self.SCREEN_PROGRESSBAR_START[0] + self._progress,
                    self.SCREEN_PROGRESSBAR_START[1],
                ),
                (
                    self.SCREEN_PROGRESSBAR_START[0] + 100,
                    self.SCREEN_PROGRESSBAR_START[1],
                ),
            ],
            fill=1,
        )

        hb_pixels = self.__get_pixels_by_color__(self._heartbeat_img)
        hb_pixels.sort(key=lambda x: x[0])  # sort pixels from left to right
        draw.point(
            [
                (
                    pixel[0] + self.SCREEN_PROGRESSBAR_START[0],
                    self.SCREEN_PROGRESSBAR_START[1]
                    + (pixel[1] - (self._heartbeat_img.height // 2)),
                )
                for pixel in hb_pixels
                if pixel[0] <= self._progress
            ],
            fill=1,
        )

        self._progress += 100 / ((self.BOOT_TIME * 1.25) / self.REDRAW_INTERVAL)
        self._curimg = image
        self.__add_rendered_image__(image)
