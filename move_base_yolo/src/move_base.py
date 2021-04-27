#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    while not rospy.is_shutdown():
        rospy.loginfo("Esperando mensagem no /govai")
        point = rospy.wait_for_message('/govai', Point)
        # rospy.loginfo("Esperando odometria")
        # odometry = rospy.wait_for_message('/odom', Odometry)
        goal = MoveBaseGoal()
        goal.target_pose.pose.position.x = point.x
        goal.target_pose.pose.position.y = point.y
        goal.target_pose.pose.orientation.w = 1

        if point.z == 0:
            rospy.loginfo("Movendo relativo")
            goal.target_pose.header.frame_id = "base_footprint"
            goal.target_pose.header.stamp = rospy.Time.now()
            client.send_goal(goal)
            wait = client.wait_for_result()
        elif point.z == 1:
            rospy.loginfo("Movendo absoluto")
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            client.send_goal(goal)
            wait = client.wait_for_result()
            if wait and client.get_result():
                rospy.loginfo("Goal execution done!")
   

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        rospy.loginfo("move_base iniciado")
        movebase_client()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")