# core/puf.py
import hashlib
import numpy as np
from pypuf.simulation import XORArbiterPUF

class PUF:
    def __init__(self, secret):
        self.secret = secret

        self.n = 64
        self.puf = XORArbiterPUF(n=self.n, k=4)

    def evaluate(self, challenge, ts_req, ts_res):
        challenge_bits = np.unpackbits(
            np.frombuffer(challenge, dtype=np.uint8)
        )[:self.n]

        challenge_bits = 2 * challenge_bits - 1

        response = self.puf.eval(challenge_bits)

        raw = self.secret + str(response).encode()
        puf_out = hashlib.sha256(raw).digest()

        return hashlib.sha256(
            puf_out + str(ts_req).encode() + str(ts_res).encode()
        ).digest()