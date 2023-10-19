module BTreeGoX where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorGoX :: Integer -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorGoX x_dir = bTreeFunctionGoX
  where
    bTreeFunctionGoX :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionGoX _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
      where
        returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
        returnStatement boardEnv = Success
          where
            (blackboard, environment) = boardEnv
        futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        futureChanges0 boardEnv = (blackboard, updateEnvXTrue environment (max 0 (min 7 ((envXTrue environment) + x_dir))))
          where
            (blackboard, environment) = boardEnv
        preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
        returnStatus = returnStatement preStatusBoardEnv
        (newBlackboard, newEnvironment) =  preStatusBoardEnv
        newFutureChanges = futureChanges0 : futureChanges
