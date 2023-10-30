module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
    envGenerator :: StdGen
  , envEnvVAR1 :: (String, String, String)
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "env = {" ++ "envEnvVAR1: " ++ (show (envEnvVAR1 environment)) ++ ", " ++ "envEnvDEFINE6: " ++ (show (envEnvDEFINE6 blackboard environment)) ++ ", " ++ "envEnvDEFINE8: " ++ (show (envEnvDEFINE8 blackboard environment)) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE6 :: BTreeBlackboard -> BTreeEnvironment -> String
envEnvDEFINE6 blackboard environment = newVal
  where
    newVal = (indexIntoEnvVAR1 (max 0 (min 2 (boardBlVAR3 blackboard))) (envEnvVAR1 environment))
envEnvDEFINE8 :: BTreeBlackboard -> BTreeEnvironment -> (String, String, String)
envEnvDEFINE8 blackboard environment = newVal
  where
    newUpdate0
      | ((False || True) == ((indexIntoBlDEFINE5 (max 0 (min 1 (-17))) (boardBlDEFINE5 blackboard)) >= ((min 50 (max (-50) (min (boardBlVAR3 blackboard) (boardBlVAR3 blackboard))))))) = "yes"
      | otherwise = "no"
    newUpdate1
      | ((False || True) == ((indexIntoBlDEFINE5 (max 0 (min 1 (-17))) (boardBlDEFINE5 blackboard)) >= ((min 50 (max (-50) (min (boardBlVAR3 blackboard) (boardBlVAR3 blackboard))))))) = "yes"
      | otherwise = "no"
    newUpdate2
      | ((False || True) == ((indexIntoBlDEFINE5 (max 0 (min 1 (-17))) (boardBlDEFINE5 blackboard)) >= ((min 50 (max (-50) (min (boardBlVAR3 blackboard) (boardBlVAR3 blackboard))))))) = "yes"
      | otherwise = "no"
    newUpdate3
      | ((False || True) == ((indexIntoBlDEFINE5 (max 0 (min 1 (-17))) (boardBlDEFINE5 blackboard)) >= ((min 50 (max (-50) (min (boardBlVAR3 blackboard) (boardBlVAR3 blackboard))))))) = "yes"
      | otherwise = "no"
    defaultValue0 = (indexIntoEnvVAR1 (max 0 (min 2 (-16))) (envEnvVAR1 environment))
    defaultValue1 = (indexIntoEnvVAR1 (max 0 (min 2 (-16))) (envEnvVAR1 environment))
    defaultValue2 = (indexIntoEnvVAR1 (max 0 (min 2 (-16))) (envEnvVAR1 environment))
    defaultValue = (defaultValue0, defaultValue1, defaultValue2)
    newVal = newArrayEnvDEFINE8 defaultValue [((max 0 (min 2 ((sereneCOUNT ((-3) <= ((min 50 (max (-50) ( (boardBlDEFINE7 blackboard)+(50 + (-5))))))) (sereneXNOR True False))))), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) (- (boardBlVAR3 blackboard))))))), newUpdate0), ((max 0 (min 2 ((sereneCOUNT ((-3) <= ((min 50 (max (-50) ( (boardBlDEFINE7 blackboard)+(50 + (-5))))))) (sereneXNOR True False))))), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) (- (boardBlVAR3 blackboard))))))), newUpdate1), ((max 0 (min 2 ((sereneCOUNT ((-3) <= ((min 50 (max (-50) ( (boardBlDEFINE7 blackboard)+(50 + (-5))))))) (sereneXNOR True False))))), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) (- (boardBlVAR3 blackboard))))))), newUpdate2), ((max 0 (min 2 ((sereneCOUNT ((-3) <= ((min 50 (max (-50) ( (boardBlDEFINE7 blackboard)+(50 + (-5))))))) (sereneXNOR True False))))), newUpdate3), ((max 0 (min 2 ((min 50 (max (-50) (- (boardBlVAR3 blackboard))))))), newUpdate3)]

