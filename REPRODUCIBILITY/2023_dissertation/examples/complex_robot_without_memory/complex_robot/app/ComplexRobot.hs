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
bTreeNodeSetZone = BTreeNode setZone [] 1
bTreeNodeFlagNotReturned = BTreeNode flagNotReturned [] 3
bTreeNodeInMaze = BTreeNode inMaze [] 6
bTreeNodeCanMoveForward = BTreeNode canMoveForward [] 10
bTreeNodeGoForward = BTreeNode goForward [] 11
bTreeNodeTryForward = BTreeNode sequenceFunc [bTreeNodeCanMoveForward, bTreeNodeGoForward] 9
bTreeNodeCanMoveSide = BTreeNode canMoveSide [] 14
bTreeNodeGoSide = BTreeNode goSide [] 15
bTreeNodeTrySide = BTreeNode sequenceFunc [bTreeNodeCanMoveSide, bTreeNodeGoSide] 13
bTreeNodeChangeSide = BTreeNode changeSide [] 17
bTreeNodeReturnFailure = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide] 16
bTreeNodeTrySideOrChange = BTreeNode selectorFunc [bTreeNodeTrySide, bTreeNodeReturnFailure] 12
bTreeNodeSuccessNode = BTreeNode successNode [] 18
bTreeNodeMoveThroughMaze = BTreeNode selectorFunc [bTreeNodeTryForward, bTreeNodeTrySideOrChange, bTreeNodeSuccessNode] 8
bTreeNodeMoveThroughMazeDecorator = BTreeNode (decoratorCreator (xISyCreator Success Running)) [bTreeNodeMoveThroughMaze] 7
bTreeNodeNavigateMaze = BTreeNode sequenceFunc [bTreeNodeInMaze, bTreeNodeMoveThroughMazeDecorator] 5
bTreeNodeInMaze_1 = BTreeNode inMaze [] 21
bTreeNodeMazeInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeInMaze_1] 20
bTreeNodeInTarget = BTreeNode inTarget [] 24
bTreeNodeFlagFound = BTreeNode flagFound [] 25
bTreeNodeGoHome = BTreeNode sequenceFunc [bTreeNodeInTarget, bTreeNodeFlagFound] 23
bTreeNodeInHome = BTreeNode inHome [] 27
bTreeNodeFlagFound_1 = BTreeNode flagFound [] 29
bTreeNodeFlagInverter = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeFlagFound_1] 28
bTreeNodeGoTarget = BTreeNode sequenceFunc [bTreeNodeInHome, bTreeNodeFlagInverter] 26
bTreeNodeTraversalNeeded = BTreeNode selectorFunc [bTreeNodeGoHome, bTreeNodeGoTarget] 22
bTreeNodeGoForward_1 = BTreeNode goForward [] 30
bTreeNodeEnterMaze = BTreeNode sequenceFunc [bTreeNodeMazeInverter, bTreeNodeTraversalNeeded, bTreeNodeGoForward_1] 19
bTreeNodeInTarget_1 = BTreeNode inTarget [] 32
bTreeNodeNeedSide = BTreeNode needSide [] 33
bTreeNodeCanMoveSide_1 = BTreeNode canMoveSide [] 37
bTreeNodeGoSide_1 = BTreeNode goSide [] 38
bTreeNodeTrySide_1 = BTreeNode sequenceFunc [bTreeNodeCanMoveSide_1, bTreeNodeGoSide_1] 36
bTreeNodeChangeSide_1 = BTreeNode changeSide [] 40
bTreeNodeReturnFailure_1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide_1] 39
bTreeNodeTrySideOrChange_1 = BTreeNode selectorFunc [bTreeNodeTrySide_1, bTreeNodeReturnFailure_1] 35
bTreeNodeSideReached = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeTrySideOrChange_1] 34
bTreeNodeNeverNeedSide = BTreeNode neverNeedSide [] 41
bTreeNodeToSide = BTreeNode sequenceFunc [bTreeNodeInTarget_1, bTreeNodeNeedSide, bTreeNodeSideReached, bTreeNodeNeverNeedSide] 31
bTreeNodeInTarget_2 = BTreeNode inTarget [] 43
bTreeNodeFlagFound_2 = BTreeNode flagFound [] 45
bTreeNodeFlagInverter_1 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeFlagFound_2] 44
bTreeNodeSearchTile = BTreeNode searchTile [] 47
bTreeNodeCanMoveSide_2 = BTreeNode canMoveSide [] 51
bTreeNodeGoSide_2 = BTreeNode goSide [] 52
bTreeNodeTrySide_2 = BTreeNode sequenceFunc [bTreeNodeCanMoveSide_2, bTreeNodeGoSide_2] 50
bTreeNodeChangeSide_2 = BTreeNode changeSide [] 54
bTreeNodeReturnFailure_2 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeChangeSide_2] 53
bTreeNodeTrySideOrChange_2 = BTreeNode selectorFunc [bTreeNodeTrySide_2, bTreeNodeReturnFailure_2] 49
bTreeNodeGoForward_2 = BTreeNode goForward [] 55
bTreeNodeMoveForFlag = BTreeNode selectorFunc [bTreeNodeTrySideOrChange_2, bTreeNodeGoForward_2] 48
bTreeNodeSearchForFlag = BTreeNode selectorFunc [bTreeNodeSearchTile, bTreeNodeMoveForFlag] 46
bTreeNodeSearchTarget = BTreeNode sequenceFunc [bTreeNodeInTarget_2, bTreeNodeFlagInverter_1, bTreeNodeSearchForFlag] 42
bTreeNodeControlSelector = BTreeNode selectorFunc [bTreeNodeNavigateMaze, bTreeNodeEnterMaze, bTreeNodeToSide, bTreeNodeSearchTarget] 4
bTreeNodeControlSequence = BTreeNode sequenceFunc [bTreeNodeFlagNotReturned, bTreeNodeControlSelector] 2
bTreeNodeControl = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeSetZone, bTreeNodeControlSequence] 0
