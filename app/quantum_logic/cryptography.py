# Original Author: Oluwatosin Olalere (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

import math
import random
import base64
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

simulator = AerSimulator()


def generate_quantum_key(num_bits: int = 256) -> str:
    """Generate a cryptographic key using quantum superposition and measurement."""
    qc = QuantumCircuit(num_bits, num_bits)
    qc.h(range(num_bits))
    qc.measure(range(num_bits), range(num_bits))

    job = simulator.run(qc, shots=1)
    bitstring = list(job.result().get_counts().keys())[0]
    return hex(int(bitstring, 2))[2:].zfill(num_bits // 4)


def score_entropy(num_bits: int = 64, shots: int = 1024) -> dict:
    """Measure the Shannon entropy of a quantum circuit's output distribution."""
    qc = QuantumCircuit(num_bits, num_bits)
    qc.h(range(num_bits))
    qc.measure(range(num_bits), range(num_bits))

    counts = simulator.run(qc, shots=shots).result().get_counts()
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    max_entropy = math.log2(total)
    score = round(entropy / max_entropy, 6) if max_entropy > 0 else 0.0

    return {"entropy_score": score, "unique_outcomes": len(counts), "shots": shots}


def quantum_otp_encrypt(plaintext: str) -> dict:
    """Encrypt plaintext using a quantum-random One-Time Pad."""
    num_bytes = len(plaintext.encode())
    num_bits = num_bytes * 8

    qc = QuantumCircuit(num_bits, num_bits)
    qc.h(range(num_bits))
    qc.measure(range(num_bits), range(num_bits))

    bitstring = list(simulator.run(qc, shots=1).result().get_counts().keys())[0]
    key_bytes = int(bitstring, 2).to_bytes(num_bytes, byteorder="big")

    plaintext_bytes = plaintext.encode()
    ciphertext_bytes = bytes(a ^ b for a, b in zip(plaintext_bytes, key_bytes))

    return {
        "ciphertext": base64.b64encode(ciphertext_bytes).decode(),
        "key": base64.b64encode(key_bytes).decode(),
        "message_length": num_bytes,
    }


def quantum_otp_decrypt(ciphertext_b64: str, key_b64: str) -> dict:
    """Decrypt a One-Time Pad ciphertext using the original quantum key."""
    ciphertext = base64.b64decode(ciphertext_b64)
    key = base64.b64decode(key_b64)
    if len(ciphertext) != len(key):
        raise ValueError("Key length must match ciphertext length.")
    plaintext = bytes(a ^ b for a, b in zip(ciphertext, key)).decode()
    return {"plaintext": plaintext}


def simulate_bb84(num_bits: int = 16) -> dict:
    """Simulate the BB84 Quantum Key Distribution protocol with eavesdropping detection."""
    # Alice generates random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.choice(["Z", "X"]) for _ in range(num_bits)]
    bob_bases = [random.choice(["Z", "X"]) for _ in range(num_bits)]

    bob_results = []
    for bit, a_base, b_base in zip(alice_bits, alice_bases, bob_bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if a_base == "X":
            qc.h(0)
        if b_base == "X":
            qc.h(0)
        qc.measure(0, 0)
        result = list(simulator.run(qc, shots=1).result().get_counts().keys())[0]
        bob_results.append(int(result))

    # Sift: keep only bits where bases matched
    matching = [i for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    alice_key = [alice_bits[i] for i in matching]
    bob_key = [bob_results[i] for i in matching]

    # Error rate on matching bits reveals eavesdropping
    errors = sum(a != b for a, b in zip(alice_key, bob_key))
    error_rate = round(errors / len(alice_key), 4) if alice_key else 0.0
    eavesdropping_detected = error_rate > 0.1

    shared_key = "".join(str(b) for a, b in zip(alice_key, bob_key) if a == b)

    return {
        "sifted_key_length": len(alice_key),
        "shared_key": shared_key,
        "error_rate": error_rate,
        "eavesdropping_detected": eavesdropping_detected,
    }
