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
        fixed_pin=pymunk.Body(body_type = pymunk.Body.STATIC)
        mass=1
        width=1
        a=(STARTING_X,STARTING_Y+TORSO_HEIGHT/2)
        b=(STARTING_X,STARTING_Y-TORSO_HEIGHT/2)
        moment = pymunk.moment_for_segment(mass,(0,0),(0,TORSO_HEIGHT),width)
        body=pymunk.Body(mass, moment)
        #body= pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position=(0,0)
        pin_joint = pymunk.PinJoint(fixed_pin,body, (0,0), (0,0))
        torso=pymunk.Segment(body,a,b,width)
        return body, torso,pin_joint

    def add_crank_arm(self):
        mass = 1
        radius=1
        length=80
        a=(STARTING_X,STARTING_Y-TORSO_HEIGHT/2)
        b=(STARTING_X+CRANK_ARM_LEN,STARTING_Y-TORSO_HEIGHT/2)
        moment = pymunk.moment_for_segment(mass,(0,0),(0,length),radius)
        body = pymunk.Body(mass, moment)
        #body= pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position=(0,0)
        body.velocity=(0,0)
        arm=pymunk.Segment(body,a,b,radius)
        return body,arm

    def add_motor(self):
        angular_velocity=5
        #motor_joint=pymunk.SimpleMotor(self.torso[0],self.crank_arm[0],angular_velocity)
        #pin_joint=pymunk.PinJoint(self.torso[0],self.crank_arm[0],(0,0),(0,0))
        #motor_joint.max_force=50
        motor_joint = pymunk.SimpleMotor(self.crank_arm[0],self.torso[0],angular_velocity)
        return motor_joint



    def add_to_space(self):
        self.space.add(self.torso,self.crank_arm,self.motor)
