# simulation/node.py

import os
import time
import hashlib
from core.puf import PUF
from core.identity import generate_pid, generate_piid
from core.tag import generate_verif_tag, generate_tag_hash
from core.pqcrypto import PQSigner, SIG_LEN

class Node:
    def __init__(self, uid):
        self.uid = uid
        self.pri_info = os.urandom(16)

        self.puf = PUF(os.urandom(16))
        self.signer = PQSigner()

        self.nonce = os.urandom(8)
        self.k = 1

        self.pid = generate_pid(uid, self.pri_info, time.time(), self.nonce)
        self.piid = generate_piid(self.pid, self.nonce, self.k)

        self.verif_tag = None
        self.tag_hash = None

    # ===== Registration Phase =====
    def registration(self):
        responses = []
        ts_req = time.time()

        for _ in range(5):
            c = os.urandom(16)
            ts_res = time.time()
            r = self.puf.evaluate(c, ts_req, ts_res)
            responses.append(r)

        return responses

    # ===== Tag Generation =====
    def generate_tag(self):
        responses = self.registration()
        ts = time.time()

        self.verif_tag = generate_verif_tag(responses, ts, self.nonce)
        self.tag_hash = generate_tag_hash(self.piid, self.verif_tag, self.k, ts)

        return self.piid, self.tag_hash

    # ===== Broadcast =====
    def broadcast(self, message):
        ts = time.time()
        seq = os.urandom(4)
        nonce = os.urandom(8)
        geo = b"loc"

        # MNisender
        sender = (
            self.piid +
            hashlib.sha256(self.verif_tag + self.k.to_bytes(2, 'big')).digest() +
            str(ts).encode() +
            geo
        )

        # MNiTag
        tag = hashlib.sha256(
            message.encode() +
            str(ts).encode() +
            seq +
            nonce +
            sender
        ).digest()

        # PQ Signature (Dilithium)
        sig = self.signer.sign(tag)

        # MNihash
        msg_hash = hashlib.sha256(
            message.encode() + tag + sig
        ).digest()

        return {
            "M": message,
            "TS": ts,
            "PIID": self.piid,
            "sender": sender,
            "seq": seq,
            "nonce": nonce,
            "tag": tag,
            "sig": sig,
            "hash": msg_hash,
            "tag_hash": self.tag_hash
        }

    # ===== Verification =====
    def verify(self, pkt, hashgraph):

        # 1. Hashgraph validation
        if not hashgraph.validate(pkt["PIID"], pkt.get("tag_hash")):
            return False

        message = pkt["M"]
        ts = pkt["TS"]
        sender = pkt["sender"]
        seq = pkt["seq"]
        nonce = pkt["nonce"]
        tag = pkt["tag"]
        sig = pkt["sig"]

        # 2. Recompute tag 
        recomputed_tag = hashlib.sha256(
            message.encode() +
            str(ts).encode() +
            seq +
            nonce +
            sender
        ).digest()

        if recomputed_tag != tag:
            return False

        # 3. Recompute hash
        recomputed_hash = hashlib.sha256(
            message.encode() + tag + sig
        ).digest()

        if recomputed_hash != pkt["hash"]:
            return False

        # 4. PQ signature verification
        return self.signer.verify(tag, sig)