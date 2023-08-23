FROM ros-node:generic

RUN mkdir /root/catkin_ws && mkdir /root/catkin_ws/src 

WORKDIR /root/

RUN catkin_create_pkg classifier rospy cv2 --rosdistro humble

WORKDIR /root/classifier/src

COPY . .
