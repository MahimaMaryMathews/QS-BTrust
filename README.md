“QS-BTrust: A Quantum-Secure Privacy-Preserving Protocol with Revocation for Trusted Broadcasting in Integrated Vehicular Networks”

---

## Setup

1. Install liboqs (with Dilithium2 support): https://github.com/open-quantum-safe/liboqs  

2. Compile crypto module:

cd crypto

gcc -shared -o libpqc.so -fPIC pqc_sign.c -loqs   # Linux

gcc -shared -o libpqc.dll -fPIC pqc_sign.c -loqs  # Windows

gcc -shared -o libpqc.dylib -fPIC pqc_sign.c -loqs # macOS

3. Install dependencies:

pip install -r requirements.txt

---

## Run

python run_all.py --all

Options:

--protocol → protocol test 

--eval → performance evaluation 

--viz → traffic visualization  

---

## Notes

- This is a research prototype  

- Hashgraph is a lightweight abstraction  

- PQC uses liboqs (Dilithium2) via C integration  

---

## Author

Mahima Mary Mathews  