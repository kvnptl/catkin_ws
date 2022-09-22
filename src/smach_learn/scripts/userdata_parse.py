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
        smach.State.__init__(self,
                             outcomes=['outcome1', 'outcome2'],
                             input_keys=['foo_counter_in'],
                             output_keys=['foo_counter_out'])

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        if userdata.foo_counter_in < 10:
            userdata.foo_counter_out = userdata.foo_counter_in + 1
            rospy.sleep(2.0)
            return 'outcome1'
        else:
            rospy.sleep(2.0)
            return 'outcome2'


# define state Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome1'],
                             input_keys=['bar_counter_in'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        rospy.loginfo('Counter = %f' % userdata.bar_counter_in)
        rospy.sleep(2.0)
        return 'outcome1'


def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4'])
    sm.userdata.sm_counter = 0

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('FOO', Foo(),
                               transitions={'outcome1': 'BAR',
                                            'outcome2': 'outcome4'},
                               remapping={'foo_counter_in': 'sm_counter',
                                          'foo_counter_out': 'sm_counter'})
        smach.StateMachine.add('BAR', Bar(),
                               transitions={'outcome1': 'FOO'},
                               remapping={'bar_counter_in': 'sm_counter'})

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.sleep(20.0)
    sis.stop()


if __name__ == '__main__':
    main()
