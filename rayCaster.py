#!/usr/bin/python
import cProfile
from antiAlaising import *
from geom3 import Point3, Vector3, Ray3, cross, dot, unit, length
from math import sqrt, tan
from colour import Colour
from sphere import Sphere
from plane import Plane
import Image
from material import Material
from scene import Scene
from light import *
from texture import *
from CSG import *
import sys


# Define various scene constants

WIN_SIZE = 400                              # Screen window size (square)
SPACING = 1.0 / WIN_SIZE                    # Pixel spacing on viewplane

SHINY_RED = Material(Colour(0.7, 0.1, 0.2), Colour(0.4,0.4,0.4), 100, .2)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200, .3)
MATT_GREEN = Material(Colour(0.1,0.85, 0.1))
CHECK_FLOOR = Material(None, None, None, None, Texture_Check(6, Colour(0,0,0), Colour(0.5,0.5,0.5)))

EYEPOINT = Point3(0.5, 0.4, 2.5)

SCENE = Scene([
	       Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE),
	       #Difference([
	       Intersection([ # Cube
		  Plane(Point3(0.2,0.0,0.5), Vector3(0,-1,0), CHECK_FLOOR),
		  Plane(Point3(0.1,0.175,0.8), Vector3(0, 1,0), CHECK_FLOOR),
		  Plane(Point3(0.1,0.1,0.5), Vector3(-1,0,0), CHECK_FLOOR),
		  Plane(Point3(0.4,0.1,0.5), Vector3( 1,0,0), CHECK_FLOOR),
		  Plane(Point3(0.5,0.1,0.8), Vector3(0,0, 1), CHECK_FLOOR),
		  Plane(Point3(0.5,0.1,0.5), Vector3(0,0,-1), CHECK_FLOOR),
		  #Sphere(Point3(0.1,0.175,0.8), 0.175, SHINY_BLUE),
			  ]),
		 # Sphere(Point3(0.1,0.175,0.8), 0.125, SHINY_RED)]),
	       Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED),
               Plane(Point3(0,0,0), Vector3(0,1,0), CHECK_FLOOR)
	       ])

SCENE.lights = [
	  #Light(SCENE, unit(Vector3(2,5,3)), Colour(0.8, 0.8, 0.8)),
	  Light(SCENE, unit(Vector3(-4,5,0)), Colour(0.3, 0.3, 0.3)),
	  #PointLight(SCENE, Point3(.7, .5, .8), Colour(0.8, 0.8, 0.8)),
	  ]
SCENE.background = Colour(0, 0, 0)
SCENE.ambient = Colour(0.1, 0.1, 0.1) 

class rayCaster(object):
    def __init__(self):
	return

    def rayColour(self, ray, depth=0):
	if depth > 100:
	    print "Max Depth reached!"
	    return Colour(0,0,0)
	
        hit = SCENE.intersect(ray)
        if hit is None:
            return SCENE.background
        else:
	    hit.calcReflections(SCENE)
	    hit.calcLights(SCENE)
	    return hit.colour()
	    
    # Main body. Set up an image then compute colour at each pixel
    def trace(self):
        img = Image.new("RGB", (WIN_SIZE, WIN_SIZE))
	aa = NoAA(EYEPOINT, self.rayColour)
	print "\tTracing Rays...   0%",
	sys.stdout.flush()
	count = 0
	max = float(WIN_SIZE**2)
	lastPercentage = 0
        for row in range(WIN_SIZE):
            for col in range(WIN_SIZE):
                count += 1

		pixelBox = (col * SPACING, (WIN_SIZE - row) * SPACING, (col+1) * SPACING, (WIN_SIZE - row+1) * SPACING)

                img.putpixel((col, row), aa.getPixel(pixelBox).intColour())
	    percentage = (count / max * 100)
	    if percentage - lastPercentage > .9:
	        print "\b\b\b\b\b\b%4.0f%%" % percentage,
		sys.stdout.flush()
		lastPercentage = percentage
	print "\b\b\b\b\b\b Done"
        img.save("out.png")  # Display image in default image-viewer application

caster = rayCaster()
#cProfile.run("caster.trace()")
caster.trace()
