#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
#
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlecode.com)
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

#Note uses framework from the example folder with gravity changed to 9.8
from examples.framework import (Framework, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2Random, b2Filter, b2CircleShape)
import numpy


class Robot(Framework):
    """You can use this class as an outline for your tests."""
    name = "Robot"  # Name of the class to display
    description = "Simple Walking Robot"

    def __init__(self):
        """
        Initialize all of your objects here.
        Be sure to call the Framework's initializer first.
        """
        super(Robot, self).__init__()
        group=-1
        self.start_y=10
        self.len_torso=6
        self.len_crank_arm=2
        self.len_leg=14
        leg_angle=numpy.arctan(self.len_torso/self.len_crank_arm)
        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=[b2EdgeShape(vertices=[(-1000, 0), (1000, 0)])]
        )

        torso = self.world.CreateDynamicBody(
            position=(0, self.start_y),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(.5, self.len_torso/2)),density=1.0,filter=b2Filter(groupIndex=group,)),
        )

        crank_arm=self.world.CreateDynamicBody(
            position=(0,self.start_y+self.len_torso/2),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(self.len_crank_arm,.1)),density=1.0,filter=b2Filter(groupIndex=group,)),
        )
        slot_joint=self.world.CreateDynamicBody(
            position=(0,self.start_y-self.len_torso/2),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=.05),density=1.0,filter=b2Filter(groupIndex=group,)),
        )
        l=numpy.sqrt(self.len_torso**2+self.len_crank_arm**2)
        x=(self.len_leg-2*l)*numpy.cos(leg_angle)/2
        y=(self.len_leg-2*l)*numpy.sin(leg_angle)/2
        right_leg=self.world.CreateDynamicBody(
            position=(x,self.start_y-y-self.len_torso/2),
            angle=(-1*leg_angle+numpy.pi/2),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(.1,self.len_leg/2)), density=1.0,filter=b2Filter(groupIndex=group,)),
        )


        self.motor = self.world.CreateRevoluteJoint(
                    bodyA=torso,
                    bodyB=crank_arm,
                    anchor=(torso.worldCenter[0],torso.worldCenter[1]+self.len_torso/2),
                    motorSpeed=5.0,
                    maxMotorTorque = 500,
                    enableMotor=False,
        )
        self.right_joint=self.world.CreateRevoluteJoint(
                    bodyA=crank_arm,
                    bodyB=right_leg,
                    anchor=(crank_arm.worldCenter[0]-self.len_crank_arm,crank_arm.worldCenter[1]),
        )
        self.right_slide_rev=self.world.CreateRevoluteJoint(
                    bodyA=slot_joint,
                    bodyB=torso,
                    anchor=(torso.worldCenter[0],torso.worldCenter[0]-self.len_torso/2),
        )
        self.right_slide_pris=self.world.CreatePrismaticJoint(
                    bodyA=right_leg,
                    bodyB=torso,
                    anchor=(torso.worldCenter[0],torso.worldCenter[0]-self.len_torso/2),
        )




        # Initialize all of the objects

    def Keyboard(self, key):
        """
        The key is from Keys.K_*
        (e.g., if key == Keys.K_z: ... )
        """
        pass

    def Step(self, settings):
        """Called upon every step.
        You should always call
         -> super(Your_Test_Class, self).Step(settings)
        at the beginning or end of your function.

        If placed at the beginning, it will cause the actual physics step to happen first.
        If placed at the end, it will cause the physics step to happen after your code.
        """

        super(Robot, self).Step(settings)

        # do stuff

        # Placed after the physics step, it will draw on top of physics objects
        #self.Print("*** Base your own testbeds on me! ***")

    def ShapeDestroyed(self, shape):
        """
        Callback indicating 'shape' has been destroyed.
        """
        pass

    def JointDestroyed(self, joint):
        """
        The joint passed in was removed.
        """
        pass

    # More functions can be changed to allow for contact monitoring and such.
    # See the other testbed examples for more information.

if __name__ == "__main__":
    main(Robot)
