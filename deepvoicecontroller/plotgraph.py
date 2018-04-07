import os
import matplotlib.pyplot as plt
os.system("ls -al Weights  -t | awk '{ print $(NF); }' | grep -o '[0-9.]\+.hdf' | grep -o '[0-9.]\+' | tr -d \"\\.$\" > val_loss.txt")
val_loss = []
with open("val_loss.txt","r") as f:
	for line in f:
		val_loss.append(int(line))

plt.plot(val_loss[::-1])
plt.ylabel('Val Loss')
plt.xlabel('Epoch')
plt.show()