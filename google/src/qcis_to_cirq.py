import re
import cirq
import google.src.noise_channel as NC
import google.src.qutrit_gate as QG
import numpy as np

class qcisToCirq():
    def __init__(self,qcis:str,qData:list,pDict:dict,tDict:dict,fHL:list,ten:bool,eleven:bool,circ:list) -> None:
        self.qcis,self.qData,self.pDict,self.tDict,self.fHL,self.circ,self.ten,self.eleven = qcis,qData,pDict,tDict,fHL,circ,ten,eleven

    def matchSQ(self,line_:re.Match,gate:cirq.Gate):
        nStr = line_.group(2)[1:]
        Qn = 'Q'+nStr
        if self.ten and Qn not in self.qData: nStr = '00'
        if self.eleven and Qn == 'Q05': nStr = '05'
        qutrit = cirq.LineQid(int(nStr),dimension=3)
        self.circ.append(gate.on(qutrit))
        pTh12 = self.tDict['tH']/self.tDict['Th12']
        self.circ.append(NC.LeakThermalChannel(pTh12,qutrit))
        self.circ.append(NC.SingleQutritNoiseChannel(self.pDict['px'][Qn],self.pDict['py'][Qn],self.pDict['pz'][Qn],qutrit))

    def matchline(self)->list:
        count = 0
        for line in self.qcis.split('\n'):
            line_ = re.match(r'([a-zA-Z0-9]*) ([a-zA-Z0-9]*) ?(.*)', line)
            if line_:
                if line_.group(1) == 'I':
                    nStr = line_.group(2)[1:]
                    Qn = 'Q'+nStr
                    if self.ten and Qn not in self.qData: nStr = '00'
                    if self.eleven and Qn == 'Q05': nStr = '05'
                    qutrit = cirq.LineQid(int(nStr),dimension=3)
                    tg = int(line_.group(3))
                    decay10 = 1-np.exp(-tg/self.tDict['T1_10'][Qn])
                    dephase10 = 1-np.exp(-tg/self.tDict['Tp_10'][Qn])
                    decay21 = 1-np.exp(-tg/self.tDict['T1_21'][Qn])
                    dephase21 = 1-np.exp(-tg/self.tDict['Tp_21'][Qn])
                    pTh12 = tg/self.tDict['Th12']
                    self.circ.append(NC.LeakThermalChannel(pTh12,qutrit))
                    self.circ.append(NC.DecayAndDephaseChannel(decay10,dephase10,decay21,dephase21).on(qutrit))
                if line_.group(1) == 'X2P':
                    self.matchSQ(line_,QG.X2p())
                if line_.group(1) == 'X2M':
                    self.matchSQ(line_,QG.X2m())
                if line_.group(1) == 'Y2P':
                    self.matchSQ(line_,QG.Y2p())
                if line_.group(1) == 'Y2M':
                    self.matchSQ(line_,QG.Y2m())
                if line_.group(1) == 'MEASURE':
                    nStr = line_.group(3)[1:]
                    Qn = 'Q'+nStr
                    if self.ten and Qn not in self.qData: nStr = '00'
                    if self.eleven and Qn == 'Q05': nStr = '05'
                    qutrit = cirq.LineQid(int(nStr),dimension=3)
                    self.circ.append(NC.BitFlipChannel(self.pDict['pM'][Qn]).on(qutrit))
                    self.circ.append(cirq.measure(qutrit,key=Qn+'m'+f'{count}'))
                    if Qn not in self.qData:
                        self.circ.append(QG.Reset012().on(qutrit))
                        self.circ.append(NC.Reset012Error(self.pDict['pReset01'][Qn],self.pDict['pReset02'][Qn],qutrit))
                    count += 1
                if line_.group(1) == 'GCZ':
                    n1 = line_.group(2)[1:3]
                    n2 = line_.group(2)[3:5]
                    if self.ten:
                        if ['Q'+n1,'Q'+n2] in self.fHL:
                            QnH,QnL = 'Q'+n1,'Q'+n2
                            if 'Q'+n1 in self.qData: 
                                qutritH,qutritL = cirq.LineQid(int(n1),dimension=3),cirq.LineQid(0,dimension=3)
                                if self.eleven and n2 == '05':
                                    qutritH,qutritL = cirq.LineQid(int(n1),dimension=3),cirq.LineQid(5,dimension=3)
                            else: 
                                qutritH,qutritL = cirq.LineQid(0,dimension=3),cirq.LineQid(int(n2),dimension=3)
                                if self.eleven and n1 == '05':
                                    qutritH,qutritL = cirq.LineQid(5,dimension=3),cirq.LineQid(int(n2),dimension=3)
                        else:
                            QnH,QnL = 'Q'+n2,'Q'+n1
                            if 'Q'+n1 in self.qData: 
                                qutritH,qutritL = cirq.LineQid(0,dimension=3),cirq.LineQid(int(n1),dimension=3)
                                if self.eleven and n2 == '05':
                                    qutritH,qutritL = cirq.LineQid(5,dimension=3),cirq.LineQid(int(n1),dimension=3)
                            else: 
                                qutritH,qutritL = cirq.LineQid(int(n2),dimension=3),cirq.LineQid(0,dimension=3)
                                if self.eleven and n1 == '05':
                                    qutritH,qutritL = cirq.LineQid(int(n2),dimension=3),cirq.LineQid(5,dimension=3)
                    else:
                        if ['Q'+n1,'Q'+n2] in self.fHL:
                            QnH,QnL = 'Q'+n1,'Q'+n2
                            qutritH,qutritL = cirq.LineQid(int(n1),dimension=3),cirq.LineQid(int(n2),dimension=3)
                        else:
                            QnH,QnL = 'Q'+n2,'Q'+n1
                            qutritH,qutritL = cirq.LineQid(int(n2),dimension=3),cirq.LineQid(int(n1),dimension=3)
                    self.circ.append(QG.CZ().on(qutritH,qutritL))
                    pTh12 = self.tDict['tCZ']/self.tDict['Th12']
                    self.circ.append(NC.LeakThermalChannel(pTh12,qutritH))
                    self.circ.append(NC.LeakThermalChannel(pTh12,qutritL))
                    self.circ.append(NC.DoubleQutritNoiseChannel(self.pDict['pLeak'],self.pDict['pCZ'][(QnH,QnL)],qutritH,qutritL))
                if line_.group(1) == 'GCT':
                    n1 = line_.group(2)[1:3]
                    n2 = line_.group(2)[3:5]
                    n3 = line_.group(2)[5:7]
                    n4 = line_.group(2)[7:9]
                    qutrit1 = cirq.LineQid(int(n1),dimension=3)
                    qutrit2 = cirq.LineQid(int(n2),dimension=3)
                    qutrit3 = cirq.LineQid(int(n3),dimension=3)
                    qutrit4 = cirq.LineQid(int(n4),dimension=3)
                    self.circ.append(NC.DoubleQutritNoiseChannel(0,1,qutrit1,qutrit2))
                    self.circ.append(NC.DoubleQutritNoiseChannel(0,1,qutrit3,qutrit4))
        return self.circ
