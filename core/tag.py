# core/tag.py
import hashlib

def generate_verif_tag(responses, ts, nonce):
    return hashlib.sha256(
        b''.join(responses) + str(ts).encode() + nonce
    ).digest()

def f_vt(k):
    return k.to_bytes(2, 'big')

def generate_tag_hash(piid, verif_tag, k, ts):
    vt_component = hashlib.sha256(
        verif_tag + f_vt(k)
    ).digest()

    return hashlib.sha256(
        piid +
        vt_component +
        str(ts).encode()
    ).digest()