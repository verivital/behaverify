module LightController where
import BehaviorTreeCore
import BTreeCheckFairness
import BTreePrepareRound
import BTreeTurnLightOff
import BTreeSwapDirection
import BTreeSetDirection
import BTreeSendLightSignal
import BTreeCheckTunnelInUse
import BTreeCheckWestAndEastCars
import BTreeCheckWestCars
import BTreeCheckEastCars
bTreeNodePrepareRound = BTreeNode bTreeFunctionPrepareRound [] 1
bTreeNodeCheckTunnelInUse = BTreeNode bTreeFunctionCheckTunnelInUse [] 4
bTreeNodeTurnLightOff = BTreeNode bTreeFunctionTurnLightOff [] 5
bTreeNodeTunnelInUse = BTreeNode sequenceFunc [bTreeNodeCheckTunnelInUse, bTreeNodeTurnLightOff] 3
bTreeNodeCheckWestAndEastCars = BTreeNode bTreeFunctionCheckWestAndEastCars [] 7
bTreeNodeCheckFairness = BTreeNode bTreeFunctionCheckFairness [] 9
bTreeNodeSwapDirection = BTreeNode bTreeFunctionSwapDirection [] 10
bTreeNodeChooseFairly = BTreeNode selectorFunc [bTreeNodeCheckFairness, bTreeNodeSwapDirection] 8
bTreeNodeTryWestAndEast = BTreeNode sequenceFunc [bTreeNodeCheckWestAndEastCars, bTreeNodeChooseFairly] 6
bTreeNodeCheckWestCars = BTreeNode bTreeFunctionCheckWestCars [] 12
bTreeNodeSetDirection = BTreeNode (bTreeFunctionCreatorSetDirection "west_to_east") [] 13
bTreeNodeTryWest = BTreeNode sequenceFunc [bTreeNodeCheckWestCars, bTreeNodeSetDirection] 11
bTreeNodeCheckEastCars = BTreeNode bTreeFunctionCheckEastCars [] 15
bTreeNodeSetDirection_1 = BTreeNode (bTreeFunctionCreatorSetDirection "east_to_west") [] 16
bTreeNodeTryEast = BTreeNode sequenceFunc [bTreeNodeCheckEastCars, bTreeNodeSetDirection_1] 14
bTreeNodeSelectDirection = BTreeNode selectorFunc [bTreeNodeTunnelInUse, bTreeNodeTryWestAndEast, bTreeNodeTryWest, bTreeNodeTryEast] 2
bTreeNodeSendLightSignal = BTreeNode bTreeFunctionSendLightSignal [] 17
bTreeNodeLightController = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodePrepareRound, bTreeNodeSelectDirection, bTreeNodeSendLightSignal] 0
