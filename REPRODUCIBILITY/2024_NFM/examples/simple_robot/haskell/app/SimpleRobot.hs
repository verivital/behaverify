module SimpleRobot where
import BehaviorTreeCore
import BTreeHaveMission
import BTreeTargetReached
import BTreeXTooSmall
import BTreeXTooBig
import BTreeYTooSmall
import BTreeYTooBig
import BTreeGetMission
import BTreeGetPosition
import BTreeClearMission
import BTreeGoRight
import BTreeGoLeft
import BTreeGoUp
import BTreeGoDown
bTreeNodeGetPosition = BTreeNode bTreeFunctionGetPosition [] 1
bTreeNodeTargetReached = BTreeNode bTreeFunctionTargetReached [] 4
bTreeNodeClearMission = BTreeNode bTreeFunctionClearMission [] 5
bTreeNodeResetCompletedMission = BTreeNode sequenceFunc [bTreeNodeTargetReached, bTreeNodeClearMission] 3
bTreeNodeResetCompletedMissionFiS = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeResetCompletedMission] 2
bTreeNodeHaveMission = BTreeNode bTreeFunctionHaveMission [] 7
bTreeNodeGetMission = BTreeNode bTreeFunctionGetMission [] 8
bTreeNodeConfirmMission = BTreeNode selectorFunc [bTreeNodeHaveMission, bTreeNodeGetMission] 6
bTreeNodeXTooSmall = BTreeNode bTreeFunctionXTooSmall [] 11
bTreeNodeGoRight = BTreeNode bTreeFunctionGoRight [] 12
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeXTooSmall, bTreeNodeGoRight] 10
bTreeNodeXTooBig = BTreeNode bTreeFunctionXTooBig [] 14
bTreeNodeGoLeft = BTreeNode bTreeFunctionGoLeft [] 15
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeXTooBig, bTreeNodeGoLeft] 13
bTreeNodeYTooSmall = BTreeNode bTreeFunctionYTooSmall [] 17
bTreeNodeGoUp = BTreeNode bTreeFunctionGoUp [] 18
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeYTooSmall, bTreeNodeGoUp] 16
bTreeNodeYTooBig = BTreeNode bTreeFunctionYTooBig [] 20
bTreeNodeGoDown = BTreeNode bTreeFunctionGoDown [] 21
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeYTooBig, bTreeNodeGoDown] 19
bTreeNodeMoveRobot = BTreeNode selectorFunc [bTreeNodeTryRight, bTreeNodeTryLeft, bTreeNodeTryUp, bTreeNodeTryDown] 9
bTreeNodeRobotControl = BTreeNode sequenceFunc [bTreeNodeGetPosition, bTreeNodeResetCompletedMissionFiS, bTreeNodeConfirmMission, bTreeNodeMoveRobot] 0
