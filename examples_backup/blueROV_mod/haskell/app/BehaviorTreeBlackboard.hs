module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBatteryLowWarning :: Bool
  , boardBbFlsWarning :: Bool
  , boardBbGeofenceWarning :: Bool
  , boardBbHomeReached :: Bool
  , boardBbMission :: String
  , boardBbObstacleWarning :: Bool
  , boardBbPipeLostWarning :: Bool
  , boardBbPipeMappingEnable :: Bool
  , boardBbRthWarning :: Bool
  , boardBbSensorFailureWarning :: Bool
  , boardCmHsdInput :: String
  , boardDdXyAxisDegradation :: Bool
  , boardDdZAxisWarning :: Bool
  , boardEmergencyStopWarning :: Bool
  , boardHSDOut :: String
  , boardLecDdAmWarning :: Bool
  , boardLec2AmLSpeedWarning :: Bool
  , boardLec2AmLPipeWarning :: Bool
  , boardLec2AmRSpeedWarning :: Bool
  , boardLec2AmRPipeWarning :: Bool
  , boardNextMission :: Bool
  , boardPipeMappingEnable :: Bool
  , boardObstacleStandoffWarning :: Bool
  , boardRtreachLongTermWarning :: Bool
  , boardRtreachObstacleWarning :: Bool
  , boardRtreachWarning :: Bool
  , boardFinishedMissions :: Bool
  , boardDdOutput :: String
  , boardBLUEROVSURFACED :: Bool
  , localBoardReadSuccessLocation2 :: Bool
  , localBoardReadSuccessLocation3 :: Bool
  , localBoardReadSuccessLocation4 :: Bool
  , localBoardReadSuccessLocation5 :: Bool
  , localBoardReadSuccessLocation6 :: Bool
  , localBoardReadSuccessLocation7 :: Bool
  , localBoardReadSuccessLocation8 :: Bool
  , localBoardReadSuccessLocation9 :: Bool
  , localBoardReadSuccessLocation10 :: Bool
  , localBoardReadSuccessLocation11 :: Bool
  , localBoardReadSuccessLocation12 :: Bool
  , localBoardReadSuccessLocation13 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBatteryLowWarning: " ++ show (boardBatteryLowWarning blackboard) ++ ", " ++ "boardBbFlsWarning: " ++ show (boardBbFlsWarning blackboard) ++ ", " ++ "boardBbGeofenceWarning: " ++ show (boardBbGeofenceWarning blackboard) ++ ", " ++ "boardBbHomeReached: " ++ show (boardBbHomeReached blackboard) ++ ", " ++ "boardBbMission: " ++ show (boardBbMission blackboard) ++ ", " ++ "boardBbObstacleWarning: " ++ show (boardBbObstacleWarning blackboard) ++ ", " ++ "boardBbPipeLostWarning: " ++ show (boardBbPipeLostWarning blackboard) ++ ", " ++ "boardBbPipeMappingEnable: " ++ show (boardBbPipeMappingEnable blackboard) ++ ", " ++ "boardBbRthWarning: " ++ show (boardBbRthWarning blackboard) ++ ", " ++ "boardBbSensorFailureWarning: " ++ show (boardBbSensorFailureWarning blackboard) ++ ", " ++ "boardCmHsdInput: " ++ show (boardCmHsdInput blackboard) ++ ", " ++ "boardDdXyAxisDegradation: " ++ show (boardDdXyAxisDegradation blackboard) ++ ", " ++ "boardDdZAxisWarning: " ++ show (boardDdZAxisWarning blackboard) ++ ", " ++ "boardEmergencyStopWarning: " ++ show (boardEmergencyStopWarning blackboard) ++ ", " ++ "boardHSDOut: " ++ show (boardHSDOut blackboard) ++ ", " ++ "boardLecDdAmWarning: " ++ show (boardLecDdAmWarning blackboard) ++ ", " ++ "boardLec2AmLSpeedWarning: " ++ show (boardLec2AmLSpeedWarning blackboard) ++ ", " ++ "boardLec2AmLPipeWarning: " ++ show (boardLec2AmLPipeWarning blackboard) ++ ", " ++ "boardLec2AmRSpeedWarning: " ++ show (boardLec2AmRSpeedWarning blackboard) ++ ", " ++ "boardLec2AmRPipeWarning: " ++ show (boardLec2AmRPipeWarning blackboard) ++ ", " ++ "boardNextMission: " ++ show (boardNextMission blackboard) ++ ", " ++ "boardPipeMappingEnable: " ++ show (boardPipeMappingEnable blackboard) ++ ", " ++ "boardObstacleStandoffWarning: " ++ show (boardObstacleStandoffWarning blackboard) ++ ", " ++ "boardRtreachLongTermWarning: " ++ show (boardRtreachLongTermWarning blackboard) ++ ", " ++ "boardRtreachObstacleWarning: " ++ show (boardRtreachObstacleWarning blackboard) ++ ", " ++ "boardRtreachWarning: " ++ show (boardRtreachWarning blackboard) ++ ", " ++ "boardFinishedMissions: " ++ show (boardFinishedMissions blackboard) ++ ", " ++ "boardDdOutput: " ++ show (boardDdOutput blackboard) ++ ", " ++ "boardBLUEROVSURFACED: " ++ show (boardBLUEROVSURFACED blackboard) ++ ", " ++ "localBoardReadSuccessLocation2: " ++ show (localBoardReadSuccess 2blackboard) ++ ", " ++ "localBoardReadSuccessLocation3: " ++ show (localBoardReadSuccess 3blackboard) ++ ", " ++ "localBoardReadSuccessLocation4: " ++ show (localBoardReadSuccess 4blackboard) ++ ", " ++ "localBoardReadSuccessLocation5: " ++ show (localBoardReadSuccess 5blackboard) ++ ", " ++ "localBoardReadSuccessLocation6: " ++ show (localBoardReadSuccess 6blackboard) ++ ", " ++ "localBoardReadSuccessLocation7: " ++ show (localBoardReadSuccess 7blackboard) ++ ", " ++ "localBoardReadSuccessLocation8: " ++ show (localBoardReadSuccess 8blackboard) ++ ", " ++ "localBoardReadSuccessLocation9: " ++ show (localBoardReadSuccess 9blackboard) ++ ", " ++ "localBoardReadSuccessLocation10: " ++ show (localBoardReadSuccess 10blackboard) ++ ", " ++ "localBoardReadSuccessLocation11: " ++ show (localBoardReadSuccess 11blackboard) ++ ", " ++ "localBoardReadSuccessLocation12: " ++ show (localBoardReadSuccess 12blackboard) ++ ", " ++ "localBoardReadSuccessLocation13: " ++ show (localBoardReadSuccess 13blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardReadSuccess :: Integer -> BTreeBlackboard -> Bool
