import rospy
from std_msgs.msg import String
from cashier_sys.msg import bill
from cashier_sys.srv import update
# from cashier_sys.srv._update import UpdateRequest

inv_p = '/inventory'
income_p = '/income'

inventory = 100
income = 0

def bill_callback(bill):
    
    quantity = bill.quantity
    price = bill.price

    # Service call
    rospy.wait_for_service('/update_parameters')
    try:
        update_parameters = rospy.ServiceProxy('/update_parameters', update)
        response = update_parameters(quantity, price)
        if response.success:
            rospy.loginfo("Parameters updated successfully.")
        else:
            rospy.loginfo("Failed to update parameters.")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)


def handle_update_parameters(request):
    # Current
    inventory = rospy.get_param(inv_p, 100) #assuming intial inventory as 100
    income = rospy.get_param(income_p, 0)

    change_in_inventory = request.quantity
    change_in_income = request.quantity * request.price

    # Updating
    rospy.set_param(inv_p, inventory - change_in_inventory)
    rospy.set_param(income_p, income + change_in_income)

    return 'Parameters updated successfully'

def subscriber():
    rospy.init_node('Cashier_Subscriber', anonymous=True)

    rospy.Subscriber('bill_invoice', bill, bill_callback)
    rospy.Service('update_parameters', update, handle_update_parameters)

    # inventory = rospy.get_param('/inventory', 100)
    # income = rospy.get_param('/income', 0)

    rospy.spin()


if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass
