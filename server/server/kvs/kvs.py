from typing import Any, Dict


class KeyNotFoundException(Exception):
    pass


class KVS:
    """This is a basic in-memory key-value store."""

    def __init__(self) -> None:
        self.mem: Dict[str, Any] = {}

    def put(self, key: str, val: Any) -> None:
        """Adds the given key-value pair to the store."""
        self.mem[key] = val

    def exists(self, key: str) -> bool:
        """Returns whether the given key exists in the store."""
        return key in self.mem

    def get(self, key: str) -> Any:
        """Returns the value associated with the given key.

        Raises:
            KeyNotFoundException: if the key does not exist.
        """
        if not self.exists(key):
            raise KeyNotFoundException(f"Key {key} not found.")
        return self.mem[key]
