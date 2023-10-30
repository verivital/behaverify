module BTreeA4 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA4 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA4 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (blackboard, environment)
    returnStatus
      | ((True || True) == ((-39) /= (-6))) = Running
      | (True || False) = Success
      | otherwise = Failure
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 = statement0
      where
        statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR2 environment newGenerator newVal)
          where
            randomPair0 = (-1, envGenerator environment)
            newGenerator = snd randomPair0
            newVal
              | (((min 50 (max (-50) (- 21)))) <= ((min 50 (max (-50) ( (envEnvVAR2 environment)* ( (envEnvVAR2 environment)*((envEnvVAR2 environment) * (envEnvVAR2 environment)))))))) = (min 5 (max 2 ((min 50 (max (-50) ( 38+(38 + ((min 50 (max (-50) (max (-41) 5)))))))))))
              | (((min 50 (max (-50) (- (-49))))) > ((min 50 (max (-50) (abs (envEnvVAR3 environment)))))) = (min 5 (max 2 (envEnvVAR2 environment)))
              | otherwise = (min 5 (max 2 (envEnvVAR3 environment)))
    newFutureChanges = futureChanges0 : futureChanges
