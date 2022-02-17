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

pop = 80000000
init = 100

b = 0.8 #Infectiousness
m = 0.01 #Immunity loss
n = 0.333 #Recoveries (high -> shorter sickness lenght)


args = ['./sirs.out', str(pop), str(init), str(b), str(m), str(n)]
subprocess.run(args)

with open("sirs.csv") as csvfile:
    sirs = np.loadtxt(csvfile, delimiter="\t")

plt.plot(sirs[:,0],sirs[:,1],'black', linewidth=1.0)
plt.plot(sirs[:,0],sirs[:,2],'red', linewidth=1.0)
plt.plot(sirs[:,0],sirs[:,3],'blue', linewidth=1.0)

plt.plot([0,600], [n/b,n/b], 'black', linestyle = 'dotted')
plt.plot([0,600], [1-n/b-(m*b-m*n)/(b*m+b*n),1-n/b-(m*b-m*n)/(b*m+b*n)], 'blue', linestyle = 'dotted')
plt.plot([0,600], [(m*b-m*n)/(b*m+b*n),(m*b-m*n)/(b*m+b*n)], 'red', linestyle = 'dotted')


plt.xlabel("Days")
plt.ylabel("Proportion of population")
plt.xlim([0,300])
plt.legend(["Susceptible", "Infected", "Recovered"])

plt.savefig('timeplot.pgf')
