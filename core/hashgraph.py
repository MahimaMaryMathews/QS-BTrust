# core/hashgraph.py
import time

class Hashgraph:
    def __init__(self):
        self.events = {}

    def add(self, piid, tag_hash, ttl=60):
        self.events[piid] = {
            "tag_hash": tag_hash,
            "valid": 1,
            "timestamp": time.time(),
            "ttl": ttl
        }

    def revoke(self, piid):
        if piid in self.events:
            self.events[piid]["valid"] = 0

    def validate(self, piid, tag_hash=None):
        if piid not in self.events:
            return False

        event = self.events[piid]

        if event["valid"] != 1:
            return False

        if time.time() - event["timestamp"] > event["ttl"]:
            return False

        if tag_hash is not None and event["tag_hash"] != tag_hash:
            return False

        return True