-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoEnvVAR1 :: Integer -> (String, String, String) -> String
indexIntoEnvVAR1 0 (value, _, _) = value
indexIntoEnvVAR1 1 (_, value, _) = value
indexIntoEnvVAR1 2 (_, _, value) = value
indexIntoEnvVAR1 _ _ = error "indexIntoEnvVAR1 illegal index value"
indexIntoEnvDEFINE8 :: Integer -> (String, String, String) -> String
indexIntoEnvDEFINE8 0 (value, _, _) = value
indexIntoEnvDEFINE8 1 (_, value, _) = value
indexIntoEnvDEFINE8 2 (_, _, value) = value
indexIntoEnvDEFINE8 _ _ = error "indexIntoEnvDEFINE8 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayEnvVAR1 :: (String, String, String) -> [(Integer, String)] -> (String, String, String)
newArrayEnvVAR1 values  []  = values
newArrayEnvVAR1 (value0, value1, value2) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (value0, value1, value2)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues
newArrayEnvDEFINE8 :: (String, String, String) -> [(Integer, String)] -> (String, String, String)
newArrayEnvDEFINE8 values  []  = values
newArrayEnvDEFINE8 (value0, value1, value2) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (value0, value1, value2)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

-- START OF UPDATES

envUpdate :: BTreeEnvironment -> StdGen -> BTreeEnvironment
envUpdate environment newGen = environment { envGenerator = newGen }
envUpdateEnvVAR1 :: BTreeEnvironment -> StdGen -> (String, String, String) -> BTreeEnvironment
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
    (newBlackboard, newEnvironment) = (statement2 (statement1 (statement0 (blackboard, environment))))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate1
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate2
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate3
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate4
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate5
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate6
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate7
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate8
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate9
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate10
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate11
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate12
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate13
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate14
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate15
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate16
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate17
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate18
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate19
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate20
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate21
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate22
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate23
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate24
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate25
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate26
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate27
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate28
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate29
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate30
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate31
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate32
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate33
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate34
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        newUpdate35
          | (((-9) < (-22)) || True) = (indexIntoEnvDEFINE8 (max 0 (min 2 (-20))) (envEnvDEFINE8 blackboard environment))
          | ((envEnvDEFINE6 blackboard environment) /= "both") = "yes"
          | otherwise = "both"
        defaultValue = (envEnvVAR1 environment)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate3), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate3), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate4), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate4), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate5), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate5), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate6), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate6), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate7), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate7), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate8), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate8), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate9), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate9), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate10), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate10), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate11), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate11), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate12), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate12), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate13), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate13), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate14), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate14), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate15), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate15), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate16), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate16), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate17), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate17), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate18), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate18), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate19), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate19), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate20), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate20), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate21), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate21), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate22), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate22), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate23), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate23), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate24), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate24), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate25), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate25), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate26), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate26), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate27), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate27), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate28), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate28), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate29), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate29), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate30), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate30), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate31), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate31), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate32), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate32), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate33), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate33), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate34), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate34), ((max 0 (min 2 ((min 50 (max (-50) (max (-25) ((min 50 (max (-50) (- (-1))))))))))), newUpdate35), ((max 0 (min 2 ((min 50 (max (-50) ( 29+ ( 29+(((min 50 (max (-50) (abs (indexIntoBlDEFINE5 (max 0 (min 1 (-9))) (boardBlDEFINE5 blackboard)))))) + ((min 50 (max (-50) (abs (boardBlVAR3 blackboard))))))))))))), newUpdate35)]
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0
          | (False || (sereneIMPLIES True True)) = (envEnvDEFINE6 blackboard environment)
          | False = (envEnvDEFINE6 blackboard environment)
          | otherwise = (envEnvDEFINE6 blackboard environment)
        newUpdate1
          | (False || (sereneIMPLIES True True)) = (envEnvDEFINE6 blackboard environment)
          | False = (envEnvDEFINE6 blackboard environment)
          | otherwise = (envEnvDEFINE6 blackboard environment)
        newUpdate2
          | (False || (sereneIMPLIES True True)) = (envEnvDEFINE6 blackboard environment)
          | False = (envEnvDEFINE6 blackboard environment)
          | otherwise = (envEnvDEFINE6 blackboard environment)
        newUpdate3
          | (False || (sereneIMPLIES True True)) = (envEnvDEFINE6 blackboard environment)
          | False = (envEnvDEFINE6 blackboard environment)
          | otherwise = (envEnvDEFINE6 blackboard environment)
        defaultValue = (envEnvVAR1 environment)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 2 23)), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) ((-33) * (boardBlVAR3 blackboard))))))), newUpdate0), ((max 0 (min 2 23)), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) ((-33) * (boardBlVAR3 blackboard))))))), newUpdate1), ((max 0 (min 2 23)), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) ((-33) * (boardBlVAR3 blackboard))))))), newUpdate2), ((max 0 (min 2 23)), newUpdate3), ((max 0 (min 2 ((min 50 (max (-50) ((-33) * (boardBlVAR3 blackboard))))))), newUpdate3)]
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0
          | (sereneIMPLIES False True) = (envEnvDEFINE6 blackboard environment)
          | True = (indexIntoEnvDEFINE8 (max 0 (min 2 (-43))) (envEnvDEFINE8 blackboard environment))
          | otherwise = "both"
        defaultValue = (envEnvVAR1 environment)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [(0, newUpdate0), (1, newUpdate0)]

