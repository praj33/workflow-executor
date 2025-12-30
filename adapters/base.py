from typing import Dict, Any
from abc import ABC, abstractmethod


class ExecutionAdapter(ABC):
    """
    Base class for all real-world execution adapters.
    """

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
