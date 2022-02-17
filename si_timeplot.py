import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import subprocess
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

pop1 = 100
init1 = 30
pop2 = 110
init2 = 0

b1 = 0.1 #Infectiousness on men
b2 = 0.01 #Infectiousness on women
n1 = 0.00333 #Recoveries of men (high -> shorter sickness lenght)
n2 = 0.00333 #Recoveries of women (high -> shorter sickness lenght)


args = ['./si.out', str(pop1), str(pop2), str(init1), str(init2), str(b1), str(b2), str(n1), str(n2)]
subprocess.run(args)

with open("si.csv") as csvfile:
    si = np.loadtxt(csvfile, delimiter="\t")

plt.plot(si[:,0],si[:,1],'black', linewidth=1.0)
plt.plot(si[:,0],si[:,3],'red', linewidth=1.0)
plt.plot(si[:,0],si[:,2],'blue', linewidth=1.0)
plt.plot(si[:,0],si[:,4],'green', linewidth=1.0)

r1 = n1/b1
r2 = n2/b2
plt.plot([0,600], [(1-r1*r2)/(r1+1),(1-r1*r2)/(r1+1)], 'red', linestyle = 'dotted')
plt.plot([0,600], [(1-r1*r2)/(r2+1),(1-r1*r2)/(r2+1)], 'green', linestyle = 'dotted')
plt.plot([0,600], [1-(1-r1*r2)/(r1+1),1-(1-r1*r2)/(r1+1)], 'black', linestyle = 'dotted')
plt.plot([0,600], [1-(1-r1*r2)/(r2+1),1-(1-r1*r2)/(r2+1)], 'blue', linestyle = 'dotted')

plt.xlabel("Days")
plt.ylabel("Proportion of population")
plt.xlim([0,600])
plt.legend(["Male susceptible", "Male infected", "Female susceptible","Female infected"])

plt.savefig('si_timeplot.pgf')
