#! /usr/bin/env python
import rospy, time
from sensor_msgs.msg import LaserScan
from  move_turtle_bot_publisher import MoveTurtleBot

class MazeRunner():
    def __init__(self):
        self.move_turtule_bot = MoveTurtleBot()
        self.end_time = 0

    def laser_call_back(self, msg):
        #infornt of the robot
        front_side = msg.ranges[len(msg.ranges)/2 + 35]
        #rightside of the robot
        right_side = msg.ranges[180]
        #left side of the robot
        left_side = msg.ranges[540]
        #wide_right_side
        wide_right_side = msg.ranges[0]
        #wide_left_side
        wide_left_side = msg.ranges[719]
        rospy.loginfo( "distance to obstacle from front side of the robot is "+ str(front_side))
        rospy.loginfo("distance to obstacle from right side of the robot is " + str(right_side))
        rospy.loginfo("distance to obstacle from left side of the robot is " + str(left_side))
        rospy.loginfo("-------------------------------------------------------------------------")

        if (front_side > 1.5):
            if(right_side > front_side and right_side > 2 and right_side > left_side):
                # print("turning right")
                if(right_side > 5):
                    self.move_turtule_bot.move_bot(0.2, -0.2)
                else:
                    self.move_turtule_bot.move_bot(0, -0.8)
                
            elif(left_side > front_side and left_side > 2 and left_side > right_side):
                # print("turning left")
                if (left_side > 5):
                    self.move_turtule_bot.move_bot(0.2, 0.2)
                else:
                    self.move_turtule_bot.move_bot(0,0.8)

            elif (right_side < front_side and left_side == float('inf') and front_side == float('inf')):
                #pring(turning left)
                self.move_turtule_bot.move_bot(0,0.8)

            elif(left_side < front_side and right_side == float('inf') and front_side == float('inf')):
                #pring(turning left)
                self.move_turtule_bot.move_bot(0,-0.8)   
                         
            else: 
                # print("moving forward")
                self.move_turtule_bot.move_bot(0.45, 0)
        # 
        if (front_side < 1.5):
            if(right_side > left_side and right_side > 1.5):
                # print("turning right")
                self.move_turtule_bot.move_bot(0, -3)  #using 3 to make a faster turn when the robot's front side is blocked

            elif(left_side > right_side and left_side > 1.5):
                # print("turning left")
                self.move_turtule_bot.move_bot(0,3)

            elif(left_side > front_side and left_side < 1.5 and left_side > right_side):
                # print("turning left")
                self.move_turtule_bot.move_bot(0,3)

            elif(right_side > front_side and right_side < 1.5 and right_side > left_side):
                # print("turning left")
                self.move_turtule_bot.move_bot(0,-3)
        
        #shut down the program when cntrl-c is pressed
        if (rospy.is_shutdown()):
            self.move_turtule_bot.stop_turtle_bot()
            
        #checks if turtle bot is out the maze 
        if (right_side == float('inf') and front_side == float('inf') and left_side == float('inf')):
            print("YES! I'm almost outside of the maze")
            self.move_turtule_bot.move_bot(0.5,0)
            if (wide_right_side == float('inf') and front_side == float('inf') and wide_left_side == float('inf')):
                self.move_turtule_bot.stop_turtle_bot()
                rospy.loginfo("Turtle Bot Has Exited the Maze!!")
                #shutsdown the program
                rospy.signal_shutdown('turtlebot is out of the maze')
                
        if(time.time() >= self.end_time):
            rospy.loginfo("SHUTTING DOWN ... Program execution was long!!! ")
            self.move_turtule_bot.stop_turtle_bot()
            #shutsdown the program
            rospy.signal_shutdown('Turtlebot could not get out of the maze in a reasonable time.')

if __name__ == '__main__':
    rospy.init_node('turtle_bot_main_node', log_level=rospy.DEBUG)
    # Create a Subscriber object that will listen to the /kobuki/laser/scan
    # topic and will cal the 'laser_call_back' function each time it reads
    # something from the topic
    maze_runner = MazeRunner()
    sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, maze_runner.laser_call_back)
    start_time = time.time()
    maze_runner.end_time = start_time + 119 # program execution time is set to 119 secs
    
    rospy.spin() # Create a loop that will keep the program in execution
    end_time = time.time() 
    total_time = end_time - start_time
    rospy.loginfo("Time of execution is %s seconds", total_time)
    