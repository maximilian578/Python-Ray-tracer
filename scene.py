"""A scene is a list of objects. It provides an intersect
method to intersect a ray with the scene, returning the t
value (distance along the ray) at the first hit, plus
the object hit, in a pair. Written for COSC363.
@author Richard Lobb, June 22, 2009."""

from builtins import object
from hit import BlankHit
import helpers


class Scene(object):

    def __init__(self, objs=[]):
        """Constructor takes a list of scene objects, each of which
        must provide an 'intersect' method that returns the ray t
        value or None of the first intersection between the ray and
        the object"""
        self.objs = objs

    def intersect(self, ray):
        """Intersect the given ray with all objects in the scene,
        returning the pair (obj, t) of the first hit or None if
        there are no hits"""

        minHit = BlankHit(self.background)
        for o in self.objs:
            hit = o.intersect(ray)
            # hit.entry can be None when hit is not None
            if hit and not helpers.isninf(hit.entry) and (hit.entry > 0):
                if minHit is None or hit < minHit:
                    minHit = hit
        return minHit
