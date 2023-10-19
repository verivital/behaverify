module LightController where
import BehaviorTreeCore
import BTreeCheckFairness
import BTreeTurnLightOff
import BTreeSwapDirection
import BTreeSetWest
import BTreeSetEast
import BTreeSendLightSignal
import BTreeCheckTunnelEmpty
import BTreeCheckWestAndEastCars
import BTreeCheckWestCars
import BTreeCheckEastCars
bTreeNodeCheckTunnelEmpty = BTreeNode bTreeFunctionCheckTunnelEmpty [] 2
bTreeNodeTurnLightOff = BTreeNode bTreeFunctionTurnLightOff [] 3
bTreeNodeTunnelClear = BTreeNode selectorFunc [bTreeNodeCheckTunnelEmpty, bTreeNodeTurnLightOff] 1
bTreeNodeCheckWestAndEastCars = BTreeNode bTreeFunctionCheckWestAndEastCars [] 6
bTreeNodeCheckFairness = BTreeNode bTreeFunctionCheckFairness [] 8
bTreeNodeSwapDirection = BTreeNode bTreeFunctionSwapDirection [] 9
bTreeNodeChooseFairly = BTreeNode selectorFunc [bTreeNodeCheckFairness, bTreeNodeSwapDirection] 7
bTreeNodeTryWestAndEast = BTreeNode sequenceFunc [bTreeNodeCheckWestAndEastCars, bTreeNodeChooseFairly] 5
bTreeNodeCheckWestCars = BTreeNode bTreeFunctionCheckWestCars [] 11
bTreeNodeSetWest = BTreeNode bTreeFunctionSetWest [] 12
bTreeNodeTryWest = BTreeNode sequenceFunc [bTreeNodeCheckWestCars, bTreeNodeSetWest] 10
bTreeNodeCheckEastCars = BTreeNode bTreeFunctionCheckEastCars [] 14
bTreeNodeSetEast = BTreeNode bTreeFunctionSetEast [] 15
bTreeNodeTryEast = BTreeNode sequenceFunc [bTreeNodeCheckEastCars, bTreeNodeSetEast] 13
bTreeNodeSelectDirection = BTreeNode selectorFunc [bTreeNodeTryWestAndEast, bTreeNodeTryWest, bTreeNodeTryEast] 4
bTreeNodeSendLightSignal = BTreeNode bTreeFunctionSendLightSignal [] 16
bTreeNodeLightController = BTreeNode sequenceFunc [bTreeNodeTunnelClear, bTreeNodeSelectDirection, bTreeNodeSendLightSignal] 0
