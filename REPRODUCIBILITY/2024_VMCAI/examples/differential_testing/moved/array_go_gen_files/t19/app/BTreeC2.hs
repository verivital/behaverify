module BTreeC2 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionC2 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionC2 _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((abs (min 97 (-80))) == (- ((sereneCOUNT ((-4) >= (boardBlVAR0 blackboard)) ((boardBlVAR0 blackboard) >= (boardBlVAR0 blackboard))) + (sereneCOUNT False (sereneXNOR False False))))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)