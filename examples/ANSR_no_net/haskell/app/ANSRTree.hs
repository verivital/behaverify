module ANSRTree where
import BehaviorTreeCore
import BTreeNotAtDestination
import BTreeYTooSmall
import BTreeYTooBig
import BTreeXTooSmall
import BTreeXTooBig
import BTreeUpdateDestination
import BTreeMove
import BTreeSendVictory
import BTreeUpdateDirection
import BTreeTargetInSight
bTreeNodeTargetInSight = BTreeNode bTreeFunctionTargetInSight [] 2
bTreeNodeSendVictory = BTreeNode bTreeFunctionSendVictory [] 3
bTreeNodeVision = BTreeNode sequenceFunc [bTreeNodeTargetInSight, bTreeNodeSendVictory] 1
bTreeNodeNotAtDestination = BTreeNode bTreeFunctionNotAtDestination [] 6
bTreeNodeUpdateDirection = BTreeNode bTreeFunctionUpdateDirection [] 8
bTreeNodeUpdateDestination = BTreeNode bTreeFunctionUpdateDestination [] 9
bTreeNodeNewDestination = BTreeNode sequenceFunc [bTreeNodeUpdateDirection, bTreeNodeUpdateDestination] 7
bTreeNodeDestination = BTreeNode selectorFunc [bTreeNodeNotAtDestination, bTreeNodeNewDestination] 5
bTreeNodeYTooSmall = BTreeNode bTreeFunctionYTooSmall [] 12
bTreeNodeMove = BTreeNode (bTreeFunctionCreatorMove (0) (1)) [] 13
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeYTooSmall, bTreeNodeMove] 11
bTreeNodeYTooBig = BTreeNode bTreeFunctionYTooBig [] 15
bTreeNodeMove_1 = BTreeNode (bTreeFunctionCreatorMove (0) ((-1))) [] 16
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeYTooBig, bTreeNodeMove_1] 14
bTreeNodeXTooBig = BTreeNode bTreeFunctionXTooBig [] 18
bTreeNodeMove_2 = BTreeNode (bTreeFunctionCreatorMove ((-1)) (0)) [] 19
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeXTooBig, bTreeNodeMove_2] 17
bTreeNodeXTooSmall = BTreeNode bTreeFunctionXTooSmall [] 21
bTreeNodeMove_3 = BTreeNode (bTreeFunctionCreatorMove (1) (0)) [] 22
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeXTooSmall, bTreeNodeMove_3] 20
bTreeNodeMovement = BTreeNode selectorFunc [bTreeNodeTryUp, bTreeNodeTryDown, bTreeNodeTryLeft, bTreeNodeTryRight] 10
bTreeNodeDestinationAndMovement = BTreeNode sequenceFunc [bTreeNodeDestination, bTreeNodeMovement] 4
bTreeNodeDroneControl = BTreeNode selectorFunc [bTreeNodeVision, bTreeNodeDestinationAndMovement] 0
