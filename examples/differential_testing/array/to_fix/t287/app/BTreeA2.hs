module BTreeA2 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA2 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA2 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement0 (blackboard, environment))
    returnStatus
      | (((min 50 (max (-50) (max 34 5)))) > ((min 50 (max (-50) (max 3 3))))) = Success
      | (boardBlVAR0 blackboard) = Running
      | (33 < ((min 50 (max (-50) ((-40) + (-40)))))) = Success
      | otherwise = Running
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (((min 50 (max (-50) ( (boardBlDEFINE5 blackboard)+((-24) + (-24)))))) <= (-18)) = (min (-2) (max (-5) ((sereneCOUNT ((envEnvDEFINE7 blackboard environment) || (boardBlVAR0 blackboard)) ((envEnvVAR4 environment) <= (-17))) + (sereneCOUNT ((boardBlVAR0 blackboard) == (boardBlVAR0 blackboard)) ((envEnvDEFINE7 blackboard environment) && True)))))
          | (((sereneCOUNT ((if (True == (boardBlVAR0 blackboard)) then 10 else (-18)) <= ((min 50 (max (-50) ( (boardBlDEFINE8 blackboard)* ( (boardBlDEFINE8 blackboard)*(2 * 2))))))) (sereneIMPLIES (False == (boardBlVAR0 blackboard)) (boardBlVAR0 blackboard))) + (if (26 == (boardBlDEFINE5 blackboard)) then 1 else 0)) <= (boardBlDEFINE5 blackboard)) = (min (-2) (max (-5) ((min 50 (max (-50) (- ((min 50 (max (-50) (abs (-36)))))))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( (if ((boardBlDEFINE5 blackboard) < (boardBlDEFINE5 blackboard)) then (-39) else 15)+(((min 50 (max (-50) ( (indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard))*((indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard)) * (indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard))))))) + ((min 50 (max (-50) ( (indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard))*((indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard)) * (indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard))))))))))))))
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 = statement0
      where
        statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
          where
            randomPair0 = (-1, envGenerator environment)
            newGenerator = snd randomPair0
            newVal
              | (sereneXNOR (boardBlVAR0 blackboard) ((if ((boardBlVAR0 blackboard) && True) then (envEnvVAR4 environment) else (envEnvVAR1 environment)) > 16)) = (min (-2) (max (-5) (-10)))
              | (((min 50 (max (-50) (max (boardBlDEFINE5 blackboard) (boardBlDEFINE5 blackboard))))) >= (if ((boardBlVAR0 blackboard) /= False) then 8 else (envEnvVAR1 environment))) = (min (-2) (max (-5) 15))
              | otherwise = (min (-2) (max (-5) ((sereneCOUNT (sereneXNOR False (boardBlVAR0 blackboard)) ((indexIntoBlDEFINE6 (max 0 (min 2 (-48))) (boardBlDEFINE6 blackboard)) == (envEnvVAR4 environment))) + (if ((boardBlVAR0 blackboard) || True) then 1 else 0))))
    futureChanges1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges1 = statement0
      where
        statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR4 environment newGenerator newVal)
          where
            randomPair0 = (-1, envGenerator environment)
            newGenerator = snd randomPair0
            newVal = (min 5 (max 2 ((sereneCOUNT (((boardBlDEFINE8 blackboard) <= (indexIntoLocalVAR2 (max 0 (min 2 (envEnvVAR1 environment))) (boardLocalVAR2 nodeLocation blackboard))) && True) (((envEnvVAR4 environment) >= (boardBlDEFINE5 blackboard)) == False)) + (if (((-7) > (envEnvVAR4 environment)) == (31 >= (-40))) then 1 else 0))))
    newFutureChanges = futureChanges1 : futureChanges0 : futureChanges
