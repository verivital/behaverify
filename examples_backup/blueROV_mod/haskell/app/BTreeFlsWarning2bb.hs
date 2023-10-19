module BTreeFlsWarning2bb where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionFlsWarning2bb :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionFlsWarning2bb _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | conditionRandomInteger == 0 = privateTempBoardEnv0
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        (conditionRandomInteger, conditionRandomGenerator) = getRandomInteger (sereneEnvGenerator (snd boardEnv)) 1
        privateTempBoardEnv0 = (fst boardEnv, updateEnvGenerator (snd boardEnv) conditionRandomGenerator)
        privateTempBoardEnv1 = (updateLocalBoardReadSuccess nodeLocation (fst privateTempBoardEnv0) True, snd privateTempBoardEnv0)
        privateBoardEnv = privateTempBoardEnv3
        privateTempBoardEnv2 = (updateBoardBbFlsWarning blackboard ((boardBbFlsWarning blackboard) || (envObstacleInView environment)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
        privateTempBoardEnv3 = (updateBoardEmergencyStopWarning blackboard ((boardEmergencyStopWarning blackboard) || (envObstacleInView environment)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv2
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (localBoardReadSuccess nodeLocation blackboard) = Success
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
