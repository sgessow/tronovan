import pymunk
from constants import *

def add_floor(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor =pymunk.Segment(body,(0.0,5.0),(SCREEN_WIDTH,5.0),5.0)
    space.add(body,floor)
    return floor

class robot:
    def __init__(self,space):
        self.space=space
        #Create all the parts of the robot
        self.torso=self.add_torso()
        self.crank_arm=self.add_crank_arm()
        self.motor=self.add_motor()

    def add_torso(self):
        mass=50
        width=10
        a=(STARTING_X,STARTING_Y+TORSO_HEIGHT/2)
        b=(STARTING_X,STARTING_Y-TORSO_HEIGHT/2)
        moment = pymunk.moment_for_segment(mass,a,b,width)
        #body=pymunk.Body(mass, moment)
        body= pymunk.Body(body_type = pymunk.Body.STATIC)
        body.velocity=(0,0)
        torso=pymunk.Segment(body,a,b,width)
        return body, torso

    def add_crank_arm(self):
        mass = 10
        radius=3
        length=80
        a=(STARTING_X,STARTING_Y-TORSO_HEIGHT/2)
        b=(STARTING_X+CRANK_ARM_LEN,STARTING_Y-TORSO_HEIGHT/2)
        moment = pymunk.moment_for_segment(mass,a,b,radius)
        body = pymunk.Body(mass, moment)
        body.velocity=(0,0)
        arm=pymunk.Segment(body,a,b,radius)
        return body,arm

    def add_motor(self):
        angular_velocity=5
        #motor_joint=pymunk.SimpleMotor(self.torso[0],self.crank_arm[0],angular_velocity)
        pin_joint=pymunk.PinJoint(self.torso[0],self.crank_arm[0],(STARTING_X,STARTING_Y-TORSO_HEIGHT/2),(STARTING_X,STARTING_Y-TORSO_HEIGHT/2))
        #motor_joint.max_force=50
        return pin_joint



    def add_to_space(self):
        self.space.add(self.torso)
        self.space.add(self.crank_arm)
        self.space.add(self.motor)
