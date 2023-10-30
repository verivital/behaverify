module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  , boardBlVAR0 :: Bool
  , boardBlVAR2 :: (String, String)
  , boardBlVAR3 :: (Bool, Bool)
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardBlVAR0: " ++ (show (boardBlVAR0 blackboard)) ++ ", " ++ "boardBlVAR2: " ++ (show (boardBlVAR2 blackboard)) ++ ", " ++ "boardBlVAR3: " ++ (show (boardBlVAR3 blackboard)) ++ ", " ++ "boardBlDEFINE5: " ++ (show (boardBlDEFINE5 blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard  -> String
boardBlDEFINE5 blackboard = newVal
  where
    newVal = (indexIntoBlVAR2 (max 0 (min 1 1)) (boardBlVAR2 blackboard))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoBlVAR2 :: Integer -> (String, String) -> String
indexIntoBlVAR2 0 (value, _) = value
indexIntoBlVAR2 1 (_, value) = value
indexIntoBlVAR2 _ _ = error "indexIntoBlVAR2 illegal index value"
indexIntoBlVAR3 :: Integer -> (Bool, Bool) -> Bool
indexIntoBlVAR3 0 (value, _) = value
indexIntoBlVAR3 1 (_, value) = value
indexIntoBlVAR3 _ _ = error "indexIntoBlVAR3 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayBlVAR2 :: (String, String) -> [(Integer, String)] -> (String, String)
newArrayBlVAR2 values  []  = values
newArrayBlVAR2 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, String)] -> (String, String)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues
newArrayBlVAR3 :: (Bool, Bool) -> [(Integer, Bool)] -> (Bool, Bool)
newArrayBlVAR3 values  []  = values
newArrayBlVAR3 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
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
boardUpdateBlVAR0 :: BTreeBlackboard -> StdGen -> Bool -> BTreeBlackboard
boardUpdateBlVAR0 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR0 = newVal }
boardUpdateBlVAR2 :: BTreeBlackboard -> StdGen -> (String, String) -> BTreeBlackboard
boardUpdateBlVAR2 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR2 = newVal }
boardUpdateBlVAR3 :: BTreeBlackboard -> StdGen -> (Bool, Bool) -> BTreeBlackboard
boardUpdateBlVAR3 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR3 = newVal }

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen True (" ", " ") (True, True)
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdateBlVAR0 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | False = (((-21) > (-41)) /= True)
          | otherwise = ((True && True) == False)
    statement1 :: BTreeBlackboard -> BTreeBlackboard
    statement1 blackboard = boardUpdateBlVAR2 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | (sereneXOR (10 < (if (False || (boardBlVAR0 blackboard)) then (-38) else 35)) (False || (boardBlVAR0 blackboard))) = "no"
          | otherwise = "both"
        newUpdate1
          | (sereneXOR (10 < (if (False || (boardBlVAR0 blackboard)) then (-38) else 35)) (False || (boardBlVAR0 blackboard))) = "no"
          | otherwise = "both"
        newUpdate2
          | (sereneXOR (10 < (if (False || (boardBlVAR0 blackboard)) then (-38) else 35)) (False || (boardBlVAR0 blackboard))) = "no"
          | otherwise = "both"
        defaultValue0
          | ((-4) < 4) = "no"
          | ((-26) >= 34) = "both"
          | otherwise = "both"
        defaultValue1
          | ((-4) < 4) = "no"
          | ((-26) >= 34) = "both"
          | otherwise = "both"
        defaultValue = (defaultValue0, defaultValue1)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR2 defaultValue [((max 0 (min 1 ((min 50 (max (-50) ( ((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0))+(((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0)) + ((min 50 (max (-50) (max (-3) (-3)))))))))))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) ( ((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0))+(((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0)) + ((min 50 (max (-50) (max (-3) (-3)))))))))))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) ( ((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0))+(((sereneCOUNT ((-5) > 7) (5 >= 21)) + (if (32 > 4) then 1 else 0)) + ((min 50 (max (-50) (max (-3) (-3)))))))))))), newUpdate2)]
    statement2 :: BTreeBlackboard -> BTreeBlackboard
    statement2 blackboard = boardUpdateBlVAR3 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newUpdate0
          | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (((min 50 (max (-50) (19 - 19)))) >= ((min 50 (max (-50) ( (-4)* ( 33*(33 * 33)))))))
          | otherwise = (((5 /= (-26)) && (sereneXNOR False (boardBlVAR0 blackboard))) || (sereneXOR (boardBlVAR0 blackboard) True))
        newUpdate1
          | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (((min 50 (max (-50) (19 - 19)))) >= ((min 50 (max (-50) ( (-4)* ( 33*(33 * 33)))))))
          | otherwise = (((5 /= (-26)) && (sereneXNOR False (boardBlVAR0 blackboard))) || (sereneXOR (boardBlVAR0 blackboard) True))
        newUpdate2
          | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (((min 50 (max (-50) (19 - 19)))) >= ((min 50 (max (-50) ( (-4)* ( 33*(33 * 33)))))))
          | otherwise = (((5 /= (-26)) && (sereneXNOR False (boardBlVAR0 blackboard))) || (sereneXOR (boardBlVAR0 blackboard) True))
        newUpdate3
          | (sereneIMPLIES (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = (((min 50 (max (-50) (19 - 19)))) >= ((min 50 (max (-50) ( (-4)* ( 33*(33 * 33)))))))
          | otherwise = (((5 /= (-26)) && (sereneXNOR False (boardBlVAR0 blackboard))) || (sereneXOR (boardBlVAR0 blackboard) True))
        newUpdate4 = False
        defaultValue0
          | ((False == False) || (True && True)) = ((indexIntoBlVAR2 (max 0 (min 1 4)) (boardBlVAR2 blackboard)) == "yes")
          | (5 > 24) = (10 == 4)
          | otherwise = ((sereneIMPLIES True True) == (1 > (-1)))
        defaultValue1
          | ((False == False) || (True && True)) = ((indexIntoBlVAR2 (max 0 (min 1 4)) (boardBlVAR2 blackboard)) == "yes")
          | (5 > 24) = (10 == 4)
          | otherwise = ((sereneIMPLIES True True) == (1 > (-1)))
        defaultValue = (defaultValue0, defaultValue1)
        newGenerator = snd randomPair0
        newVal = newArrayBlVAR3 defaultValue [((max 0 (min 1 ((min 50 (max (-50) (((min 50 (max (-50) ( (-3)+((-3) + (-41)))))) + ((min 50 (max (-50) ( (-3)+((-3) + (-41)))))))))))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) (((min 50 (max (-50) ( (-3)+((-3) + (-41)))))) + ((min 50 (max (-50) ( (-3)+((-3) + (-41)))))))))))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) (((min 50 (max (-50) ( (-3)+((-3) + (-41)))))) + ((min 50 (max (-50) ( (-3)+((-3) + (-41)))))))))))), newUpdate2), ((max 0 (min 1 ((min 50 (max (-50) (((min 50 (max (-50) ( (-3)+((-3) + (-41)))))) + ((min 50 (max (-50) ( (-3)+((-3) + (-41)))))))))))), newUpdate3), ((max 0 (min 1 ((min 50 (max (-50) (max ((min 50 (max (-50) (4 * 4)))) ((min 50 (max (-50) ( (-2)*((-2) * (-4)))))))))))), newUpdate4)]
    newBlackboard = (statement2 (statement1 (statement0 dummy)))

