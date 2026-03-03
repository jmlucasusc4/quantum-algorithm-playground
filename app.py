import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.circuit.library import PhaseOracle
from qiskit_algorithms import Grover

# --- Page Config ---
st.set_page_config(page_title="Quantum Cybersecurity Lab", layout="wide")
st.title("⚛️ Quantum Cybersecurity Research Lab")

# --- Sidebar Navigation ---
menu = st.sidebar.selectbox("Choose Module", [
    "Superposition Demo",
    "Entanglement Demo",
    "Grover’s Search",
    "BB84 Protocol (QKD)",
    "Quantum Teleportation",
    "Bernstein-Vazirani",
    "Classical vs Quantum Speed",
    "Bloch Sphere Visualization",
    "Shor’s Algorithm + RSA Crack",
    "Quantum Risk Auditor 🧪"
])

# --- Utility Functions ---
def run_sim(qc, shots=1024):
    """Standard simulation utility for counts."""
    backend = AerSimulator()
    qc_copy = qc.copy()
    qc_copy.measure_all()
    job = backend.run(qc_copy, shots=shots)
    return job.result().get_counts()

# ---------------- SUPERPOSITION ----------------
if menu == "Superposition Demo":
    st.header("Superposition Demo ⚛️")
    st.write("Creating a 50/50 probability using a Hadamard (H) gate.")
    qc = QuantumCircuit(1)
    qc.h(0)
    st.pyplot(qc.draw(output='mpl'))
    counts = run_sim(qc)
    st.pyplot(plot_histogram(counts))

# ---------------- ENTANGLEMENT ----------------
elif menu == "Entanglement Demo":
    st.header("Entanglement Demo 🔗")
    st.write("Creating a Bell State (EPR Pair) where two qubits are perfectly correlated.")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    st.pyplot(qc.draw(output='mpl'))
    counts = run_sim(qc)
    st.pyplot(plot_histogram(counts))

# ---------------- GROVER'S SEARCH ----------------
elif menu == "Grover’s Search":
    st.header("Grover’s Search Algorithm 🔎")
    st.info("Quantum speedup for unstructured database searching.")
    n = st.slider("Number of Qubits", 2, 4, 3)
    target = st.text_input("Target Binary State", "1" + "0"*(n-1))
    
    if len(target) != n or not all(c in "01" for c in target):
        st.error(f"Target must be exactly {n} bits.")
    else:
        bit_expr = " & ".join([f"{'' if b=='1' else '~'}x{i}" for i, b in enumerate(target[::-1])])
        oracle = PhaseOracle(bit_expr)
        
        # Explicit iterations=1 to avoid Qiskit NoneType error
        grover = Grover(iterations=1)
        circuit = grover.construct_circuit(oracle)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Oracle Circuit")
            st.pyplot(circuit.draw(output='mpl'))
        with col2:
            st.write("### Search Results")
            st.pyplot(plot_histogram(run_sim(circuit)))
        st.success(f"Most Likely Result → **{max(run_sim(circuit), key=run_sim(circuit).get)}**")

# ---------------- BB84 PROTOCOL (QKD) ----------------
elif menu == "BB84 Protocol (QKD)":
    st.header("🔐 BB84 Quantum Key Distribution")
    st.write("Alice sends a qubit; Bob measures it. If Eve eavesdrops, the 'Collapse' alerts them.")
    eve_present = st.checkbox("Enable Eavesdropper (Eve)")
    
    # Alice's choice
    alice_bit = np.random.randint(2)
    alice_basis = np.random.randint(2) # 0: Z, 1: X
    
    qc = QuantumCircuit(1, 1)
    if alice_bit == 1: qc.x(0)
    if alice_basis == 1: qc.h(0) 
    
    if eve_present:
        # Eve intervenes
        eve_basis = np.random.randint(2)
        if eve_basis == 1: qc.h(0)
        qc.measure(0, 0)
        if eve_basis == 1: qc.h(0) 

    # Bob measures
    bob_basis = np.random.randint(2)
    if bob_basis == 1: qc.h(0)
    qc.measure(0, 0)
    
    backend = AerSimulator()
    res = backend.run(qc, shots=1).result().get_counts()
    bob_bit = int(list(res.keys())[0])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Alice Bit/Basis", f"{alice_bit} / {'X' if alice_basis else 'Z'}")
    col2.metric("Bob Basis", 'X' if bob_basis else 'Z')
    col3.metric("Bob Result", bob_bit)

    if alice_basis == bob_basis:
        if alice_bit == bob_bit:
            st.success("Key Match! No eavesdropping detected in this bit.")
        else:
            st.error("🚨 SECURITY ALERT: Eve detected! Basis matched but bits differ.")
    else:
        st.warning("Basis Mismatch: This qubit is discarded.")
    

