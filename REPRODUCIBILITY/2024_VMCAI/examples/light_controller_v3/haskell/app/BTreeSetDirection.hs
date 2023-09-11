module BTreeSetDirection where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorSetDirection :: String -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorSetDirection new_direction = bTreeFunctionSetDirection
  where
    bTreeFunctionSetDirection :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionSetDirection _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
      where
        boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        boardEnvUpdate0 boardEnv = (updateBoardDirection blackboard new_direction, environment)
          where
            (blackboard, environment) = boardEnv
        boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        boardEnvUpdate1 boardEnv = (updateBoardFairnessCounter blackboard 0, environment)
          where
            (blackboard, environment) = boardEnv
        returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
        returnStatement boardEnv = Success
          where
            (blackboard, environment) = boardEnv
        preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
        returnStatus = returnStatement preStatusBoardEnv
        (newBlackboard, newEnvironment) =  preStatusBoardEnv
        newFutureChanges = futureChanges
