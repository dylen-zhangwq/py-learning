from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Installer(ABC):
    def __init__(self) -> None:
        self._register_config()

    @abstractmethod
    def _register_config(self) -> None:
        """Register configurations for the installer"""
        raise NotImplementedError

    @abstractmethod
    def installed(self) -> Any:
        """:returns: a list of packages installed (JSON dump-able)"""
        raise NotImplementedError

    @abstractmethod
    def install(self, arguments: Any, section: str, of_type: str) -> None:
        raise NotImplementedError
