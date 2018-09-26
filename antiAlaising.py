from __future__ import division
from builtins import range
from builtins import object
from past.utils import old_div
from geom3 import Point3, Vector3, Ray3, cross, dot, unit, length
from colour import Colour
from math import sqrt
import random

class NoAA(object):
    def __init__(self, eyepoint, rayfunc):
    	self.eye = eyepoint
	self.rayfunc = rayfunc
	
    def getPixel(self, pixelBox):
	(x, y, x2, y2) = pixelBox
    	pixelCentre = Point3(old_div((x + x2),2), old_div((y2 + y),2), 1)
	ray = Ray3(self.eye, pixelCentre - self.eye)
	return self.rayfunc(ray)

class SuperSampling(object):
    def __init__(self, eyepoint, rayfunc, subPixels=4):
	self.eye = eyepoint
	self.rayfunc = rayfunc
	self.subPixels= int(sqrt(subPixels))

    def getPixel(self, pixelBox):
	(x, y, x2, y2) = pixelBox
	pitch = old_div((x2 - x), (self.subPixels * 2))
	xx = x
	yy = y
	count = 0
	colour = Colour(0,0,0)
	for col in range(self.subPixels):
	    for row in range(self.subPixels):
	        colour += self.rayfunc(Ray3(self.eye, (Point3(xx + pitch,yy + pitch,1) - self.eye)))
                count += 1
		yy += pitch * 2
	    yy = y
	    xx += pitch * 2
	assert count == self.subPixels * self.subPixels
	return old_div(colour, count)


class Jitter(object):
    def __init__(self, eyepoint, rayfunc, subPixels=4):
	self.eye = eyepoint
	self.rayfunc = rayfunc
	self.subPixels= int(sqrt(subPixels))

    def getPixel(self, pixelBox):
	(x, y, x2, y2) = pixelBox
	pitch = old_div((x2 - x), self.subPixels)
	xx = x
	yy = y
	count = 0
	colour = Colour(0,0,0)
	for col in range(self.subPixels):
	    for row in range(self.subPixels):
	        colour += self.rayfunc(Ray3(self.eye, (Point3(xx + random.uniform(0, pitch) ,yy + random.uniform(0, pitch),1) - self.eye)))
                count += 1
		yy += pitch
	    yy = y
	    xx += pitch
	assert count == self.subPixels * self.subPixels
	return old_div(colour, count)

class Jitter2(object):
    def __init__(self, eyepoint, rayfunc, subPixels=4):
	self.eye = eyepoint
	self.rayfunc = rayfunc
	self.subPixels= subPixels

    def getPixel(self, pixelBox):
	(x, y, x2, y2) = pixelBox
	pixSize = x2 - x
	colour = Colour(0,0,0)
	for i in range(self.subPixels):
	    colour += self.rayfunc(Ray3(self.eye, (Point3(random.uniform(x,x2) ,random.uniform(y,y2),1) - self.eye)))
	return old_div(colour, self.subPixels)



