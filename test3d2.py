import matplotlib.pyplot as plt

ax = plt.figure().add_subplot(projection='3d')

x = [0.16, 0.5, 0.84]
y = [0.16, 0.5, 0.84]
z = [0.16, 0.5, 0.84]
c_list = ['r', 'g', 'b']

ax.scatter(x, y, z, c=c_list, s=3000)

# Make legend, set axes limits and labels
#ax.legend()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ticks = [0, 0.33, 0.66, 1]
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_zticks(ticks)

# Customize the view angle so it's easier to see that the scatter points lie
# on the plane y=0
ax.view_init(elev=20., azim=-35, roll=0)

plt.show()
