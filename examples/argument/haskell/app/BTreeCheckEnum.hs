module BTreeCheckEnum where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorCheckEnum :: String -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorCheckEnum arg_name = bTreeFunctionCheckEnum
  where
    bTreeFunctionCheckEnum :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionCheckEnum _ nodeLocation _ _ _ _ blackboard environment futureChanges
      | (arg_name == "Hello") = (Success, [], [], blackboard, environment, futureChanges)
      | otherwise = (Failure, [], [], blackboard, environment, futureChanges)