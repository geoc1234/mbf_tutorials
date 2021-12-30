#!/usr/bin/env python
#
# @author Julian Gaal
# License: 3-Clause BSD 

import actionlib
import rospy
import mbf_msgs.msg as mbf_msgs
import geometry_msgs.msg as geometry_msgs


def create_pose(x, y, z, xx, yy, zz, ww):
    pose = geometry_msgs.PoseStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = xx
    pose.pose.orientation.y = yy
    pose.pose.orientation.z = zz
    pose.pose.orientation.w = ww
    return pose


def create_path_goal(path, tolerance_from_action, dist_tolerance, angle_tolerance):
    goal = mbf_msgs.ExePathGoal()
    goal.path = path
    goal.tolerance_from_action = tolerance_from_action
    goal.dist_tolerance = dist_tolerance
    goal.angle_tolerance = angle_tolerance
    return goal


def exe_path(path_goal):
    mbf_ep_ac.send_goal(path_goal)
    mbf_ep_ac.wait_for_result()
    return mbf_ep_ac.get_result()


def get_plan(pose):
    path_goal = mbf_msgs.GetPathGoal(target_pose=pose, tolerance=0.5)
    mbf_gp_ac.send_goal(path_goal)
    mbf_gp_ac.wait_for_result()
    return mbf_gp_ac.get_result()


def drive_circle():
    target_poses = [   
        create_pose(0.0, 0.0, 0, 0, 0, -0.020, 0.999)
    ]

    for target_pose in target_poses:
        rospy.loginfo("Attempting to reach (%1.3f, %1.3f)", target_pose.pose.position.x, target_pose.pose.position.y)
        
        get_path_result = get_plan(target_pose)
        if get_path_result.outcome != mbf_msgs.MoveBaseResult.SUCCESS:
            rospy.loginfo("Unable to complete plan: %s", result.message)
            return 

        path_goal = create_path_goal(get_path_result.path, True, 0.5, 3.14/18.0)

        exe_path_result = exe_path(path_goal)
        if exe_path_result.outcome != mbf_msgs.MoveBaseResult.SUCCESS:
            rospy.loginfo("Unable to complete exe:")
            return 


if __name__ == '__main__':
    rospy.init_node("move_base_flex_client")

    # move_base_flex exe path client
    mbf_ep_ac = actionlib.SimpleActionClient("move_base_flex/exe_path", mbf_msgs.ExePathAction)
    mbf_ep_ac.wait_for_server(rospy.Duration(10))
    rospy.loginfo("Connected to Move Base Flex ExePath server!")

    # move base flex get path client
    mbf_gp_ac = actionlib.SimpleActionClient("move_base_flex/get_path", mbf_msgs.GetPathAction)
    mbf_gp_ac.wait_for_server(rospy.Duration(10))

    drive_circle()

    rospy.on_shutdown(lambda: mbf_ep_ac.cancel_all_goals())

