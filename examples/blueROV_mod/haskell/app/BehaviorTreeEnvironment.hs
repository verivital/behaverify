module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envBattery :: Integer
  , envBbGeofence :: Bool
  , envBbHomeDist :: Integer
  , envBbPipelost :: Bool
  , envBbRth :: Bool
  , envBbSensorFailure :: Bool
  , envBbWaypointsCompleted :: Bool
  , envFlsRange :: String
  , envLecDdAm :: Bool
  , envLec2AmL :: String
  , envLec2AmR :: String
  , envObstacleInView :: Bool
  , envRtreachResult :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envBattery: " ++ show (envBattery environment) ++ ", " ++ "envBbGeofence: " ++ show (envBbGeofence environment) ++ ", " ++ "envBbHomeDist: " ++ show (envBbHomeDist environment) ++ ", " ++ "envBbPipelost: " ++ show (envBbPipelost environment) ++ ", " ++ "envBbRth: " ++ show (envBbRth environment) ++ ", " ++ "envBbSensorFailure: " ++ show (envBbSensorFailure environment) ++ ", " ++ "envBbWaypointsCompleted: " ++ show (envBbWaypointsCompleted environment) ++ ", " ++ "envFlsRange: " ++ show (envFlsRange environment) ++ ", " ++ "envLecDdAm: " ++ show (envLecDdAm environment) ++ ", " ++ "envLec2AmL: " ++ show (envLec2AmL environment) ++ ", " ++ "envLec2AmR: " ++ show (envLec2AmR environment) ++ ", " ++ "envObstacleInView: " ++ show (envObstacleInView environment) ++ ", " ++ "envRtreachResult: " ++ show (envRtreachResult environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvBattery :: Integer -> Integer
checkValueEnvBattery value
  | 0 > value || value > 1 = error "envBattery illegal value"
  | otherwise = value

checkValueEnvBbGeofence :: Bool -> Bool
checkValueEnvBbGeofence value = value

checkValueEnvBbHomeDist :: Integer -> Integer
checkValueEnvBbHomeDist 10 = 10
checkValueEnvBbHomeDist 100 = 100
checkValueEnvBbHomeDist _ = error "envBbHomeDist illegal value"

checkValueEnvBbPipelost :: Bool -> Bool
checkValueEnvBbPipelost value = value

checkValueEnvBbRth :: Bool -> Bool
checkValueEnvBbRth value = value

checkValueEnvBbSensorFailure :: Bool -> Bool
checkValueEnvBbSensorFailure value = value

checkValueEnvBbWaypointsCompleted :: Bool -> Bool
checkValueEnvBbWaypointsCompleted value = value

checkValueEnvFlsRange :: String -> String
checkValueEnvFlsRange "danger_zone" = "danger_zone"
checkValueEnvFlsRange "safe" = "safe"
checkValueEnvFlsRange _ = error "envFlsRange illegal value"

checkValueEnvLecDdAm :: Bool -> Bool
checkValueEnvLecDdAm value = value

checkValueEnvLec2AmL :: String -> String
checkValueEnvLec2AmL "safe" = "safe"
checkValueEnvLec2AmL "speed" = "speed"
checkValueEnvLec2AmL "pipe" = "pipe"
checkValueEnvLec2AmL "speed_pipe" = "speed_pipe"
checkValueEnvLec2AmL _ = error "envLec2AmL illegal value"

checkValueEnvLec2AmR :: String -> String
checkValueEnvLec2AmR "safe" = "safe"
checkValueEnvLec2AmR "speed" = "speed"
checkValueEnvLec2AmR "pipe" = "pipe"
checkValueEnvLec2AmR "speed_pipe" = "speed_pipe"
checkValueEnvLec2AmR _ = error "envLec2AmR illegal value"

checkValueEnvObstacleInView :: Bool -> Bool
checkValueEnvObstacleInView value = value

