import os, sys
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import parameters as params


def plot_head_layers(xlim, ylim, radii, ax):
    # Plotting the layers of the head model
    max_angle = np.abs(np.rad2deg(np.arcsin(xlim[0] / ylim[0])))
    plot_angle = np.linspace(-max_angle, max_angle, 100)
    for b_idx in range(len(radii)):
        x_ = radii[b_idx] * np.sin(np.deg2rad(plot_angle))
        z_ = radii[b_idx] * np.cos(np.deg2rad(plot_angle))
        l_curved, = ax.plot(x_, z_, ':', c="gray", lw=0.6)

    ax.text(xlim[0], radii[0] - 70, "Brain", va="top", ha="left", color="k")
    ax.text(xlim[0], radii[0] + 70, "CSF", va="top", ha="left", color="k")
    ax.text(xlim[0], radii[1] + 70, "Skull", va="top", ha="left", color="k")


rad_tol = 1e-2
scalp_rad = 9.

brain_rad = 7.9
csftop_rad = 8.
skull_rad = 8.5
scalp_rad = 9.

# x,z = np.meshgrid(np.linspace(-scalp_rad +rad_tol, scalp_rad-rad_tol, 1000),
#                   np.linspace(-scalp_rad+rad_tol, scalp_rad-rad_tol, 1000))
# whithin_idxs = np.where(np.sqrt(x**2 + z**2) < scalp_rad-rad_tol)
#
# x_points = x[whithin_idxs]#.flatten()
# z_points = z[whithin_idxs]#.flatten()

sim_name = params.return_sim_name()


x_points, y_points, z_points = np.load(os.path.join('results', 'elecs_{}.npy'.format(sim_name))).T

# center_idxs = np.where((np.abs(x_points) < 1e-4) & (np.abs(y_points) < 1e-4) & (z_points > 5))

center_idxs = np.where((np.abs(x_points) == np.min(np.abs(x_points))))
print(z_points[center_idxs])
sys.exit()

print(x_points.shape)

ecp_sig = np.load(join("results", "disc_numerical_{}_rad.npy".format(sim_name)))

vmax_ecp = 1000#np.max(np.abs(ecp_sig))
vmin_ecp = -vmax_ecp

# levels_ecp = np.linspace(vmin_ecp, vmax_ecp, 128)
steps = np.logspace(-5, 0, 20) * vmax_ecp
levels_ecp = np.r_[-steps[::-1], steps]

fig = plt.figure(figsize=[8, 8])

xlim = [-3, 3]

ylim = [5, 9.1]

ax1 = fig.add_subplot(111, aspect=1, ylim=ylim, xlim=xlim)


plot_head_layers(xlim, ylim, [params.wm_rad, brain_rad, csftop_rad, skull_rad, scalp_rad], ax1)

# print(vmax_ecp)
print(levels_ecp)
print(steps)
# plt.scatter(x_points, z_points, d)
img = plt.tricontourf(x_points, z_points, ecp_sig, levels_ecp, cmap="bwr", norm=colors.SymLogNorm(linthresh=0.1))
plt.tricontour(x_points, z_points, ecp_sig, levels_ecp, colors="k")


cbar = plt.colorbar(img, orientation="horizontal")
ticks = 10**np.linspace(-4, 0, 5) * vmax_ecp


cbar.set_ticks(np.r_[-ticks[::-1], 0, ticks])
# ticklabels = ["{:.1e}".format(t) for t in cbar.get_ticks()]
# cbar.set_ticklabels(ticklabels)
plt.savefig("ep_crossec_{}_rad.png".format(sim_name), dpi=150)