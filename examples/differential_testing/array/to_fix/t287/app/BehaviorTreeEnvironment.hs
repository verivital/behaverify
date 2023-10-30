module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
    envGenerator :: StdGen
  , envEnvVAR1 :: Integer
  , envEnvVAR4 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "env = {" ++ "envEnvVAR1: " ++ (show (envEnvVAR1 environment)) ++ ", " ++ "envEnvVAR4: " ++ (show (envEnvVAR4 environment)) ++ ", " ++ "envEnvDEFINE7: " ++ (show (envEnvDEFINE7 blackboard environment)) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE7 blackboard environment = newVal
  where
    newVal = ((sereneIMPLIES (boardBlVAR0 blackboard) True) == (boardBlVAR0 blackboard))

-- START OF INDEX FUNCTIONS FOR ARRAYS


-- START OF NEW ARRAY FUNCTIONS


-- START OF UPDATES

envUpdate :: BTreeEnvironment -> StdGen -> BTreeEnvironment
envUpdate environment newGen = environment { envGenerator = newGen }
envUpdateEnvVAR1 :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateEnvVAR1 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR1 = newVal }
envUpdateEnvVAR4 :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateEnvVAR4 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR4 = newVal }

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
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR4 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | ((envEnvDEFINE7 blackboard environment) && (sereneXOR False (boardBlVAR0 blackboard))) = (min 5 (max 2 (indexIntoBlDEFINE6 (max 0 (min 2 (-45))) (boardBlDEFINE6 blackboard))))
          | (((min 50 (max (-50) ((boardBlDEFINE8 blackboard) - (boardBlDEFINE8 blackboard))))) <= ((min 50 (max (-50) ( (boardBlDEFINE5 blackboard)+ ( (boardBlDEFINE5 blackboard)+(9 + 27))))))) = (min 5 (max 2 ((min 50 (max (-50) (- (-15)))))))
          | otherwise = (min 5 (max 2 ((min 50 (max (-50) ( (envEnvVAR4 environment)+ ( (envEnvVAR4 environment)+(((min 50 (max (-50) ((if ((boardBlVAR0 blackboard) && (envEnvDEFINE7 blackboard environment)) then (-5) else (boardBlDEFINE8 blackboard)) - (if ((boardBlVAR0 blackboard) && (envEnvDEFINE7 blackboard environment)) then (-5) else (boardBlDEFINE8 blackboard)))))) + 2))))))))
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal = (min (-2) (max (-5) (-33)))
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (sereneXOR (True && False) (envEnvDEFINE7 blackboard environment)) = (min (-2) (max (-5) ((sereneCOUNT ((envEnvDEFINE7 blackboard environment) == (13 <= (-44))) (((min 50 (max (-50) ( (indexIntoBlDEFINE6 (max 0 (min 2 (boardBlDEFINE8 blackboard))) (boardBlDEFINE6 blackboard))*((indexIntoBlDEFINE6 (max 0 (min 2 (boardBlDEFINE8 blackboard))) (boardBlDEFINE6 blackboard)) * (indexIntoBlDEFINE6 (max 0 (min 2 (boardBlDEFINE8 blackboard))) (boardBlDEFINE6 blackboard))))))) > ((min 50 (max (-50) ((-12) - (-12))))))) + (if (sereneXOR True (envEnvDEFINE7 blackboard environment)) then 1 else 0))))
          | ((boardBlDEFINE8 blackboard) >= (boardBlDEFINE5 blackboard)) = (min (-2) (max (-5) 31))
          | otherwise = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (envEnvVAR1 environment) (envEnvVAR1 environment))))) > (if ((17 >= 20) == ((envEnvVAR1 environment) < (boardBlDEFINE5 blackboard))) then ((min 50 (max (-50) (42 - 42)))) else (if ((envEnvVAR4 environment) >= 10) then (envEnvVAR4 environment) else (-2)))) then ((sereneCOUNT (2 <= 14) ((envEnvDEFINE7 blackboard environment) == (boardBlVAR0 blackboard))) + (if (sereneXOR ((envEnvDEFINE7 blackboard environment) == (boardBlVAR0 blackboard)) ((-2) == (-46))) then 1 else 0)) else ((min 50 (max (-50) (min ((sereneCOUNT (sereneXNOR False (boardBlVAR0 blackboard)) ((-17) /= (-10))) + (sereneCOUNT (16 <= (envEnvVAR4 environment)) (False || (envEnvDEFINE7 blackboard environment)))) (boardBlDEFINE8 blackboard))))))))

-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = newEnvironment
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeEnvironment firstGen 0 0
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | ((if (25 > (-35)) then (-5) else (-3)) > ((min 50 (max (-50) ( 29+(5 + 11)))))) = (min (-2) (max (-5) ((min 50 (max (-50) (- ((min 50 (max (-50) (min ((min 50 (max (-50) ( 28* ( 28*(44 * (-2))))))) (-3)))))))))))
          | True = (min (-2) (max (-5) (-3)))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ((-16) + (-41)))))))
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR4 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | False = (min 5 (max 2 16))
          | otherwise = (min 5 (max 2 ((min 50 (max (-50) ((envEnvVAR1 environment) - ((min 50 (max (-50) ((envEnvVAR1 environment) - (envEnvVAR1 environment)))))))))))
    (_, newEnvironment) = (statement1 (statement0 (blackboard, dummy)))