# ---------------- QUANTUM TELEPORTATION ----------------
elif menu == "Quantum Teleportation":
    st.header("🛸 Quantum Teleportation")
    st.write("Moving a quantum state from Alice to Bob using entanglement.")
    
    qc = QuantumCircuit(3, 3)
    # The state to teleport (prepare Q0 in some state)
    qc.h(0); qc.t(0) 
    qc.barrier()
    # Create entanglement between Q1 and Q2
    qc.h(1); qc.cx(1, 2)
    qc.barrier()
    # Alice measures Q0 and Q1
    qc.cx(0, 1); qc.h(0)
    qc.measure([0,1], [0,1])
    qc.barrier()
    # Bob applies corrections based on Alice's classical bits
    qc.cx(1, 2); qc.cz(0, 2)
    
    st.pyplot(qc.draw(output='mpl'))
    st.info("The math proves that Qubit 2 now holds the original state of Qubit 0.")
    

# ---------------- BERNSTEIN-VAZIRANI ----------------
elif menu == "Bernstein-Vazirani":
    st.header("⚡ Bernstein-Vazirani Algorithm")
    st.write("Finding a hidden bitstring in exactly ONE query.")
    secret = st.text_input("Hidden Bitstring", "1101")
    
    if all(c in "01" for c in secret):
        n_bv = len(secret)
        qc = QuantumCircuit(n_bv + 1, n_bv)
        qc.x(n_bv); qc.h(range(n_bv + 1))
        qc.barrier()
        for i, bit in enumerate(reversed(secret)):
            if bit == '1': qc.cx(i, n_bv)
        qc.barrier()
        qc.h(range(n_bv))
        qc.measure(range(n_bv), range(n_bv))
        
        st.pyplot(qc.draw(output='mpl'))
        counts = run_sim(qc)
        st.success(f"Quantum computer output: **{list(counts.keys())[0]}**")
    

# ---------------- CLASSICAL VS QUANTUM SPEED ----------------
elif menu == "Classical vs Quantum Speed":
    st.header("Classical vs Quantum Speed Comparison 📈")
    max_n = st.slider("Max Search Space Size (N)", 10, 10000, 1000)
    N = np.arange(1, max_n+1)
    fig, ax = plt.subplots()
    ax.plot(N, N, label="Classical O(N)", color="red")
    ax.plot(N, np.sqrt(N), label="Grover O(√N)", color="cyan", linewidth=3)
    ax.set_xlabel("Search Space Size")
    ax.set_ylabel("Steps")
    ax.legend()
    st.pyplot(fig)

# ---------------- BLOCH SPHERE ----------------
elif menu == "Bloch Sphere Visualization":
    st.header("Bloch Sphere — State Rotation 🌐")
    theta = st.slider("Rotation Angle (θ)", 0.0, np.pi, np.pi/2)
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    qc.save_statevector() # Critical for AerSimulator
    
    backend = AerSimulator()
    state = backend.run(qc).result().get_statevector()
    st.pyplot(plot_bloch_multivector(state))
    st.write("Statevector:", state)
    

[Image of bloch sphere rotation]


# ---------------- SHOR'S / RSA ----------------
elif menu == "Shor’s Algorithm + RSA Crack":
    st.header("Shor’s Algorithm — RSA Breaking Demo 🔐")
    N = st.number_input("Composite Number (RSA Modulus)", 15, 999, 21)
    if st.button("Simulate Attack"):
        factors = [(i, N//i) for i in range(2, int(np.sqrt(N))+1) if N % i == 0]
        if factors:
            st.success(f"🔓 RSA CRACKED: {N} = {factors[0][0]} × {factors[0][1]}")
        else:
            st.error("Try a composite number like 15, 21, or 35.")

# ---------------- RISK AUDITOR ----------------
elif menu == "Quantum Risk Auditor 🧪":
    st.header("Quantum Risk Auditor 🧪")
    encryption = st.selectbox("Current Encryption:", ["RSA-2048", "AES-256", "Kyber-768"])
    if st.button("Analyze Vulnerability"):
        scores = {"RSA-2048": 95, "AES-256": 20, "Kyber-768": 5}
        st.progress(scores[encryption]/100)
        st.warning(f"Vulnerability Score: {scores[encryption]}/100")
