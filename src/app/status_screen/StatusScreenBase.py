from PIL import Image, ImageDraw
import logging
import threading
import abc
import queue
from Constants import Constants


class StatusScreenBase(abc.ABC):
    """
    @brief  Base class defining a status screen on an display with fixed with
    """

    RENDER_COUNT = 2

    def __init__(
        self,
        width: int,
        height: int,
        display_time_s: int = 10,
        redraw_interval: float | int = Constants.SCREEN_REDRAW_INTERVAL,
    ):
        if not isinstance(width, int):
            raise TypeError("Param width must be int")
        if not isinstance(height, int):
            raise TypeError("Param height must be of type int")
        if not isinstance(display_time_s, int):
            raise TypeError("Param display_time_s must be of type int")
        if not isinstance(redraw_interval, (int, float)):
            raise TypeError("Param redraw_interval must be of type int or float")

        self.__logger__ = logging.getLogger(self.__class__.__name__)

        self.__width__ = width
        self.__height__ = height
        self.__display_time_s__ = display_time_s
        self._redraw_interval = redraw_interval
        self.__images__ = queue.Queue(self.RENDER_COUNT)
        self.__thread_lock__ = threading.Lock()
        self.__done_event__ = threading.Event()
        self.__done_event__.clear()
        # rendering threads will be handled as FIFO
        self._render_threads: list[threading.Thread] = [None, None]

        self.__logger__.debug(
            f"New instance created with size {'x'.join([str(width), str(height)])}px, display_time={display_time_s}s, redraw_interval={redraw_interval}s"
        )

    def stop(self):
        for thread in self._render_threads:
            if isinstance(thread, threading.Thread):
                self.__logger__.debug(f"Waiting for thread '{thread}' to terminate...")
                thread.join()

    def render(self, blocking=False):
        render_thread: threading.Thread = None
        for idx in range(self.RENDER_COUNT):
            # find the next free element and create a new render thread for this
            if (
                not self._render_threads[idx]
                or not self._render_threads[idx].is_alive()
            ):
                self._render_threads[idx] = threading.Thread(
                    target=self.__render__,
                    name=f"{self.__class__.__name__}-{self.render.__name__}-{idx}",
                )
                self.__logger__.debug(
                    f"Starting new renderer thread '{self._render_threads[idx].name}'..."
                )
                self._render_threads[idx].start()
                render_thread = self._render_threads[idx]
                break
        # if all render threads are active, pick the first one
        if not render_thread:
            self.__logger__.warning(
                f"All renderer threads are busy, declining new render request!"
            )
            render_thread = self._render_threads[0]

        if blocking:
            self.__logger__.debug(
                f"Waiting for thread '{render_thread}' to terminate..."
            )
            render_thread.join()

    def get_image(self) -> Image.Image:
        image = self.__images__.get()
        return image

    def get_display_time(self):
        return self.__display_time_s__

    def get_redraw_interval(self) -> float:
        return float(self._redraw_interval)

    def is_done(self) -> bool:
        return self.__done_event__.is_set()

    def __create_image__(self) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        with self.__thread_lock__:
            image = Image.new("1", (self.__width__, self.__height__), 0)
            draw = ImageDraw.Draw(image)

        return image, draw

    def __get_line_pixels__(self, start, end) -> list[tuple[int, int]]:
        # Create a blank image
        width, height = max(start[0], end[0]) + 1, max(start[1], end[1]) + 1
        with self.__thread_lock__:
            image = Image.new("1", (width, height), 0)  # 1-bit image (black and white)
            draw = ImageDraw.Draw(image)

        # Draw the line
        draw.line([start, end], fill=1, width=1)

        # Get the list of pixels
        pixels = []
        for y in range(height):
            for x in range(width):
                if (
                    image.getpixel((x, y)) == 1
                ):  # Check if the pixel is part of the line
                    pixels.append((x, y))

        return pixels

    def __get_pixels_by_color__(self, image: Image.Image, color: int = 0xFF):
        # Get the list of pixels
        pixels = []
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                if (
                    image.getpixel((x, y)) == color
                ):  # Check if the pixel is part of the line
                    pixels.append((x, y))

        return pixels

    def __hcenter_text__(self, text: str, draw: ImageDraw.ImageDraw) -> int:
        text_len = draw.textlength(text, draw.font)
        xpos = (draw._image.width - text_len) // 2
        return xpos

    def __add_rendered_image__(self, image: Image.Image):
        try:
            self.__images__.put(image, timeout=self._redraw_interval, block=True)
        except:
            self.__logger__.warning("image render queue is full, image discarded!")

    @abc.abstractmethod
    def __render__(self):
        raise NotImplementedError()
