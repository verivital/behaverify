module BTreeGoForward where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionGoForward :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionGoForward _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | ((((boardForward blackboard) + (envX environment)) >= 0) && ((((boardForward blackboard) + (envX environment)) <= 18) && (((envActiveHole blackboard environment) == (-1)) || ((envActiveHole blackboard environment) == (envY environment))))) = (blackboard, updateEnvX environment ((envX environment) + (boardForward blackboard)))
      | otherwise = (blackboard, updateEnvX environment (envX environment))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
