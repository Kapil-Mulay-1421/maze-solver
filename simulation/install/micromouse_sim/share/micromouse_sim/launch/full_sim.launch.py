from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
import os

def generate_launch_description():
    pkg_share = FindPackageShare('micromouse_sim')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([pkg_share, 'worlds', 'maze.world'])
        }.items()
    )

    robot_description_content = Command([
    'xacro ', PathJoinSubstitution([pkg_share, 'urdf', 'skid.xacro'])
    ])

    robot_description = {'robot_description': robot_description_content}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Spawn URDF model into Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_micromouse',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'micromouse',
            '-x', '-1.5', '-y', '-2.32', '-z', '0.08'
        ],
        output='screen'
    )

    # Launch your control node
    controller = Node(
        package='micromouse_sim',
        executable='ros_simulator',
        name='ros_simulator',
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher_node,
        spawn_robot,
        controller
    ])