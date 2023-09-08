module ComplexRobot where
import BehaviorTreeCore
import BTreeInHome
import BTreeInMaze
import BTreeInTarget
import BTreeFlagFound
import BTreeNeedSide
import BTreeSuccessNode
import BTreeChangeSide
import BTreeGoForward
import BTreeGoSide
import BTreeNeverNeedSide
import BTreeSearchTile
import BTreeSetZone
import BTreeFlagNotReturned
import BTreeCanMoveForward
import BTreeCanMoveSide
bTreeNodeSetZone = BTreeNode bTreeFunctionSetZone [] 1
bTreeNodeFlagNotReturned = BTreeNode bTreeFunctionFlagNotReturned [] 3
bTreeNodeInMaze = BTreeNode bTreeFunctionInMaze [] 6
bTreeNodeCanMoveForward = BTreeNode bTreeFunctionCanMoveForward [] 10
bTreeNodeGoForward = BTreeNode bTreeFunctionGoForward [] 11
bTreeNodeTryForward = BTreeNode sequenceFunc [bTreeNodeCanMoveForward, bTreeNodeGoForward] 9
bTreeNodeCanMoveSide = BTreeNode bTreeFunctionCanMoveSide [] 14
bTreeNodeGoSide = BTreeNode bTreeFunctionGoSide [] 15
bTreeNodeTrySide = BTreeNode sequenceFunc [bTreeNodeCanMoveSide, bTreeNodeGoSide] 13
bTreeNodeChangeSide = BTreeNode bTreeFunctionChangeSide [] 17
bTreeNodeReturnFailure = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide] 16
bTreeNodeTrySideOrChange = BTreeNode selectorFunc [bTreeNodeTrySide, bTreeNodeReturnFailure] 12
bTreeNodeSuccessNode = BTreeNode bTreeFunctionSuccessNode [] 18
bTreeNodeMoveThroughMaze = BTreeNode selectorFunc [bTreeNodeTryForward, bTreeNodeTrySideOrChange, bTreeNodeSuccessNode] 8
bTreeNodeMoveThroughMazeDecorator = BTreeNode (decoratorCreator (xISyCreator Success Running)) [bTreeNodeMoveThroughMaze] 7
bTreeNodeNavigateMaze = BTreeNode sequenceFunc [bTreeNodeInMaze, bTreeNodeMoveThroughMazeDecorator] 5
bTreeNodeInMaze_1 = BTreeNode bTreeFunctionInMaze [] 21
bTreeNodeMazeInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeInMaze_1] 20
bTreeNodeInTarget = BTreeNode bTreeFunctionInTarget [] 24
bTreeNodeFlagFound = BTreeNode bTreeFunctionFlagFound [] 25
bTreeNodeGoHome = BTreeNode sequenceFunc [bTreeNodeInTarget, bTreeNodeFlagFound] 23
bTreeNodeInHome = BTreeNode bTreeFunctionInHome [] 27
bTreeNodeFlagFound_1 = BTreeNode bTreeFunctionFlagFound [] 29
bTreeNodeFlagInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeFlagFound_1] 28
bTreeNodeGoTarget = BTreeNode sequenceFunc [bTreeNodeInHome, bTreeNodeFlagInverter] 26
bTreeNodeTraversalNeeded = BTreeNode selectorFunc [bTreeNodeGoHome, bTreeNodeGoTarget] 22
bTreeNodeGoForward_1 = BTreeNode bTreeFunctionGoForward [] 30
bTreeNodeEnterMaze = BTreeNode sequenceFunc [bTreeNodeMazeInverter, bTreeNodeTraversalNeeded, bTreeNodeGoForward_1] 19
bTreeNodeInTarget_1 = BTreeNode bTreeFunctionInTarget [] 32
bTreeNodeNeedSide = BTreeNode bTreeFunctionNeedSide [] 33
bTreeNodeCanMoveSide_1 = BTreeNode bTreeFunctionCanMoveSide [] 37
bTreeNodeGoSide_1 = BTreeNode bTreeFunctionGoSide [] 38
bTreeNodeTrySide_1 = BTreeNode sequenceFunc [bTreeNodeCanMoveSide_1, bTreeNodeGoSide_1] 36
bTreeNodeChangeSide_1 = BTreeNode bTreeFunctionChangeSide [] 40
bTreeNodeReturnFailure_1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide_1] 39
bTreeNodeTrySideOrChange_1 = BTreeNode selectorFunc [bTreeNodeTrySide_1, bTreeNodeReturnFailure_1] 35
bTreeNodeSideReached = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeTrySideOrChange_1] 34
bTreeNodeNeverNeedSide = BTreeNode bTreeFunctionNeverNeedSide [] 41
bTreeNodeToSide = BTreeNode sequenceFunc [bTreeNodeInTarget_1, bTreeNodeNeedSide, bTreeNodeSideReached, bTreeNodeNeverNeedSide] 31
bTreeNodeInTarget_2 = BTreeNode bTreeFunctionInTarget [] 43
bTreeNodeFlagFound_2 = BTreeNode bTreeFunctionFlagFound [] 45
bTreeNodeFlagInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeFlagFound_2] 44
bTreeNodeSearchTile = BTreeNode bTreeFunctionSearchTile [] 47
bTreeNodeCanMoveSide_2 = BTreeNode bTreeFunctionCanMoveSide [] 51
bTreeNodeGoSide_2 = BTreeNode bTreeFunctionGoSide [] 52
bTreeNodeTrySide_2 = BTreeNode sequenceFunc [bTreeNodeCanMoveSide_2, bTreeNodeGoSide_2] 50
bTreeNodeChangeSide_2 = BTreeNode bTreeFunctionChangeSide [] 54
bTreeNodeReturnFailure_2 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide_2] 53
bTreeNodeTrySideOrChange_2 = BTreeNode selectorFunc [bTreeNodeTrySide_2, bTreeNodeReturnFailure_2] 49
bTreeNodeGoForward_2 = BTreeNode bTreeFunctionGoForward [] 55
bTreeNodeMoveForFlag = BTreeNode selectorFunc [bTreeNodeTrySideOrChange_2, bTreeNodeGoForward_2] 48
bTreeNodeSearchForFlag = BTreeNode selectorFunc [bTreeNodeSearchTile, bTreeNodeMoveForFlag] 46
bTreeNodeSearchTarget = BTreeNode sequenceFunc [bTreeNodeInTarget_2, bTreeNodeFlagInverter_1, bTreeNodeSearchForFlag] 42
bTreeNodeControlSelector = BTreeNode selectorFunc [bTreeNodeNavigateMaze, bTreeNodeEnterMaze, bTreeNodeToSide, bTreeNodeSearchTarget] 4
bTreeNodeControlSequence = BTreeNode sequenceFunc [bTreeNodeFlagNotReturned, bTreeNodeControlSelector] 2
bTreeNodeControl = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeSetZone, bTreeNodeControlSequence] 0
