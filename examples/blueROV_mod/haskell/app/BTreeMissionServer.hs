module BTreeMissionServer where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionMissionServer :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionMissionServer _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | ((boardNextMission blackboard) && (boardFinishedMissions blackboard)) = (updateBoardGenerator (updateBoardFinishedMissions blackboard (privateRandom1 (fst (getRandomInteger (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInteger (sereneBoardGenerator blackboard) 1)), environment)
          | otherwise = (updateBoardFinishedMissions blackboard (boardFinishedMissions blackboard), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            privateRandom1 :: Integer -> Bool
            privateRandom1 0 = True
            privateRandom1 _ = False
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | (boardNextMission blackboard) = (updateBoardBbRthWarning blackboard (boardFinishedMissions blackboard), environment)
      | otherwise = (updateBoardBbRthWarning blackboard (boardBbRthWarning blackboard), environment)
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | ((boardNextMission blackboard) && (not (boardFinishedMissions blackboard))) = (updateBoardGenerator (updateBoardBbMission blackboard (privateRandom1 (fst (getRandomInteger (sereneBoardGenerator blackboard) 2)))) (snd (getRandomInteger (sereneBoardGenerator blackboard) 2)), environment)
          | otherwise = (updateBoardBbMission blackboard (boardBbMission blackboard), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            privateRandom1 :: Integer -> String
            privateRandom1 0 = "waypoint_following"
            privateRandom1 1 = "e_stop"
            privateRandom1 _ = "pipe_following"
    boardEnvUpdate3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate3 boardEnv
      | (((boardNextMission blackboard) && (not (boardFinishedMissions blackboard))) && ("e_stop" == (boardBbMission blackboard))) = (updateBoardEmergencyStopWarning blackboard True, environment)
      | otherwise = (updateBoardEmergencyStopWarning blackboard (boardEmergencyStopWarning blackboard), environment)
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate4 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate4 boardEnv = (updateBoardNextMission blackboard False, environment)
      where
        (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Running
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate4 . boardEnvUpdate3 . boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