localBoardReadSuccess 2 = localBoardReadSuccessLocation2
localBoardReadSuccess 3 = localBoardReadSuccessLocation3
localBoardReadSuccess 4 = localBoardReadSuccessLocation4
localBoardReadSuccess 5 = localBoardReadSuccessLocation5
localBoardReadSuccess 6 = localBoardReadSuccessLocation6
localBoardReadSuccess 7 = localBoardReadSuccessLocation7
localBoardReadSuccess 8 = localBoardReadSuccessLocation8
localBoardReadSuccess 9 = localBoardReadSuccessLocation9
localBoardReadSuccess 10 = localBoardReadSuccessLocation10
localBoardReadSuccess 11 = localBoardReadSuccessLocation11
localBoardReadSuccess 12 = localBoardReadSuccessLocation12
localBoardReadSuccess 13 = localBoardReadSuccessLocation13
localBoardReadSuccess _ = error "read_success illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBatteryLowWarning :: Bool -> Bool
checkValueBoardBatteryLowWarning value = value

checkValueBoardBbFlsWarning :: Bool -> Bool
checkValueBoardBbFlsWarning value = value

checkValueBoardBbGeofenceWarning :: Bool -> Bool
checkValueBoardBbGeofenceWarning value = value

checkValueBoardBbHomeReached :: Bool -> Bool
checkValueBoardBbHomeReached value = value

checkValueBoardBbMission :: String -> String
checkValueBoardBbMission "waypoint_following" = "waypoint_following"
checkValueBoardBbMission "e_stop" = "e_stop"
checkValueBoardBbMission "pipe_following" = "pipe_following"
checkValueBoardBbMission _ = error "boardBbMission illegal value"

checkValueBoardBbObstacleWarning :: Bool -> Bool
checkValueBoardBbObstacleWarning value = value

