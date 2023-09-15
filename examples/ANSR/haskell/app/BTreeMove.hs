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
    bTreeFunctionMove _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
      where
        boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        boardEnvUpdate0 boardEnv = (updateBoardCurX blackboard (max 0 (min 6 (delta_x + (boardCurX blackboard)))), environment)
          where
            (blackboard, environment) = boardEnv
        boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        boardEnvUpdate1 boardEnv = (updateBoardCurY blackboard (max 0 (min 6 (delta_y + (boardCurY blackboard)))), environment)
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
