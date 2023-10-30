module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  , boardBlVAR0 :: (Integer, Integer, Integer)
  , boardLocalVAR2Location3 :: Integer
  , boardBlVAR3 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardBlVAR0: " ++ (show (boardBlVAR0 blackboard)) ++ ", " ++ "boardLocalVAR2Location3: " ++ (show (boardLocalVAR2Location3 blackboard)) ++ ", " ++ "boardBlVAR3: " ++ (show (boardBlVAR3 blackboard)) ++ ", " ++ "boardBlDEFINE5: " ++ (show (boardBlDEFINE5 blackboard)) ++ ", " ++ "boardBlDEFINE7: " ++ (show (boardBlDEFINE7 blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

boardLocalVAR2 :: Integer -> BTreeBlackboard -> Integer
boardLocalVAR2 3 = boardLocalVAR2Location3
boardLocalVAR2 _ = error "illegal local reference: boardLocalVAR2"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard  -> (Integer, Integer)
boardBlDEFINE5 blackboard = newVal
  where
    newUpdate0
      | ((boardBlVAR3 blackboard) < 43) = (min (-2) (max (-5) ((min 50 (max (-50) (abs 17))))))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (- (-18))))) - ((min 50 (max (-50) ((-37) + (indexIntoBlVAR0 (max 0 (min 2 (boardBlVAR3 blackboard))) (boardBlVAR0 blackboard))))))))))))
    defaultValue0
      | ("no" /= "both") = (min (-2) (max (-5) ((min 50 (max (-50) (44 - 44))))))
      | (sereneXOR False False) = (min (-2) (max (-5) 13))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (abs (boardBlVAR3 blackboard)))))))
    defaultValue1
      | ("no" /= "both") = (min (-2) (max (-5) ((min 50 (max (-50) (44 - 44))))))
      | (sereneXOR False False) = (min (-2) (max (-5) 13))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (abs (boardBlVAR3 blackboard)))))))
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayBlDEFINE5 defaultValue [(0, newUpdate0), (1, newUpdate0)]
boardBlDEFINE7 :: BTreeBlackboard  -> Integer
boardBlDEFINE7 blackboard = newVal
  where
    newVal
      | False = (min (-2) (max (-5) 14))
      | (((sereneCOUNT ((sereneXOR False True) == False) (((min 50 (max (-50) ( 50+ ( (-28)+((-6) + (boardBlVAR3 blackboard))))))) >= ((min 50 (max (-50) (abs (indexIntoBlVAR0 (max 0 (min 2 12)) (boardBlVAR0 blackboard)))))))) + (sereneCOUNT (sereneXNOR False True) (4 >= ((min 50 (max (-50) (2 - 2))))))) < ((min 50 (max (-50) (max (-29) (-29)))))) = (min (-2) (max (-5) ((min 50 (max (-50) ( 46*(46 * 46)))))))
      | otherwise = (min (-2) (max (-5) (-22)))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoBlVAR0 :: Integer -> (Integer, Integer, Integer) -> Integer
indexIntoBlVAR0 0 (value, _, _) = value
indexIntoBlVAR0 1 (_, value, _) = value
indexIntoBlVAR0 2 (_, _, value) = value
indexIntoBlVAR0 _ _ = error "indexIntoBlVAR0 illegal index value"
indexIntoBlDEFINE5 :: Integer -> (Integer, Integer) -> Integer
indexIntoBlDEFINE5 0 (value, _) = value
indexIntoBlDEFINE5 1 (_, value) = value
indexIntoBlDEFINE5 _ _ = error "indexIntoBlDEFINE5 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayBlVAR0 :: (Integer, Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer, Integer)
newArrayBlVAR0 values  []  = values
newArrayBlVAR0 (value0, value1, value2) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
      updateValues [] = (value0, value1, value2)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues
newArrayBlDEFINE5 :: (Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer)
newArrayBlDEFINE5 values  []  = values
newArrayBlDEFINE5 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF UPDATES

