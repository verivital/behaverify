module BTreeA3 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA3 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA3 _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    (newBlackboard, newEnvironment) = (statement3 (statement2 (statement1 (statement0 (blackboard, environment)))))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | True = (min (-2) (max (-5) (if ((indexIntoBlVAR3 (max 0 (min 1 (-20))) (boardBlVAR3 blackboard)) == True) then 19 else 2)))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (abs 4))))))
          | otherwise = (min (-2) (max (-5) (envEnvVAR1 environment)))
    returnStatus
      | (sereneXOR ((-2) /= (-33)) (boardBlVAR0 blackboard)) = Failure
      | otherwise = Failure
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (boardUpdateBlVAR0 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | ((indexIntoBlVAR3 (max 0 (min 1 (-2))) (boardBlVAR3 blackboard)) || True) = ((False || True) == (False == (boardBlVAR0 blackboard)))
          | (((min 50 (max (-50) ( 13* ( 13*((-5) * 47)))))) <= ((min 50 (max (-50) (min 2 41))))) = (37 >= (-23))
          | otherwise = (sereneXOR (((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) == (sereneXNOR True True)) ((True == (boardBlVAR0 blackboard)) == True))
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (preBlackboard, environment) = (newBlackboard, newEnvironment)
      where
        (newBlackboard, newEnvironment) = if condition then (statement3 (blackboard, environment)) else (blackboard, environment)
        condPair = (-1, boardGenerator preBlackboard)
        condition = (sereneXOR ((sereneIMPLIES (boardBlVAR0 blackboard) True) && (sereneXNOR False True)) (False && False))
        blackboard = boardUpdate preBlackboard (snd condPair)
        statement3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
        statement3 (blackboard, environment)  = (boardUpdateBlVAR2 blackboard newGenerator newVal, environment)
          where
            randomPair0 = (-1, boardGenerator blackboard)
            newUpdate0 = "both"
            newUpdate1 = "both"
            newUpdate2 = "both"
            newUpdate3 = "both"
            newUpdate4 = "both"
            newUpdate5 = "both"
            newUpdate6 = "both"
            newUpdate7 = "both"
            newUpdate8 = "both"
            newUpdate9 = "both"
            newUpdate10 = "both"
            newUpdate11 = "both"
            newUpdate12 = "both"
            newUpdate13 = "both"
            newUpdate14 = "both"
            newUpdate15 = "both"
            newUpdate16 = "both"
            newUpdate17 = "both"
            newUpdate18 = "both"
            newUpdate19 = "both"
            newUpdate20 = "both"
            newUpdate21 = "both"
            newUpdate22 = "both"
            newUpdate23 = "both"
            defaultValue = (boardBlVAR2 blackboard)
            newGenerator = snd randomPair0
            newVal = newArrayBlVAR2 defaultValue [((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate0), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate1), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate2), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate2), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate3), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate3), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate4), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate4), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate5), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate5), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate6), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate6), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate7), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate7), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate8), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate8), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate9), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate9), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate10), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate10), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate11), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate11), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate12), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate12), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate13), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate13), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate14), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate14), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate15), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate15), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate16), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate16), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate17), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate17), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate18), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate18), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate19), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate19), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate20), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate20), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate21), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate21), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate22), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate22), ((max 0 (min 1 (if (sereneXOR True (boardBlVAR0 blackboard)) then 29 else 19))), newUpdate23), ((max 0 (min 1 ((min 50 (max (-50) (min (-34) (-34))))))), newUpdate23)]
    statement3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement3 (blackboard, environment)  = (boardUpdateBlVAR0 blackboard newGenerator newVal, environment)
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = ((indexIntoBlVAR3 (max 0 (min 1 (-50))) (boardBlVAR3 blackboard)) == (True || (boardBlVAR0 blackboard)))
    newFutureChanges = futureChanges
