module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  , boardBlVAR0 :: Bool
  , boardLocalVAR2Location4 :: (Integer, Integer, Integer)
  , boardLocalVAR2Location6 :: (Integer, Integer, Integer)
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardBlVAR0: " ++ (show (boardBlVAR0 blackboard)) ++ ", " ++ "boardLocalVAR2Location4: " ++ (show (boardLocalVAR2Location4 blackboard)) ++ ", " ++ "boardLocalVAR2Location6: " ++ (show (boardLocalVAR2Location6 blackboard)) ++ ", " ++ "boardBlDEFINE5: " ++ (show (boardBlDEFINE5 blackboard)) ++ ", " ++ "boardBlDEFINE6: " ++ (show (boardBlDEFINE6 blackboard)) ++ ", " ++ "boardBlDEFINE8: " ++ (show (boardBlDEFINE8 blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

boardLocalVAR2 :: Integer -> BTreeBlackboard -> (Integer, Integer, Integer)
boardLocalVAR2 4 = boardLocalVAR2Location4
boardLocalVAR2 6 = boardLocalVAR2Location6
boardLocalVAR2 _ = error "illegal local reference: boardLocalVAR2"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard  -> Integer
boardBlDEFINE5 blackboard = newVal
  where
    newVal
      | (2 <= (-2)) = (min 5 (max 2 33))
      | otherwise = (min 5 (max 2 (if ((-9) /= (if (sereneXOR True (boardBlVAR0 blackboard)) then (-20) else 3)) then ((min 50 (max (-50) (max 25 5)))) else ((min 50 (max (-50) ((-1) + (-1))))))))
boardBlDEFINE6 :: BTreeBlackboard  -> (Integer, Integer, Integer)
boardBlDEFINE6 blackboard = newVal
  where
    newUpdate0
      | ((boardBlVAR0 blackboard) && False) = (min 5 (max 2 36))
      | ((boardBlDEFINE5 blackboard) == (boardBlDEFINE5 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (max (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7)))))) (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7))))))))))))
      | otherwise = (min 5 (max 2 31))
    newUpdate1
      | ((boardBlVAR0 blackboard) && False) = (min 5 (max 2 36))
      | ((boardBlDEFINE5 blackboard) == (boardBlDEFINE5 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (max (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7)))))) (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7))))))))))))
      | otherwise = (min 5 (max 2 31))
    newUpdate2
      | ((boardBlVAR0 blackboard) && False) = (min 5 (max 2 36))
      | ((boardBlDEFINE5 blackboard) == (boardBlDEFINE5 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (max (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7)))))) (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7))))))))))))
      | otherwise = (min 5 (max 2 31))
    newUpdate3
      | ((boardBlVAR0 blackboard) && False) = (min 5 (max 2 36))
      | ((boardBlDEFINE5 blackboard) == (boardBlDEFINE5 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (max (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7)))))) (if ((boardBlDEFINE5 blackboard) >= (boardBlDEFINE5 blackboard)) then (if ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) then (boardBlDEFINE5 blackboard) else 16) else ((min 50 (max (-50) (- (-7))))))))))))
      | otherwise = (min 5 (max 2 31))
    defaultValue0
      | (sereneXNOR True (boardBlVAR0 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (abs (if (False /= True) then (boardBlDEFINE5 blackboard) else (boardBlDEFINE5 blackboard))))))))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard)))))))
    defaultValue1
      | (sereneXNOR True (boardBlVAR0 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (abs (if (False /= True) then (boardBlDEFINE5 blackboard) else (boardBlDEFINE5 blackboard))))))))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard)))))))
    defaultValue2
      | (sereneXNOR True (boardBlVAR0 blackboard)) = (min 5 (max 2 ((min 50 (max (-50) (abs (if (False /= True) then (boardBlDEFINE5 blackboard) else (boardBlDEFINE5 blackboard))))))))
      | otherwise = (min 5 (max 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard)))))))
    defaultValue = (defaultValue0, defaultValue1, defaultValue2)
    newVal = newArrayBlDEFINE6 defaultValue [((max 0 (min 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard))))))), newUpdate0), ((max 0 (min 2 (boardBlDEFINE5 blackboard))), newUpdate0), ((max 0 (min 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard))))))), newUpdate1), ((max 0 (min 2 (boardBlDEFINE5 blackboard))), newUpdate1), ((max 0 (min 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard))))))), newUpdate2), ((max 0 (min 2 (boardBlDEFINE5 blackboard))), newUpdate2), ((max 0 (min 2 ((min 50 (max (-50) ((boardBlDEFINE5 blackboard) - (boardBlDEFINE5 blackboard))))))), newUpdate3), ((max 0 (min 2 (boardBlDEFINE5 blackboard))), newUpdate3)]
