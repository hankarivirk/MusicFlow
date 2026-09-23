class QueueManager:
    def __init__(self):
        self._queues = {}

    def get_queue(self, chat_id: int):
        return self._queues.setdefault(chat_id, [])

    def add_to_queue(self, chat_id: int, track: dict):
        self.get_queue(chat_id).append(track)

    def pop_queue(self, chat_id: int):
        q = self.get_queue(chat_id)
        return q.pop(0) if q else None

    def clear_queue(self, chat_id: int):
        self.get_queue(chat_id).clear()

Queues = QueueManager()
