module ANSRTree where
import BehaviorTreeCore
import BTreeNotAtDestination
import BTreeYTooSmall
import BTreeYTooBig
import BTreeXTooSmall
import BTreeXTooBig
import BTreeCallXyNet
import BTreeMove
import BTreeSendVictory
import BTreeUpdateDirection
import BTreeUpdatePreviousDestination
import BTreeTargetInSight
bTreeNodeTargetInSight = BTreeNode bTreeFunctionTargetInSight [] 2
bTreeNodeSendVictory = BTreeNode bTreeFunctionSendVictory [] 3
bTreeNodeVision = BTreeNode sequenceFunc [bTreeNodeTargetInSight, bTreeNodeSendVictory] 1
bTreeNodeNotAtDestination = BTreeNode bTreeFunctionNotAtDestination [] 6
bTreeNodeUpdateDirection = BTreeNode bTreeFunctionUpdateDirection [] 8
bTreeNodeCallXyNet = BTreeNode bTreeFunctionCallXyNet [] 9
bTreeNodeUpdatePreviousDestination = BTreeNode bTreeFunctionUpdatePreviousDestination [] 10
bTreeNodeNewDestination = BTreeNode sequenceFunc [bTreeNodeUpdateDirection, bTreeNodeCallXyNet, bTreeNodeUpdatePreviousDestination] 7
bTreeNodeDestination = BTreeNode selectorFunc [bTreeNodeNotAtDestination, bTreeNodeNewDestination] 5
bTreeNodeYTooSmall = BTreeNode bTreeFunctionYTooSmall [] 13
bTreeNodeMove = BTreeNode (bTreeFunctionCreatorMove 0 1) [] 14
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeYTooSmall, bTreeNodeMove] 12
bTreeNodeYTooBig = BTreeNode bTreeFunctionYTooBig [] 16
bTreeNodeMove_1 = BTreeNode (bTreeFunctionCreatorMove 0 (-1)) [] 17
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeYTooBig, bTreeNodeMove_1] 15
bTreeNodeXTooBig = BTreeNode bTreeFunctionXTooBig [] 19
bTreeNodeMove_2 = BTreeNode (bTreeFunctionCreatorMove (-1) 0) [] 20
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeXTooBig, bTreeNodeMove_2] 18
bTreeNodeXTooSmall = BTreeNode bTreeFunctionXTooSmall [] 22
bTreeNodeMove_3 = BTreeNode (bTreeFunctionCreatorMove 1 0) [] 23
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeXTooSmall, bTreeNodeMove_3] 21
bTreeNodeMovement = BTreeNode selectorFunc [bTreeNodeTryUp, bTreeNodeTryDown, bTreeNodeTryLeft, bTreeNodeTryRight] 11
bTreeNodeDestinationAndMovement = BTreeNode sequenceFunc [bTreeNodeDestination, bTreeNodeMovement] 4
bTreeNodeDroneControl = BTreeNode selectorFunc [bTreeNodeVision, bTreeNodeDestinationAndMovement] 0
