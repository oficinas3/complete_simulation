#!/usr/bin/env python
import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point

target_id = 0
def update_goal(markers_data):
    for m in markers_data.markers:
        if m.id == target_id:
            
            rospy.loginfo(m.pose.pose.position.z)
            
def get_artag_pose():
    pub = rospy.Publisher('/govai', Point, queue_size=10)
    rospy.init_node('follower', anonymous=True)
    # rospy.Subscriber('/ar_pose_marker', AlvarMarkers, update_goal)
    rospy.loginfo("No iniciado")
    
    pt = Point()
    pt.x = 7
    pt.y = 1
    rospy.loginfo(pt)
    pub.publish(pt)
    
    rospy.loginfo("Publicando")

    rospy.spin()
if __name__ == "__main__":
    try:
        get_artag_pose()
    except rospy.ROSInterruptException:
        pass