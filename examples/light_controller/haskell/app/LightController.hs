module LightController where
import BehaviorTreeCore
import BTreeCheckFairness
import BTreeSwapDirection
import BTreeSetWest
import BTreeSetEast
import BTreeSendLightSignal
import BTreeCheckWestAndEastCars
import BTreeCheckWestCars
import BTreeCheckEastCars
import BTreeCheckSafety
bTreeNodeCheckWestAndEastCars = BTreeNode bTreeFunctionCheckWestAndEastCars [] 3
bTreeNodeCheckFairness = BTreeNode bTreeFunctionCheckFairness [] 5
bTreeNodeSwapDirection = BTreeNode bTreeFunctionSwapDirection [] 6
bTreeNodeChooseFairly = BTreeNode selectorFunc [bTreeNodeCheckFairness, bTreeNodeSwapDirection] 4
bTreeNodeTryWestAndEast = BTreeNode sequenceFunc [bTreeNodeCheckWestAndEastCars, bTreeNodeChooseFairly] 2
bTreeNodeCheckWestCars = BTreeNode bTreeFunctionCheckWestCars [] 8
bTreeNodeSetWest = BTreeNode bTreeFunctionSetWest [] 9
bTreeNodeTryWest = BTreeNode sequenceFunc [bTreeNodeCheckWestCars, bTreeNodeSetWest] 7
bTreeNodeCheckEastCars = BTreeNode bTreeFunctionCheckEastCars [] 11
bTreeNodeSetEast = BTreeNode bTreeFunctionSetEast [] 12
bTreeNodeTryEast = BTreeNode sequenceFunc [bTreeNodeCheckEastCars, bTreeNodeSetEast] 10
bTreeNodeSelectDirection = BTreeNode selectorFunc [bTreeNodeTryWestAndEast, bTreeNodeTryWest, bTreeNodeTryEast] 1
bTreeNodeCheckSafety = BTreeNode bTreeFunctionCheckSafety [] 14
bTreeNodeSendLightSignal = BTreeNode bTreeFunctionSendLightSignal [] 15
bTreeNodeActivateLight = BTreeNode sequenceFunc [bTreeNodeCheckSafety, bTreeNodeSendLightSignal] 13
bTreeNodeLightController = BTreeNode sequenceFunc [bTreeNodeSelectDirection, bTreeNodeActivateLight] 0
