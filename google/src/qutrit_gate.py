import cirq
import numpy as np

class X2m(cirq.Gate):
    def __init__(self):
        super(X2m, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[1, 1j, 0],
                         [1j, 1, 0],
                         [0, 0, 1]]/ np.sqrt(2))

    def _circuit_diagram_info_(self, args):
        return 'X2m'

class X2p(cirq.Gate):
    def __init__(self):
        super(X2p, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[1, -1j, 0],
                         [-1j, 1, 0],
                         [0, 0, 1]]/ np.sqrt(2))

    def _circuit_diagram_info_(self, args):
        return 'X2p'

class Y2m(cirq.Gate):
    def __init__(self):
        super(Y2m, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[1, 1, 0],
                         [-1, 1, 0],
                         [0, 0, 1]]/ np.sqrt(2))

    def _circuit_diagram_info_(self, args):
        return 'Y2m'

class Y2p(cirq.Gate):
    def __init__(self):
        super(Y2p, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[1, -1, 0],
                         [1, 1, 0],
                         [0, 0, 1]]/ np.sqrt(2))

    def _circuit_diagram_info_(self, args):
        return 'Y2p'

class X02(cirq.Gate):
    def __init__(self):
        super(X02, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[0, 0, 1],
                         [0, 1, 0],
                         [1, 0, 0]])

    def _circuit_diagram_info_(self, args):
        return 'X02'

class X12(cirq.Gate):
    def __init__(self):
        super(X12, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([[1, 0, 0],
                         [0, 0, 1],
                         [0, 1, 0]])

    def _circuit_diagram_info_(self, args):
        return 'X12'

class Reset012(cirq.Gate):
    def __init__(self):
        super(Reset012, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _kraus_(self):
        return (np.array([[1,0,0],[0,0,0],[0,0,0]]),
                np.array([[0,1,0],[0,0,0],[0,0,0]]),
                np.array([[0,0,1],[0,0,0],[0,0,0]]))

    def _has_kraus_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args):
        return 'R12'

class Reset01(cirq.Gate):
    def __init__(self):
        super(Reset01, self)

    def _num_qubits_(self):
        return 1

    def _qid_shape_(self):
        return (3,)

    def _kraus_(self):
        return (np.array([[1,0,0],[0,0,0],[0,0,0]]),
                np.array([[0,1,0],[0,0,0],[0,0,0]]),
                np.array([[0,0,0],[0,0,0],[0,0,1]]))

    def _has_kraus_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args):
        return 'R1'

class CZ(cirq.Gate):
    def __init__(self):
        super(CZ, self)

    def _num_qubits_(self):
        return 2

    def _qid_shape_(self):
        return (3,3)

    def _unitary_(self):
        return np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, -1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 1]])

    def _circuit_diagram_info_(self, args):
        return 'CZ','CZ'

if __name__ == '__main__':
    q0,q1 = cirq.LineQid.range(2, dimension=3)
    circuit = cirq.Circuit(
        # Y2m().on(q0),
        # Y2m().on(q1),
        # CZ().on(q0,q1),
        # Y2p().on(q1),
        # Y2p().on(q0),
        cirq.measure(q0, key='m0'))
    result = cirq.Simulator().simulate(circuit,initial_state=[0,0,1])
    print(circuit)
    print(result)