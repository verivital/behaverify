module BTreeGetPosition where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



getPosition :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
getPosition _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1 = (updateBoardX blackboard (envXTrue environment), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2 = (updateBoardY blackboard (envYTrue environment), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
