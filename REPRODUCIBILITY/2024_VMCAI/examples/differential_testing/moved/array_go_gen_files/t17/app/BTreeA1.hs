module BTreeA1 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA1 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA1 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 (boardBlDEFINE5 blackboard))), updateValue0)
        updatePair1 = ((min 2 (max 0 (max (boardBlDEFINE5 blackboard) (0 + 5)))), updateValue1)
        updateValue0 = (min (-2) (max (-5) (boardBlDEFINE5 blackboard)))
          where
            (blackboard, environment) = boardEnv
        updateValue1 = (min (-2) (max (-5) (max ((boardBlVAR0 1 blackboard) + ((boardBlDEFINE5 blackboard) + ((boardBlVAR0 1 blackboard) + (boardBlDEFINE5 blackboard)))) (boardBlVAR0 1 blackboard))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | not ((sereneIMPLIES (sereneXNOR (sereneIMPLIES False (envEnvDEFINE6 conditionBlackboard conditionEnvironment)) ((envEnvDEFINE6 conditionBlackboard conditionEnvironment) || (envEnvVAR4 conditionEnvironment))) ((-26) > (-97)))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((min 2 (max 0 (sereneCOUNT ((boardBlVAR0 2 blackboard) < (min (-22) (boardBlVAR0 1 blackboard))) ((boardBlDEFINE5 blackboard) <= (boardBlDEFINE5 blackboard))))), updateValue0)
            updateValue0 = (min (-2) (max (-5) 19))
              where
                (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Failure
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
