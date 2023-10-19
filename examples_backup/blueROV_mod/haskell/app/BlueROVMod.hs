module BlueROVMod where
import BehaviorTreeCore
import BTreeEmergencyStopFs
import BTreeObstacleStandoffFs
import BTreeIsReallocationRequested
import BTreeCheckLec2amLs
import BTreeCheckLec2amRs
import BTreeCheckGeofence
import BTreeCheckRth
import BTreeCheckSurface
import BTreeCheckPipeLost
import BTreeCheckSensorFailure
import BTreeBatteryLowFs
import BTreeIsTrackPipeMissionRequested
import BTreeIsWaypointRequested
import BTreeObstacleAvoidanceRequired
import BTreeFls2bb
import BTreeFlsWarning2bb
import BTreeBattery2bb
import BTreeRth2bb
import BTreeGeofence2bb
import BTreeLec2AmL2bb
import BTreeLec2AmR2bb
import BTreePipeLost2bb
import BTreeSensorFailure2bb
import BTreeWaypointsCompleted2bb
import BTreeHome2bb
import BTreeRtreach2bb
import BTreeEmergencyStopTask
import BTreeSurfaceTask
import BTreeRthTask
import BTreeLoiterTask
import BTreeObstacleAvoidance
import BTreeMissionServer
import BTreeNextMissionNode
import BTreeSpeedMaxTask
import BTreeSpeedMinTask
import BTreeTrackingTask
import BTreeWaypointTask
import BTreeReallocateTask
import BTreeDdLecTask
import BTreePublishHSDCommand
import BTreeFailureNode
import BTreeCheckWaypointsCompleted
bTreeNodeBattery2bb = BTreeNode bTreeFunctionBattery2bb [] 2
bTreeNodeRth2bb = BTreeNode bTreeFunctionRth2bb [] 3
bTreeNodeGeofence2bb = BTreeNode bTreeFunctionGeofence2bb [] 4
bTreeNodeLec2AmR2bb = BTreeNode bTreeFunctionLec2AmR2bb [] 5
bTreeNodeLec2AmL2bb = BTreeNode bTreeFunctionLec2AmL2bb [] 6
bTreeNodePipeLost2bb = BTreeNode bTreeFunctionPipeLost2bb [] 7
bTreeNodeSensorFailure2bb = BTreeNode bTreeFunctionSensorFailure2bb [] 8
bTreeNodeWaypointsCompleted2bb = BTreeNode bTreeFunctionWaypointsCompleted2bb [] 9
bTreeNodeFls2bb = BTreeNode bTreeFunctionFls2bb [] 10
bTreeNodeFlsWarning2bb = BTreeNode bTreeFunctionFlsWarning2bb [] 11
bTreeNodeRtreach2bb = BTreeNode bTreeFunctionRtreach2bb [] 12
bTreeNodeHome2bb = BTreeNode bTreeFunctionHome2bb [] 13
bTreeNodeTopics2bb = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeBattery2bb, bTreeNodeRth2bb, bTreeNodeGeofence2bb, bTreeNodeLec2AmR2bb, bTreeNodeLec2AmL2bb, bTreeNodePipeLost2bb, bTreeNodeSensorFailure2bb, bTreeNodeWaypointsCompleted2bb, bTreeNodeFls2bb, bTreeNodeFlsWarning2bb, bTreeNodeRtreach2bb, bTreeNodeHome2bb] 1
bTreeNodeDdLecTask = BTreeNode bTreeFunctionDdLecTask [] 15
bTreeNodeIsReallocationRequested = BTreeNode bTreeFunctionIsReallocationRequested [] 18
bTreeNodeReallocateTask = BTreeNode bTreeFunctionReallocateTask [] 19
bTreeNodeEmergencyStopCheck = BTreeNode selectorFunc [bTreeNodeIsReallocationRequested, bTreeNodeReallocateTask] 17
bTreeNodeEmergencyStopCheckSIF = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeEmergencyStopCheck] 16
bTreeNodeDdTasks = BTreeNode selectorFunc [bTreeNodeDdLecTask, bTreeNodeEmergencyStopCheckSIF] 14
bTreeNodeIsWaypointRequested = BTreeNode bTreeFunctionIsWaypointRequested [] 23
bTreeNodeCheckWaypointsCompleted = BTreeNode bTreeFunctionCheckWaypointsCompleted [] 24
bTreeNodeWaypointMissionEnd = BTreeNode sequenceFunc [bTreeNodeIsWaypointRequested, bTreeNodeCheckWaypointsCompleted] 22
bTreeNodeIsTrackPipeMissionRequested = BTreeNode bTreeFunctionIsTrackPipeMissionRequested [] 26
bTreeNodeFailureNode = BTreeNode bTreeFunctionFailureNode [] 27
bTreeNodePipeTrackingMisisonEnd = BTreeNode sequenceFunc [bTreeNodeIsTrackPipeMissionRequested, bTreeNodeFailureNode] 25
bTreeNodeConfirmMissionEnded = BTreeNode selectorFunc [bTreeNodeWaypointMissionEnd, bTreeNodePipeTrackingMisisonEnd] 21
bTreeNodeNextMissionNode = BTreeNode bTreeFunctionNextMissionNode [] 28
bTreeNodeMissionEnd = BTreeNode sequenceFunc [bTreeNodeConfirmMissionEnded, bTreeNodeNextMissionNode] 20
bTreeNodeMissionServer = BTreeNode bTreeFunctionMissionServer [] 29
bTreeNodeObstacleAvoidance = BTreeNode bTreeFunctionObstacleAvoidance [] 30
bTreeNodeEmergencyStopFs = BTreeNode bTreeFunctionEmergencyStopFs [] 34
bTreeNodeEmergencyStopTask = BTreeNode bTreeFunctionEmergencyStopTask [] 36
bTreeNodeSurfaceTask = BTreeNode bTreeFunctionSurfaceTask [] 37
bTreeNodeEmergencyStopTasks = BTreeNode sequenceFunc [bTreeNodeEmergencyStopTask, bTreeNodeSurfaceTask] 35
bTreeNodeEmergencyStopCheck_1 = BTreeNode selectorFunc [bTreeNodeEmergencyStopFs, bTreeNodeEmergencyStopTasks] 33
bTreeNodeEmergencyStopCheckSIF_1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeEmergencyStopCheck_1] 32
bTreeNodeObstacleAvoidanceRequired = BTreeNode bTreeFunctionObstacleAvoidanceRequired [] 38
bTreeNodeBatteryLowFs = BTreeNode bTreeFunctionBatteryLowFs [] 41
bTreeNodeCheckSensorFailure = BTreeNode bTreeFunctionCheckSensorFailure [] 42
bTreeNodeObstacleStandoffFs = BTreeNode bTreeFunctionObstacleStandoffFs [] 43
bTreeNodeCheckRth = BTreeNode bTreeFunctionCheckRth [] 46
bTreeNodeCheckGeofence = BTreeNode bTreeFunctionCheckGeofence [] 47
bTreeNodeRthNeeded = BTreeNode selectorFunc [bTreeNodeCheckRth, bTreeNodeCheckGeofence] 45
bTreeNodeCheckSurface = BTreeNode bTreeFunctionCheckSurface [] 48
bTreeNodeRthSurface = BTreeNode sequenceFunc [bTreeNodeRthNeeded, bTreeNodeCheckSurface] 44
bTreeNodeFailsafeTriggered = BTreeNode selectorFunc [bTreeNodeBatteryLowFs, bTreeNodeCheckSensorFailure, bTreeNodeObstacleStandoffFs, bTreeNodeRthSurface] 40
bTreeNodeSurfaceTask_1 = BTreeNode bTreeFunctionSurfaceTask [] 49
bTreeNodeFailsafeSurface = BTreeNode sequenceFunc [bTreeNodeFailsafeTriggered, bTreeNodeSurfaceTask_1] 39
bTreeNodeCheckRth_1 = BTreeNode bTreeFunctionCheckRth [] 52
bTreeNodeCheckGeofence_1 = BTreeNode bTreeFunctionCheckGeofence [] 53
bTreeNodeRthNeeded_1 = BTreeNode selectorFunc [bTreeNodeCheckRth_1, bTreeNodeCheckGeofence_1] 51
bTreeNodeRthTask = BTreeNode bTreeFunctionRthTask [] 54
bTreeNodeRth = BTreeNode sequenceFunc [bTreeNodeRthNeeded_1, bTreeNodeRthTask] 50
bTreeNodeCheckPipeLost = BTreeNode bTreeFunctionCheckPipeLost [] 57
bTreeNodeLoiterTask = BTreeNode bTreeFunctionLoiterTask [] 58
bTreeNodePipeLostSelector = BTreeNode selectorFunc [bTreeNodeCheckPipeLost, bTreeNodeLoiterTask] 56
bTreeNodePipeLostSelectorSIF = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodePipeLostSelector] 55
bTreeNodeIsTrackPipeMissionRequested_1 = BTreeNode bTreeFunctionIsTrackPipeMissionRequested [] 60
bTreeNodeTrackingTask = BTreeNode bTreeFunctionTrackingTask [] 61
bTreeNodeCheckLec2amLs = BTreeNode bTreeFunctionCheckLec2amLs [] 65
bTreeNodeCheckLec2amRs = BTreeNode bTreeFunctionCheckLec2amRs [] 66
bTreeNodeSpeedWarning = BTreeNode selectorFunc [bTreeNodeCheckLec2amLs, bTreeNodeCheckLec2amRs] 64
bTreeNodeSpeedMinTask = BTreeNode bTreeFunctionSpeedMinTask [] 67
bTreeNodeSpeedMin = BTreeNode sequenceFunc [bTreeNodeSpeedWarning, bTreeNodeSpeedMinTask] 63
bTreeNodeSpeedMaxTask = BTreeNode bTreeFunctionSpeedMaxTask [] 68
bTreeNodeLec2amSpeedCmd = BTreeNode selectorFunc [bTreeNodeSpeedMin, bTreeNodeSpeedMaxTask] 62
bTreeNodeTrackPipeMission = BTreeNode sequenceFunc [bTreeNodeIsTrackPipeMissionRequested_1, bTreeNodeTrackingTask, bTreeNodeLec2amSpeedCmd] 59
bTreeNodeIsWaypointRequested_1 = BTreeNode bTreeFunctionIsWaypointRequested [] 70
bTreeNodeWaypointTask = BTreeNode bTreeFunctionWaypointTask [] 71
bTreeNodeWaypointMission = BTreeNode sequenceFunc [bTreeNodeIsWaypointRequested_1, bTreeNodeWaypointTask] 69
bTreeNodeLoiterTask_1 = BTreeNode bTreeFunctionLoiterTask [] 72
bTreeNodePriorities = BTreeNode selectorFunc [bTreeNodeEmergencyStopCheckSIF_1, bTreeNodeObstacleAvoidanceRequired, bTreeNodeFailsafeSurface, bTreeNodeRth, bTreeNodePipeLostSelectorSIF, bTreeNodeTrackPipeMission, bTreeNodeWaypointMission, bTreeNodeLoiterTask_1] 31
bTreeNodePublishHSDCommand = BTreeNode bTreeFunctionPublishHSDCommand [] 73
bTreeNodeBlueROV = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeTopics2bb, bTreeNodeDdTasks, bTreeNodeMissionEnd, bTreeNodeMissionServer, bTreeNodeObstacleAvoidance, bTreeNodePriorities, bTreeNodePublishHSDCommand] 0
