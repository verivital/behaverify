module BTreeUpdateDirection where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionUpdateDirection :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionUpdateDirection _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatus = returnStatusFunction midBlackboard midEnvironment
    (newBlackboard, newEnvironment) = (midBlackboard, midEnvironment)
    newFutureChanges = futureChanges
    (midBlackboard, midEnvironment) = (statement0 (blackboard, environment))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (boardUpdateDir blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | ((boardCurY blackboard) == 10) = (-1)
          | ((boardCurY blackboard) == 0) = 1
          | otherwise = (boardDir blackboard)
    returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus
    returnStatusFunction blackboard environment = returnStatus
      where
        returnStatus = Success