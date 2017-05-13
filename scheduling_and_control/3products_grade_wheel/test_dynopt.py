from apm import *
import numpy as np

def signal_zoh(x,y,epsilon = 0.001):
    """
        Fills in the data from a Zero-Order Hold (stair-step) signal
    """
    deltaX = np.array(x[1:],dtype='float') - x[:-1]
    fudge = min(deltaX) *epsilon
    retX = np.zeros((len(x)*2-1,))
    retY = np.zeros((len(y)*2-1,))
    retX[0::2] = x
    retX[1::2] = x[1:]+fudge*np.sign(deltaX)
    retY[0::2] = y
    retY[1::2] = y[:-1]
    return retX,retY

s = 'http://byu.apmonitor.com'
a = 'products'

apm(s,a,'clear all')
apm_load(s,a,'schedule.apm')
csv_load(s,a,'schedule.csv')
apm_info(s,a,'MV','u')
apm_option(s,a,'u.status',1)
apm_option(s,a,'u.dcost',1.0)
apm_option(s,a,'u.dmax',0.16)
apm_option(s,a,'u.upper',8.0)
apm_option(s,a,'u.lower',0.0)
apm_option(s,a,'nlc.imode',6)
apm_option(s,a,'nlc.max_iter',200)
apm_option(s,a,'nlc.solver',3)
apm_option(s,a,'nlc.nodes',2)

output = apm(s,a,'solve')
print(output)

sol = apm_sol(s,a)


time1,u1 = signal_zoh(sol['time'],sol['u'])

import matplotlib.pyplot as plt
plt.figure(1)
plt.subplot(3,1,1)
plt.plot(sol['time'],sol['pfcn'],'b-',linewidth=2)
plt.plot(sol['time'],sol['x'],'k--',linewidth=2)
#plt.plot(sol['time'],sol['u'],'r-',linewidth=2)
plt.plot(time1,u1,'r-',linewidth=2)
plt.plot([10.0],[4.5],'ko',markersize=8)
plt.text(6.3,4.4,'Periodic')
plt.text(6.3,3.7,'Constraint')
plt.plot([7.2,10.0],[4.5,4.5],'k:')
plt.legend(['Product Profit','CV','MV'],loc='best')
plt.ylabel('Control')
plt.xlim([0.0,10.0])
plt.ylim([-0.1,6.1])

plt.subplot(3,1,2)
plt.plot(sol['time'],sol['x'],'k--',linewidth=2)
plt.plot([5.0,5.9],[0,0],'r-',linewidth=2)
plt.plot([1.7,4.1],[2,2],'b-',linewidth=2)
plt.plot([0.0,0.8],[4,4],'g-',linewidth=2)
plt.plot([5.0,5.9],[1,1],'r-',linewidth=2)
plt.plot([1.7,4.1],[3,3],'b-',linewidth=2)
plt.plot([0.0,0.8],[5,5],'g-',linewidth=2)

plt.plot([6.9,7.8],[2,2],'b-',linewidth=2)
plt.plot([6.9,7.8],[3,3],'b-',linewidth=2)

plt.plot([8.8,10.0],[4,4],'g-',linewidth=2)
plt.plot([8.8,10.0],[5,5],'g-',linewidth=2)

plt.legend(['Produced','Product A','Product B','Product C'],loc='best')
plt.ylabel('Schedule')
plt.ylim([-0.1,6.1])
plt.xlim([0.0,10.0])

ax = plt.subplot(3,1,3)
plt.plot(sol['time'],sol['iprod[1]'],'r:',linewidth=2)
plt.plot(sol['time'],sol['iprod[2]'],'b-',linewidth=2)
plt.plot(sol['time'],sol['iprod[3]'],'g--',linewidth=2)
plt.plot([6,5.1],[3,5],'k:')
plt.plot([6,10],[3,3],'k:')
plt.plot([6,10],[3,2],'k:')
plt.plot([6,7.1],[3,2],'k:')
plt.plot([5.1],[5.0],'bo',markersize=8)
plt.plot([7.1],[2.0],'ro',markersize=8)
#plt.plot([10.0],[0.0],'ro',markersize=8)
plt.plot([10.0],[2.0],'bo',markersize=8)
plt.plot([10.0],[3.0],'go',markersize=8)
plt.text(6.0,4.0,'Required')
plt.text(6.0,3.2,'Deliveries')
plt.ylim([-0.1,6.1])
plt.xlim([0.0,10.0])
plt.legend(['Product A','Product B','Product C'],loc='best')
plt.ylabel('Accumulated')
plt.xlabel('Time (hr)')

plt.show()
