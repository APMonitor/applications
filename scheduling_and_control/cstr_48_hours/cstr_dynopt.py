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
#s = 'http://127.0.0.1'
a = 'products1'

apm(s,a,'clear all')
apm_load(s,a,'schedule.apm')

apm_info(s,a,'FV','eps')
apm_option(s,a,'eps.fstatus',1.0)

apm_info(s,a,'MV','Tc')
apm_option(s,a,'Tc.dcost',10.0)
apm_option(s,a,'Tc.dmax',10.0)
apm_option(s,a,'Tc.upper',350)
apm_option(s,a,'Tc.lower',200)

apm_option(s,a,'nlc.imode',6)
apm_option(s,a,'nlc.max_iter',5000)
apm_option(s,a,'nlc.solver',3)
apm_option(s,a,'nlc.nodes',2)

# initialize
apm_option(s,a,'Tc.status',0)
apm_meas(s,a,'eps',0.0)
csv_load(s,a,'schedule_init.csv')
output = apm(s,a,'solve')
print(output)

# solve with IPOPT
apm_option(s,a,'nlc.time_shift',0)
apm_option(s,a,'nlc.solver',3)
apm_option(s,a,'Tc.status',1)
apm(s,a,'clear csv')
csv_load(s,a,'schedule.csv')
apm_meas(s,a,'eps',1e-3)
output = apm(s,a,'solve')
apm_meas(s,a,'eps',1e-5)
output = apm(s,a,'solve')
print(output)

sol = apm_sol(s,a)

import matplotlib.pyplot as plt
plt.close('all')

plt.figure(1)

tf = 48

plt.subplot(3,1,1)
plt.plot(sol['time'],sol['tc'],'r--',linewidth=2)
plt.ylabel(r'$T_c (K)$')
plt.xlim([0,tf])
plt.legend([r'Jacket Temperature'],loc='best')

gap = 0.01
plt.subplot(3,1,2)
plt.plot(sol['time'],sol['ca'],'k--',linewidth=2)
plt.plot([0,tf],[0.35-gap,0.35-gap],'g-',linewidth=2)
plt.plot([0,tf],[0.25-gap,0.25-gap],'b-',linewidth=2)
plt.plot([0,tf],[0.12-gap,0.12-gap],'r-',linewidth=2)
plt.plot([0,tf],[0.35+gap,0.35+gap],'g-',linewidth=2)
plt.plot([0,tf],[0.25+gap,0.25+gap],'b-',linewidth=2)
plt.plot([0,tf],[0.12+gap,0.12+gap],'r-',linewidth=2)
plt.legend(['Concentration','Product 3','Product 2','Product 1'],loc='best')
plt.ylabel(r'$Schedule$')
plt.text(5,0.04,'$9/m^3$')
plt.text(20,0.18,'$11/m^3$')
plt.text(38,0.38,'$6/m^3$')
plt.xlim([0,tf])
plt.ylim([0.0,0.5])

plt.subplot(3,1,3)
plt.plot(sol['time'],sol['iprod[1]'],'r-',linewidth=2)
plt.plot(sol['time'],sol['iprod[2]'],'b-',linewidth=2)
plt.plot(sol['time'],sol['iprod[3]'],'g-',linewidth=2)
plt.plot(sol['time'],sol['q'],'k:',linewidth=2)
plt.plot([48],[120],'ro',markersize=8)
plt.plot([48],[130],'bo',markersize=8)
plt.plot([48],[150],'go',markersize=8)
plt.ylim([-10.0,210])
plt.legend([r'Product 1 > 120 $(m^3)$',   \
            r'Product 2 > 130 $(m^3)$',   \
            r'Product 3 > 150 $(m^3)$',   \
            r'Feed Flow Rate $(m^3/hr)$'],loc='best')
plt.ylabel(r'$Production$')
plt.xlabel('Time (hr)')
plt.xlim([0,tf])
plt.tight_layout()



plt.figure(2)

ax1 = plt.subplot2grid((4, 2), (0, 0), colspan=2)
ax2 = plt.subplot2grid((4, 2), (1, 0))
ax3 = plt.subplot2grid((4, 2), (1, 1))
ax4 = plt.subplot2grid((4, 2), (2, 0))
ax5 = plt.subplot2grid((4, 2), (2, 1))
ax6 = plt.subplot2grid((4, 2), (3, 0))
ax7 = plt.subplot2grid((4, 2), (3, 1))

p0 = ax1.plot(sol['time'],sol['pfcn'],'k-',linewidth=3)
ax1.set_xlim([0,tf])
ax1.set_ylabel(r'Profit/$m^3$')
ax1.text(40,9,'Profit Function')
ax1.text(3,2,'Product 1')
ax1.text(18,2,'Product 2')
ax1.text(35,2,'Product 3')

p1, = ax2.plot(sol['time'],sol['w[1]'],'b:',linewidth=3)
p2, = ax2.plot(sol['time'],sol['s1[1]'],'g-.',linewidth=3)
p3, = ax2.plot(sol['time'],sol['s2[1]'],'r--',linewidth=3)
ax2.set_xlim([0,tf])
ax2.set_ylim([-0.1,1.1])
ax2.set_ylabel(r'Step 1 ($P_1$ up)')
plt.legend([p1,p2,p3],['Step Function',\
                       'Slack 1',\
                       'Slack 2'])

ax3.plot(sol['time'],sol['w[2]'],'b:',linewidth=3)
ax3.plot(sol['time'],sol['s1[2]'],'g-.',linewidth=3)
ax3.plot(sol['time'],sol['s2[2]'],'r--',linewidth=3)
ax3.set_xlim([0,tf])
ax3.set_ylim([-0.1,1.1])
ax3.set_ylabel(r'Step 2 ($P_1$ down)')

ax4.plot(sol['time'],sol['w[3]'],'b:',linewidth=3)
ax4.plot(sol['time'],sol['s1[3]'],'g-.',linewidth=3)
ax4.plot(sol['time'],sol['s2[3]'],'r--',linewidth=3)
ax4.set_xlim([0,tf])
ax4.set_ylim([-0.1,1.1])
ax4.set_ylabel(r'Step 3 ($P_2$ up)')

ax5.plot(sol['time'],sol['w[4]'],'b:',linewidth=3)
ax5.plot(sol['time'],sol['s1[4]'],'g-.',linewidth=3)
ax5.plot(sol['time'],sol['s2[4]'],'r--',linewidth=3)
ax5.set_xlim([0,tf])
ax5.set_ylim([-0.1,1.1])
ax5.set_ylabel(r'Step 4 ($P_2$ down)')

ax6.plot(sol['time'],sol['w[5]'],'b:',linewidth=3)
ax6.plot(sol['time'],sol['s1[5]'],'g-.',linewidth=3)
ax6.plot(sol['time'],sol['s2[5]'],'r--',linewidth=3)
ax6.set_xlabel('Time (hr)')
ax6.set_xlim([0,tf])
ax6.set_ylim([-0.1,1.1])
ax6.set_ylabel(r'Step 5 ($P_3$ up)')

ax7.plot(sol['time'],sol['w[6]'],'b:',linewidth=3)
ax7.plot(sol['time'],sol['s1[6]'],'g-.',linewidth=3)
ax7.plot(sol['time'],sol['s2[6]'],'r--',linewidth=3)
ax7.set_xlabel('Time (hr)')
ax7.set_xlim([0,tf])
ax7.set_ylim([-0.1,1.1])
ax7.set_ylabel(r'Step 6 ($P_3$ down)')

plt.tight_layout()

plt.show()
