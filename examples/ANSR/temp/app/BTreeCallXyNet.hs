module BTreeCallXyNet where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCallXyNet :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionCallXyNet _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatus = returnStatusFunction midBlackboard midEnvironment
    (newBlackboard, newEnvironment) = (midBlackboard, midEnvironment)
    newFutureChanges = futureChanges
    (midBlackboard, midEnvironment) = (statement1 (statement0 (blackboard, environment)))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (boardUpdateDestX blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (max 0 (min 10 (boardXNetOutput blackboard)))
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (boardUpdateDestY blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (max 0 (min 10 (boardYNetOutput blackboard)))
    returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus
    returnStatusFunction blackboard environment = returnStatus
      where
        returnStatus = Success
