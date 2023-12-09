module BTreeUpdateDestination where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionUpdateDestination :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionUpdateDestination _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
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
        newVal
          | (boardXMode blackboard) = (if ((boardDestX blackboard) == 10) then 0 else 10)
          | otherwise = (boardDestX blackboard)
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (boardUpdateDestY blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | (not (boardXMode blackboard)) = (min 10 (max 0 ((boardDestY blackboard) + ((boardYDir blackboard) * 2))))
          | otherwise = (boardDestY blackboard)
    returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus
    returnStatusFunction blackboard environment = returnStatus
      where
        returnStatus = Success