-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = newEnvironment
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeEnvironment firstGen (" ", " ", " ")
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate1
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate2
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate3
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate4
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate5
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate6
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate7
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate8
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate9
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate10
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate11
          | (((sereneCOUNT ((sereneIMPLIES False False) || (sereneXNOR False True)) (sereneXNOR ((indexIntoBlVAR0 (max 0 (min 2 3)) (boardBlVAR0 blackboard)) < 4) False))) > 5) = "both"
          | otherwise = "both"
        newUpdate12 = "no"
        defaultValue0
          | ((indexIntoBlVAR0 (max 0 (min 2 5)) (boardBlVAR0 blackboard)) > ((min 50 (max (-50) (min 5 34))))) = "no"
          | (2 >= 3) = "yes"
          | otherwise = "yes"
        defaultValue1
          | ((indexIntoBlVAR0 (max 0 (min 2 5)) (boardBlVAR0 blackboard)) > ((min 50 (max (-50) (min 5 34))))) = "no"
          | (2 >= 3) = "yes"
          | otherwise = "yes"
        defaultValue2
          | ((indexIntoBlVAR0 (max 0 (min 2 5)) (boardBlVAR0 blackboard)) > ((min 50 (max (-50) (min 5 34))))) = "no"
          | (2 >= 3) = "yes"
          | otherwise = "yes"
        defaultValue = (defaultValue0, defaultValue1, defaultValue2)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 2 (-34))), newUpdate0), ((max 0 (min 2 (-34))), newUpdate1), ((max 0 (min 2 (-34))), newUpdate2), ((max 0 (min 2 (-34))), newUpdate3), ((max 0 (min 2 (-34))), newUpdate4), ((max 0 (min 2 (-34))), newUpdate5), ((max 0 (min 2 (-34))), newUpdate6), ((max 0 (min 2 (-34))), newUpdate7), ((max 0 (min 2 (-34))), newUpdate8), ((max 0 (min 2 (-34))), newUpdate9), ((max 0 (min 2 (-34))), newUpdate10), ((max 0 (min 2 (-34))), newUpdate11), ((max 0 (min 2 29)), newUpdate12)]
    (_, newEnvironment) = (statement0 (blackboard, dummy))

