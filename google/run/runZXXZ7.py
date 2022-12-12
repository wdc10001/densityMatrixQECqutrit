import sys,os
sys.path.append(os.path.abspath(''))
import cirq,time
from google.src.qcisToCirq import qcisToCirq
from google.circuits.ZXXZ7 import EC,ECM
from google.src.config import *
import multiprocessing
from functools import partial
import numpy as np
from google.src.qubitPara import *
from numpy import random

Q_ALL = [Q0,Q1,Q2,Q3,Q4,Q8,Q9]
Q_Data = [Q1,Q2,Q4,Q8]
MZ = f'''
{Y2M([Q2,Q4])}
'''
init_Z = f'''
{Y2P([Q2,Q4])}
'''
M_ALL = ''.join([f'MEASURE {QR_Dict[i]} {i}\n' for i in Q_ALL])

nD = 0
M_Dire = MZ
fHL = fWest
qData = Q_Data

pDict = {'px':px,'py':py,'pz':pz,'pM':pM,'pReset01':pReset01,'pReset02':pReset02,'pLeak':pLeak,'pCZ':pCZ,'pCT':pCT}
tDict = {'T1_10':T1_10,'T1_21':T1_21,'Tp_10':Tp_10,'Tp_21':Tp_21,'Th12':Th12,'tH':tH,'tCZ':tCZ}

start = time.time()
def runCirc(ncycle:int,shots:int)->list:
    # start = time.time()
    qcis = f'{init_Z}'+ncycle*f'{ECM(nD,tH,tCZ,tM,tR,pCT)}'+f'{EC(tH,tCZ,pCT)}{M_Dire}{M_ALL}'
    circuitList = qcisToCirq(qcis,qData,pDict,tDict,fHL,ten=False,eleven=False,circ=[]).matchline()
    circuit = cirq.Circuit(circuitList)
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    mDict = {i:result.measurements[i][0] for i in result.measurements}
    mList = [mDict[key] for i in Q_ALL for key in mDict if key[:3] == i]
    # print(time.time()-start)
    if shots%1000 == 0: print('ncycle',ncycle,'shots',shots,'time',time.time()-start)
    return mList

if __name__ == '__main__':
    # runCirc(8,0)
    shots = 10000
    pools = multiprocessing.Pool()
    for ncycle in range(10,11):
        result = pools.map(partial(runCirc,ncycle),range(shots))
        np.savetxt(f'google/result/resultZXXZ7/qubit_initX_ncycle{ncycle+1}shots{shots}tH400pM0.03pCZ0.02pxyz0.01.txt',result,fmt='%d',delimiter='')
    pools.close()
    pools.join()

#测试结果：2.3分钟一个周期