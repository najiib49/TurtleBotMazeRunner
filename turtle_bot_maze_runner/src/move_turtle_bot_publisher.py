#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class MoveTurtleBot():
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist)
        self.vel = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(2)
        rospy.on_shutdown(self.shutdownhook)
    def publish_cmd_vel(self):
        while not self.ctrl_c:
            #check if there are connections to publish
            connections = self.pub.get_num_connections()
            print connections
            if connections > 0:
                #publishing the actions
                self.pub.publish(self.vel)
                rospy.loginfo("cmd_vel published")
                break
                
            else:
                #if no connections
                self.rate.sleep()

    def shutdownhook(self):
        self.ctrl_c = True
        self.stop_turtle_bot()

    def move_bot(self, linear_speed = 0.2, angular_speed = 0.2):
        self.vel.linear.x = linear_speed
        self.vel.angular.z = angular_speed
        self.publish_cmd_vel()

    #in case you need to stop the robot
    def stop_turtle_bot(self):
        #stop the bb8
        self.vel.linear.x = 0
        self.vel.linear.y = 0
        self.vel.linear.z = 0
        self.vel.angular.z = 0
        
        self.pub.publish(self.vel)
        # rospy.loginfo("cmd_vel stopped")
        self.rate.sleep()

if __name__ == '__main__':
    rospy.init_node('move_turtle_bot_test', log_level=rospy.DEBUG)
    move_turtle_bot_object = MoveTurtleBot()
    try:
        move_turtle_bot_object.move_bot(0.2, 0)
    except rospy.ROSInterruptException:
        pass