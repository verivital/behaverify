module BTreeUpdatePreviousDestination where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionUpdatePreviousDestination :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionUpdatePreviousDestination _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement1 (statement0 (blackboard, environment)))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (boardUpdatePrevDestX blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (boardCurX blackboard)
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (boardUpdatePrevDestY blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (boardCurY blackboard)
    returnStatus = Success
    newFutureChanges = futureChanges
