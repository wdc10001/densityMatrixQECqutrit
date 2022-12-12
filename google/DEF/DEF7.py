import sys,os
sys.path.append(os.path.abspath(''))
import plotly.graph_objects as go
import numpy as np

title = 'qubit_ncycle11shots40000tH400pM0.03pCZ0.02pxyz0.01'
path = f'google/result/resultCSS7/{title}.txt'
CycleNum = 11
ExperimentNum = 40000

qnum = 7
d_2_qubit = [0,6]
d_4_qubit = [3]
meas_qubit = d_2_qubit + d_4_qubit
data_qubit = [1,2,4,5]

data_def = [[0 for i2 in range(CycleNum-1)] for i1 in range(qnum)]
with open(path,'r') as f:
    data_raw = [[ [] for i2 in range(qnum) ] for i1 in range(ExperimentNum)]
    for expi in range(ExperimentNum):
        data_line = f.readline()
        shift = 0
        for ii in range(qnum):
            data_num = CycleNum if ii in meas_qubit else 1
            data_raw[expi][ii] = [int(data_line[e]) if int(data_line[e])<2 else 1 for e in range(shift,shift+data_num)]
            shift += data_num

fig = go.Figure()
for ii in meas_qubit:
    for cycle_num in range(CycleNum-1):
        data_def[ii][cycle_num] = sum([int(data_raw[expi][ii][cycle_num] != data_raw[expi][ii][cycle_num+1]) for expi in range(ExperimentNum)])/ExperimentNum
    data_def[ii][0] =  sum([int(data_raw[expi][ii][0] != 0) for expi in range(ExperimentNum)])/ExperimentNum
    DEF_std = np.std(data_def[ii][1:-1],ddof=1)
    fig.add_trace(go.Scatter(x=list(range(CycleNum)),y=data_def[ii][:-1],mode='lines+markers',name=f'qubit{ii}_std{round(DEF_std,4)}'))

data_def[0].append(sum([int(data_raw[expi][1][0]) ^ int(data_raw[expi][2][0]) for expi in range(ExperimentNum)])/ExperimentNum)
data_def[3].append(sum([int(data_raw[expi][1][0]) ^ int(data_raw[expi][2][0]) ^ int(data_raw[expi][4][0]) ^ int(data_raw[expi][5][0]) for expi in range(ExperimentNum)])/ExperimentNum)
data_def[6].append(sum([int(data_raw[expi][4][0]) ^ int(data_raw[expi][5][0]) for expi in range(ExperimentNum)])/ExperimentNum)

d2_def = [0 for cycle_num in range(CycleNum-1)]
for cycle_num in range(CycleNum-1):
    for ii in d_2_qubit:
        d2_def[cycle_num] += data_def[ii][cycle_num]
    d2_def[cycle_num] /= len(d_2_qubit)
d4_def = [0 for cycle_num in range(CycleNum-1)]
for cycle_num in range(CycleNum-1):
    for ii in d_4_qubit:
        d4_def[cycle_num] += data_def[ii][cycle_num]
    d4_def[cycle_num] /= len(d_4_qubit)

fig.add_trace(go.Scatter(x=list(range(CycleNum)),y=d2_def[:-1],mode='lines+markers',name=f'd2_qubit'))
fig.add_trace(go.Scatter(x=list(range(CycleNum)),y=d4_def[:-1],mode='lines+markers',name=f'd4_qubit'))

fig.update_layout(xaxis=dict(tickmode='linear',dtick=1),xaxis_title='cycle',yaxis_title='DEF',title=title)
fig.show()