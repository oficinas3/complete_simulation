#!/usr/bin/env python
import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Pose
from std_srvs.srv import Empty

target_id = 0
pub = rospy.Publisher('/govai', Pose, queue_size=10)

def update_goal(markers_data):
    lost = False
    for m in markers_data.markers:
        if m.id == target_id:
            artag_pose = Pose()
            artag_pose.position.x = m.pose.pose.position.z - 0.8
            artag_pose.position.y = m.pose.pose.position.x
            rospy.loginfo(m.pose.pose)
            if artag_pose.position.x > 0:
                pub.publish(artag_pose)

    # rospy.wait_for_service('clear_costmaps')
    # clear_costmaps = rospy.ServiceProxy('clear_costmaps', Empty)
    # clear_costmaps()

def get_artag_pose():
    rospy.init_node('follower', anonymous=True)
    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, update_goal)
    rospy.loginfo("No iniciado")

    rospy.spin()
if __name__ == "__main__":
    
    try:
        get_artag_pose()
    except rospy.ROSInterruptException:
        pass