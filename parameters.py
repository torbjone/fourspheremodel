import numpy as np

# All numbers in cm
dipole_loc = 7.8
wm_rad = 7.6
brain_rad = 7.9
csftop_rad = 8.
skull_rad = 8.5
scalp_rad = 9.

sigma_wm = 1. / 300. # S / cm
sigma_brain = 1. / 300.  # S / cm
sigma_scalp = sigma_brain
sigma_csf = sigma_brain * 5
sigma_skull = sigma_brain / 20

def return_sim_name():

    sim_name = 'wm{:1.6f}_gm{:1.6f}_csf{:1.6f}_skull{:1.6f}_scalp{:1.6f}'.format(sigma_wm, sigma_brain, sigma_csf, sigma_skull, sigma_scalp)
    return sim_name

# from gmsh sphere_4.geo
centervol = 32
whitemattervol = 64
graymattervol = 96
csfvol = 128
skullvol = 160
scalpvol = 192

# measument points
# theta = np.arange(0, 180)
# phi_angle = 0 # -90 to 90

theta, phi_angle = np.mgrid[0:180:1, -90:90:1]
theta = theta.flatten()
phi_angle = phi_angle.flatten()

theta_r = np.deg2rad(theta)
phi_angle_r = np.deg2rad(phi_angle)

rad_tol = 1e-2
#x_points = (scalp_rad - rad_tol) * np.sin(theta_r) * np.cos(phi_angle_r)
#y_points = (scalp_rad - rad_tol) * np.sin(theta_r) * np.sin(phi_angle_r)
#z_points = (scalp_rad - rad_tol) * np.cos(theta_r)

x,z = np.meshgrid(np.linspace(-3, 3, 1000),
                  np.linspace(5, scalp_rad-rad_tol, 1000))

whithin_idxs = np.where(np.sqrt(x**2 + z**2) < scalp_rad-rad_tol)

x_points = x[whithin_idxs].flatten()
y_points = np.zeros(len(x_points))
z_points = z[whithin_idxs].flatten()


ele_coords = np.vstack((x_points, y_points, z_points)).T


# dipole location - Radial
rad_dipole = {'src_pos': [0., 0., 7.85],
              'snk_pos': [0., 0., 7.75],
              'name': 'rad'}

# # dipole location - Tangential
tan_dipole = {'src_pos': [0., -0.05, 7.8],
              'snk_pos': [0., 0.05, 7.8],
              'name': 'tan'}

# # # dipole location - Mix
mix_dipole = {'src_pos': [0., -0.0353, 7.835],
              'snk_pos': [0., 0.0353, 7.764],
              'name': 'mix'}

dipole_list = [rad_dipole, tan_dipole]
