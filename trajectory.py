import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import subprocess
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


pop = 80000000
init = 1

b = 0.5 #Infectiousness
m = 0.01 #Immunity loss
n = 0.333 #Recoveries (high -> shorter sickness lenght)

for i in range(1,9):
    tmp=i*1000000
    args = [ './sirs.out', str(pop-tmp), str(tmp), str(b), str(m), str(n)]
    subprocess.run(args)

    with open("sirs.csv") as csvfile:
        sirs = np.loadtxt(csvfile, delimiter="\t")

    plt.plot(sirs[:,1],sirs[:,2],'black', linewidth=0.6)


x = np.linspace(0,1,1000)
plt.plot(x,1-x, 'black', linestyle = 'dashed')

plt.plot([n/b,n/b], [0,1], 'black', linestyle = 'dotted')
plt.plot(x, (m*(1-x))/(b*x+m),'black', linestyle = 'dotted')

plt.xlabel("Susceptible proportion of population")
plt.ylabel("Infected proportion of population")
plt.xlim([0.35,1])
plt.ylim([0,0.15])

plt.savefig("trajectories.pgf")
