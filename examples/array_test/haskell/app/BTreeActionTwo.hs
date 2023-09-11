module BTreeActionTwo where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionActionTwo :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionActionTwo _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv = (arrayUpdateBoardFoo blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((boardIndexVar blackboard), updateValue0)
        updatePair1 = ((rem ((boardIndexVar blackboard) + 1) 3), updateValue1)
        updateValue0
          | ("increase" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = (min 10 ((boardFoo (boardIndexVar blackboard) blackboard) * 2))
          | ("decrease" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = (max 0 (quot (boardFoo (boardIndexVar blackboard) blackboard) 2))
          | otherwise = (boardFoo (boardIndexVar blackboard) blackboard)
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | ("increase" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = (min 10 ((boardFoo (boardIndexVar blackboard) blackboard) * 2))
          | ("decrease" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = (max 0 (quot (boardFoo (boardIndexVar blackboard) blackboard) 2))
          | otherwise = (boardFoo (boardIndexVar blackboard) blackboard)
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (arrayUpdateLocalBoardBar nodeLocation (updateBoardGenerator blackboard randomGenerator2) updates, environment)
      where
        (blackboard, environment) = boardEnv
        randomGenerator0 = sereneBoardGenerator blackboard
        randomGenerator1 = snd (getRandomInteger randomGenerator0 1)
        randomGenerator2 = snd (getRandomInteger randomGenerator1 1)
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = (0, updateValue0)
        updatePair1 = (1, updateValue1)
        updatePair2 = (2, updateValue2)
        updateValue0
          | ("increase" == (localBoardBar nodeLocation 0 blackboard)) = privateRandom1 (fst (getRandomInteger randomGenerator0 1))
          | ("decrease" == (localBoardBar nodeLocation 0 blackboard)) = privateRandom2 (fst (getRandomInteger randomGenerator0 1))
          | otherwise = privateRandom0 (fst (getRandomInteger randomGenerator0 1))
          where
            (blackboard, environment) = boardEnv
            privateRandom1 :: Integer -> String
            privateRandom1 0 = "decrease"
            privateRandom1 _ = "nope"
            privateRandom2 :: Integer -> String
            privateRandom2 0 = "nope"
            privateRandom2 _ = "increase"
            privateRandom0 :: Integer -> String
            privateRandom0 0 = "increase"
            privateRandom0 _ = "decrease"
        updateValue1
          | ("increase" == (localBoardBar nodeLocation 1 blackboard)) = privateRandom1 (fst (getRandomInteger randomGenerator1 1))
          | ("decrease" == (localBoardBar nodeLocation 1 blackboard)) = privateRandom2 (fst (getRandomInteger randomGenerator1 1))
          | otherwise = privateRandom0 (fst (getRandomInteger randomGenerator1 1))
          where
            (blackboard, environment) = boardEnv
            privateRandom1 :: Integer -> String
            privateRandom1 0 = "decrease"
            privateRandom1 _ = "nope"
            privateRandom2 :: Integer -> String
            privateRandom2 0 = "nope"
            privateRandom2 _ = "increase"
            privateRandom0 :: Integer -> String
            privateRandom0 0 = "increase"
            privateRandom0 _ = "decrease"
        updateValue2
          | ("increase" == (localBoardBar nodeLocation 2 blackboard)) = privateRandom1 (fst (getRandomInteger randomGenerator2 1))
          | ("decrease" == (localBoardBar nodeLocation 2 blackboard)) = privateRandom2 (fst (getRandomInteger randomGenerator2 1))
          | otherwise = privateRandom0 (fst (getRandomInteger randomGenerator2 1))
          where
            (blackboard, environment) = boardEnv
            privateRandom1 :: Integer -> String
            privateRandom1 0 = "decrease"
            privateRandom1 _ = "nope"
            privateRandom2 :: Integer -> String
            privateRandom2 0 = "nope"
            privateRandom2 _ = "increase"
            privateRandom0 :: Integer -> String
            privateRandom0 0 = "increase"
            privateRandom0 _ = "decrease"
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv = (arrayUpdateLocalBoardBar nodeLocation (updateBoardGenerator blackboard randomGenerator0) updates, environment)
      where
        (blackboard, environment) = boardEnv
        randomGenerator0 = sereneBoardGenerator blackboard
        updates = [updatePair0]
        updatePair0 = ((boardIndexVar blackboard), updateValue0)
        updateValue0
          | ("increase" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = privateRandom1 (fst (getRandomInteger randomGenerator0 1))
          | ("decrease" == (localBoardBar nodeLocation (boardIndexVar blackboard) blackboard)) = privateRandom2 (fst (getRandomInteger randomGenerator0 1))
          | otherwise = privateRandom0 (fst (getRandomInteger randomGenerator0 1))
          where
            (blackboard, environment) = boardEnv
            privateRandom1 :: Integer -> String
            privateRandom1 0 = "decrease"
            privateRandom1 _ = "nope"
            privateRandom2 :: Integer -> String
            privateRandom2 0 = "nope"
            privateRandom2 _ = "increase"
            privateRandom0 :: Integer -> String
            privateRandom0 0 = "increase"
            privateRandom0 _ = "decrease"
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate2 . boardEnvUpdate1 $ preStatusBoardEnv
    newFutureChanges = futureChanges
