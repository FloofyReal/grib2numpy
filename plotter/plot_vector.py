import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
 
name = 'Vector'
endfile = 'vector/'
if not os.path.exists(endfile):
    os.makedirs(endfile)

vector = np.random.rand(1,100)
fig = plt.figure(figsize = (10,1))
ax = fig.add_subplot(111)
ax.imshow(vector, interpolation='nearest')
ax.axis('off')

plt.show()

plt.savefig(endfile + name +'.png', dpi=1000) # Set the output file name