checkValueBoardBbPipeLostWarning :: Bool -> Bool
checkValueBoardBbPipeLostWarning value = value

checkValueBoardBbPipeMappingEnable :: Bool -> Bool
checkValueBoardBbPipeMappingEnable value = value

checkValueBoardBbRthWarning :: Bool -> Bool
checkValueBoardBbRthWarning value = value

checkValueBoardBbSensorFailureWarning :: Bool -> Bool
checkValueBoardBbSensorFailureWarning value = value

checkValueBoardCmHsdInput :: String -> String
checkValueBoardCmHsdInput "cm_surface_task" = "cm_surface_task"
checkValueBoardCmHsdInput "cm_rth_task" = "cm_rth_task"
checkValueBoardCmHsdInput "cm_loiter_task" = "cm_loiter_task"
checkValueBoardCmHsdInput "cm_obstacle_avoidance_task" = "cm_obstacle_avoidance_task"
checkValueBoardCmHsdInput "cm_tracking_task" = "cm_tracking_task"
checkValueBoardCmHsdInput "cm_waypoint_task" = "cm_waypoint_task"
checkValueBoardCmHsdInput _ = error "boardCmHsdInput illegal value"

checkValueBoardDdXyAxisDegradation :: Bool -> Bool
checkValueBoardDdXyAxisDegradation value = value

checkValueBoardDdZAxisWarning :: Bool -> Bool
checkValueBoardDdZAxisWarning value = value

checkValueBoardEmergencyStopWarning :: Bool -> Bool
checkValueBoardEmergencyStopWarning value = value

checkValueBoardHSDOut :: String -> String
checkValueBoardHSDOut "uuv_min_speed" = "uuv_min_speed"
checkValueBoardHSDOut "uuv_max_speed" = "uuv_max_speed"
checkValueBoardHSDOut _ = error "boardHSDOut illegal value"

checkValueBoardLecDdAmWarning :: Bool -> Bool
checkValueBoardLecDdAmWarning value = value

checkValueBoardLec2AmLSpeedWarning :: Bool -> Bool
checkValueBoardLec2AmLSpeedWarning value = value

checkValueBoardLec2AmLPipeWarning :: Bool -> Bool
checkValueBoardLec2AmLPipeWarning value = value

checkValueBoardLec2AmRSpeedWarning :: Bool -> Bool
checkValueBoardLec2AmRSpeedWarning value = value

checkValueBoardLec2AmRPipeWarning :: Bool -> Bool
checkValueBoardLec2AmRPipeWarning value = value

checkValueBoardNextMission :: Bool -> Bool
checkValueBoardNextMission value = value

checkValueBoardPipeMappingEnable :: Bool -> Bool
checkValueBoardPipeMappingEnable value = value

checkValueBoardObstacleStandoffWarning :: Bool -> Bool
checkValueBoardObstacleStandoffWarning value = value

checkValueBoardRtreachLongTermWarning :: Bool -> Bool
checkValueBoardRtreachLongTermWarning value = value

checkValueBoardRtreachObstacleWarning :: Bool -> Bool
checkValueBoardRtreachObstacleWarning value = value

checkValueBoardRtreachWarning :: Bool -> Bool
checkValueBoardRtreachWarning value = value

checkValueBoardFinishedMissions :: Bool -> Bool
checkValueBoardFinishedMissions value = value

checkValueBoardDdOutput :: String -> String
checkValueBoardDdOutput "safe" = "safe"
checkValueBoardDdOutput "xy_warn" = "xy_warn"
checkValueBoardDdOutput "z_warn" = "z_warn"
checkValueBoardDdOutput _ = error "boardDdOutput illegal value"

checkValueBoardBLUEROVSURFACED :: Bool -> Bool
checkValueBoardBLUEROVSURFACED value = value

