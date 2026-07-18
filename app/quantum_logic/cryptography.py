# Original Author: Joshua Tosin Pamilerin (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def generate_quantum_key(num_bits: int = 256) -> str:
    """Generate a cryptographic key using quantum superposition and measurement."""
    qc = QuantumCircuit(num_bits, num_bits)
    qc.h(range(num_bits))          # Hadamard: put all qubits into superposition
    qc.measure(range(num_bits), range(num_bits))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1)
    counts = job.result().get_counts()

    bitstring = list(counts.keys())[0]
    return hex(int(bitstring, 2))[2:].zfill(num_bits // 4)
