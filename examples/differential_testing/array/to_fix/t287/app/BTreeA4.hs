module BTreeA4 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA4 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA4 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement1 (statement0 (blackboard, environment)))
    returnStatus
      | (sereneIMPLIES False True) = Running
      | (((min 50 (max (-50) (abs 11)))) == ((min 50 (max (-50) ( (-47)+ ( (-10)+((-45) + (boardBlDEFINE8 blackboard)))))))) = Success
      | otherwise = Success
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | ((-49) < (-20)) = (min (-2) (max (-5) (indexIntoBlDEFINE6 (max 0 (min 2 (-20))) (boardBlDEFINE6 blackboard))))
          | (sereneIMPLIES (False == (boardBlVAR0 blackboard)) (sereneXOR ((boardBlVAR0 blackboard) == (envEnvDEFINE7 blackboard environment)) (boardBlVAR0 blackboard))) = (min (-2) (max (-5) ((min 50 (max (-50) (max (-28) (boardBlDEFINE8 blackboard)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (- (envEnvVAR1 environment)))))))
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR4 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (23 >= ((min 50 (max (-50) (- 14))))) = (min 5 (max 2 ((min 50 (max (-50) (((min 50 (max (-50) ((-43) - (-31))))) - ((min 50 (max (-50) ((-43) - (-31)))))))))))
          | (((min 50 (max (-50) (max (boardBlDEFINE8 blackboard) (-10))))) >= (indexIntoLocalVAR2 (max 0 (min 2 (-2))) (boardLocalVAR2 nodeLocation blackboard))) = (min 5 (max 2 (-41)))
          | otherwise = (min 5 (max 2 (-36)))
    newFutureChanges = futureChanges