checkValueLocalBoardReadSuccess :: Bool -> Bool
checkValueLocalBoardReadSuccess value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardReadSuccess :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccess 2 = updateLocalBoardReadSuccessLocation2
updateLocalBoardReadSuccess 3 = updateLocalBoardReadSuccessLocation3
updateLocalBoardReadSuccess 4 = updateLocalBoardReadSuccessLocation4
updateLocalBoardReadSuccess 5 = updateLocalBoardReadSuccessLocation5
updateLocalBoardReadSuccess 6 = updateLocalBoardReadSuccessLocation6
updateLocalBoardReadSuccess 7 = updateLocalBoardReadSuccessLocation7
updateLocalBoardReadSuccess 8 = updateLocalBoardReadSuccessLocation8
updateLocalBoardReadSuccess 9 = updateLocalBoardReadSuccessLocation9
updateLocalBoardReadSuccess 10 = updateLocalBoardReadSuccessLocation10
updateLocalBoardReadSuccess 11 = updateLocalBoardReadSuccessLocation11
updateLocalBoardReadSuccess 12 = updateLocalBoardReadSuccessLocation12
updateLocalBoardReadSuccess 13 = updateLocalBoardReadSuccessLocation13
updateLocalBoardReadSuccess _ = error "localBoardReadSuccess illegal local reference"
updateBoardBatteryLowWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBatteryLowWarning blackboard value = blackboard { boardBatteryLowWarning = (checkValueBoardBatteryLowWarning value)}
updateBoardBbFlsWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbFlsWarning blackboard value = blackboard { boardBbFlsWarning = (checkValueBoardBbFlsWarning value)}
updateBoardBbGeofenceWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbGeofenceWarning blackboard value = blackboard { boardBbGeofenceWarning = (checkValueBoardBbGeofenceWarning value)}
updateBoardBbHomeReached :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbHomeReached blackboard value = blackboard { boardBbHomeReached = (checkValueBoardBbHomeReached value)}
updateBoardBbMission :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBbMission blackboard value = blackboard { boardBbMission = (checkValueBoardBbMission value)}
updateBoardBbObstacleWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbObstacleWarning blackboard value = blackboard { boardBbObstacleWarning = (checkValueBoardBbObstacleWarning value)}
updateBoardBbPipeLostWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbPipeLostWarning blackboard value = blackboard { boardBbPipeLostWarning = (checkValueBoardBbPipeLostWarning value)}
updateBoardBbPipeMappingEnable :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbPipeMappingEnable blackboard value = blackboard { boardBbPipeMappingEnable = (checkValueBoardBbPipeMappingEnable value)}
updateBoardBbRthWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbRthWarning blackboard value = blackboard { boardBbRthWarning = (checkValueBoardBbRthWarning value)}
updateBoardBbSensorFailureWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBbSensorFailureWarning blackboard value = blackboard { boardBbSensorFailureWarning = (checkValueBoardBbSensorFailureWarning value)}
updateBoardCmHsdInput :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardCmHsdInput blackboard value = blackboard { boardCmHsdInput = (checkValueBoardCmHsdInput value)}
updateBoardDdXyAxisDegradation :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardDdXyAxisDegradation blackboard value = blackboard { boardDdXyAxisDegradation = (checkValueBoardDdXyAxisDegradation value)}
updateBoardDdZAxisWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardDdZAxisWarning blackboard value = blackboard { boardDdZAxisWarning = (checkValueBoardDdZAxisWarning value)}
updateBoardEmergencyStopWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardEmergencyStopWarning blackboard value = blackboard { boardEmergencyStopWarning = (checkValueBoardEmergencyStopWarning value)}
updateBoardHSDOut :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardHSDOut blackboard value = blackboard { boardHSDOut = (checkValueBoardHSDOut value)}
updateBoardLecDdAmWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardLecDdAmWarning blackboard value = blackboard { boardLecDdAmWarning = (checkValueBoardLecDdAmWarning value)}
updateBoardLec2AmLSpeedWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardLec2AmLSpeedWarning blackboard value = blackboard { boardLec2AmLSpeedWarning = (checkValueBoardLec2AmLSpeedWarning value)}
updateBoardLec2AmLPipeWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardLec2AmLPipeWarning blackboard value = blackboard { boardLec2AmLPipeWarning = (checkValueBoardLec2AmLPipeWarning value)}
updateBoardLec2AmRSpeedWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardLec2AmRSpeedWarning blackboard value = blackboard { boardLec2AmRSpeedWarning = (checkValueBoardLec2AmRSpeedWarning value)}
updateBoardLec2AmRPipeWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardLec2AmRPipeWarning blackboard value = blackboard { boardLec2AmRPipeWarning = (checkValueBoardLec2AmRPipeWarning value)}
updateBoardNextMission :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardNextMission blackboard value = blackboard { boardNextMission = (checkValueBoardNextMission value)}
updateBoardPipeMappingEnable :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardPipeMappingEnable blackboard value = blackboard { boardPipeMappingEnable = (checkValueBoardPipeMappingEnable value)}
updateBoardObstacleStandoffWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardObstacleStandoffWarning blackboard value = blackboard { boardObstacleStandoffWarning = (checkValueBoardObstacleStandoffWarning value)}
updateBoardRtreachLongTermWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardRtreachLongTermWarning blackboard value = blackboard { boardRtreachLongTermWarning = (checkValueBoardRtreachLongTermWarning value)}
updateBoardRtreachObstacleWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardRtreachObstacleWarning blackboard value = blackboard { boardRtreachObstacleWarning = (checkValueBoardRtreachObstacleWarning value)}
updateBoardRtreachWarning :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardRtreachWarning blackboard value = blackboard { boardRtreachWarning = (checkValueBoardRtreachWarning value)}
updateBoardFinishedMissions :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardFinishedMissions blackboard value = blackboard { boardFinishedMissions = (checkValueBoardFinishedMissions value)}
updateBoardDdOutput :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardDdOutput blackboard value = blackboard { boardDdOutput = (checkValueBoardDdOutput value)}
updateBoardBLUEROVSURFACED :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBLUEROVSURFACED blackboard value = blackboard { boardBLUEROVSURFACED = (checkValueBoardBLUEROVSURFACED value)}
updateLocalBoardReadSuccessLocation2 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation2 blackboard value = blackboard { localBoardReadSuccessLocation2 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation3 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation3 blackboard value = blackboard { localBoardReadSuccessLocation3 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation4 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation4 blackboard value = blackboard { localBoardReadSuccessLocation4 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation5 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation5 blackboard value = blackboard { localBoardReadSuccessLocation5 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation6 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation6 blackboard value = blackboard { localBoardReadSuccessLocation6 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation7 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation7 blackboard value = blackboard { localBoardReadSuccessLocation7 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation8 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation8 blackboard value = blackboard { localBoardReadSuccessLocation8 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation9 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation9 blackboard value = blackboard { localBoardReadSuccessLocation9 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation10 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation10 blackboard value = blackboard { localBoardReadSuccessLocation10 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation11 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation11 blackboard value = blackboard { localBoardReadSuccessLocation11 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation12 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation12 blackboard value = blackboard { localBoardReadSuccessLocation12 = (checkValueLocalBoardReadSuccess value)}
updateLocalBoardReadSuccessLocation13 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardReadSuccessLocation13 blackboard value = blackboard { localBoardReadSuccessLocation13 = (checkValueLocalBoardReadSuccess value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 localNewValReadSuccessLocation9 localNewValReadSuccessLocation10 localNewValReadSuccessLocation11 localNewValReadSuccessLocation12 localNewValReadSuccessLocation13  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen41
    partialBlackboardBatteryLowWarning = BTreeBlackboard newSereneGenerator True True True True " " True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBatteryLowWarning :: StdGen -> (Bool, StdGen)
    initValBatteryLowWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBatteryLowWarning

    (newValBatteryLowWarning, tempGen1) = initValBatteryLowWarning tempGen0

    partialBlackboardBbFlsWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning True True True " " True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbFlsWarning :: StdGen -> (Bool, StdGen)
    initValBbFlsWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbFlsWarning

    (newValBbFlsWarning, tempGen2) = initValBbFlsWarning tempGen1

    partialBlackboardBbGeofenceWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning True True " " True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbGeofenceWarning :: StdGen -> (Bool, StdGen)
    initValBbGeofenceWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbGeofenceWarning

    (newValBbGeofenceWarning, tempGen3) = initValBbGeofenceWarning tempGen2

    partialBlackboardBbHomeReached = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning True " " True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbHomeReached :: StdGen -> (Bool, StdGen)
    initValBbHomeReached curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbHomeReached

    (newValBbHomeReached, tempGen4) = initValBbHomeReached tempGen3

    partialBlackboardBbMission = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached " " True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbMission :: StdGen -> (String, StdGen)
    initValBbMission curGen = ("waypoint_following", curGen)
      where
        blackboard = partialBlackboardBbMission

    (newValBbMission, tempGen5) = initValBbMission tempGen4

    partialBlackboardBbObstacleWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission True True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbObstacleWarning :: StdGen -> (Bool, StdGen)
    initValBbObstacleWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbObstacleWarning

    (newValBbObstacleWarning, tempGen6) = initValBbObstacleWarning tempGen5

    partialBlackboardBbPipeLostWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning True True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbPipeLostWarning :: StdGen -> (Bool, StdGen)
    initValBbPipeLostWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbPipeLostWarning

    (newValBbPipeLostWarning, tempGen7) = initValBbPipeLostWarning tempGen6

    partialBlackboardBbPipeMappingEnable = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning True True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbPipeMappingEnable :: StdGen -> (Bool, StdGen)
    initValBbPipeMappingEnable curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbPipeMappingEnable

    (newValBbPipeMappingEnable, tempGen8) = initValBbPipeMappingEnable tempGen7

    partialBlackboardBbRthWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable True True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbRthWarning :: StdGen -> (Bool, StdGen)
    initValBbRthWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbRthWarning

    (newValBbRthWarning, tempGen9) = initValBbRthWarning tempGen8

    partialBlackboardBbSensorFailureWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning True " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValBbSensorFailureWarning :: StdGen -> (Bool, StdGen)
    initValBbSensorFailureWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardBbSensorFailureWarning

    (newValBbSensorFailureWarning, tempGen10) = initValBbSensorFailureWarning tempGen9

    partialBlackboardCmHsdInput = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning " " True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValCmHsdInput :: StdGen -> (String, StdGen)
    initValCmHsdInput curGen = ("cm_loiter_task", curGen)
      where
        blackboard = partialBlackboardCmHsdInput

    (newValCmHsdInput, tempGen11) = initValCmHsdInput tempGen10

    partialBlackboardDdXyAxisDegradation = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput True True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValDdXyAxisDegradation :: StdGen -> (Bool, StdGen)
    initValDdXyAxisDegradation curGen = (False, curGen)
      where
        blackboard = partialBlackboardDdXyAxisDegradation

    (newValDdXyAxisDegradation, tempGen12) = initValDdXyAxisDegradation tempGen11

    partialBlackboardDdZAxisWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation True True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValDdZAxisWarning :: StdGen -> (Bool, StdGen)
    initValDdZAxisWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardDdZAxisWarning

    (newValDdZAxisWarning, tempGen13) = initValDdZAxisWarning tempGen12

    partialBlackboardEmergencyStopWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning True " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValEmergencyStopWarning :: StdGen -> (Bool, StdGen)
    initValEmergencyStopWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardEmergencyStopWarning

    (newValEmergencyStopWarning, tempGen14) = initValEmergencyStopWarning tempGen13

    partialBlackboardHSDOut = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning " " True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValHSDOut :: StdGen -> (String, StdGen)
    initValHSDOut curGen = ("uuv_max_speed", curGen)
      where
        blackboard = partialBlackboardHSDOut

    (newValHSDOut, tempGen15) = initValHSDOut tempGen14

    partialBlackboardLecDdAmWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut True True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValLecDdAmWarning :: StdGen -> (Bool, StdGen)
    initValLecDdAmWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardLecDdAmWarning

    (newValLecDdAmWarning, tempGen16) = initValLecDdAmWarning tempGen15

    partialBlackboardLec2AmLSpeedWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning True True True True True True True True True True True " " True True True True True True True True True True True True True
    initValLec2AmLSpeedWarning :: StdGen -> (Bool, StdGen)
    initValLec2AmLSpeedWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardLec2AmLSpeedWarning

    (newValLec2AmLSpeedWarning, tempGen17) = initValLec2AmLSpeedWarning tempGen16

    partialBlackboardLec2AmLPipeWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning True True True True True True True True True True " " True True True True True True True True True True True True True
    initValLec2AmLPipeWarning :: StdGen -> (Bool, StdGen)
    initValLec2AmLPipeWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardLec2AmLPipeWarning

    (newValLec2AmLPipeWarning, tempGen18) = initValLec2AmLPipeWarning tempGen17

    partialBlackboardLec2AmRSpeedWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning True True True True True True True True True " " True True True True True True True True True True True True True
    initValLec2AmRSpeedWarning :: StdGen -> (Bool, StdGen)
    initValLec2AmRSpeedWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardLec2AmRSpeedWarning

    (newValLec2AmRSpeedWarning, tempGen19) = initValLec2AmRSpeedWarning tempGen18

    partialBlackboardLec2AmRPipeWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning True True True True True True True True " " True True True True True True True True True True True True True
    initValLec2AmRPipeWarning :: StdGen -> (Bool, StdGen)
    initValLec2AmRPipeWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardLec2AmRPipeWarning

    (newValLec2AmRPipeWarning, tempGen20) = initValLec2AmRPipeWarning tempGen19

    partialBlackboardNextMission = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning True True True True True True True " " True True True True True True True True True True True True True
    initValNextMission :: StdGen -> (Bool, StdGen)
    initValNextMission curGen = (False, curGen)
      where
        blackboard = partialBlackboardNextMission

    (newValNextMission, tempGen21) = initValNextMission tempGen20

    partialBlackboardPipeMappingEnable = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission True True True True True True " " True True True True True True True True True True True True True
    initValPipeMappingEnable :: StdGen -> (Bool, StdGen)
    initValPipeMappingEnable curGen = (False, curGen)
      where
        blackboard = partialBlackboardPipeMappingEnable

    (newValPipeMappingEnable, tempGen22) = initValPipeMappingEnable tempGen21

    partialBlackboardObstacleStandoffWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable True True True True True " " True True True True True True True True True True True True True
    initValObstacleStandoffWarning :: StdGen -> (Bool, StdGen)
    initValObstacleStandoffWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardObstacleStandoffWarning

    (newValObstacleStandoffWarning, tempGen23) = initValObstacleStandoffWarning tempGen22

    partialBlackboardRtreachLongTermWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning True True True True " " True True True True True True True True True True True True True
    initValRtreachLongTermWarning :: StdGen -> (Bool, StdGen)
    initValRtreachLongTermWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardRtreachLongTermWarning

    (newValRtreachLongTermWarning, tempGen24) = initValRtreachLongTermWarning tempGen23

    partialBlackboardRtreachObstacleWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning True True True " " True True True True True True True True True True True True True
    initValRtreachObstacleWarning :: StdGen -> (Bool, StdGen)
    initValRtreachObstacleWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardRtreachObstacleWarning

    (newValRtreachObstacleWarning, tempGen25) = initValRtreachObstacleWarning tempGen24

    partialBlackboardRtreachWarning = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning True True " " True True True True True True True True True True True True True
    initValRtreachWarning :: StdGen -> (Bool, StdGen)
    initValRtreachWarning curGen = (False, curGen)
      where
        blackboard = partialBlackboardRtreachWarning

    (newValRtreachWarning, tempGen26) = initValRtreachWarning tempGen25

    partialBlackboardFinishedMissions = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning True " " True True True True True True True True True True True True True
    initValFinishedMissions :: StdGen -> (Bool, StdGen)
    initValFinishedMissions curGen = (False, curGen)
      where
        blackboard = partialBlackboardFinishedMissions

    (newValFinishedMissions, tempGen27) = initValFinishedMissions tempGen26

    partialBlackboardDdOutput = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions " " True True True True True True True True True True True True True
    initValDdOutput :: StdGen -> (String, StdGen)
    initValDdOutput curGen = ("safe", curGen)
      where
        blackboard = partialBlackboardDdOutput

    (newValDdOutput, tempGen28) = initValDdOutput tempGen27

    partialBlackboardBLUEROVSURFACED = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput True True True True True True True True True True True True True
    initValBLUEROVSURFACED :: StdGen -> (Bool, StdGen)
    initValBLUEROVSURFACED curGen = (False, curGen)
      where
        blackboard = partialBlackboardBLUEROVSURFACED

    (newValBLUEROVSURFACED, tempGen29) = initValBLUEROVSURFACED tempGen28

    partialBlackboardReadSuccessLocation2 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED True True True True True True True True True True True True
    localInitValReadSuccessLocation2 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation2 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation2
        nodeLocation = 2

    (localNewValReadSuccessLocation2, tempGen30) = localInitValReadSuccessLocation2 tempGen29

    partialBlackboardReadSuccessLocation3 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 True True True True True True True True True True True
    localInitValReadSuccessLocation3 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation3 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation3
        nodeLocation = 3

    (localNewValReadSuccessLocation3, tempGen31) = localInitValReadSuccessLocation3 tempGen30

    partialBlackboardReadSuccessLocation4 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 True True True True True True True True True True
    localInitValReadSuccessLocation4 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation4 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation4
        nodeLocation = 4

    (localNewValReadSuccessLocation4, tempGen32) = localInitValReadSuccessLocation4 tempGen31

    partialBlackboardReadSuccessLocation5 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 True True True True True True True True True
    localInitValReadSuccessLocation5 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation5 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation5
        nodeLocation = 5

    (localNewValReadSuccessLocation5, tempGen33) = localInitValReadSuccessLocation5 tempGen32

    partialBlackboardReadSuccessLocation6 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 True True True True True True True True
    localInitValReadSuccessLocation6 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation6 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation6
        nodeLocation = 6

    (localNewValReadSuccessLocation6, tempGen34) = localInitValReadSuccessLocation6 tempGen33

    partialBlackboardReadSuccessLocation7 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 True True True True True True True
    localInitValReadSuccessLocation7 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation7 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation7
        nodeLocation = 7

    (localNewValReadSuccessLocation7, tempGen35) = localInitValReadSuccessLocation7 tempGen34

    partialBlackboardReadSuccessLocation8 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 True True True True True True
    localInitValReadSuccessLocation8 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation8 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation8
        nodeLocation = 8

    (localNewValReadSuccessLocation8, tempGen36) = localInitValReadSuccessLocation8 tempGen35

    partialBlackboardReadSuccessLocation9 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 True True True True True
    localInitValReadSuccessLocation9 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation9 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation9
        nodeLocation = 9

    (localNewValReadSuccessLocation9, tempGen37) = localInitValReadSuccessLocation9 tempGen36

    partialBlackboardReadSuccessLocation10 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 localNewValReadSuccessLocation9 True True True True
    localInitValReadSuccessLocation10 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation10 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation10
        nodeLocation = 10

    (localNewValReadSuccessLocation10, tempGen38) = localInitValReadSuccessLocation10 tempGen37

    partialBlackboardReadSuccessLocation11 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 localNewValReadSuccessLocation9 localNewValReadSuccessLocation10 True True True
    localInitValReadSuccessLocation11 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation11 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation11
        nodeLocation = 11

    (localNewValReadSuccessLocation11, tempGen39) = localInitValReadSuccessLocation11 tempGen38

    partialBlackboardReadSuccessLocation12 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 localNewValReadSuccessLocation9 localNewValReadSuccessLocation10 localNewValReadSuccessLocation11 True True
    localInitValReadSuccessLocation12 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation12 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation12
        nodeLocation = 12

    (localNewValReadSuccessLocation12, tempGen40) = localInitValReadSuccessLocation12 tempGen39

    partialBlackboardReadSuccessLocation13 = BTreeBlackboard newSereneGenerator newValBatteryLowWarning newValBbFlsWarning newValBbGeofenceWarning newValBbHomeReached newValBbMission newValBbObstacleWarning newValBbPipeLostWarning newValBbPipeMappingEnable newValBbRthWarning newValBbSensorFailureWarning newValCmHsdInput newValDdXyAxisDegradation newValDdZAxisWarning newValEmergencyStopWarning newValHSDOut newValLecDdAmWarning newValLec2AmLSpeedWarning newValLec2AmLPipeWarning newValLec2AmRSpeedWarning newValLec2AmRPipeWarning newValNextMission newValPipeMappingEnable newValObstacleStandoffWarning newValRtreachLongTermWarning newValRtreachObstacleWarning newValRtreachWarning newValFinishedMissions newValDdOutput newValBLUEROVSURFACED localNewValReadSuccessLocation2 localNewValReadSuccessLocation3 localNewValReadSuccessLocation4 localNewValReadSuccessLocation5 localNewValReadSuccessLocation6 localNewValReadSuccessLocation7 localNewValReadSuccessLocation8 localNewValReadSuccessLocation9 localNewValReadSuccessLocation10 localNewValReadSuccessLocation11 localNewValReadSuccessLocation12 True
    localInitValReadSuccessLocation13 :: StdGen -> (Bool, StdGen)
    localInitValReadSuccessLocation13 curGen = (False, curGen)
      where
        blackboard = partialBlackboardReadSuccessLocation13
        nodeLocation = 13

    (localNewValReadSuccessLocation13, tempGen41) = localInitValReadSuccessLocation13 tempGen40