boardUpdate :: BTreeBlackboard -> StdGen -> BTreeBlackboard
boardUpdate blackboard newGen = blackboard { boardGenerator = newGen }
boardUpdateBlVAR0 :: BTreeBlackboard -> StdGen -> (Integer, Integer, Integer) -> BTreeBlackboard
boardUpdateBlVAR0 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR0 = newVal }
boardUpdateBlVAR3 :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateBlVAR3 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR3 = newVal }
boardUpdateLocalVAR2 :: Integer ->BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateLocalVAR2 3 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardLocalVAR2Location3 = newVal }
boardUpdateLocalVAR2 _ _ _ _ = error "illegal local reference: boardUpdateLocalVAR2"

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen (0, 0, 0) 0 0
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdateBlVAR0 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0 = (min 5 (max 2 ((min 50 (max (-50) ( 2* ( 2*(((min 50 (max (-50) ((if (False || False) then (-15) else 2) + (if (False || False) then (-15) else 2))))) * 6))))))))
        newUpdate1
          | (True == False) = (min 5 (max 2 ((min 50 (max (-50) (- ((min 50 (max (-50) ( (-18)+ ( (-18)+((-18) + (-18)))))))))))))
          | False = (min 5 (max 2 ((min 50 (max (-50) (max 33 41))))))
          | otherwise = (min 5 (max 2 ((sereneCOUNT (True /= False) (False || True)) + (sereneCOUNT (5 /= 48) (sereneXOR False False)))))
        newUpdate2
          | (True == False) = (min 5 (max 2 ((min 50 (max (-50) (- ((min 50 (max (-50) ( (-18)+ ( (-18)+((-18) + (-18)))))))))))))
          | False = (min 5 (max 2 ((min 50 (max (-50) (max 33 41))))))
          | otherwise = (min 5 (max 2 ((sereneCOUNT (True /= False) (False || True)) + (sereneCOUNT (5 /= 48) (sereneXOR False False)))))
        newUpdate3
          | (True == False) = (min 5 (max 2 ((min 50 (max (-50) (- ((min 50 (max (-50) ( (-18)+ ( (-18)+((-18) + (-18)))))))))))))
          | False = (min 5 (max 2 ((min 50 (max (-50) (max 33 41))))))
          | otherwise = (min 5 (max 2 ((sereneCOUNT (True /= False) (False || True)) + (sereneCOUNT (5 /= 48) (sereneXOR False False)))))
        defaultValue0
          | (((min 50 (max (-50) (3 - 3)))) <= ((min 50 (max (-50) ( 2* ( 2*(2 * 2))))))) = (min 5 (max 2 ((min 50 (max (-50) (min ((min 50 (max (-50) (- 4)))) ((min 50 (max (-50) (- 4))))))))))
          | otherwise = (min 5 (max 2 (-47)))
        defaultValue1
          | (((min 50 (max (-50) (3 - 3)))) <= ((min 50 (max (-50) ( 2* ( 2*(2 * 2))))))) = (min 5 (max 2 ((min 50 (max (-50) (min ((min 50 (max (-50) (- 4)))) ((min 50 (max (-50) (- 4))))))))))
          | otherwise = (min 5 (max 2 (-47)))
        defaultValue2
          | (((min 50 (max (-50) (3 - 3)))) <= ((min 50 (max (-50) ( 2* ( 2*(2 * 2))))))) = (min 5 (max 2 ((min 50 (max (-50) (min ((min 50 (max (-50) (- 4)))) ((min 50 (max (-50) (- 4))))))))))
          | otherwise = (min 5 (max 2 (-47)))
        defaultValue = (defaultValue0, defaultValue1, defaultValue2)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR0 defaultValue [((max 0 (min 2 (if (5 < (-2)) then (-5) else (-14)))), newUpdate0), ((max 0 (min 2 2)), newUpdate1), ((max 0 (min 2 2)), newUpdate2), ((max 0 (min 2 2)), newUpdate3)]
    statement1 :: BTreeBlackboard -> BTreeBlackboard
    statement1 blackboard = boardUpdateBlVAR3 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (min 5 (max 2 ((min 50 (max (-50) (max (-4) (-4)))))))
    statement2 :: BTreeBlackboard -> BTreeBlackboard
    statement2 blackboard = boardUpdateLocalVAR2 nodeLocation blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | (((sereneCOUNT ((-27) <= (indexIntoBlVAR0 (max 0 (min 2 39)) (boardBlVAR0 blackboard))) (False || True)) + (sereneCOUNT ("yes" /= "yes") (True == False))) == (-16)) = (min (-2) (max (-5) (-4)))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (- 3))))))
        nodeLocation = 3
    newBlackboard = (statement2 (statement1 (statement0 dummy)))

