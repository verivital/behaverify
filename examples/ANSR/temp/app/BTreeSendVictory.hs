module BTreeSendVictory where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionSendVictory :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionSendVictory _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatus = returnStatusFunction midBlackboard midEnvironment
    (newBlackboard, newEnvironment) = (midBlackboard, midEnvironment)
    newFutureChanges = futureChanges
    (midBlackboard, midEnvironment) = (statement0 (blackboard, environment))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (boardUpdateVictory blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = True
    returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus
    returnStatusFunction blackboard environment = returnStatus
      where
        returnStatus = Success
