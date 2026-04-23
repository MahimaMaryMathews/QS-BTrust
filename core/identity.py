# core/identity.py
import hashlib
import os

def generate_pid(uid, pri_info, ts, nonce):
    return hashlib.sha256(uid + pri_info + str(ts).encode() + nonce).digest()

def generate_piid(pid, nonce, k):
    return hashlib.sha256(pid + nonce + k.to_bytes(2, 'big')).digest()