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
    qc = QuantumCircuit(1)
    qc.h(0)
    st.text(qc.draw())
    counts = run_sim(qc)
    fig = plot_histogram(counts)
    st.pyplot(fig)

# ---------------- ENTANGLEMENT ----------------
elif menu == "Entanglement Demo":
    st.header("Entanglement Demo 🔗")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    st.text(qc.draw())
    counts = run_sim(qc)
    fig = plot_histogram(counts)
    st.pyplot(fig)

# ---------------- GROVER ----------------
elif menu == "Grover’s Search":
    st.header("Grover’s Search Algorithm 🔎")
    n = st.slider("Number of Qubits", 2, 6, 3)
    target = st.text_input("Target Binary State", "101")
    if len(target) != n or not all(c in "01" for c in target):
        st.error("Target must match qubit count.")
    else:
        expr = " & ".join([f"{'' if b=='1' else '~'}x{i}" for i,b in enumerate(target)])
        oracle = PhaseOracle(expr)
        grover = Grover()
        circuit = grover.construct_circuit(oracle)
        backend = AerSimulator()
        circuit.measure_all()
        result = backend.run(circuit, shots=1024).result()
        counts = result.get_counts()
        fig = plot_histogram(counts)
        st.pyplot(fig)
        st.code(f"Most Likely Result → {max(counts, key=counts.get)}")
        st.text(circuit.draw())

# ---------------- CLASSICAL VS QUANTUM SPEED ----------------
elif menu == "Classical vs Quantum Speed":
    st.header("Classical vs Quantum Speed Comparison 📈")
    max_n = st.slider("Max Search Space Size (N)", 10, 10000, 1000)
    N = np.arange(1, max_n+1)
    classical = N
    quantum = np.sqrt(N)
    fig, ax = plt.subplots()
    ax.plot(N, classical, label="Classical O(N)")
    ax.plot(N, quantum, label="Grover O(√N)")
    ax.set_xlabel("Search Space Size")
    ax.set_ylabel("Operations")
    ax.legend()
    ax.set_title("Quantum Speed Advantage")
    st.pyplot(fig)

# ---------------- BLOCH SPHERE ----------------
elif menu == "Bloch Sphere Visualization":
    st.header("Bloch Sphere — Amplitude Growth 🌐")
    theta = st.slider("Rotation Angle (θ)", 0.0, np.pi, np.pi/4)
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    backend = AerSimulator(method="statevector")
    result = backend.run(qc).result()
    state = result.get_statevector()
    fig = plot_bloch_multivector(state)
    st.pyplot(fig)
    st.text(qc.draw())

# ---------------- SHOR + RSA DEMO ----------------
elif menu == "Shor’s Algorithm + RSA Crack":
    st.header("Shor’s Algorithm — RSA Breaking Demo 🔐")
    st.info("For demo purposes, classical factoring is used here.")
    N = st.number_input("Composite Number to Factor (RSA Modulus)", min_value=15, max_value=999, value=21)
    if st.button("Break RSA"):
        # Simple classical factoring
        factors = [(i, N//i) for i in range(2, N) if N % i == 0]
        if factors:
            p,q = factors[0]
            st.success(f"🔓 FACTORED: {N} = {p} × {q}")
        else:
            st.error("Failed to factor — try smaller composite numbers.")

# ---------------- QUANTUM TIC-TAC-TOE ----------------
elif menu == "Quantum Tic-Tac-Toe":
    st.header("🌀 Quantum Tic-Tac-Toe")
    BOARD_SIZE = 3
    backend = AerSimulator(method="statevector")

    # Initialize session state
    if "board" not in st.session_state:
        st.session_state.board = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        st.session_state.player = "X"
        st.session_state.quantum_moves = []
        st.session_state.quantum_target = []

    board = st.session_state.board
    player = st.session_state.player
    quantum_moves = st.session_state.quantum_moves
    quantum_target = st.session_state.quantum_target

    move_type = st.sidebar.radio("Move Type", ["Classical", "Quantum"])

    def switch_player():
        st.session_state.player = "O" if st.session_state.player == "X" else "X"

    def reset_game():
        st.session_state.board = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        st.session_state.player = "X"
        st.session_state.quantum_moves = []
        st.session_state.quantum_target = []

    def collapse_quantum(move):
        qc = QuantumCircuit(1)
        qc.h(0)
        state = backend.run(qc).result().get_statevector()
        prob_0 = np.abs(state[0])**2
        return move[0] if np.random.rand() < prob_0 else move[1]

    st.sidebar.button("Reset Game", on_click=reset_game)
    st.write(f"**Current Player:** {player}")

    # Board buttons
    for i in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE)
        for j in range(BOARD_SIZE):
            btn_label = str(board[i][j]) if board[i][j] else "-"
            if cols[j].button(btn_label, key=f"{i}-{j}"):
                if move_type=="Classical":
                    if not board[i][j]:
                        board[i][j] = player
                        switch_player()
                else:
                    if len(quantum_target) < 2:
                        quantum_target.append((i,j))
                    if len(quantum_target)==2:
                        quantum_moves.append((player, quantum_target.copy()))
                        quantum_target.clear()
                        switch_player()

    # Collapse quantum moves
    for p, move in quantum_moves:
        collapsed = collapse_quantum(move)
        board[collapsed[0]][collapsed[1]] = p
    st.session_state.board = board
    st.session_state.quantum_moves = []

# ---------------- QUANTUM RISK AUDITOR ----------------
elif menu == "Quantum Risk Auditor 🧪":
    st.header("Quantum Risk Auditor 🧪")
    encryption = st.selectbox("Select your encryption:", ["RSA-2048", "AES-256", "Kyber-768"])
    sensitivity = st.selectbox("Data Sensitivity:", ["Low","Medium","High"])
    if st.button("Run Audit"):
        risk_scores = {"RSA-2048": 95, "AES-256": 20, "Kyber-768": 5}
        time_to_crack = {"RSA-2048": "Hours (20M qubits)", "AES-256": "Millennia", "Kyber-768": "Unknown"}
        score = risk_scores[encryption]
        st.progress(score/100)
        st.warning(f"Quantum Vulnerability Score: {score}/100")
        st.info(f"Estimated Time to Crack: {time_to_crack[encryption]}")
        if score>50:
            st.error("⚠️ ACTION REQUIRED: Migrate to post-quantum cryptography.")
