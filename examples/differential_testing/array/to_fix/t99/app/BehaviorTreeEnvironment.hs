module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
    envGenerator :: StdGen
  , envEnvVAR1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "env = {" ++ "envEnvVAR1: " ++ (show (envEnvVAR1 environment)) ++ ", " ++ "envEnvDEFINE4: " ++ (show (envEnvDEFINE4 blackboard environment)) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE4 :: BTreeBlackboard -> BTreeEnvironment -> (Integer, Integer)
envEnvDEFINE4 blackboard environment = newVal
  where
    newUpdate0
      | (boardBlVAR0 blackboard) = (min 5 (max 2 ((min 50 (max (-50) (min (envEnvVAR1 environment) (envEnvVAR1 environment)))))))
      | (((min 50 (max (-50) ( (envEnvVAR1 environment)+((envEnvVAR1 environment) + 13))))) <= (-22)) = (min 5 (max 2 (-4)))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) (min ((min 50 (max (-50) (((min 50 (max (-50) (max (-32) (-32))))) - (envEnvVAR1 environment))))) ((min 50 (max (-50) (((min 50 (max (-50) (max (-32) (-32))))) - (envEnvVAR1 environment)))))))))))
    defaultValue0
      | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (min 5 (max 2 (envEnvVAR1 environment)))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) ( (-33)*((-33) * (envEnvVAR1 environment))))))))
    defaultValue1
      | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (min 5 (max 2 (envEnvVAR1 environment)))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) ( (-33)*((-33) * (envEnvVAR1 environment))))))))
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayEnvDEFINE4 defaultValue [(0, newUpdate0), (1, newUpdate0)]

-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoEnvDEFINE4 :: Integer -> (Integer, Integer) -> Integer
indexIntoEnvDEFINE4 0 (value, _) = value
indexIntoEnvDEFINE4 1 (_, value) = value
indexIntoEnvDEFINE4 _ _ = error "indexIntoEnvDEFINE4 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayEnvDEFINE4 :: (Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer)
newArrayEnvDEFINE4 values  []  = values
newArrayEnvDEFINE4 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF UPDATES

envUpdate :: BTreeEnvironment -> StdGen -> BTreeEnvironment
envUpdate environment newGen = environment { envGenerator = newGen }
envUpdateEnvVAR1 :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateEnvVAR1 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR1 = newVal }

-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

-- START OF FUTURE CHANGES

applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)

-- START OF BETWEEN TICK CHANGES

betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, environment) = (newBlackboard, newEnvironment)
  where
    (newBlackboard, newEnvironment) = (blackboard, environment)

-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = newEnvironment
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeEnvironment firstGen 0
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (sereneXNOR ((boardBlVAR0 blackboard) /= True) (True == False)) = (min (-2) (max (-5) 3))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) ( ((min 50 (max (-50) ( (-5)* ( (-5)*((-34) * 4))))))*(35 * 50))))) - (if (32 < 3) then (-2) else 2)))))))
    (_, newEnvironment) = (statement0 (blackboard, dummy))

