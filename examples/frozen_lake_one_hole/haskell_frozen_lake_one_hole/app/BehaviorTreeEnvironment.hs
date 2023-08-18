module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import BehaviorTreeBlackboard
import SereneOperations

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envStartLoc :: Int
  , envGoalLoc :: Int
  , envLoc :: Int
  , envHoleLoc :: Int
  , envFallsRemaining :: Int
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ envStartLoc envGoalLoc envLoc envHoleLoc envFallsRemaining) = "Env = {" ++ "envStartLoc: " ++ show envStartLoc ++ ", envGoalLoc: " ++ show envGoalLoc ++ ", envLoc: " ++ show envLoc ++ ", envHoleLoc: " ++ show envHoleLoc ++ ", envFallsRemaining: " ++ show envFallsRemaining ++ "}"


envXLoc :: BTreeBlackboard -> BTreeEnvironment -> Int
envXLoc blackboard environment = (rem (envLoc environment) 4)
envYLoc :: BTreeBlackboard -> BTreeEnvironment -> Int
envYLoc blackboard environment = (quot ((envLoc environment) - (envXLoc blackboard environment)) 4)


updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvStartLoc :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvStartLoc environment _ = environment

updateEnvGoalLoc :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvGoalLoc environment _ = environment

updateEnvLoc :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvLoc environment value
  | 0 > value || value > 15 = error "loc illegal value"
  | otherwise = environment { envLoc = value }

updateEnvHoleLoc :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHoleLoc environment _ = environment

updateEnvFallsRemaining :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvFallsRemaining environment value
  | (-1) > value || value > 1 = error "falls_remaining illegal value"
  | otherwise = environment { envFallsRemaining = value }

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment
modifiedID _ environment = environment
applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)


betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)
  where
    tempEnvironment0 = curEnvironment
    newEnvironment = tempEnvironment2
    tickUpdate1Loc :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1Loc environment
      | ((boardAction blackboard) == (-1)) = environment { envLoc = (envStartLoc environment) }
      | ((boardAction blackboard) == 3) = environment { envLoc = ((envXLoc blackboard environment) + (4 * (max 0 ((envYLoc blackboard environment) - 1)))) }
      | ((boardAction blackboard) == 1) = environment { envLoc = ((envXLoc blackboard environment) + (4 * (min 3 ((envYLoc blackboard environment) + 1)))) }
      | ((boardAction blackboard) == 0) = environment { envLoc = ((max 0 ((envXLoc blackboard environment) - 1)) + (4 * (envYLoc blackboard environment))) }
      | ((boardAction blackboard) == 2) = environment { envLoc = ((min 3 ((envXLoc blackboard environment) + 1)) + (4 * (envYLoc blackboard environment))) }
      | otherwise = environment { envLoc = (envLoc environment) }

    tempEnvironment1 = tickUpdate1Loc tempEnvironment0

    tickUpdate2FallsRemaining :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2FallsRemaining environment
      | ((envLoc environment) == (envHoleLoc environment)) = environment { envFallsRemaining = (max (-1) ((envFallsRemaining environment) - 1)) }
      | otherwise = environment { envFallsRemaining = (envFallsRemaining environment) }

    tempEnvironment2 = tickUpdate2FallsRemaining tempEnvironment1




initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValStartLoc newValGoalLoc newValLoc newValHoleLoc newValFallsRemaining
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentStartLoc = BTreeEnvironment newSereneGenerator 0 0 0 0 0
    initValStartLoc :: StdGen -> (Int, StdGen)
    initValStartLoc curGen = (privateRandom0 (fst (getRandomInt curGen 15)), snd (getRandomInt curGen 15))
      where
        environment = partialEnvironmentStartLoc
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 7 = 7
        privateRandom0 8 = 8
        privateRandom0 9 = 9
        privateRandom0 10 = 10
        privateRandom0 11 = 11
        privateRandom0 12 = 12
        privateRandom0 13 = 13
        privateRandom0 14 = 14
        privateRandom0 _ = 15

    (newValStartLoc, tempGen1) = initValStartLoc tempGen0

    partialEnvironmentGoalLoc = BTreeEnvironment newSereneGenerator newValStartLoc 0 0 0 0
    initValGoalLoc :: StdGen -> (Int, StdGen)
    initValGoalLoc curGen = (privateRandom0 (fst (getRandomInt curGen 15)), snd (getRandomInt curGen 15))
      where
        environment = partialEnvironmentGoalLoc
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 7 = 7
        privateRandom0 8 = 8
        privateRandom0 9 = 9
        privateRandom0 10 = 10
        privateRandom0 11 = 11
        privateRandom0 12 = 12
        privateRandom0 13 = 13
        privateRandom0 14 = 14
        privateRandom0 _ = 15

    (newValGoalLoc, tempGen2) = initValGoalLoc tempGen1

    partialEnvironmentLoc = BTreeEnvironment newSereneGenerator newValStartLoc newValGoalLoc 0 0 0
    initValLoc :: StdGen -> (Int, StdGen)
    initValLoc curGen = (newValStartLoc, curGen)
      where
        environment = partialEnvironmentLoc

    (newValLoc, tempGen3) = initValLoc tempGen2

    partialEnvironmentHoleLoc = BTreeEnvironment newSereneGenerator newValStartLoc newValGoalLoc newValLoc 0 0
    initValHoleLoc :: StdGen -> (Int, StdGen)
    initValHoleLoc curGen
      | (newValStartLoc == 0) = (privateRandom0 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 1) = (privateRandom1 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 2) = (privateRandom2 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 3) = (privateRandom3 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 4) = (privateRandom4 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 5) = (privateRandom5 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 6) = (privateRandom6 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 7) = (privateRandom7 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 8) = (privateRandom8 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 9) = (privateRandom9 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 10) = (privateRandom10 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 11) = (privateRandom11 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 12) = (privateRandom12 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 13) = (privateRandom13 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 14) = (privateRandom14 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | (newValStartLoc == 15) = (privateRandom15 (fst (getRandomInt curGen 14)), snd (getRandomInt curGen 14))
      | otherwise = (0, curGen)
      where
        environment = partialEnvironmentHoleLoc
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 1
        privateRandom0 1 = 2
        privateRandom0 2 = 3
        privateRandom0 3 = 4
        privateRandom0 4 = 5
        privateRandom0 5 = 6
        privateRandom0 6 = 7
        privateRandom0 7 = 8
        privateRandom0 8 = 9
        privateRandom0 9 = 10
        privateRandom0 10 = 11
        privateRandom0 11 = 12
        privateRandom0 12 = 13
        privateRandom0 13 = 14
        privateRandom0 _ = 15
        privateRandom1 :: Int -> Int
        privateRandom1 0 = 0
        privateRandom1 1 = 2
        privateRandom1 2 = 3
        privateRandom1 3 = 4
        privateRandom1 4 = 5
        privateRandom1 5 = 6
        privateRandom1 6 = 7
        privateRandom1 7 = 8
        privateRandom1 8 = 9
        privateRandom1 9 = 10
        privateRandom1 10 = 11
        privateRandom1 11 = 12
        privateRandom1 12 = 13
        privateRandom1 13 = 14
        privateRandom1 _ = 15
        privateRandom2 :: Int -> Int
        privateRandom2 0 = 0
        privateRandom2 1 = 1
        privateRandom2 2 = 3
        privateRandom2 3 = 4
        privateRandom2 4 = 5
        privateRandom2 5 = 6
        privateRandom2 6 = 7
        privateRandom2 7 = 8
        privateRandom2 8 = 9
        privateRandom2 9 = 10
        privateRandom2 10 = 11
        privateRandom2 11 = 12
        privateRandom2 12 = 13
        privateRandom2 13 = 14
        privateRandom2 _ = 15
        privateRandom3 :: Int -> Int
        privateRandom3 0 = 0
        privateRandom3 1 = 1
        privateRandom3 2 = 2
        privateRandom3 3 = 4
        privateRandom3 4 = 5
        privateRandom3 5 = 6
        privateRandom3 6 = 7
        privateRandom3 7 = 8
        privateRandom3 8 = 9
        privateRandom3 9 = 10
        privateRandom3 10 = 11
        privateRandom3 11 = 12
        privateRandom3 12 = 13
        privateRandom3 13 = 14
        privateRandom3 _ = 15
        privateRandom4 :: Int -> Int
        privateRandom4 0 = 0
        privateRandom4 1 = 1
        privateRandom4 2 = 2
        privateRandom4 3 = 3
        privateRandom4 4 = 5
        privateRandom4 5 = 6
        privateRandom4 6 = 7
        privateRandom4 7 = 8
        privateRandom4 8 = 9
        privateRandom4 9 = 10
        privateRandom4 10 = 11
        privateRandom4 11 = 12
        privateRandom4 12 = 13
        privateRandom4 13 = 14
        privateRandom4 _ = 15
        privateRandom5 :: Int -> Int
        privateRandom5 0 = 0
        privateRandom5 1 = 1
        privateRandom5 2 = 2
        privateRandom5 3 = 3
        privateRandom5 4 = 4
        privateRandom5 5 = 6
        privateRandom5 6 = 7
        privateRandom5 7 = 8
        privateRandom5 8 = 9
        privateRandom5 9 = 10
        privateRandom5 10 = 11
        privateRandom5 11 = 12
        privateRandom5 12 = 13
        privateRandom5 13 = 14
        privateRandom5 _ = 15
        privateRandom6 :: Int -> Int
        privateRandom6 0 = 0
        privateRandom6 1 = 1
        privateRandom6 2 = 2
        privateRandom6 3 = 3
        privateRandom6 4 = 4
        privateRandom6 5 = 5
        privateRandom6 6 = 7
        privateRandom6 7 = 8
        privateRandom6 8 = 9
        privateRandom6 9 = 10
        privateRandom6 10 = 11
        privateRandom6 11 = 12
        privateRandom6 12 = 13
        privateRandom6 13 = 14
        privateRandom6 _ = 15
        privateRandom7 :: Int -> Int
        privateRandom7 0 = 0
        privateRandom7 1 = 1
        privateRandom7 2 = 2
        privateRandom7 3 = 3
        privateRandom7 4 = 4
        privateRandom7 5 = 5
        privateRandom7 6 = 6
        privateRandom7 7 = 8
        privateRandom7 8 = 9
        privateRandom7 9 = 10
        privateRandom7 10 = 11
        privateRandom7 11 = 12
        privateRandom7 12 = 13
        privateRandom7 13 = 14
        privateRandom7 _ = 15
        privateRandom8 :: Int -> Int
        privateRandom8 0 = 0
        privateRandom8 1 = 1
        privateRandom8 2 = 2
        privateRandom8 3 = 3
        privateRandom8 4 = 4
        privateRandom8 5 = 5
        privateRandom8 6 = 6
        privateRandom8 7 = 7
        privateRandom8 8 = 9
        privateRandom8 9 = 10
        privateRandom8 10 = 11
        privateRandom8 11 = 12
        privateRandom8 12 = 13
        privateRandom8 13 = 14
        privateRandom8 _ = 15
        privateRandom9 :: Int -> Int
        privateRandom9 0 = 0
        privateRandom9 1 = 1
        privateRandom9 2 = 2
        privateRandom9 3 = 3
        privateRandom9 4 = 4
        privateRandom9 5 = 5
        privateRandom9 6 = 6
        privateRandom9 7 = 7
        privateRandom9 8 = 8
        privateRandom9 9 = 10
        privateRandom9 10 = 11
        privateRandom9 11 = 12
        privateRandom9 12 = 13
        privateRandom9 13 = 14
        privateRandom9 _ = 15
        privateRandom10 :: Int -> Int
        privateRandom10 0 = 0
        privateRandom10 1 = 1
        privateRandom10 2 = 2
        privateRandom10 3 = 3
        privateRandom10 4 = 4
        privateRandom10 5 = 5
        privateRandom10 6 = 6
        privateRandom10 7 = 7
        privateRandom10 8 = 8
        privateRandom10 9 = 9
        privateRandom10 10 = 11
        privateRandom10 11 = 12
        privateRandom10 12 = 13
        privateRandom10 13 = 14
        privateRandom10 _ = 15
        privateRandom11 :: Int -> Int
        privateRandom11 0 = 0
        privateRandom11 1 = 1
        privateRandom11 2 = 2
        privateRandom11 3 = 3
        privateRandom11 4 = 4
        privateRandom11 5 = 5
        privateRandom11 6 = 6
        privateRandom11 7 = 7
        privateRandom11 8 = 8
        privateRandom11 9 = 9
        privateRandom11 10 = 10
        privateRandom11 11 = 12
        privateRandom11 12 = 13
        privateRandom11 13 = 14
        privateRandom11 _ = 15
        privateRandom12 :: Int -> Int
        privateRandom12 0 = 0
        privateRandom12 1 = 1
        privateRandom12 2 = 2
        privateRandom12 3 = 3
        privateRandom12 4 = 4
        privateRandom12 5 = 5
        privateRandom12 6 = 6
        privateRandom12 7 = 7
        privateRandom12 8 = 8
        privateRandom12 9 = 9
        privateRandom12 10 = 10
        privateRandom12 11 = 11
        privateRandom12 12 = 13
        privateRandom12 13 = 14
        privateRandom12 _ = 15
        privateRandom13 :: Int -> Int
        privateRandom13 0 = 0
        privateRandom13 1 = 1
        privateRandom13 2 = 2
        privateRandom13 3 = 3
        privateRandom13 4 = 4
        privateRandom13 5 = 5
        privateRandom13 6 = 6
        privateRandom13 7 = 7
        privateRandom13 8 = 8
        privateRandom13 9 = 9
        privateRandom13 10 = 10
        privateRandom13 11 = 11
        privateRandom13 12 = 12
        privateRandom13 13 = 14
        privateRandom13 _ = 15
        privateRandom14 :: Int -> Int
        privateRandom14 0 = 0
        privateRandom14 1 = 1
        privateRandom14 2 = 2
        privateRandom14 3 = 3
        privateRandom14 4 = 4
        privateRandom14 5 = 5
        privateRandom14 6 = 6
        privateRandom14 7 = 7
        privateRandom14 8 = 8
        privateRandom14 9 = 9
        privateRandom14 10 = 10
        privateRandom14 11 = 11
        privateRandom14 12 = 12
        privateRandom14 13 = 13
        privateRandom14 _ = 15
        privateRandom15 :: Int -> Int
        privateRandom15 0 = 0
        privateRandom15 1 = 1
        privateRandom15 2 = 2
        privateRandom15 3 = 3
        privateRandom15 4 = 4
        privateRandom15 5 = 5
        privateRandom15 6 = 6
        privateRandom15 7 = 7
        privateRandom15 8 = 8
        privateRandom15 9 = 9
        privateRandom15 10 = 10
        privateRandom15 11 = 11
        privateRandom15 12 = 12
        privateRandom15 13 = 13
        privateRandom15 _ = 14

    (newValHoleLoc, tempGen4) = initValHoleLoc tempGen3

    partialEnvironmentFallsRemaining = BTreeEnvironment newSereneGenerator newValStartLoc newValGoalLoc newValLoc newValHoleLoc 0
    initValFallsRemaining :: StdGen -> (Int, StdGen)
    initValFallsRemaining curGen = (1, curGen)
      where
        environment = partialEnvironmentFallsRemaining

    (newValFallsRemaining, tempGen5) = initValFallsRemaining tempGen4


