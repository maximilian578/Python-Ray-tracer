"""A ray-traceable Plane is a Plane through a given
   point with a given normal and surface material.
   It needs an intersect method that returns the
   point of intersection of a given ray with the
   plane and a normal method that returns the normal
   at a given point (which is irrelevant for a plane
   as the normal is the same everywhere)."""
from __future__ import division

from builtins import object
from geom3 import Vector3, Point3, Ray3, dot, unit
from math import sqrt
from hit import Hit
from helpers import isninf


class Plane(object):
    """A ray-traceable plane"""

    def __init__(self, point, normal, material):
        """Create a plane through a given point with given normal
        and surface material"""
        self.point = point
        self.norm = unit(normal)
        self.mat = material

    def intersect(self, ray):
        """Returns a hit, or None if the ray is parallel to the plane"""

        t = None
        hit = None
        angle = ray.dir.dot(self.norm)
        if angle != 0:
            t = (self.point - ray.start).dot(self.norm) / angle
            if angle < 0:
                hit = Hit(self, ray, t, float('inf'), self.norm, self.mat)
            else:
                hit = Hit(self, ray, float('-inf'), t, self.norm, self.mat)
        else:
            vector = unit(ray.start - self.point)
            if vector.dot(self.norm) < 0:
                hit = Hit(self, ray, float('-inf'), float('inf'), self.norm, self.mat)
            else:
                return None
        if (self.mat.texture is not None and not isninf(hit.entry)) > 0:
            hit.texCords = self.texCords(ray.pos(t))
        return hit

    def texCords(self, point):
        vect = point - self.point
        u = vect.dx
        v = vect.dz
        return (u, v)
