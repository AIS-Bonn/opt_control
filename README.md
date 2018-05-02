
opt_control - Time-optimal Trajectory Generation and Control
=====================================================================

`opt_control` generates time-optimal third order trajectories with constant jerk, resulting in bang-singular-bang trajectories.
The trajectories respect per-axis constraints on minimum and maximum velocity, acceleration and jerk.
Individual axes can be coupled by synchronizing the total time of the each trajectory.
Since the method is very fast (<<1ms), it can be used in closed loop even for fast systems.
With the ability to predict the target state, trajectories end in an optimal interception point when the waypoint is non-stationary.
It has been successfully used on different micro aerial vehicles, in different research projects and robotic competitions.


Papers Describing the Approach
--------
Marius Beul and Sven Behnke: [Fast Full State Trajectory Generation for Multirotors](http://ais.uni-bonn.de/papers/ICUAS_2017_Beul_Trajectory_Generation.pdf) In Proceedings of International Conference on Unmanned Aircraft Systems (ICUAS), Miami, FL, USA, June 2017

Marius Beul and Sven Behnke: [Analytical Time-optimal Trajectory Generation and Control for Multirotors](http://ais.uni-bonn.de/papers/ICUAS_2016_Beul.pdf) In Proceedings of International Conference on Unmanned Aircraft Systems (ICUAS), Arlington, VA, USA, June 2016


Dependencies
---------------

* Ubuntu 16.04

* [ROS Kinetic](http://wiki.ros.org/kinetic/Installation):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.sh}
sudo apt-get install ros-kinetic-desktop-full
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Getting started
---------------
Clone the repository in your catkin workspace (here ~/catkin_ws)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.sh}
cd ~/catkin_ws/src
git clone https://github.com/AIS-Bonn/opt_control opt_control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
and build it with catkin_make (or catkin tools):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.sh}
cd ~/catkin_ws/
catkin_make
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
run opt_control.launch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.sh}
roslaunch opt_control opt_control.launch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

License
-------

`opt_control` is licensed under the BSD 3-clause license.

Contact
-----------------

```
Marius Beul <mbeul@ais.uni-bonn.de>
Institute of Computer Science VI
Rheinische Friedrich-Wilhelms-Universität Bonn
Endenicher Allee 19a
53115 Bonn
```
