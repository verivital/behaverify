module BTreeA1 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA1 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA1 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement0 (blackboard, environment))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (preBlackboard, environment) = (newBlackboard, newEnvironment)
      where
        (newBlackboard, newEnvironment) = if condition then (statement3 (statement2 (statement1 (blackboard, environment)))) else (blackboard, environment)
        condPair = (-1, boardGenerator preBlackboard)
        condition = (envEnvDEFINE7 blackboard environment)
        blackboard = boardUpdate preBlackboard (snd condPair)
        statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement1 (blackboard, environment)  = (boardUpdateBlVAR0 blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newGenerator = snd randomPair0
            newVal
              | (11 < 8) = (((min 50 (max (-50) (max (-23) 16)))) > (boardBlDEFINE8 blackboard))
              | (((min 50 (max (-50) (max 20 (boardBlDEFINE5 blackboard))))) /= ((min 50 (max (-50) (max (envEnvVAR1 environment) (envEnvVAR1 environment)))))) = (37 < (indexIntoBlDEFINE6 (max 0 (min 2 (-39))) (boardBlDEFINE6 blackboard)))
              | otherwise = ((-2) /= (envEnvVAR1 environment))
        statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement2 (blackboard, environment)  = (boardUpdateBlVAR0 blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newGenerator = snd randomPair0
            newVal
              | (((boardBlDEFINE8 blackboard) == (-16)) == (((indexIntoBlDEFINE6 (max 0 (min 2 (boardBlDEFINE5 blackboard))) (boardBlDEFINE6 blackboard)) >= 3) && ((boardBlVAR0 blackboard) == (envEnvDEFINE7 blackboard environment)))) = ((boardBlDEFINE5 blackboard) <= ((min 50 (max (-50) (min (boardBlDEFINE8 blackboard) (boardBlDEFINE8 blackboard))))))
              | ((envEnvVAR1 environment) > (-21)) = True
              | otherwise = (envEnvDEFINE7 blackboard environment)
        statement3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement3 (blackboard, environment)  = (boardUpdateBlVAR0 blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newGenerator = snd randomPair0
            newVal
              | (20 < (-34)) = (sereneXNOR False (sereneXNOR False False))
              | ((envEnvDEFINE7 blackboard environment) && (boardBlVAR0 blackboard)) = (((min 50 (max (-50) ( (-17)+((-17) + (-17)))))) /= (-1))
              | otherwise = ((envEnvVAR1 environment) >= (boardBlDEFINE5 blackboard))
    returnStatus
      | (((min 50 (max (-50) ((boardBlDEFINE8 blackboard) - (boardBlDEFINE8 blackboard))))) >= ((min 50 (max (-50) ( (boardBlDEFINE5 blackboard)+((boardBlDEFINE5 blackboard) + (boardBlDEFINE5 blackboard))))))) = Running
      | (((min 50 (max (-50) (abs (boardBlDEFINE5 blackboard))))) >= (boardBlDEFINE5 blackboard)) = Running
      | otherwise = Failure
    newFutureChanges = futureChanges
