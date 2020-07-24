def initialize_qubits(given_circuit, measurement_qubits, target_qubit):
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - START
    given_circuit.h(measurement_qubits)
    given_circuit.x(target_qubit)
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
def unitary_operator(given_circuit, control_qubit, target_qubit, theta):
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - START
    given_circuit.cu1(pi*theta,control_qubit,target_qubit)
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
def unitary_operator_exponent(given_circuit, control_qubit, target_qubit, theta, exponent):
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - START
    unitary_operator(given_circuit,control_qubit,target_qubit,exponent*theta)
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
def apply_iqft(given_circuit, measurement_qubits, n,theta):
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - START
    for qubit in range(n//2):
        given_circuit.swap(qubit,n-qubit-1)
    for j in range(n):
        for m in range(j):
            given_circuit.cu1(-pi*(2**(m-j)),m,j)
        given_circuit.h(j)    
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
def qpe_program(n, theta):
    
    # Create a quantum circuit on n+1 qubits (n measurement, 1 target)
    qc = QuantumCircuit(n+1, n)
    
    # Initialize the qubits
    initialize_qubits(qc, range(n), n)
    
    # Apply the controlled unitary operators in sequence
    for x in range(n):
        exponent = 2**(n-x)
        unitary_operator_exponent(qc, x, n, theta, exponent)
        
    # Apply the inverse quantum Fourier transform
    apply_iqft(qc, range(n), n,theta)
    
    # Measure all qubits
    qc.measure(range(n), range(n))
  
    return qc
    
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit import Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import operator
n = 5; theta = 0.5;pi = np.pi
mycircuit = qpe_program(n, theta)
mycircuit.draw(output="text")
simulator = Aer.get_backend('qasm_simulator')
counts = execute(mycircuit, backend=simulator, shots=1000).result().get_counts(mycircuit)
plot_histogram(counts)
plt.show()
highest_probability_outcome = max(counts.items(), key=operator.itemgetter(1))[0][::-1]
measured_theta = int(highest_probability_outcome, 2)/2**n
print("Using %d qubits with theta = %.2f, measured_theta = %.2f." % (n, theta, measured_theta))