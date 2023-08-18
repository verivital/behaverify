module HaskellFrozenLake where
import BehaviorTreeCore
import BTreeXStrategy
import BTreeYStrategy
import BTreeGetInfo
import BTreeRequestHold
import BTreeRequestReset
import BTreeRequestUp
import BTreeRequestDown
import BTreeRequestLeft
import BTreeRequestRight
import BTreeSetNewSubgoal
import BTreeChangeStrategy
import BTreeSometimesChangeStrategy
import BTreeFellInHole
import BTreeUpBad
import BTreeDownBad
import BTreeLeftBad
import BTreeRightBad
import BTreeUpUnknown
import BTreeDownUnknown
import BTreeLeftUnknown
import BTreeRightUnknown
import BTreeNeedNewSubgoal
import BTreeNeedUp
import BTreeNeedDown
import BTreeNeedLeft
import BTreeNeedRight
import BTreeReachedGoal
import BTreeSubgoalUnreachable
bTreeNodeGetInfo = BTreeNode getInfo [] 1
bTreeNodeReachedGoal = BTreeNode reachedGoal [] 4
bTreeNodeRequestHold = BTreeNode requestHold [] 5
bTreeNodeAtGoalSequence = BTreeNode sequenceFunc [bTreeNodeReachedGoal, bTreeNodeRequestHold] 3
bTreeNodeFellInHole = BTreeNode fellInHole [] 7
bTreeNodeRequestReset = BTreeNode requestReset [] 8
bTreeNodeResetSequence = BTreeNode sequenceFunc [bTreeNodeFellInHole, bTreeNodeRequestReset] 6
bTreeNodeUpUnknown = BTreeNode upUnknown [] 11
bTreeNodeRequestUp = BTreeNode requestUp [] 12
bTreeNodeUpUnknownSeq = BTreeNode sequenceFunc [bTreeNodeUpUnknown, bTreeNodeRequestUp] 10
bTreeNodeDownUnknown = BTreeNode downUnknown [] 14
bTreeNodeRequestDown = BTreeNode requestDown [] 15
bTreeNodeDownUnknownSeq = BTreeNode sequenceFunc [bTreeNodeDownUnknown, bTreeNodeRequestDown] 13
bTreeNodeLeftUnknown = BTreeNode leftUnknown [] 17
bTreeNodeRequestLeft = BTreeNode requestLeft [] 18
bTreeNodeLeftUnknownSeq = BTreeNode sequenceFunc [bTreeNodeLeftUnknown, bTreeNodeRequestLeft] 16
bTreeNodeRightUnknown = BTreeNode rightUnknown [] 20
bTreeNodeRequestRight = BTreeNode requestRight [] 21
bTreeNodeRightUnknownSeq = BTreeNode sequenceFunc [bTreeNodeRightUnknown, bTreeNodeRequestRight] 19
bTreeNodeAdjacentUnknown = BTreeNode selectorFunc [bTreeNodeUpUnknownSeq, bTreeNodeDownUnknownSeq, bTreeNodeLeftUnknownSeq, bTreeNodeRightUnknownSeq] 9
bTreeNodeNeedNewSubgoal = BTreeNode needNewSubgoal [] 25
bTreeNodeSetNewSubgoal = BTreeNode setNewSubgoal [] 26
bTreeNodeSubgoalSeq = BTreeNode sequenceFunc [bTreeNodeNeedNewSubgoal, bTreeNodeSetNewSubgoal] 24
bTreeNodeSubgoalFailureIsSuccess = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeSubgoalSeq] 23
bTreeNodeXStrategy = BTreeNode xStrategy [] 30
bTreeNodeNeedLeft = BTreeNode needLeft [] 33
bTreeNodeLeftBad = BTreeNode leftBad [] 35
bTreeNodeLeftBadInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeLeftBad] 34
bTreeNodeRequestLeft_1 = BTreeNode requestLeft [] 36
bTreeNodeTryLeft = BTreeNode sequenceFunc [bTreeNodeNeedLeft, bTreeNodeLeftBadInverter, bTreeNodeRequestLeft_1] 32
bTreeNodeNeedRight = BTreeNode needRight [] 38
bTreeNodeRightBad = BTreeNode rightBad [] 40
bTreeNodeRightBadInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeRightBad] 39
bTreeNodeRequestRight_1 = BTreeNode requestRight [] 41
bTreeNodeTryRight = BTreeNode sequenceFunc [bTreeNodeNeedRight, bTreeNodeRightBadInverter, bTreeNodeRequestRight_1] 37
bTreeNodeTryX = BTreeNode selectorFunc [bTreeNodeTryLeft, bTreeNodeTryRight] 31
bTreeNodeOptXMovement = BTreeNode sequenceFunc [bTreeNodeXStrategy, bTreeNodeTryX] 29
bTreeNodeYStrategy = BTreeNode yStrategy [] 43
bTreeNodeNeedUp = BTreeNode needUp [] 46
bTreeNodeUpBad = BTreeNode upBad [] 48
bTreeNodeUpBadInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeUpBad] 47
bTreeNodeRequestUp_1 = BTreeNode requestUp [] 49
bTreeNodeTryUp = BTreeNode sequenceFunc [bTreeNodeNeedUp, bTreeNodeUpBadInverter, bTreeNodeRequestUp_1] 45
bTreeNodeNeedDown = BTreeNode needDown [] 51
bTreeNodeDownBad = BTreeNode downBad [] 53
bTreeNodeDownBadInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeDownBad] 52
bTreeNodeRequestDown_1 = BTreeNode requestDown [] 54
bTreeNodeTryDown = BTreeNode sequenceFunc [bTreeNodeNeedDown, bTreeNodeDownBadInverter, bTreeNodeRequestDown_1] 50
bTreeNodeTryY = BTreeNode selectorFunc [bTreeNodeTryUp, bTreeNodeTryDown] 44
bTreeNodeOptYMovement = BTreeNode sequenceFunc [bTreeNodeYStrategy, bTreeNodeTryY] 42
bTreeNodeXOrYMovementSelector = BTreeNode selectorFunc [bTreeNodeOptXMovement, bTreeNodeOptYMovement] 28
bTreeNodeNeedLeft_1 = BTreeNode needLeft [] 57
bTreeNodeLeftBad_1 = BTreeNode leftBad [] 59
bTreeNodeLeftBadInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeLeftBad_1] 58
bTreeNodeRequestLeft_2 = BTreeNode requestLeft [] 60
bTreeNodeTryLeft_1 = BTreeNode sequenceFunc [bTreeNodeNeedLeft_1, bTreeNodeLeftBadInverter_1, bTreeNodeRequestLeft_2] 56
bTreeNodeNeedRight_1 = BTreeNode needRight [] 62
bTreeNodeRightBad_1 = BTreeNode rightBad [] 64
bTreeNodeRightBadInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeRightBad_1] 63
bTreeNodeRequestRight_2 = BTreeNode requestRight [] 65
bTreeNodeTryRight_1 = BTreeNode sequenceFunc [bTreeNodeNeedRight_1, bTreeNodeRightBadInverter_1, bTreeNodeRequestRight_2] 61
bTreeNodeTryX_1 = BTreeNode selectorFunc [bTreeNodeTryLeft_1, bTreeNodeTryRight_1] 55
bTreeNodeNeedUp_1 = BTreeNode needUp [] 68
bTreeNodeUpBad_1 = BTreeNode upBad [] 70
bTreeNodeUpBadInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeUpBad_1] 69
bTreeNodeRequestUp_2 = BTreeNode requestUp [] 71
bTreeNodeTryUp_1 = BTreeNode sequenceFunc [bTreeNodeNeedUp_1, bTreeNodeUpBadInverter_1, bTreeNodeRequestUp_2] 67
bTreeNodeNeedDown_1 = BTreeNode needDown [] 73
bTreeNodeDownBad_1 = BTreeNode downBad [] 75
bTreeNodeDownBadInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeDownBad_1] 74
bTreeNodeRequestDown_2 = BTreeNode requestDown [] 76
bTreeNodeTryDown_1 = BTreeNode sequenceFunc [bTreeNodeNeedDown_1, bTreeNodeDownBadInverter_1, bTreeNodeRequestDown_2] 72
bTreeNodeTryY_1 = BTreeNode selectorFunc [bTreeNodeTryUp_1, bTreeNodeTryDown_1] 66
bTreeNodeSubgoalUnreachable = BTreeNode subgoalUnreachable [] 79
bTreeNodeRequestHold_1 = BTreeNode requestHold [] 80
bTreeNodeNewSubgoalStrategy = BTreeNode sequenceFunc [bTreeNodeSubgoalUnreachable, bTreeNodeRequestHold_1] 78
bTreeNodeXStrategy_1 = BTreeNode xStrategy [] 83
bTreeNodeUpBad_2 = BTreeNode upBad [] 85
bTreeNodeUpBadInverter_2 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeUpBad_2] 84
bTreeNodeRequestUp_3 = BTreeNode requestUp [] 86
bTreeNodeSometimesChangeStrategy = BTreeNode sometimesChangeStrategy [] 87
bTreeNodeNaviUp = BTreeNode sequenceFunc [bTreeNodeXStrategy_1, bTreeNodeUpBadInverter_2, bTreeNodeRequestUp_3, bTreeNodeSometimesChangeStrategy] 82
bTreeNodeXStrategy_2 = BTreeNode xStrategy [] 89
bTreeNodeDownBad_2 = BTreeNode downBad [] 91
bTreeNodeDownBadInverter_2 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeDownBad_2] 90
bTreeNodeRequestDown_3 = BTreeNode requestDown [] 92
bTreeNodeSometimesChangeStrategy_1 = BTreeNode sometimesChangeStrategy [] 93
bTreeNodeNaviDown = BTreeNode sequenceFunc [bTreeNodeXStrategy_2, bTreeNodeDownBadInverter_2, bTreeNodeRequestDown_3, bTreeNodeSometimesChangeStrategy_1] 88
bTreeNodeYStrategy_1 = BTreeNode yStrategy [] 95
bTreeNodeLeftBad_2 = BTreeNode leftBad [] 97
bTreeNodeLeftBadInverter_2 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeLeftBad_2] 96
bTreeNodeRequestLeft_3 = BTreeNode requestLeft [] 98
bTreeNodeSometimesChangeStrategy_2 = BTreeNode sometimesChangeStrategy [] 99
bTreeNodeNaviLeft = BTreeNode sequenceFunc [bTreeNodeYStrategy_1, bTreeNodeLeftBadInverter_2, bTreeNodeRequestLeft_3, bTreeNodeSometimesChangeStrategy_2] 94
bTreeNodeYStrategy_2 = BTreeNode yStrategy [] 101
bTreeNodeRightBad_2 = BTreeNode rightBad [] 103
bTreeNodeRightBadInverter_2 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeRightBad_2] 102
bTreeNodeRequestRight_3 = BTreeNode requestRight [] 104
bTreeNodeSometimesChangeStrategy_3 = BTreeNode sometimesChangeStrategy [] 105
bTreeNodeNaviRight = BTreeNode sequenceFunc [bTreeNodeYStrategy_2, bTreeNodeRightBadInverter_2, bTreeNodeRequestRight_3, bTreeNodeSometimesChangeStrategy_3] 100
bTreeNodeRequestHold_2 = BTreeNode requestHold [] 107
bTreeNodeChangeStrategy = BTreeNode changeStrategy [] 108
bTreeNodeHoldAndChange = BTreeNode sequenceFunc [bTreeNodeRequestHold_2, bTreeNodeChangeStrategy] 106
bTreeNodeNewNavigationStrategy = BTreeNode selectorFunc [bTreeNodeNaviUp, bTreeNodeNaviDown, bTreeNodeNaviLeft, bTreeNodeNaviRight, bTreeNodeHoldAndChange] 81
bTreeNodeFailurePlan = BTreeNode selectorFunc [bTreeNodeNewSubgoalStrategy, bTreeNodeNewNavigationStrategy] 77
bTreeNodeMoveSelector = BTreeNode selectorFunc [bTreeNodeXOrYMovementSelector, bTreeNodeTryX_1, bTreeNodeTryY_1, bTreeNodeFailurePlan] 27
bTreeNodeNavigationSequence = BTreeNode sequenceFunc [bTreeNodeSubgoalFailureIsSuccess, bTreeNodeMoveSelector] 22
bTreeNodePickAction = BTreeNode selectorFunc [bTreeNodeAtGoalSequence, bTreeNodeResetSequence, bTreeNodeAdjacentUnknown, bTreeNodeNavigationSequence] 2
bTreeNodeExecutionSequence = BTreeNode sequenceFunc [bTreeNodeGetInfo, bTreeNodePickAction] 0
