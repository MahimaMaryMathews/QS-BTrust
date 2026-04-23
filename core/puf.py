# core/puf.py
import hashlib

class PUF:
    def __init__(self, secret):
        self.secret = secret

    def evaluate(self, challenge, ts_req, ts_res):
        raw = self.secret + challenge
        puf_out = hashlib.sha256(raw).digest()

        return hashlib.sha256(
            puf_out + str(ts_req).encode() + str(ts_res).encode()
        ).digest()