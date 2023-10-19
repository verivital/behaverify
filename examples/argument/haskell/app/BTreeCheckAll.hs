module BTreeCheckAll where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCreatorCheckAll :: String -> String -> Integer -> Integer -> Bool -> Bool -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
bTreeFunctionCreatorCheckAll enum0 enum1 int0 int1 bool0 bool1 = bTreeFunctionCheckAll
  where
    bTreeFunctionCheckAll :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
    bTreeFunctionCheckAll _ nodeLocation _ _ _ _ blackboard environment futureChanges
      | ( (enum0 == enum1)&&((int0 == int1) && (bool0 == bool1))) = (Success, [], [], blackboard, environment, futureChanges)
      | otherwise = (Failure, [], [], blackboard, environment, futureChanges)