checkValueEnvRtreachResult :: String -> String
checkValueEnvRtreachResult "safe" = "safe"
checkValueEnvRtreachResult "short" = "short"
checkValueEnvRtreachResult "long" = "long"
checkValueEnvRtreachResult "short_long" = "short_long"
checkValueEnvRtreachResult _ = error "envRtreachResult illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvBattery :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvBattery environment value = environment { envBattery = (checkValueEnvBattery value)}
updateEnvBbGeofence :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvBbGeofence environment value = environment { envBbGeofence = (checkValueEnvBbGeofence value)}
updateEnvBbHomeDist :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvBbHomeDist environment value = environment { envBbHomeDist = (checkValueEnvBbHomeDist value)}
updateEnvBbPipelost :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvBbPipelost environment value = environment { envBbPipelost = (checkValueEnvBbPipelost value)}
updateEnvBbRth :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvBbRth environment value = environment { envBbRth = (checkValueEnvBbRth value)}
updateEnvBbSensorFailure :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvBbSensorFailure environment value = environment { envBbSensorFailure = (checkValueEnvBbSensorFailure value)}
updateEnvBbWaypointsCompleted :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvBbWaypointsCompleted environment value = environment { envBbWaypointsCompleted = (checkValueEnvBbWaypointsCompleted value)}
updateEnvFlsRange :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvFlsRange environment value = environment { envFlsRange = (checkValueEnvFlsRange value)}
updateEnvLecDdAm :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvLecDdAm environment value = environment { envLecDdAm = (checkValueEnvLecDdAm value)}
updateEnvLec2AmL :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvLec2AmL environment value = environment { envLec2AmL = (checkValueEnvLec2AmL value)}
updateEnvLec2AmR :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvLec2AmR environment value = environment { envLec2AmR = (checkValueEnvLec2AmR value)}
updateEnvObstacleInView :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvObstacleInView environment value = environment { envObstacleInView = (checkValueEnvObstacleInView value)}
updateEnvRtreachResult :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvRtreachResult environment value = environment { envRtreachResult = (checkValueEnvRtreachResult value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = (not (boardBLUEROVSURFACED blackboard))

-- START OF FUTURE CHANGES

applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)

-- START OF BETWEEN TICK CHANGES

betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)
  where
    tempEnvironment0 = curEnvironment
    newEnvironment = tempEnvironment13
    tickUpdate1FlsRange :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1FlsRange environment = updateEnvGenerator (updateEnvFlsRange environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "danger_zone"
        privateRandom0 _ = "safe"

    tempEnvironment1 = tickUpdate1FlsRange tempEnvironment0

    tickUpdate2ObstacleInView :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2ObstacleInView environment = updateEnvGenerator (updateEnvObstacleInView environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment2 = tickUpdate2ObstacleInView tempEnvironment1

    tickUpdate3Battery :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3Battery environment = updateEnvGenerator (updateEnvBattery environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 _ = 1

    tempEnvironment3 = tickUpdate3Battery tempEnvironment2

    tickUpdate4LecDdAm :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4LecDdAm environment = updateEnvGenerator (updateEnvLecDdAm environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment4 = tickUpdate4LecDdAm tempEnvironment3

    tickUpdate5BbRth :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5BbRth environment = updateEnvGenerator (updateEnvBbRth environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment5 = tickUpdate5BbRth tempEnvironment4

    tickUpdate6BbGeofence :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate6BbGeofence environment = updateEnvGenerator (updateEnvBbGeofence environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment6 = tickUpdate6BbGeofence tempEnvironment5

    tickUpdate7Lec2AmL :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate7Lec2AmL environment = updateEnvGenerator (updateEnvLec2AmL environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 3)))) (snd (getRandomInteger (sereneEnvGenerator environment) 3))
      where
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "safe"
        privateRandom0 1 = "speed"
        privateRandom0 2 = "pipe"
        privateRandom0 _ = "speed_pipe"

    tempEnvironment7 = tickUpdate7Lec2AmL tempEnvironment6

    tickUpdate8Lec2AmR :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate8Lec2AmR environment = updateEnvGenerator (updateEnvLec2AmR environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 3)))) (snd (getRandomInteger (sereneEnvGenerator environment) 3))
      where
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "safe"
        privateRandom0 1 = "speed"
        privateRandom0 2 = "pipe"
        privateRandom0 _ = "speed_pipe"

    tempEnvironment8 = tickUpdate8Lec2AmR tempEnvironment7

    tickUpdate9BbPipelost :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate9BbPipelost environment = updateEnvGenerator (updateEnvBbPipelost environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment9 = tickUpdate9BbPipelost tempEnvironment8

    tickUpdate10BbSensorFailure :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate10BbSensorFailure environment = updateEnvGenerator (updateEnvBbSensorFailure environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment10 = tickUpdate10BbSensorFailure tempEnvironment9

    tickUpdate11BbWaypointsCompleted :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate11BbWaypointsCompleted environment = updateEnvGenerator (updateEnvBbWaypointsCompleted environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    tempEnvironment11 = tickUpdate11BbWaypointsCompleted tempEnvironment10

    tickUpdate12BbHomeDist :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate12BbHomeDist environment = updateEnvGenerator (updateEnvBbHomeDist environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 10
        privateRandom0 _ = 100

    tempEnvironment12 = tickUpdate12BbHomeDist tempEnvironment11

    tickUpdate13RtreachResult :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate13RtreachResult environment = updateEnvGenerator (updateEnvRtreachResult environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 3)))) (snd (getRandomInteger (sereneEnvGenerator environment) 3))
      where
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "safe"
        privateRandom0 1 = "short"
        privateRandom0 2 = "long"
        privateRandom0 _ = "short_long"

    tempEnvironment13 = tickUpdate13RtreachResult tempEnvironment12



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange newValLecDdAm newValLec2AmL newValLec2AmR newValObstacleInView newValRtreachResult  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen13
    partialEnvironmentBattery = BTreeEnvironment newSereneGenerator 0 True 0 True True True True " " True " " " " True " "
    initValBattery :: StdGen -> (Integer, StdGen)
    initValBattery curGen = (1, curGen)
      where
        environment = partialEnvironmentBattery

    (newValBattery, tempGen1) = initValBattery tempGen0

    partialEnvironmentBbGeofence = BTreeEnvironment newSereneGenerator newValBattery True 0 True True True True " " True " " " " True " "
    initValBbGeofence :: StdGen -> (Bool, StdGen)
    initValBbGeofence curGen = (False, curGen)
      where
        environment = partialEnvironmentBbGeofence

    (newValBbGeofence, tempGen2) = initValBbGeofence tempGen1

    partialEnvironmentBbHomeDist = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence 0 True True True True " " True " " " " True " "
    initValBbHomeDist :: StdGen -> (Integer, StdGen)
    initValBbHomeDist curGen = (10, curGen)
      where
        environment = partialEnvironmentBbHomeDist

    (newValBbHomeDist, tempGen3) = initValBbHomeDist tempGen2

    partialEnvironmentBbPipelost = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist True True True True " " True " " " " True " "
    initValBbPipelost :: StdGen -> (Bool, StdGen)
    initValBbPipelost curGen = (False, curGen)
      where
        environment = partialEnvironmentBbPipelost

    (newValBbPipelost, tempGen4) = initValBbPipelost tempGen3

    partialEnvironmentBbRth = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost True True True " " True " " " " True " "
    initValBbRth :: StdGen -> (Bool, StdGen)
    initValBbRth curGen = (False, curGen)
      where
        environment = partialEnvironmentBbRth

    (newValBbRth, tempGen5) = initValBbRth tempGen4

    partialEnvironmentBbSensorFailure = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth True True " " True " " " " True " "
    initValBbSensorFailure :: StdGen -> (Bool, StdGen)
    initValBbSensorFailure curGen = (False, curGen)
      where
        environment = partialEnvironmentBbSensorFailure

    (newValBbSensorFailure, tempGen6) = initValBbSensorFailure tempGen5

    partialEnvironmentBbWaypointsCompleted = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure True " " True " " " " True " "
    initValBbWaypointsCompleted :: StdGen -> (Bool, StdGen)
    initValBbWaypointsCompleted curGen = (False, curGen)
      where
        environment = partialEnvironmentBbWaypointsCompleted

    (newValBbWaypointsCompleted, tempGen7) = initValBbWaypointsCompleted tempGen6

    partialEnvironmentFlsRange = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted " " True " " " " True " "
    initValFlsRange :: StdGen -> (String, StdGen)
    initValFlsRange curGen = ("safe", curGen)
      where
        environment = partialEnvironmentFlsRange

    (newValFlsRange, tempGen8) = initValFlsRange tempGen7

    partialEnvironmentLecDdAm = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange True " " " " True " "
    initValLecDdAm :: StdGen -> (Bool, StdGen)
    initValLecDdAm curGen = (False, curGen)
      where
        environment = partialEnvironmentLecDdAm

    (newValLecDdAm, tempGen9) = initValLecDdAm tempGen8

    partialEnvironmentLec2AmL = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange newValLecDdAm " " " " True " "
    initValLec2AmL :: StdGen -> (String, StdGen)
    initValLec2AmL curGen = ("safe", curGen)
      where
        environment = partialEnvironmentLec2AmL

    (newValLec2AmL, tempGen10) = initValLec2AmL tempGen9

    partialEnvironmentLec2AmR = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange newValLecDdAm newValLec2AmL " " True " "
    initValLec2AmR :: StdGen -> (String, StdGen)
    initValLec2AmR curGen = ("safe", curGen)
      where
        environment = partialEnvironmentLec2AmR

    (newValLec2AmR, tempGen11) = initValLec2AmR tempGen10

    partialEnvironmentObstacleInView = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange newValLecDdAm newValLec2AmL newValLec2AmR True " "
    initValObstacleInView :: StdGen -> (Bool, StdGen)
    initValObstacleInView curGen = (False, curGen)
      where
        environment = partialEnvironmentObstacleInView

    (newValObstacleInView, tempGen12) = initValObstacleInView tempGen11

    partialEnvironmentRtreachResult = BTreeEnvironment newSereneGenerator newValBattery newValBbGeofence newValBbHomeDist newValBbPipelost newValBbRth newValBbSensorFailure newValBbWaypointsCompleted newValFlsRange newValLecDdAm newValLec2AmL newValLec2AmR newValObstacleInView " "
    initValRtreachResult :: StdGen -> (String, StdGen)
    initValRtreachResult curGen = ("safe", curGen)
      where
        environment = partialEnvironmentRtreachResult

    (newValRtreachResult, tempGen13) = initValRtreachResult tempGen12


