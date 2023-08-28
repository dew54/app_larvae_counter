import rclpy
from rclpy.node import Node
import os
import cv2
import threading
from cv_bridge import CvBridge
from preProcess import PreProcess
from featureExtraction import FeatureExtraction
from model import Model

from std_msgs.msg import String

class Counter(Node):
    def __init__(self):
        super().__init__('counter')
        self.subscription = self.create_subscription(
            String,
            'floater/microscope',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(String, 'counter', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.message_processed = threading.Event()

    def image_callback(self, msg):
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")  # Convert ROS Image message to OpenCV format
            self.count = counter(cv_image)
            self.message_processed.set()
            # cv2.imshow("Microscope Image", cv_image)
            # cv2.waitKey(1)
        except Exception as e:
            print(e)
    
    def timer_callback(self):
        msg = String()
        msg.data = self.counter
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


            
    def counter(image):

        descBatch = extractDescriptors(image)
        counter = 0       

        for descList in descBatch:
            response = model.classifyImage(descList)
            counter += response

        return response
    def extractDescriptors(image):

        image = PreProcess.resize(image, 1280, 720)
        correlationMap = PreProcess.sliding_correlation(image)
        circles_info = PreProcess.findCenters(correlationMap)
        image = PreProcess.unsharpMask(image)
        equalizedImage = PreProcess.equalize(image)
        descBatch = FeatureExtraction.extract_DESC(image, circles_info)

        return descBatch


    def main(args=None):
        rclpy.init(args=args)

        counter = Counter()

        rclpy.spin(counter)

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        minimal_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()