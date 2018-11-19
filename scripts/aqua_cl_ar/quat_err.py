#! /usr/bin/env python3

from rt_transformations import *
import numpy as np

def quat_ang(q1, q2):
    # dq = q2 * inv(q1)
    # v2 = conj(dq) * v1 * dq
    # cos(dtheta) = (v1 . v2) / (|v1| |v2|)
    # dtheta = arccos(cos(dtheta))
    dq = qmult(q1, quat_inverse(q2))
    v1 = np.array([0,0,0,1])  # any pure vector works
    print(q1,q2,quat_inverse(q1))
    dq_conj = dq.copy()
    dq_conj[1:] = -dq_conj[1:]
    v2 = qmult(qmult(dq_conj, v1), dq)
    v1norm = np.sqrt(v1.dot(v1))
    v2norm = np.sqrt(v2.dot(v2))
    print(v1,v2,dq)
    assert v1norm > 0 and v2norm > 0, "Vector cannot be zero length"
    cos_theta = (v1.dot(v2)) / (v1norm + v2norm)
    assert -1 <= cos_theta <= 1, "Cosine angle out of bounds"
    return np.arccos(cos_theta)

def main():
    print(quat_ang([0,1,0,0], [0,0,.7,.7])*180/np.pi)

if __name__ == "__main__":
    main()
