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
        if self.counter < 3:
            self.counter += 1
            rospy.sleep(2.0)
            return 'outcome1'
        else:
            rospy.sleep(2.0)
            return 'outcome2'


# define state Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        rospy.sleep(2.0)
        return 'outcome1'


# define state Bas
class Bas(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome3'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAS')
        rospy.sleep(2.0)
        return 'outcome3'


def main():
    rospy.init_node('smach_example_state_machine')

    # Create the top level SMACH state machine
    sm_top = smach.StateMachine(outcomes=['outcome5'])

    # Open the container
    with sm_top:
        smach.StateMachine.add('BAS', Bas(),
                               transitions={'outcome3': 'SUB'})

        # Create the sub SMACH state machine
        sm_sub = smach.StateMachine(outcomes=['outcome4'])

        # Open the container
        with sm_sub:
            # Add states to the container
            smach.StateMachine.add('FOO', Foo(),
                                   transitions={'outcome1': 'BAR',
                                                'outcome2': 'outcome4'})
            smach.StateMachine.add('BAR', Bar(),
                                   transitions={'outcome1': 'FOO'})

        smach.StateMachine.add('SUB', sm_sub,
                               transitions={'outcome4': 'outcome5'})
    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
    sis.start()
    """The Obsever need to be set at last. Otherwise it can't see the  SM defined after it."""
    # Execute SMACH plan
    outcome = sm_top.execute()
    sis.stop()


if __name__ == '__main__':
    main()
