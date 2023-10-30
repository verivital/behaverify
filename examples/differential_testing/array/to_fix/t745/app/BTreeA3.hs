module BTreeA3 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA3 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA3 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement0 (blackboard, environment))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR2 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | False = (min 5 (max 2 (-17)))
          | otherwise = (min 5 (max 2 (if ((if ((-39) == (if (False == True) then 43 else 48)) then ((min 50 (max (-50) ((indexIntoEnvDEFINE7 (max 0 (min 1 (-45))) (envEnvDEFINE7 blackboard environment)) + 13)))) else ((min 50 (max (-50) (min (-1) (-1)))))) <= ((min 50 (max (-50) (- (envEnvVAR2 environment)))))) then (if ((envEnvFROZENVAR4 environment) /= (envEnvFROZENVAR4 environment)) then ((min 50 (max (-50) (- (-2))))) else ((min 50 (max (-50) ( (-31)+ ( (-31)+((-31) + 28))))))) else ((min 50 (max (-50) (max ((min 50 (max (-50) (max 3 3)))) (envEnvVAR2 environment))))))))
    returnStatus
      | False = Running
      | otherwise = Failure
    newFutureChanges = futureChanges
