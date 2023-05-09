import threading
from collections import defaultdict

class P2PNetwork:
    def __init__(self):
        self.nodes = {}
        self.message_queues = defaultdict(list)
        self.lock = threading.Lock()

    def register_node(self, node):
        self.nodes[node.node_id] = node

    def unregister_node(self, node):
        with self.lock:
            if node.node_id in self.nodes:
                del self.nodes[node.node_id]

    def broadcast(self, sender, message):
        with self.lock:
            for node_id, node in self.nodes.items():
                if node_id != sender.node_id:
                    self.message_queues[node_id].append(message)

    def receive(self, receiver):
        with self.lock:
            messages = self.message_queues[receiver.node_id]
            self.message_queues[receiver.node_id] = []
            return messages
