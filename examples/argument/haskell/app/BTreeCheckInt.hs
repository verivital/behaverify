module BTreeCheckInt where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorCheckInt :: Integer -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorCheckInt arg_name = bTreeFunctionCheckInt
  where
    bTreeFunctionCheckInt :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionCheckInt _ nodeLocation _ _ _ _ blackboard environment futureChanges
      | (arg_name == 55) = (Success, [], [], blackboard, environment, futureChanges)
      | otherwise = (Failure, [], [], blackboard, environment, futureChanges)