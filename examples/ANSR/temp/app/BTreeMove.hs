module BTreeMove where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorMove :: Integer -> Integer -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorMove delta_x delta_y = bTreeFunctionMove
  where
    bTreeFunctionMove :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionMove _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
      where
        returnStatus = returnStatusFunction midBlackboard midEnvironment
        (newBlackboard, newEnvironment) = (midBlackboard, midEnvironment)
        newFutureChanges = futureChanges
        (midBlackboard, midEnvironment) = (statement1 (statement0 (blackboard, environment)))
        statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement0 (blackboard, environment)  = (boardUpdateCurX blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newGenerator = snd randomPair0
            newVal = (max 0 (min 10 (delta_x + (boardCurX blackboard))))
        statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement1 (blackboard, environment)  = (boardUpdateCurY blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newGenerator = snd randomPair0
            newVal = (max 0 (min 10 (delta_y + (boardCurY blackboard))))
        returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus
        returnStatusFunction blackboard environment = returnStatus
          where
            returnStatus = Success
