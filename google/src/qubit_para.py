from google.src.config import *
tH = 25
tCZ = 34
tM = 500
tR = 160
Th12 = 700000
pLeak = 8e-4
pCT = 9.5e-4

tH = 400
tCZ = 0
tM = 0
tR = 0
pLeak = 0.1
pCT = 0

pM = {Q0:0.0202825,Q1:0.012895,Q2:0.01651,Q3:0.0217675,Q4:0.0156625,Q5:0.02664,Q6:0.02419,Q7:0.0415325,Q8:0.0157925,Q9:0.0204225,Q10:0.02023,Q11:0.0119225,Q12:0.0142775,Q13:0.024005,Q14:0.020165,Q15:0.0203325,Q16:0.028835}
for i in pM: pM[i] = 0.01

pCZ = {(Q0,Q1):0.00373065,(Q2,Q0):0.00269513,(Q5,Q4):0.00508742,(Q5,Q10):0.00416312,(Q11,Q6):0.00646084,(Q11,Q12):0.0052115,(Q14,Q16):0.0155869,(Q15,Q16):0.00687236,(Q3,Q1):0.00656797,(Q2,Q3):0.00582391,(Q4,Q3):0.00417455,(Q3,Q8):0.00521475,(Q2,Q7):0.000990486,(Q7,Q6):0.00267779,(Q7,Q8):0.00610335,(Q7,Q12):0.00734976,(Q9,Q4):0.00726272,(Q9,Q8):0.00433387,(Q9,Q10):0.00655108,(Q14,Q9):0.00598616,(Q13,Q8):0.00421312,(Q13,Q12):0.00706892,(Q14,Q13):0.0146966,(Q15,Q13):0.00450499}
for i in pCZ: pCZ[i] = 0.01

pReset01 = {Q0:0.00815,Q3:0.0082125,Q5:0.001025,Q7:0.004725,Q9:0.000725,Q11:0,Q13:0,Q16:0.000325}
for i in pReset01: pReset01[i] = 0

pReset02 = {Q0:0,Q3:0,Q5:0,Q7:0,Q9:0,Q11:0,Q13:0,Q16:0}

px = py = pz = {Q0:0.00096303/3,Q1:0.000643401/3,Q2:0.000929993/3,Q3:0.00117476/3,Q4:0.00118143/3,Q5:0.00111441/3,Q6:0.00110168/3,Q7:0.00119987/3,Q8:0.000839588/3,Q9:0.000880877/3,Q10:0.0016446/3,Q11:0.000528111/3,Q12:0.0013969/3,Q13:0.00123634/3,Q14:0.00157196/3,Q15:0.000732493/3,Q16:0.00132455/3}
for i in [px,py,pz]:
    for j in i:
        i[j] = 0.01

T1_10 = {Q0:22.9*1000,Q1:26*1000,Q2:21.7*1000,Q3:23.1*1000,Q4:25.3*1000,Q5:22.1*1000,Q6:18.6*1000,Q7:21.2*1000,Q8:22*1000,Q9:26*1000,Q10:16.6*1000,Q11:17.5*1000,Q12:17.2*1000,Q13:17.9*1000,Q14:19.9*1000,Q15:18*1000,Q16:22.5*1000}

T1_21 = {i:T1_10[i]/2 for i in T1_10}

Tp_10 = {Q0:37.7*1000,Q1:18.7*1000,Q2:52.3*1000,Q3:26.6*1000,Q4:35.9*1000,Q5:34.4*1000,Q6:29.4*1000,Q7:31.7*1000,Q8:27.7*1000,Q9:14.8*1000,Q10:24.7*1000,Q11:31.9*1000,Q12:26.3*1000,Q13:30.1*1000,Q14:29.1*1000,Q15:27.1*1000,Q16:35*1000}

Tp_21 = Tp_10