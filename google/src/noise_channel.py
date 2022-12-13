import cirq
import numpy as np
from numpy import random
from google.src.qutrit_gate import *
from scipy.linalg import sqrtm

class IdentityChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _qid_shape_(self):
        return (3,)

    def _mixture_(self):
        ps = [1 - self._p, self._p]
        ops = [np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([[1,0,0],[0,1,0],[0,0,1]])]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"ID"

class BitAndPhaseFlipChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _qid_shape_(self):
        return (3,)

    def _mixture_(self):
        ps = [1 - self._p, self._p]
        ops = [np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([[0,-1j,0],[1j,0,0],[0,0,1]])]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"BPF"

class BitFlipChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _qid_shape_(self):
        return (3,)

    def _mixture_(self):
        ps = [1 - self._p, self._p]
        ops = [np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([[0,1,0],[1,0,0],[0,0,1]])]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"BF"

class PhaseFlipChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _qid_shape_(self):
        return (3,)

    def _mixture_(self):
        ps = [1 - self._p, self._p]
        ops = [np.array([[1,0,0],[0,1,0],[0,0,1]]), np.array([[1,0,0],[0,-1,0],[0,0,1]])]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"PF"

# class DecayAndDephaseChannel(cirq.Gate):
#     def _num_qubits_(self) -> int:
#         return 1

#     def __init__(self, decay10: float, dephase10:float, decay21: float, dephase21:float,pTh12:float) -> None:
#         '''
#         decay or dephase = 1-exp(-t/T)
#         pTh12 is the probability of 1 <-> 2 thermal excitation
#         '''
#         self._decay10 = decay10
#         self._dephase10 = dephase10
#         self._decay21 = decay21
#         self._dephase21 = 0
#         self._pTh12 = pTh12

#     def _qid_shape_(self)->tuple:
#         return (3,)

#     def _kraus_(self)->tuple:
#         return (
#             np.array([[1, 0, 0], [0, np.sqrt(1-self._decay10-self._dephase10-self._pTh12), 0], [0, 0, np.sqrt(1-self._decay21-self._dephase21-self._pTh12)]]),
#             np.array([[0, np.sqrt(self._decay10), 0], [0, 0, 0], [0, 0, 0]]),
#             np.array([[0, 0, 0], [0, 0, np.sqrt(self._decay21)], [0, 0, 0]]),
#             np.array([[0, 0, 0], [0, np.sqrt(self._dephase10), 0], [0, 0, 0]]),
#             np.array([[0, 0, 0], [0, 0, 0], [0, 0, np.sqrt(self._dephase21)]]),
#             np.array([[0, 0, 0], [0, 0, np.sqrt(self._pTh12)], [0, np.sqrt(self._pTh12), 0]])
#         )

#     def _has_kraus_(self) -> bool:
#         return True

#     def _circuit_diagram_info_(self, args) -> str:
#         # return f"DecayAndDephase({self._decay10},{self._dephase10},{self._decay21},{self._dephase21})"
#         return "DaD"

class DecayAndDephaseChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, decay10: float, dephase10:float, decay21: float, dephase21:float) -> None:
        '''
        decay or dephase = 1-exp(-t/T)
        '''
        self._decay10 = decay10
        self._dephase10 = dephase10
        self._decay21 = decay21
        self._dephase21 = 0

    def _qid_shape_(self)->tuple:
        return (3,)

    def _kraus_(self)->tuple:
        return (
            np.array([[1, 0, 0], [0, np.sqrt(1-self._decay10-self._dephase10), 0], [0, 0, np.sqrt(1-self._decay21-self._dephase21)]]),
            np.array([[0, np.sqrt(self._decay10), 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 0, 0], [0, 0, np.sqrt(self._decay21)], [0, 0, 0]]),
            np.array([[0, 0, 0], [0, np.sqrt(self._dephase10), 0], [0, 0, 0]]),
            np.array([[0, 0, 0], [0, 0, 0], [0, 0, np.sqrt(self._dephase21)]])
        )

    def _has_kraus_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return "De"

def LeakThermalChannel(pTh12:float,qutrit:cirq.Qid)->cirq.Gate:
    errorRate = random.random()
    if errorRate < pTh12:
        return X12().on(qutrit)
    else:
        return IdentityChannel(1).on(qutrit)

class LeakCzChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 2

    def __init__(self, pLeak: float) -> None:
        self._pLeak = pLeak

    def _qid_shape_(self)->tuple:
        return (3,3)

    # def _kraus_(self)->tuple[np.ndarray]:
    #     s02 = np.array([[0],[0],[1],[0],[0],[0],[0],[0],[0]])
    #     s11 = np.array([[0],[0],[0],[0],[1],[0],[0],[0],[0]])
    #     K1 = np.sqrt(self._pLeak)*(np.dot(s02,s11.T)+np.dot(s11,s02.T))
    #     K0 = sqrtm(np.identity(9)-K1.T.conjugate()*K1)
    #     return (K0,K1)

    # def _has_kraus_(self) -> bool:
    #     return True

    def _mixture_(self)->tuple:
        ps = [1 - self._pLeak, self._pLeak]
        ops = [np.identity(9),
               np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 1]])]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return (f"LC",f"LC")

def SingleQutritNoiseChannel(px:float,py:float,pz:float,qutrit:cirq.Qid)->cirq.Gate:
    errorRate = random.random()
    if errorRate < px:
        return BitFlipChannel(1).on(qutrit)
    elif errorRate < px+py:
        return BitAndPhaseFlipChannel(1).on(qutrit)
    elif errorRate < px+py+pz:
        return PhaseFlipChannel(1).on(qutrit)
    else:
        return IdentityChannel(1).on(qutrit)

def DoubleQutritNoiseChannel(pLeak:float,pCZ:float,qutritH:cirq.Qid,qutritL:cirq.Qid)->list:
    errorRate = random.random()
    channelList1 = [IdentityChannel(1).on(qutritH),BitFlipChannel(1).on(qutritH),BitAndPhaseFlipChannel(1).on(qutritH),PhaseFlipChannel(1).on(qutritH)]
    channelList2 = [IdentityChannel(1).on(qutritL),BitFlipChannel(1).on(qutritL),BitAndPhaseFlipChannel(1).on(qutritL),PhaseFlipChannel(1).on(qutritL)]
    if errorRate < pLeak:
        return LeakCzChannel(1).on(qutritH,qutritL)
    errorRate = random.random()
    if errorRate < pCZ:
        channelList = [random.choice(channelList1,1),random.choice(channelList2,1)]
        if channelList1[0] in channelList and channelList2[0] in channelList:
            return DoubleQutritNoiseChannel(0,1,qutritH,qutritL)
        else:
            return channelList
    else:
        return [channelList1[0],channelList2[0]]

def Reset012Error(pReset01:float,pReset02:float,qutrit:cirq.Qid)->cirq.Gate:
    errorRate = random.random()
    if errorRate < pReset01:
        return BitFlipChannel(1).on(qutrit)
    elif errorRate < pReset01+pReset02:
        return X02().on(qutrit)
    else:
        return IdentityChannel(1).on(qutrit)

if __name__ == '__main__':
    # customChannel = LeakDecayAndDephaseChannel(0.1,0.2)
    # for kraus in cirq.kraus(customChannel):
    #     print(kraus, end="\n\n")

    # customChannel = LeakHeatChannel(p=0.05)
    # for prob, kraus in cirq.mixture(customChannel):
    #     print(f"With probability {prob}, apply\n", kraus, end="\n\n")

    import qutrit_gate as QG
    q0, q1 = cirq.LineQid(0, dimension=3),cirq.LineQid(1, dimension=3)
    # q0, q1 = cirq.LineQid.range(2, dimension=3)
    circuit = cirq.Circuit([
        QG.Y2p().on(q0),
        QG.Y2p().on(q0),
        QG.Y2m().on(q1),
        QG.CZ().on(q0,q1),
        QG.Y2p().on(q1),
        LeakCzChannel(1).on(q0,q1),
        # QG.Reset012().on(q0),
        cirq.measure([q0, q1]),
        # QG.Reset012().on(q0)
    ])
    # import qsimcirq
    for _ in range(1):
        sim = cirq.DensityMatrixSimulator()
        result = sim.simulate(circuit)
        print(circuit)
        print({i:result.measurements[i] for i in result.measurements})
        # qsim_simulator = qsimcirq.QSimSimulator()
        # qsim_results = qsim_simulator.run(circuit, repetitions=5)
        # print(qsim_results)