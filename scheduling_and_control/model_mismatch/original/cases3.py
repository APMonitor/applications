from APMonitor import *
import numpy as np
import matplotlib.pyplot as plt

s = 'http://127.0.0.1'
a = 'mismatch'

# optimize at mesh points
K = [3.0,1.0,0.2] # np.arange(0.2, 3.0, 0.1) # 0.1
tau = [0.2,1.0,5.0] # np.arange(0.2, 5.0, 0.1) # 0.1

t = np.linspace(0.0,10.0,20)
x = np.zeros(20)
y = np.zeros(20)

plt.figure()

subplot = 0
for j in range(3):
    for k in range(3):
        apm(s,a,'clear all')
        apm_load(s,a,'model.apm')
        csv_load(s,a,'model.csv')
        
        apm_option(s,a,'nlc.imode',6)
        
        apm_info(s,a,'FV','tau2')
        apm_info(s,a,'FV','K2')
        apm_info(s,a,'MV','u')
        apm_info(s,a,'SV','x')
        apm_info(s,a,'CV','y')
        
        apm_option(s,a,'u.status',1)
        apm_option(s,a,'u.dcost',01)
        apm_option(s,a,'u.fstatus',0)
        
        apm_option(s,a,'y.status',1)
        apm_option(s,a,'y.tau',1)
        apm_option(s,a,'y.sphi',5.0)
        apm_option(s,a,'y.splo',5.0)
        apm_option(s,a,'y.wsphi',100)
        apm_option(s,a,'y.wsplo',100)
        apm_option(s,a,'y.tr_init',0)
        apm_option(s,a,'y.fstatus',1)
        #apm_option(s,a,'nlc.web_plot_freq',1)
        
        apm_meas(s,a,'K2',K[j])
        apm_meas(s,a,'tau2',tau[k])
        
        for i in range(20):
            output = apm(s,a,'solve')
            print(output)
            sol = apm_sol(s,a)
            x[i] = apm_tag(s,a,'x.model')
            y[i] = apm_tag(s,a,'y.model')
            apm_meas(s,a,'y',sol['x'][1])
            print(str(i) + ' ' + str(x[i]))

        Km = str(K[j])
        taum = str(tau[k])
        subplot = subplot + 1
        plt.subplot(3,3,subplot)
        plt.plot(t,x,'b-',linewidth=3) #label=r'$K_m='+Km+' \tau_m=' + taum + '$')
        plt.plot([0,10],[5,5],'r:',linewidth=2)
        if j==2:
            if k==0:
                plt.xlabel(r'$\tau_m$=0.2')
            if k==1:
                plt.xlabel(r'$\tau_m$=1.0')
            if k==2:
                plt.xlabel(r'$\tau_m$=5.0')
        if k==0:
            if j==0:
                plt.ylabel(r'$K_m$=3.0')
            if j==1:
                plt.ylabel(r'$K_m$=1.0')
            if j==2:
                plt.ylabel(r'$K_m$=0.2')
            
plt.legend(loc=1)
# Save the figure as a PNG
plt.savefig('control.png')
plt.savefig('control.eps')

plt.show()

