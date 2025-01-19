import time
import threading
import abc
import logging


class ServiceBase(abc.ABC):
    def __init__(self, description: str):
        self.__description__ = description
        self._thread = None
        self.__running__ = threading.Event()
        self.__running__.clear()

        self.__logger__ = logging.getLogger(self.__class__.__name__)

    def _main(self):
        self.__logger__.info(f"Started {self.__description__}!")
        self.__running__.set()
        self.__main__()
        self.__running__.clear()
        self.__logger__.info(f"Stopped {self.__description__}!")

    @abc.abstractmethod
    def __main__(self):
        raise NotImplementedError()

    def start(self):
        self.__logger__.info(f"Starting service...")
        self._thread = threading.Thread(target=self._main, name=self.__class__.__name__)
        self._thread.start()

    def stop(self):
        self.__logger__.info("Stopping service...")
        self.__running__.clear()

    def wait_stop(self):
        self.stop()
        if not self._thread:
            return
        self._thread.join()
