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
    qc.measure_all()
    job = backend.run(qc, shots=shots)
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
        # Create oracle: Logic to flip phase of the target state
        # Reverse bit order for Qiskit convention (little-endian)
        bit_expr = " & ".join([f"{'' if b=='1' else '~'}x{i}" for i, b in enumerate(target[::-1])])
        oracle = PhaseOracle(bit_expr)
        
        grover = Grover()
        circuit = grover.construct_circuit(oracle)
        circuit.measure_all()
        
        backend = AerSimulator()
        result = backend.run(circuit, shots=1024).result()
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
    
    backend = AerSimulator(method="statevector")
    result = backend.run(qc).result()
    state = result.get_statevector()
    st.pyplot(plot_bloch_multivector(state))

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

# ---------------- QUANTUM TIC-TAC-TOE ----------------
elif menu == "Quantum Tic-Tac-Toe":
    st.header("🌀 Quantum Tic-Tac-Toe")
    if "board" not in st.session_state:
        st.session_state.board = np.full((3, 3), None)
        st.session_state.player = "X"

    def reset_game():
        st.session_state.board = np.full((3, 3), None)
        st.session_state.player = "X"

    st.sidebar.button("Reset Game", on_click=reset_game)
    
    # Simple Logic for Quantum-Style Play
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            label = st.session_state.board[i, j] if st.session_state.board[i, j] else "-"
            if cols[j].button(label, key=f"cell-{i}-{j}"):
                if st.session_state.board[i, j] is None:
                    # Simulation of "Quantum Collapse"
                    outcome = "X" if np.random.random() > 0.5 else "O"
                    st.session_state.board[i, j] = outcome
                    st.session_state.player = "O" if st.session_state.player == "X" else "X"
                    st.rerun()

# ---------------- QUANTUM RISK AUDITOR ----------------
elif menu == "Quantum Risk Auditor 🧪":
    st.header("Quantum Risk Auditor 🧪")
    encryption = st.selectbox("Select your encryption:", ["RSA-2048", "AES-256", "Kyber-768"])
    if st.button("Run Audit"):
        risk_scores = {"RSA-2048": 95, "AES-256": 20, "Kyber-768": 5}
        score = risk_scores[encryption]
        st.progress(score/100)
        st.warning(f"Quantum Vulnerability Score: {score}/100")
        if score > 50:
            st.error("⚠️ HIGH RISK: Migrate to Post-Quantum Cryptography (PQC) immediately.")
        else:
            st.success("✅ LOW RISK: This algorithm is currently Quantum-Resistant.")
