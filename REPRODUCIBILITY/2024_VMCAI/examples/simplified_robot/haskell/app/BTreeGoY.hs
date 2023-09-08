module BTreeGoY where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorGoY :: Integer -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorGoY y_dir = bTreeFunctionGoY
  where
    bTreeFunctionGoY :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionGoY _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
      where
        returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
        returnStatement boardEnv = Success
          where
            (blackboard, environment) = boardEnv
        futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        futureChanges0 boardEnv = (blackboard, updateEnvYTrue environment (max 0 (min 7 ((envYTrue environment) + y_dir))))
          where
            (blackboard, environment) = boardEnv
        preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
        returnStatus = returnStatement preStatusBoardEnv
        (newBlackboard, newEnvironment) =  preStatusBoardEnv
        newFutureChanges = futureChanges0 : futureChanges
