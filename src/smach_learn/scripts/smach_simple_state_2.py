#!/usr/bin/env python3
"""
Modify the example from smach Learning by Example :
* Link : http://wiki.ros.org/smach/Tutorials)
And add the SMACH_Viewer
* Reference: http://wiki.ros.org/smach/Tutorials/Smach%20Viewer
"""
import rospy
import smach
import smach_ros


# define state Foo
class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1', 'outcome2'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        if self.counter < 10:
            self.counter += 1
            rospy.sleep(5.0)
            return 'outcome1'
        else:
            rospy.sleep(5.0)
            return 'outcome2'

# define state Bar


class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        rospy.sleep(5.0)
        return 'outcome1'


def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4'])

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('FOO', Foo(),
                               transitions={'outcome1': 'BAR', 'outcome2': 'outcome4'})
        smach.StateMachine.add('BAR', Bar(),
                               transitions={'outcome1': 'FOO'})

    # Execute SMACH plan
    outcome = sm.execute()
    sis.stop()


if __name__ == '__main__':
    main()
