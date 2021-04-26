#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Point
from tf.transformations import quaternion_from_euler

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    point = rospy.wait_for_message('/govai', Point)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = point.x
    goal.target_pose.pose.position.y = point.y
    goal.target_pose.pose.orientation.w = 1
    

    client.send_goal(goal)
    wait = client.wait_for_result()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    orientation = quaternion_from_euler(0,0,3.14)
    rospy.loginfo(orientation)
    goal.target_pose.pose.orientation.x = orientation[0]
    goal.target_pose.pose.orientation.y = orientation[1]
    goal.target_pose.pose.orientation.z = orientation[2]
    goal.target_pose.pose.orientation.w = orientation[3]
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")