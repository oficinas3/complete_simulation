#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from geometry_msgs.msg import Pose

def movebase_client():
    pub = rospy.Publisher('/lost', String, queue_size=1)
    killer = rospy.Publisher('/killme', String, queue_size=1)

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    while not rospy.is_shutdown():
        rospy.loginfo("Esperando mensagem no /govai")
        pose = rospy.wait_for_message('/govai', Pose)
        
        # rospy.loginfo("Esperando odometria")
        # odometry = rospy.wait_for_message('/odom', Odometry)
        goal = MoveBaseGoal()
        goal.target_pose.pose.position.x = pose.position.x
        goal.target_pose.pose.position.y = pose.position.y
        goal.target_pose.pose.orientation.w = 1
        
        

        if pose.position.z == 0:
            client.cancel_all_goals()
            rospy.loginfo("Movendo relativo")
            goal.target_pose.header.frame_id = "base_footprint"
            goal.target_pose.header.stamp = rospy.Time.now()
            client.send_goal(goal)
        elif pose.position.z == 1:
            rospy.loginfo("Movendo absoluto")
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            client.send_goal(goal)
            wait = client.wait_for_result()
            if wait and client.get_result():
                msg = String()
                msg.data = "0"
                pub.publish(msg)
                rospy.loginfo("Goal execution done!")
        elif pose.position.z == -1:
            rospy.loginfo("Movendo para base")
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            client.send_goal(goal)
            wait = client.wait_for_result()
            if wait and client.get_result():
                killer.publish(String())

   

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        rospy.loginfo("move_base iniciado")
        movebase_client()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")