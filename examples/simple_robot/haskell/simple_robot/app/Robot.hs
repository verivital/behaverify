module Robot where
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
bTreeNodeGetPosition = BTreeNode getPosition [] 1
bTreeNodeTargetReached = BTreeNode targetReached [] 4
bTreeNodeClearMission = BTreeNode clearMission [] 5
bTreeNodeResetCompletedMission = BTreeNode sequenceFunc [bTreeNodeTargetReached, bTreeNodeClearMission] 3
bTreeNodeResetCompletedMissionFis = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeResetCompletedMission] 2
bTreeNodeHaveMission = BTreeNode haveMission [] 7
bTreeNodeGetMission = BTreeNode getMission [] 8
bTreeNodeConfirmMission = BTreeNode selectorFunc [bTreeNodeHaveMission, bTreeNodeGetMission] 6
bTreeNodeXTooSmall = BTreeNode xTooSmall [] 11
bTreeNodeGoRight = BTreeNode goRight [] 12
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeXTooSmall, bTreeNodeGoRight] 10
bTreeNodeXTooBig = BTreeNode xTooBig [] 14
bTreeNodeGoLeft = BTreeNode goLeft [] 15
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeXTooBig, bTreeNodeGoLeft] 13
bTreeNodeYTooSmall = BTreeNode yTooSmall [] 17
bTreeNodeGoUp = BTreeNode goUp [] 18
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeYTooSmall, bTreeNodeGoUp] 16
bTreeNodeYTooBig = BTreeNode yTooBig [] 20
bTreeNodeGoDown = BTreeNode goDown [] 21
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeYTooBig, bTreeNodeGoDown] 19
bTreeNodeMoveRobot = BTreeNode selectorFunc [bTreeNodeTryRight, bTreeNodeTryLeft, bTreeNodeTryUp, bTreeNodeTryDown] 9
bTreeNodeRobotControl = BTreeNode sequenceFunc [bTreeNodeGetPosition, bTreeNodeResetCompletedMissionFis, bTreeNodeConfirmMission, bTreeNodeMoveRobot] 0
