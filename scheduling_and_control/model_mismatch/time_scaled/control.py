from APMonitor import *
import numpy as np

if True:
    K_mesh = np.load('K_mesh.npy')
    tau_mesh = np.load('tau_mesh.npy')
    obj = np.load('obj.npy')
else:        
    s = 'http://127.0.0.1'
    a = 'mismatch'

    # optimize at mesh points
    K = np.arange(0.2, 3.0, 0.1) # 0.1
    tau = np.arange(0.2, 5.0, 0.1) # 0.1
    K_mesh, tau_mesh = np.meshgrid(K, tau)

    icycle = 0
    total = K_mesh.shape[0] * K_mesh.shape[1]
    x = np.zeros(20)
    y = np.zeros(20)

    # initialize objective matrix
    obj = np.empty_like(K_mesh)

    for j in range(K_mesh.shape[0]):
        for k in range(K_mesh.shape[1]):
            icycle = icycle + 1
            print('Cycle ' + str(icycle) + ' of ' + str(total)) 
            apm(s,a,'clear all')
            apm_load(s,a,'model.apm')
            csv_load(s,a,'model.csv')
            
            apm_option(s,a,'nlc.imode',6)
            
            apm_info(s,a,'FV','tau2')
            apm_info(s,a,'FV','K2')
            apm_info(s,a,'MV','u')
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
            
            apm_meas(s,a,'tau2',1.0)
            apm_meas(s,a,'K2',K_mesh[j,k])
            
            for i in range(20):
                apm(s,a,'solve')
                sol = apm_sol(s,a)
                x[i] = apm_tag(s,a,'x.model')
                y[i] = apm_tag(s,a,'y.model')
                apm_meas(s,a,'y',sol['x'][1])
                    
            obj[j,k] = np.sum(np.abs(y-5.0))

    # save results
    np.save('K_mesh',K_mesh)
    np.save('tau_mesh',tau_mesh)
    np.save('obj',obj)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(K_mesh, tau_mesh, obj, \
                       rstride=1, cstride=1, cmap=cm.coolwarm) #, \
                       #vmin = 7, vmax = 24, linewidth=0, antialiased=False)

ax.set_xlim3d(0.0, 3.0)
ax.set_ylim3d(0.0, 5.0)
#ax.set_zlim3d(0, 10)

ax.set_xlabel(r'Model Gain $(K_m)$')
ax.set_ylabel(r'Model Time Constant $(\tau_m)$')
ax.set_zlabel(r'$Objective \; \sum |y_i-5|$')
plt.savefig('3d_contour.png')
plt.savefig('3d_contour.eps')

# Create a contour plot
plt.figure()
# Weight contours
CS = plt.contour(K_mesh, tau_mesh, obj,[6.0,12.0,16.0,22.0,40.0,60.0,80.0,100.0,120.0])
plt.clabel(CS, inline=1, fontsize=10)
# Acceptable control
CS = plt.contour(K_mesh, tau_mesh, obj,[7.0],colors='k',linewidths=[4.0])
plt.clabel(CS, inline=1, fontsize=10)
# Poor control
CS = plt.contour(K_mesh, tau_mesh, obj,[30.0],colors='r',linewidths=[4.0])
plt.clabel(CS, inline=1, fontsize=10)
plt.plot([0.7,1.3],[0.5,0.5],'b--')
plt.plot([0.7,1.3],[1.5,1.5],'b--')
plt.plot([0.7,0.7],[0.5,1.5],'b--')
plt.plot([1.3,1.3],[0.5,1.5],'b--')
# Add some labels
plt.xlabel(r'Model Gain $(K_m)$')
plt.ylabel(r'Model Time Constant $(\tau_m)$')
plt.xlim([0.2,3.0])
plt.ylim([0.2,4.0])
#plt.legend(['Objective','Acceptable Control','Poor Control'])
# Save the figure as a PNG
plt.savefig('contour.png')
plt.savefig('contour.eps')

plt.show()

