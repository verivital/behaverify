module BTreeA2 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA2 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA2 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement2 (statement1 (statement0 (blackboard, environment))))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (boardUpdateBlVAR3 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | ((False /= True) /= ((-38) > 5)) = (((-39) > ((min 50 (max (-50) (abs (-2)))))) && False)
          | otherwise = (((min 50 (max (-50) (((min 50 (max (-50) (max 4 4)))) * ((min 50 (max (-50) (max 4 4)))))))) < ((min 50 (max (-50) ((-24) - ((min 50 (max (-50) ( 18+ ( 18+(18 + 18)))))))))))
        defaultValue = (boardBlVAR3 blackboard)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR3 defaultValue [(0, newUpdate0), (1, newUpdate0)]
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (boardUpdateBlVAR2 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | (True == ((-5) <= (-30))) = "yes"
          | (sereneIMPLIES ("yes" == (indexIntoBlVAR2 (max 0 (min 1 (-13))) (boardBlVAR2 blackboard))) (True && (boardBlVAR0 blackboard))) = "yes"
          | otherwise = (boardBlDEFINE5 blackboard)
        defaultValue = (boardBlVAR2 blackboard)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR2 defaultValue [(0, newUpdate0), (1, newUpdate0)]
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (boardUpdateBlVAR3 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0 = (((-30) < 46) && True)
        defaultValue = (boardBlVAR3 blackboard)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR3 defaultValue [((max 0 (min 1 (if (True == False) then (-3) else 2))), newUpdate0)]
    returnStatus
      | (sereneIMPLIES (boardBlVAR0 blackboard) ((-2) >= (-44))) = Failure
      | otherwise = Failure
    newFutureChanges = futureChanges
