module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import BehaviorTreeBlackboard
import SereneOperations

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envXGoal :: Int
  , envYGoal :: Int
  , envXTrue :: Int
  , envYTrue :: Int
  , envRemainingGoals :: Int
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ envXGoal envYGoal envXTrue envYTrue envRemainingGoals) = "Env = {" ++ "envXGoal: " ++ show envXGoal ++ ", envYGoal: " ++ show envYGoal ++ ", envXTrue: " ++ show envXTrue ++ ", envYTrue: " ++ show envYTrue ++ ", envRemainingGoals: " ++ show envRemainingGoals ++ "}"




updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvXGoal :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvXGoal environment value
  | 0 > value || value > 1 = error "x_goal illegal value"
  | otherwise = environment { envXGoal = value }

updateEnvYGoal :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvYGoal environment value
  | 0 > value || value > 1 = error "y_goal illegal value"
  | otherwise = environment { envYGoal = value }

updateEnvXTrue :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvXTrue environment value
  | 0 > value || value > 1 = error "x_true illegal value"
  | otherwise = environment { envXTrue = value }

updateEnvYTrue :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvYTrue environment value
  | 0 > value || value > 1 = error "y_true illegal value"
  | otherwise = environment { envYTrue = value }

updateEnvRemainingGoals :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvRemainingGoals environment value
  | 0 > value || value > 3 = error "remaining_goals illegal value"
  | otherwise = environment { envRemainingGoals = value }

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = ((envRemainingGoals environment) > 0)

modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment
modifiedID _ environment = environment
applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)


betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)
  where
    tempEnvironment0 = curEnvironment
    newEnvironment = tempEnvironment3
    tickUpdateRemainingGoals :: BTreeEnvironment -> BTreeEnvironment
    tickUpdateRemainingGoals environment
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = environment { envRemainingGoals = (max 0 ((envRemainingGoals environment) - 1)) }
      | otherwise = environment { envRemainingGoals = (envRemainingGoals environment) }

    tempEnvironment1 = tickUpdateRemainingGoals tempEnvironment0

    tickUpdateXGoal :: BTreeEnvironment -> BTreeEnvironment
    tickUpdateXGoal environment
      | (0 == (envRemainingGoals environment)) = environment { envXGoal = (envXGoal environment) }
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = environment { sereneEnvGenerator = (snd (getRandomInt (sereneEnvGenerator environment) 1)), envXGoal = privateRandom0 (fst (getRandomInt (sereneEnvGenerator environment) 1)) }
      | otherwise = environment { envXGoal = (envXGoal environment) }
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    tempEnvironment2 = tickUpdateXGoal tempEnvironment1

    tickUpdateYGoal :: BTreeEnvironment -> BTreeEnvironment
    tickUpdateYGoal environment
      | (0 == (envRemainingGoals environment)) = environment { envYGoal = (envYGoal environment) }
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = environment { sereneEnvGenerator = (snd (getRandomInt (sereneEnvGenerator environment) 1)), envYGoal = privateRandom0 (fst (getRandomInt (sereneEnvGenerator environment) 1)) }
      | otherwise = environment { envYGoal = (envYGoal environment) }
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    tempEnvironment3 = tickUpdateYGoal tempEnvironment2


betweenTickUpdate environment = environment


initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValXGoal newValYGoal newValXTrue newValYTrue newValRemainingGoals
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    initValXGoal :: StdGen -> (Int, StdGen)
    initValXGoal curGen = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    (newValXGoal, tempGen1) = initValXGoal tempGen0

    initValYGoal :: StdGen -> (Int, StdGen)
    initValYGoal curGen = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    (newValYGoal, tempGen2) = initValYGoal tempGen1

    initValXTrue :: StdGen -> (Int, StdGen)
    initValXTrue curGen = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    (newValXTrue, tempGen3) = initValXTrue tempGen2

    initValYTrue :: StdGen -> (Int, StdGen)
    initValYTrue curGen = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    (newValYTrue, tempGen4) = initValYTrue tempGen3

    initValRemainingGoals :: StdGen -> (Int, StdGen)
    initValRemainingGoals curGen = (privateRandom0 (fst (getRandomInt curGen 3)), snd (getRandomInt curGen 3))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 _ = 3

    (newValRemainingGoals, tempGen5) = initValRemainingGoals tempGen4


