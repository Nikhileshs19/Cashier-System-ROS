#!/usr/bin/python3
import rospy
from std_msgs.msg import String
from cashier_sys.msg import bill


def publisher():
    rospy.init_node('Cashier_Publisher', anonymous=True)
    pub = rospy.Publisher('bill_invoice', bill, queue_size=10)
    
    rate = rospy.Rate(10) # 10hz

    bill_num = 1

    # print("Enter your input below")
    while not rospy.is_shutdown():
        quantity = int(input("Enter number of products: "))
        price = float(input("Enter price of product: "))

        bill_msg = bill()
        bill_msg.bill_number = bill_num
        bill_num += 1
        bill_msg.timestamp = rospy.Time.now()
        bill_msg.quantity = quantity
        bill_msg.price = price
        bill_msg.total = (bill_msg.quantity * bill_msg.price)

        pub.publish(bill_msg)
        # rospy.loginfo('Bill published: {}'.format(bill_msg))

        rate.sleep()


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass