from typing import Dict, List, Callable, Any
from src.domain import EventBus as EventBusProtocol


class EventBus(EventBusProtocol):
    """Global event bus for decoupled communication between components."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def publish(self, event: Any) -> None:
        """Publish an event to all subscribers."""
        event_type = type(event).__name__
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    # Log error but don't stop other handlers
                    print(f"Error in event handler for {event_type}: {e}")

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            if handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
                if not self._subscribers[event_type]:
                    del self._subscribers[event_type]

    def get_subscribers_count(self, event_type: str) -> int:
        """Get number of subscribers for an event type."""
        return len(self._subscribers.get(event_type, []))

    def clear_all_subscribers(self) -> None:
        """Clear all subscribers (useful for testing)."""
        self._subscribers.clear()


# Global event bus instance
event_bus = EventBus()