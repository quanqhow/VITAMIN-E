from autograd import numpy as np

from vitamine.pose_estimation import solve_pnp
from vitamine.so3 import rodrigues


class Pose(object):
    def __init__(self, R, t):
        self.R, self.t = R, t

    @staticmethod
    def identity():
        return Pose(np.identity(3), np.zeros(3))

    def __eq__(self, other):
        return (np.isclose(self.R, other.R).all() and
                np.isclose(self.t, other.t).all())


def estimate_pose(points, keypoints):
    omega, t = solve_pnp(points, keypoints)
    R = rodrigues(omega.reshape(1, -1))[0]
    return R, t
