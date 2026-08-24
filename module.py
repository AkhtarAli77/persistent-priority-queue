import json
import os


class PersistentPriorityQueue:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.queue = []
        self._load()

    def _load(self):
        """Load queue data from the JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.queue = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.queue = []
        else:
            self.queue = []

    def _save(self):
        """Save queue data to the JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.queue, file, indent=4)

    def insert(self, item, priority):
        """Insert an item with a priority."""
        self.queue.append({
            "item": item,
            "priority": priority
        })

        self.queue.sort(key=lambda x: x["priority"])
        self._save()

    def extract_min(self):
        """Remove and return the item with the smallest priority."""
        if self.is_empty():
            return None

        item = self.queue.pop(0)
        self._save()

        return item

    def extract_max(self):
        """Remove and return the item with the largest priority."""
        if self.is_empty():
            return None

        item = self.queue.pop()
        self._save()

        return item

    def peek(self):
        """Return the highest-priority item without removing it."""
        if self.is_empty():
            return None

        return self.queue[0]

    def update(self, item, new_priority):
        """Update the priority of an existing item."""
        for entry in self.queue:
            if entry["item"] == item:
                entry["priority"] = new_priority
                self.queue.sort(key=lambda x: x["priority"])
                self._save()
                return True

        return False

    def delete(self, item):
        """Delete an item from the queue."""
        for i, entry in enumerate(self.queue):
            if entry["item"] == item:
                self.queue.pop(i)
                self._save()
                return True

        return False

    def is_empty(self):
        """Check whether the queue is empty."""
        return len(self.queue) == 0