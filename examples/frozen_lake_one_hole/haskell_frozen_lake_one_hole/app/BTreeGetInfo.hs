module BTreeGetInfo where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



getInfo :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
getInfo _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardTiles blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((envLoc environment), updateValue0)
            updateValue0
              | ((envLoc environment) == (envGoalLoc environment)) = "goal"
              | ((envLoc environment) == (envHoleLoc environment)) = "hole"
              | otherwise = "safe"
              where
                (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
