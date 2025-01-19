import gpiod
import time

from services.ServiceBase import ServiceBase


class LedHeartbeatService(ServiceBase):
    def __init__(self, gpio_chip_num: int, pin: int):

        if not isinstance(gpio_chip_num, int):
            raise TypeError(
                "Param 'gpio_chip_num' must be of type int a valid gpiochip device number!"
            )
        if not isinstance(pin, int):
            raise TypeError(
                "Param pin must be of type int and a valid GPIO pin number!"
            )
        super().__init__("LED heartbeat service")
        self._gpio_chip = f"/dev/gpiochip{gpio_chip_num}"
        self._pin = pin

    def __main__(self):
        with gpiod.request_lines(
            self._gpio_chip,
            consumer=f"{self.__class__.__name__}-{self.__description__}",
            config={
                self._pin: gpiod.LineSettings(
                    direction=gpiod.line.Direction.OUTPUT,
                    output_value=gpiod.line.Value.ACTIVE,
                )
            },
        ) as request:
            while self.__running__.is_set():
                for _ in range(2):
                    request.set_value(self._pin, gpiod.line.Value.ACTIVE)
                    time.sleep(0.1)
                    request.set_value(self._pin, gpiod.line.Value.INACTIVE)
                    time.sleep(0.1)
                request.set_value(self._pin, gpiod.line.Value.ACTIVE)
                time.sleep(1)


if __name__ == "__main__":
    Led = LedHeartbeatService(4, 17)
    try:
        Led.start()
        time.sleep(10)
        Led.wait_stop()

    except KeyboardInterrupt:
        pass

    print("Exiting!")
