from matplotlib import pyplot;
from pylab import genfromtxt;

folderPath="./Data/"

numOfRepetitions=5

fig = pyplot.figure(figsize=(8,6));
for i in range(1,numOfRepetitions+1):
    acc = genfromtxt(folderPath+str(i)+".txt",delimiter=",");
    ax = fig.add_subplot(3,2,i)
    ax = pyplot.plot(acc[:,0], label = "x");
    ax = pyplot.plot(acc[:,1], label = "y");
    ax = pyplot.plot(acc[:,2], label = "z");
    pyplot.draw();
pyplot.legend(loc='center left', bbox_to_anchor=(1, 0.5));
pyplot.suptitle("Accelerometer - " + folderPath[len(folderPath)-10:]);

fig = pyplot.figure(figsize=(8,6));
for i in range(1,numOfRepetitions+1):
    acc = genfromtxt(folderPath+str(i)+".txt",delimiter=",");
    ax = fig.add_subplot(3,2,i)
    ax = pyplot.plot(acc[:,3], label = "x");
    ax = pyplot.plot(acc[:,4], label = "y");
    ax = pyplot.plot(acc[:,5], label = "z");
    pyplot.draw();
pyplot.legend(loc='center left', bbox_to_anchor=(1, 0.5));
pyplot.suptitle("Gyroscope - " + folderPath[len(folderPath)-10:]);
pyplot.show();
