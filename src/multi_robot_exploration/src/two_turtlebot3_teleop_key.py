#!/usr/bin/env python2

'''
 Created on Tue Jan 14 2020

 Copyright (c) 2020 HITSZ-NRSL
 All rights reserved

 Author: EpsAvlc
'''

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control Your TurtleBot3! Two turtlebot version.
---------------------------
Moving around:
        w                  8
   a    s    d        4    5    6
        x                  2
for turtlebot 1      for turtlebot 2  

w/x 8/2 : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d 4/6 : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)

space key, s, 5 : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)

    return vel

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('turtlebot3_teleop')
    tb_1_pub = rospy.Publisher('tb_1/cmd_vel', Twist, queue_size=10)
    tb_2_pub = rospy.Publisher('tb_2/cmd_vel', Twist, queue_size=10)

    turtlebot3_model = rospy.get_param("model", "burger")

    status = 0
    tb_1_target_linear_vel   = 0.0
    tb_1_target_angular_vel  = 0.0
    tb_1_control_linear_vel  = 0.0
    tb_1_control_angular_vel = 0.0

    tb_2_target_linear_vel   = 0.0
    tb_2_target_angular_vel  = 0.0
    tb_2_control_linear_vel  = 0.0
    tb_2_control_angular_vel = 0.0

    try:
        print msg
        while(1):
            key = getKey()
            if key == 'w' :
                tb_1_target_linear_vel = checkLinearLimitVelocity(tb_1_target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_1:'
                print vels(tb_1_target_linear_vel,tb_1_target_angular_vel)
            elif key == 'x' :
                tb_1_target_linear_vel = checkLinearLimitVelocity(tb_1_target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_1:'
                print vels(tb_1_target_linear_vel,tb_1_target_angular_vel)
            elif key == 'a' :
                tb_1_target_angular_vel = checkAngularLimitVelocity(tb_1_target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_1:'
                print vels(tb_1_target_linear_vel,tb_1_target_angular_vel)
            elif key == 'd' :
                tb_1_target_angular_vel = checkAngularLimitVelocity(tb_1_target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_1:'
                print vels(tb_1_target_linear_vel,tb_1_target_angular_vel)
            elif key == ' ' or key == 's' :
                tb_1_target_linear_vel   = 0.0
                tb_1_target_angular_vel  = 0.0
                tb_1_control_linear_vel  = 0.0
                tb_1_control_angular_vel = 0.0
            elif key == '8' :
                tb_2_target_linear_vel = checkLinearLimitVelocity(tb_2_target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_2:'
                print vels(tb_2_target_linear_vel,tb_2_target_angular_vel)
            elif key == '2' :
                tb_2_target_linear_vel = checkLinearLimitVelocity(tb_2_target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_2:'
                print vels(tb_2_target_linear_vel,tb_2_target_angular_vel)
            elif key == '4' :
                tb_2_target_angular_vel = checkAngularLimitVelocity(tb_2_target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_2:'
                print vels(tb_2_target_linear_vel,tb_2_target_angular_vel)
            elif key == '6' :
                tb_2_target_angular_vel = checkAngularLimitVelocity(tb_2_target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print 'tb_2:'
                print vels(tb_2_target_linear_vel,tb_2_target_angular_vel)
            elif key == '5' :
                tb_2_target_linear_vel   = 0.0
                tb_2_target_angular_vel  = 0.0
                tb_2_control_linear_vel  = 0.0
                tb_2_control_angular_vel = 0.0
            else:
                if (key == '\x03'):
                    break

            if status == 20 :
                print msg
                status = 0

            tb_1_twist = Twist()

            tb_1_control_linear_vel = makeSimpleProfile(tb_1_control_linear_vel, tb_1_target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            tb_1_twist.linear.x = tb_1_control_linear_vel; tb_1_twist.linear.y = 0.0; tb_1_twist.linear.z = 0.0

            tb_1_control_angular_vel = makeSimpleProfile(tb_1_control_angular_vel, tb_1_target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            tb_1_twist.angular.x = 0.0; tb_1_twist.angular.y = 0.0; tb_1_twist.angular.z = tb_1_control_angular_vel

            tb_1_pub.publish(tb_1_twist)


            tb_2_twist = Twist()

            tb_2_control_linear_vel = makeSimpleProfile(tb_2_control_linear_vel, tb_2_target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            tb_2_twist.linear.x = tb_2_control_linear_vel; tb_2_twist.linear.y = 0.0; tb_2_twist.linear.z = 0.0

            tb_2_control_angular_vel = makeSimpleProfile(tb_2_control_angular_vel, tb_2_target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            tb_2_twist.angular.x = 0.0; tb_2_twist.angular.y = 0.0; tb_2_twist.angular.z = tb_2_control_angular_vel

            tb_2_pub.publish(tb_2_twist)

    except:
        print e

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        tb_1_pub.publish(twist)
        tb_2_pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)