from apm import *

s = 'http://byu.apmonitor.com'
a = 'smr'

apm(s,a,'clear all')

apm_load(s,a,'mpc.apm')
csv_load(s,a,'mpc.csv')

apm_option(s,a,'nlc.imode',6)

apm(s,a,'solve')

apm_web(s,a)
