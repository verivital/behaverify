module BTreeA2 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA2 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA2 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement0 (blackboard, environment))
    returnStatus
      | ((boardBlDEFINE7 blackboard) >= (if (False == False) then (boardBlVAR3 blackboard) else (boardBlVAR3 blackboard))) = Running
      | False = Failure
      | otherwise = Running
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0 = "yes"
        newUpdate1 = "yes"
        newUpdate2 = "yes"
        newUpdate3 = "yes"
        newUpdate4 = "yes"
        newUpdate5 = "yes"
        newUpdate6 = "yes"
        newUpdate7 = "yes"
        newUpdate8 = "yes"
        newUpdate9 = "yes"
        newUpdate10 = "yes"
        newUpdate11 = "yes"
        newUpdate12 = "yes"
        newUpdate13 = "yes"
        newUpdate14 = "yes"
        newUpdate15 = "yes"
        newUpdate16 = "yes"
        newUpdate17 = "yes"
        newUpdate18 = "yes"
        newUpdate19 = "yes"
        newUpdate20 = "yes"
        newUpdate21 = "yes"
        newUpdate22 = "yes"
        newUpdate23 = "yes"
        newUpdate24 = "yes"
        newUpdate25 = "yes"
        newUpdate26 = "yes"
        newUpdate27 = "yes"
        newUpdate28 = "yes"
        newUpdate29 = "yes"
        newUpdate30 = "yes"
        newUpdate31 = "yes"
        newUpdate32 = "yes"
        newUpdate33 = "yes"
        newUpdate34 = "yes"
        newUpdate35 = "yes"
        newUpdate36 = "yes"
        newUpdate37 = "yes"
        newUpdate38 = "yes"
        newUpdate39 = "yes"
        newUpdate40 = "yes"
        newUpdate41 = "yes"
        newUpdate42 = "yes"
        newUpdate43 = "yes"
        newUpdate44 = "yes"
        newUpdate45 = "yes"
        newUpdate46 = "yes"
        newUpdate47 = "yes"
        newUpdate48 = (indexIntoEnvVAR1 (max 0 (min 2 (boardBlDEFINE7 blackboard))) (envEnvVAR1 environment))
        defaultValue = (envEnvVAR1 environment)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate3), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate4), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate5), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate6), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate7), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate8), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate9), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate10), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate11), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate12), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate13), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate14), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate15), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate16), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate17), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate18), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate19), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate20), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate21), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate22), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate23), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate24), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate25), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate26), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate27), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate28), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate29), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate30), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate31), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate32), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate33), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate34), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate35), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate36), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate37), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate38), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate39), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate40), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate41), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate42), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate43), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate44), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate45), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate46), ((max 0 (min 2 ((min 50 (max (-50) (((min 50 (max (-50) (min (boardBlVAR3 blackboard) (indexIntoBlDEFINE5 (max 0 (min 1 39)) (boardBlDEFINE5 blackboard)))))) - (boardBlDEFINE7 blackboard))))))), newUpdate47), ((max 0 (min 2 (-4))), newUpdate48)]
    newFutureChanges = futureChanges
