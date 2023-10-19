module SimplifiedRobot where
import BehaviorTreeCore
import BTreeGoX
import BTreeGoY
import BTreeXTooSmall
import BTreeXTooBig
import BTreeYTooSmall
import BTreeYTooBig
bTreeNodeXTooSmall = BTreeNode bTreeFunctionXTooSmall [] 2
bTreeNodeGoX = BTreeNode (bTreeFunctionCreatorGoX 1) [] 3
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeXTooSmall, bTreeNodeGoX] 1
bTreeNodeXTooBig = BTreeNode bTreeFunctionXTooBig [] 5
bTreeNodeGoX_1 = BTreeNode (bTreeFunctionCreatorGoX (-1)) [] 6
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeXTooBig, bTreeNodeGoX_1] 4
bTreeNodeYTooSmall = BTreeNode bTreeFunctionYTooSmall [] 8
bTreeNodeGoY = BTreeNode (bTreeFunctionCreatorGoY 1) [] 9
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeYTooSmall, bTreeNodeGoY] 7
bTreeNodeYTooBig = BTreeNode bTreeFunctionYTooBig [] 11
bTreeNodeGoY_1 = BTreeNode (bTreeFunctionCreatorGoY (-1)) [] 12
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeYTooBig, bTreeNodeGoY_1] 10
bTreeNodeMoveRobot = BTreeNode selectorFunc [bTreeNodeTryRight, bTreeNodeTryLeft, bTreeNodeTryUp, bTreeNodeTryDown] 0