boardBlDEFINE8 :: BTreeBlackboard  -> Integer
boardBlDEFINE8 blackboard = newVal
  where
    newVal
      | ((boardBlVAR0 blackboard) == (sereneIMPLIES False True)) = (min (-2) (max (-5) ((min 50 (max (-50) (min ((min 50 (max (-50) ((-29) + (-43))))) ((min 50 (max (-50) ((-29) + (-43)))))))))))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (23 - 23))))))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoLocalVAR2 :: Integer -> (Integer, Integer, Integer) -> Integer
indexIntoLocalVAR2 0 (value, _, _) = value
indexIntoLocalVAR2 1 (_, value, _) = value
indexIntoLocalVAR2 2 (_, _, value) = value
indexIntoLocalVAR2 _ _ = error "indexIntoLocalVAR2 illegal index value"
indexIntoBlDEFINE6 :: Integer -> (Integer, Integer, Integer) -> Integer
indexIntoBlDEFINE6 0 (value, _, _) = value
indexIntoBlDEFINE6 1 (_, value, _) = value
indexIntoBlDEFINE6 2 (_, _, value) = value
indexIntoBlDEFINE6 _ _ = error "indexIntoBlDEFINE6 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayLocalVAR2 :: (Integer, Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer, Integer)
newArrayLocalVAR2 values  []  = values
newArrayLocalVAR2 (value0, value1, value2) indicesValues = updateValues indicesValues
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
newArrayBlDEFINE6 :: (Integer, Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer, Integer)
newArrayBlDEFINE6 values  []  = values
newArrayBlDEFINE6 (value0, value1, value2) indicesValues = updateValues indicesValues
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

-- START OF UPDATES

boardUpdate :: BTreeBlackboard -> StdGen -> BTreeBlackboard
boardUpdate blackboard newGen = blackboard { boardGenerator = newGen }
boardUpdateBlVAR0 :: BTreeBlackboard -> StdGen -> Bool -> BTreeBlackboard
boardUpdateBlVAR0 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR0 = newVal }
boardUpdateLocalVAR2 :: Integer ->BTreeBlackboard -> StdGen -> (Integer, Integer, Integer) -> BTreeBlackboard
boardUpdateLocalVAR2 4 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardLocalVAR2Location4 = newVal }
boardUpdateLocalVAR2 6 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardLocalVAR2Location6 = newVal }
boardUpdateLocalVAR2 _ _ _ _ = error "illegal local reference: boardUpdateLocalVAR2"

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen True (0, 0, 0) (0, 0, 0)
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdateBlVAR0 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | (sereneXOR False True) = True
          | False = (((min 50 (max (-50) (abs 4)))) < ((min 50 (max (-50) (min 5 5)))))
          | otherwise = (((min 50 (max (-50) ((-7) + 4)))) <= ((min 50 (max (-50) (- 40)))))
    statement1 :: BTreeBlackboard -> BTreeBlackboard
    statement1 blackboard = boardUpdateLocalVAR2 nodeLocation blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | False = (min (-2) (max (-5) 7))
          | ((sereneXNOR True (boardBlVAR0 blackboard)) && (boardBlVAR0 blackboard)) = (min (-2) (max (-5) (if (sereneXNOR ((-15) <= (-6)) ((-27) >= 13)) then ((min 50 (max (-50) (max 22 22)))) else ((min 50 (max (-50) ( (-46)+((-46) + (-46)))))))))
          | otherwise = (min (-2) (max (-5) (-1)))
        defaultValue0
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue1
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue2
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue = (defaultValue0, defaultValue1, defaultValue2)
        newGenerator = snd randomPair0
        newVal = newArrayLocalVAR2 defaultValue [(0, newUpdate0), (1, newUpdate0)]
        nodeLocation = 4
    statement2 :: BTreeBlackboard -> BTreeBlackboard
    statement2 blackboard = boardUpdateLocalVAR2 nodeLocation blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | False = (min (-2) (max (-5) 7))
          | ((sereneXNOR True (boardBlVAR0 blackboard)) && (boardBlVAR0 blackboard)) = (min (-2) (max (-5) (if (sereneXNOR ((-15) <= (-6)) ((-27) >= 13)) then ((min 50 (max (-50) (max 22 22)))) else ((min 50 (max (-50) ( (-46)+((-46) + (-46)))))))))
          | otherwise = (min (-2) (max (-5) (-1)))
        defaultValue0
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue1
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue2
          | (sereneXOR True (3 >= 2)) = (min (-2) (max (-5) ((min 50 (max (-50) (((min 50 (max (-50) (5 + 5)))) - ((min 50 (max (-50) (min (-4) (-4)))))))))))
          | True = (min (-2) (max (-5) ((min 50 (max (-50) (max (-50) (-50)))))))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) (min (-4) 30))))))
        defaultValue = (defaultValue0, defaultValue1, defaultValue2)
        newGenerator = snd randomPair0
        newVal = newArrayLocalVAR2 defaultValue [(0, newUpdate0), (1, newUpdate0)]
        nodeLocation = 6
    newBlackboard = (statement2 (statement1 (statement0 dummy)))

