import slicer
from Utils.logger import logger

class ObserverManager:
    """Manages VTK observers to prevent leaks and organize event listening."""
    
    def __init__(self):
        self.observers = []

    def add_observer(self, node, event, callback):
        if not node:
            return
        tag = node.AddObserver(event, callback)
        self.observers.append((node, tag))
        logger.debug(f"Added observer for {event} on {node.GetName() if hasattr(node, 'GetName') else node}")

    def remove_all(self):
        for node, tag in self.observers:
            try:
                node.RemoveObserver(tag)
            except Exception:
                pass
        self.observers.clear()
        logger.debug("Removed all observers.")
