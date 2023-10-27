#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from cashier_sys.msg import bill


inv_p = '/inventory'
income_p = '/income'

# Init
last_bill = None

def bill_callback(bill):
    global last_bill
    last_bill = bill

def monitor():
    rospy.init_node('Cashier_Monitor', anonymous=True)

    rospy.Subscriber('bill_invoice', bill, bill_callback)

    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():

        user_input = input()
        # Print last bill
        if last_bill is not None:
            rospy.loginfo('Last Bill: {}'.format(last_bill))
        else:
            rospy.loginfo('No bills received yet.')

        inventory = rospy.get_param(inv_p, 100) # assuming init inv as 100
        income = rospy.get_param(income_p, 0)

        rospy.loginfo('Current Inventory: {}'.format(inventory))
        rospy.loginfo('Current Income: {}'.format(income))

        rate.sleep()

if __name__ == '__main__':
    try:
        monitor()
    except rospy.ROSInterruptException:
        pass
