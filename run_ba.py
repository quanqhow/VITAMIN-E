from autograd import numpy as np

from bundle_adjustment.triangulation import two_view_reconstruction
from bundle_adjustment.bundle_adjustment import BundleAdjustment
from camera import CameraParameters
from dataset.points import cubic_lattice
from dataset.bundle_adjustment import generate_observations, generate_translations
from projection.projections import PerspectiveProjection
from optimization.residuals import BaseResidual
from rigid.transformation import transform_each
from rigid.rotation import rodrigues


camera_parameters = CameraParameters(
    focal_length=[1., 1.],
    offset=[0., 0.]
)


points_true = cubic_lattice(3)
n_viewpoints = 128
projection = PerspectiveProjection(camera_parameters)


omegas = np.random.uniform(-1, 1, (n_viewpoints, 3))
translations = generate_translations(rodrigues(omegas), points_true)

observations, mask = generate_observations(
    rodrigues(omegas), translations, points_true, projection)

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from visualizer.visualizers import plot3d
plot3d(points_true)

ba = BundleAdjustment(observations, camera_parameters)
omegas, translations, points = ba.optimize()

plot3d(points)
plt.show()
