import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.circuit.library import PhaseOracle
from qiskit_algorithms import Grover

st.set_page_config(page_title="Quantum Cybersecurity Playground", layout="wide")
st.title("⚛️ Quantum Cybersecurity Research Lab")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox("Choose Module", [
    "Superposition Demo",
    "Entanglement Demo",
    "Grover’s Search",
    "Classical vs Quantum Speed",
    "Bloch Sphere Visualization",
    "Shor’s Algorithm + RSA Crack",
    "Quantum Tic-Tac-Toe",
    "Quantum Risk Auditor 🧪"
])

# ---------------- UTIL ----------------
def run_sim(qc, shots=1024):
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
    st.write("Creating a Bell State where two qubits are perfectly correlated.")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    st.pyplot(qc.draw(output='mpl'))
    counts = run_sim(qc)
    st.pyplot(plot_histogram(counts))

# ---------------- GROVER ----------------
elif menu == "Grover’s Search":
    st.header("Grover’s Search Algorithm 🔎")
    n = st.slider("Number of Qubits", 2, 4, 3)
    target = st.text_input("Target Binary State", "1" + "0"*(n-1))
    
    if len(target) != n or not all(c in "01" for c in target):
        st.error(f"Target must be exactly {n} bits (0s and 1s).")
    else:
        bit_expr = " & ".join([f"{'' if b=='1' else '~'}x{i}" for i, b in enumerate(target[::-1])])
        oracle = PhaseOracle(bit_expr)
        
        grover = Grover()
        circuit = grover.construct_circuit(oracle)
        
        # We use a copy for measurement to keep the original circuit clean
        meas_circuit = circuit.copy()
        meas_circuit.measure_all()
        
        backend = AerSimulator()
        result = backend.run(meas_circuit, shots=1024).result()
        counts = result.get_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(circuit.draw(output='mpl'))
        with col2:
            st.pyplot(plot_histogram(counts))
        
        st.success(f"Most Likely Result → **{max(counts, key=counts.get)}**")

# ---------------- CLASSICAL VS QUANTUM SPEED ----------------
elif menu == "Classical vs Quantum Speed":
    st.header("Classical vs Quantum Speed Comparison 📈")
    max_n = st.slider("Max Search Space Size (N)", 10, 10000, 1000)
    N = np.arange(1, max_n+1)
    fig, ax = plt.subplots()
    ax.plot(N, N, label="Classical O(N)", color="red")
    ax.plot(N, np.sqrt(N), label="Grover O(√N)", color="cyan", linewidth=3)
    ax.set_xlabel("Search Space Size")
    ax.set_ylabel("Operations Required")
    ax.legend()
    st.pyplot(fig)

# ---------------- BLOCH SPHERE ----------------
elif menu == "Bloch Sphere Visualization":
    st.header("Bloch Sphere — State Rotation 🌐")
    theta = st.slider("Rotation Angle (θ)", 0.0, np.pi, np.pi/2)
    
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    
    # FIX: Tell the simulator to save the statevector before any measurement happens
    qc.save_statevector()
    
    backend = AerSimulator()
    result = backend.run(qc).result()
    state = result.get_statevector()
    
    # Render Bloch Multivector
    fig = plot_bloch_multivector(state)
    st.pyplot(fig)
    st.write("Mathematical Statevector Representation:")
    st.code(state)

# ---------------- SHOR + RSA DEMO ----------------
elif menu == "Shor’s Algorithm + RSA Crack":
    st.header("Shor’s Algorithm — RSA Breaking Demo 🔐")
    N = st.number_input("Composite Number (RSA Modulus)", min_value=15, max_value=999, value=21)
    if st.button("Run Quantum Attack Simulation"):
        factors = [(i, N//i) for i in range(2, int(np.sqrt(N))+1) if N % i == 0]
        if factors:
            p, q = factors[0]
            st.success(f"🔓 RSA CRACKED: Factors are {p} and {q}")
        else:
            st.error("Number is prime or too complex for this demo.")

