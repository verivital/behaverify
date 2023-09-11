module BTreeCheckBoolean where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorCheckBoolean :: Bool -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorCheckBoolean arg_name = bTreeFunctionCheckBoolean
  where
    bTreeFunctionCheckBoolean :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionCheckBoolean _ nodeLocation _ _ _ _ blackboard environment futureChanges
      | arg_name = (Success, [], [], blackboard, environment, futureChanges)
      | otherwise = (Failure, [], [], blackboard, environment, futureChanges)