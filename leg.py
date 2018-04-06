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

    def __init__(self,args=None):
        """
        Initialize all of your objects here.
        Be sure to call the Framework's initializer first.
        """
        if args==None:
            args={"start_y":10,"len_torso":6,"len_crank_arm":2,"len_leg":14,"motor_torque":400, "motor_speed":5}
        super(Robot, self).__init__()
        self.count=0
        self.points=[]
        self.group=-1
        self.start_y=args["start_y"]
        self.len_torso=args["len_torso"]
        self.len_crank_arm=args["len_crank_arm"]
        self.len_leg=args["len_leg"]
        self.motor_torque=args["motor_torque"]
        self.motor_speed=args["motor_speed"]
        #Non controlled constants
        torso_width=.001
        other_width=.001
        leg_angle=numpy.arctan(self.len_torso/self.len_crank_arm)
        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=[b2EdgeShape(vertices=[(-1000, 0), (1000, 0)])]
        )

        self.torso = self.world.CreateDynamicBody(
            position=(0, self.start_y),
            fixedRotation=True,
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(torso_width, self.len_torso/2)),density=1.3,filter=b2Filter(groupIndex=self.group,)),
        )

        self.crank_arm=self.world.CreateDynamicBody(
            position=(0,self.start_y+self.len_torso/2),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(self.len_crank_arm,other_width)),density=.1,filter=b2Filter(groupIndex=self.group,)),
        )
        #Creating the legs
        l=numpy.sqrt(self.len_torso**2+self.len_crank_arm**2)
        x=(self.len_leg-2*l)*numpy.cos(leg_angle)/2
        y=(self.len_leg-2*l)*numpy.sin(leg_angle)/2
        self.right_leg=self.world.CreateDynamicBody(
            position=(x,self.start_y-y-self.len_torso/2),
            angle=(-1*leg_angle+numpy.pi/2),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(other_width,self.len_leg/2)), density=.50,filter=b2Filter(groupIndex=self.group),friction=1,restitution=0),
        )
        self.left_leg=self.world.CreateDynamicBody(
            position=(-x,self.start_y-y-self.len_torso/2),
            angle=(leg_angle+numpy.pi/2),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(other_width,self.len_leg/2)), density=1.0,filter=b2Filter(groupIndex=self.group),friction=1,restitution=0),
        )
        self.right_foot=self.world.CreateDynamicBody(
            position=(self.len_leg/2*numpy.cos(leg_angle),self.len_leg*numpy.sin(leg_angle)),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=.003),density=0.1,filter=b2Filter(groupIndex=self.group,)),
        )
        self.left_foot=self.world.CreateDynamicBody(
            position=(-1*self.len_leg/2*numpy.cos(leg_angle),self.len_leg*numpy.sin(leg_angle)),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=.003),density=0.1,filter=b2Filter(groupIndex=self.group,)),
        )
        slot_joint_right=self.world.CreateDynamicBody(
            position=(0,self.torso.worldCenter[1]-self.len_torso/2),
            angle=(-1*leg_angle+numpy.pi/2),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=.0005),density=1.0,filter=b2Filter(groupIndex=self.group,)),
        )
        slot_joint_left=self.world.CreateDynamicBody(
            position=(0,self.torso.worldCenter[1]-self.len_torso/2),
            angle=(leg_angle+numpy.pi/2),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=.0005),density=1.0,filter=b2Filter(groupIndex=self.group,)),
        )
        #Attach Feat to legs
        self.right_foot_weld=self.world.CreateWeldJoint(
            bodyA=self.right_foot,
            bodyB=self.right_leg,
            anchor=(self.torso.worldCenter[0]+self.len_leg/2*numpy.cos(leg_angle),self.torso.worldCenter[1]+self.len_leg*numpy.sin(leg_angle)),
        )
        self.left_foot_weld=self.world.CreateWeldJoint(
            bodyA=self.left_foot,
            bodyB=self.left_leg,
            anchor=(self.torso.worldCenter[0]-self.len_leg/2*numpy.cos(leg_angle),self.torso.worldCenter[1]+self.len_leg*numpy.sin(leg_angle)),
        )
        #Motor Joint
        self.motor = self.world.CreateRevoluteJoint(
                    bodyA=self.torso,
                    bodyB=self.crank_arm,
                    anchor=(self.torso.worldCenter[0],self.torso.worldCenter[1]+self.len_torso/2),
                    motorSpeed=self.motor_speed,
                    maxMotorTorque = self.motor_torque,
                    enableMotor=True,
        )
        #Joints at end of pivot
        self.right_joint=self.world.CreateRevoluteJoint(
                    bodyA=self.crank_arm,
                    bodyB=self.right_leg,
                    anchor=(self.crank_arm.worldCenter[0]-self.len_crank_arm,self.crank_arm.worldCenter[1]),
        )
        self.left_joint=self.world.CreateRevoluteJoint(
                    bodyA=self.crank_arm,
                    bodyB=self.left_leg,
                    anchor=(self.crank_arm.worldCenter[0]+self.len_crank_arm,self.crank_arm.worldCenter[1]),
        )
        #Making the slot joint composed of rev joint and prismatic joints
        self.left_joint_rev=self.world.CreateRevoluteJoint(
                    bodyA=slot_joint_right,
                    bodyB=self.torso,
                    anchor=(0,self.start_y-self.len_torso/2),
        )
        self.right_joint_rev=self.world.CreateRevoluteJoint(
                    bodyA=slot_joint_left,
                    bodyB=self.torso,
                    anchor=(0,self.start_y-self.len_torso/2),
        )
        self.right_slide_pris=self.world.CreatePrismaticJoint(
                    bodyA=slot_joint_right,
                    bodyB=self.right_leg,
                    anchor=(self.torso.worldCenter[0],self.torso.worldCenter[0]-self.len_torso/2),
                    localAxisA=(0,1),
        )
        self.left_slide_pris=self.world.CreatePrismaticJoint(
                    bodyA=slot_joint_left,
                    bodyB=self.left_leg,
                    anchor=(self.torso.worldCenter[0],self.torso.worldCenter[0]-self.len_torso/2),
                    localAxisA=(0,1),
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
        if(self.count%5==0):
            position_of_foot=(self.right_foot.position)
            position_of_body=(self.torso.position)
            point_foot = self.world.CreateStaticBody(
                position=position_of_foot,
                shapes=[b2CircleShape(radius=.0001)],
                active=False,
            )
            point_body = self.world.CreateStaticBody(
                position=position_of_body,
                shapes=[b2CircleShape(radius=.0001)],
                active=False,
            )
            self.points.append(point_foot)
            self.points.append(point_body)
            self.count=1
            # if(len(self.points)>=10):
            #     to_delete_one=self.points.pop(0)
            #     to_delete_one.delete
        else:
            self.count+=1
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
    main(Robot,{"start_y":.1,"len_torso":.03,"len_crank_arm":.01,"len_leg":.06,"motor_torque":10, "motor_speed":2})
