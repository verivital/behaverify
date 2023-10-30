module BTreeA1 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA1 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA1 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement2 (statement1 (statement0 (blackboard, environment))))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (indexIntoBlVAR3 (max 0 (min 1 (envEnvVAR1 environment))) (boardBlVAR3 blackboard)) = (min (-2) (max (-5) ((min 50 (max (-50) (((sereneCOUNT ("no" /= "no") ((sereneIMPLIES True False) /= False)) + (sereneCOUNT (True || False) (sereneIMPLIES True False))) - ((sereneCOUNT ("no" /= "no") ((sereneIMPLIES True False) /= False)) + (sereneCOUNT (True || False) (sereneIMPLIES True False)))))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (max 4 4)))) - ((min 50 (max (-50) (max 4 4))))))))))
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal = (min (-2) (max (-5) ((min 50 (max (-50) ((indexIntoEnvDEFINE4 (max 0 (min 1 (envEnvVAR1 environment))) (envEnvDEFINE4 blackboard environment)) - (envEnvVAR1 environment)))))))
    returnStatus
      | (sereneXOR False (5 > (-9))) = Failure
      | otherwise = Failure
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (boardUpdateBlVAR2 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | ((-5) < 2) = (boardBlDEFINE5 blackboard)
          | (((min 50 (max (-50) ((-4) - 28)))) <= 4) = (boardBlDEFINE5 blackboard)
          | otherwise = (boardBlDEFINE5 blackboard)
        defaultValue = (boardBlVAR2 blackboard)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR2 defaultValue [(0, newUpdate0), (1, newUpdate0)]
    newFutureChanges = futureChanges
