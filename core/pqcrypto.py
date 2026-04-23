# core/pqcrypto.py

import ctypes
import os
import platform

# Detect OS and set correct library name
system = platform.system()

if system == "Windows":
    lib_name = "libpqc.dll"
elif system == "Darwin":
    lib_name = "libpqc.dylib"
else:
    lib_name = "libpqc.so"

lib_path = os.path.join(os.path.dirname(__file__), "../crypto", lib_name)

if not os.path.exists(lib_path):
    raise RuntimeError(
        f"{lib_name} not found. Compile crypto module first."
    )

lib = ctypes.CDLL(lib_path)

lib.pq_sig_length.restype = ctypes.c_size_t

SIG_LEN = lib.pq_sig_length()

class PQSigner:
    def sign(self, message: bytes) -> bytes:
        output = (ctypes.c_ubyte * SIG_LEN)()
        lib.pq_sign(message, len(message), output)
        return bytes(output)

    def verify(self, message: bytes, signature: bytes) -> bool:
        sig_array = (ctypes.c_ubyte * len(signature)).from_buffer_copy(signature)
        return lib.pq_verify(message, len(message), sig_array) == 1