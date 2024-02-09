module V4 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array.IArray as IArray ( (!), array, Array )

data State = State {
  varA :: Integer
  , varB :: Array Integer Integer
  }
  deriving (Eq, Ord, Show)


type StateMap = Map.Map State (Set.Set State)


ifThenElse :: Bool -> a -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val

initialStates :: Set.Set State
initialStates = iStates
  where
    varA_init_func :: Integer -> Set.Set Integer
    varA_init_func _ = result_true
      where
        result_true = Set.fromList [0]
    varA_init = varA_init_func 0
    varB_init = Set.singleton (IArray.array (0, 3) [(i, 0) | i <- [0..3]])
    iStates = Set.fromList [State varA_val varB_val | varA_val <- Set.toList varA_init, varB_val <- Set.toList varB_init]
      

nextStates :: State -> Set.Set State
nextStates state = nextStates
  where
    varA_stage0 = Set.singleton (varA state)
    varB_stage0 = Set.singleton (varB state)
    varA_stage1_func :: Integer -> Set.Set Integer
    varA_stage1_func 0
      | guardTrue && guardFalse = Set.union resultTrue resultFalse
      | guardTrue = resultTrue
      | otherwise = resultFalse
      where
        guardTrue = or guardVals
        guardFalse = not (and guardVals)
        guardFunc :: Integer -> Bool
        guardFunc varA_val = (<) (varA_val) (3)
        guardVals = [guardFunc varA_val | varA_val <- Set.toList varA_stage0]
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varA_val = Set.singleton ((+) varA_val 1)
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <- Set.toList varA_stage0]
          )
        resultFalse = varA_stage1_func 1
    varA_stage1_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varA_val = Set.singleton 0
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <-Set.toList  varA_stage0]
          )
    varA_stage1 = varA_stage1_func 0
    varB_stage1_func :: Integer -> Set.Set (Array Integer Integer)
    varB_stage1_func 0
      | guardTrue && guardFalse = Set.union resultTrue resultFalse
      | guardTrue = resultTrue
      | otherwise = resultFalse
      where
        guardTrue = or guardVals
        guardFalse = not (and guardVals)
        guardFunc :: Array Integer Integer -> Integer -> Bool
        guardFunc varB_val varA_val = (/=) (varB_val ! varA_val) (0)
        guardVals = [guardFunc varB_val varA_val | varA_val <- Set.toList varA_stage1, varB_val <- Set.toList varB_stage0]
        valueFunc1 :: Array Integer Integer -> Set.Set (Array Integer Integer)
        valueFunc1 varB_val = Set.singleton varB_val
        resultTrue = Set.unions [valueFunc1 varB_val
                                | varB_val <- Set.toList varB_stage0]
        resultFalse = varB_stage1_func 1
    varB_stage1_func _ = resultTrue
      where
        valueFunc1 :: Array Integer Integer -> Integer -> Set.Set (Array Integer Integer)
        valueFunc1 varB_val varA_val = Set.singleton (IArray.array (0, 3) [(index, (ifThenElse (index == varA_val) ((*) ((+) varA_val 1) (-1)) (varB_val ! index))) | index <- [0..3]])
        valueFunc2 :: Array Integer Integer -> Integer -> Set.Set (Array Integer Integer)
        valueFunc2 varB_val varA_val = Set.singleton (IArray.array (0, 3) [(index, (ifThenElse (index == varA_val) ((+) varA_val 1) (varB_val ! index))) | index <- [0..3]])
        resultTrue = Set.unions (
          [valueFunc1 varB_val varA_val
          | varB_val <- Set.toList varB_stage0, varA_val <- Set.toList varA_stage0]
          ++
          [valueFunc2 varB_val varA_val
          | varB_val <- Set.toList varB_stage0, varA_val <- Set.toList varA_stage0]
          )
    varB_stage1 = varB_stage1_func 0
    nextStates = Set.fromList [State varA_val varB_val | varA_val <- Set.toList varA_stage1, varB_val <- Set.toList varB_stage1]
    
reachableStates :: Set.Set State
reachableStates = reachableStatesFunc Set.empty initialStates
  where
    reachableStatesFunc :: Set.Set State -> Set.Set State -> Set.Set State
    reachableStatesFunc seenStates statesToExplore
      | Set.null unvisitedStates = seenStates
      | otherwise = reachable
      where
        unvisitedStates = Set.difference statesToExplore seenStates
        reachable = reachableStatesFunc (Set.union seenStates unvisitedStates) (Set.unions (Set.map nextStates unvisitedStates))

stateMap :: StateMap
stateMap = constructStateMap Map.empty (Map.fromList [(newState, Set.empty) | newState <- Set.toList initialStates])
  where
    dummyNextStates :: State -> a -> Set.Set State
    dummyNextStates state _ = nextStates state
    constructStateMap :: StateMap -> StateMap -> StateMap
    constructStateMap seenMap toExploreMap
      | Map.null unvisitedMap = seenMap
      | otherwise = fullMap
      where
        unvisitedMap = Map.difference toExploreMap seenMap
        exploredMap = Map.mapWithKey dummyNextStates unvisitedMap
        newSeenMap
          | Map.size seenMap > Map.size exploredMap = Map.union seenMap exploredMap
          | otherwise = Map.union exploredMap seenMap
        nextExplore = Map.fromList [(newState, Set.empty) | newState <- Set.toList (Set.unions (Map.elems exploredMap))]
        fullMap = constructStateMap newSeenMap nextExplore

reversedMapLookup :: StateMap -> State -> Set.Set State
reversedMapLookup stateMap state = fromJust (Map.lookup state stateMap)

ctlAX :: (State -> Bool) -> State -> Bool
ctlAX function state = Set.foldr ((&&) . function) True (fromJust (Map.lookup state stateMap))

ctlEX :: (State -> Bool) -> State -> Bool
ctlEX function state = Set.foldr ((||) . function) False (fromJust (Map.lookup state stateMap))

ctlAF :: (State -> Bool) -> State -> Bool
ctlAF function state = ctlAFStateSearch function Set.empty Set.empty (fromJust (Map.lookup state stateMap))
ctlAFStateSearch :: (State -> Bool) -> Set.Set State -> Set.Set State -> Set.Set State -> Bool
ctlAFStateSearch function seenStates falseStates statesToExplore
  | Set.null unexploredStates = False -- This means we haven't reached true and have nothing left to check
  | Set.foldr ((||) . flip Set.member falseStates) False statesToExplore = False -- This means we found a state that we've already visited that didn't evaluate to true, meaning an infinite loop where we don't reach true is possible.
  | otherwise = conclusion -- This means we still have states to check and we haven't encountered an infinit loop
  where
    unexploredStates = Set.difference statesToExplore seenStates -- Make sure to remove any overlap
    unexploredFalseStates = Set.filter (not . function) unexploredStates -- Filter so we only have states where the condition is false.
    conclusion
      | Set.null unexploredFalseStates = True -- If the condition was true for all the states we were exploring, then we've proved that we always reach true.
      | otherwise = ctlAFStateSearch function (Set.union seenStates unexploredStates) (Set.union falseStates unexploredFalseStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredFalseStates) -- more searching required.


ctlEF :: (State -> Bool) -> State -> Bool
ctlEF function state = ctlEFStateSearch function Set.empty (fromJust (Map.lookup state stateMap))
ctlEFStateSearch :: (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlEFStateSearch function seenStates statesToExplore
  | Set.null unexploredStates = False -- This means we haven't reached true and have nothing left to check
  | otherwise = conclusion -- This means we still have states to check
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    foundTrue = Set.foldr ((||) . function) False unexploredStates -- check if the condition holds for any of the new states
    conclusion
      | foundTrue = True -- if the condition holds for any of the new states, then we're done.
      | otherwise = ctlEFStateSearch function (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredStates) -- more searching required.


ctlAG :: (State -> Bool) -> State -> Bool
ctlAG function state = ctlAGStateSearch function Set.empty (fromJust (Map.lookup state stateMap))
ctlAGStateSearch :: (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlAGStateSearch function seenStates statesToExplore
  | Set.null unexploredStates = True -- we ran out of states and found nothing wrong, return true.
  | otherwise = conclusion
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    allTrue = Set.foldr ((&&) . function) True unexploredStates -- check if the condition holds for all of the new states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't hold globally.
      | otherwise = ctlAGStateSearch function (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredStates) -- keep searching

ctlEG :: (State -> Bool) -> State -> Bool
ctlEG function state = ctlEGStateSearch function Set.empty (fromJust (Map.lookup state stateMap))
ctlEGStateSearch :: (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlEGStateSearch function seenStates statesToExplore = not (ctlAFStateSearch (not . function) seenStates Set.empty statesToExplore)


ctl1 :: Bool
ctl1 = Set.foldr ((&&) . ctlFunc) True initialStates
  where
    ctlFunc :: State -> Bool
    ctlFunc state = ctlAF (\state -> (>) ((!) (varB state) 0) 0) state


ctl2 :: Bool
ctl2 = Set.foldr ((&&) . ctlFunc) True initialStates
  where
    ctlFunc :: State -> Bool
    ctlFunc state = (==) ((!) (varB state) (varA state)) 0

ctl3 :: Bool
ctl3 = Set.foldr ((&&) . ctlFunc) True initialStates
  where
    ctlFunc :: State -> Bool
    ctlFunc state = (not) ((ctlAX (\state -> (==) ((!) (varB state) (varA state)) 0)) state)
    
-- ctl2 :: Bool
-- ctl2 = Set.foldr ((&&) . ctlFunc) True initialStates
--   where
--     ctlFunc :: State -> Bool
--     ctlFunc = (\state -> (ctlEX (\state1 )ctlAF (\state -> ((>) ((!) (varB state) 0) 0))
    

main :: IO ()
main =
  do {
    --mapM_ (putStrLn . stateToString) initialStates
    --mapM_ (putStrLn . stateToString) reachableStates
    --mapM_ print (checkInvariants invariants reachableStates)
    print initialStates
    --; print (nextStates (Set.findMin initialStates))
    ; print reachableStates
    ; print ctl1
    ; print ctl2
    ; print ctl3
    -- ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec1)
    -- ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec2)
    -- ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec3)
    --; print (and [evaluateLTLElement state stateMap ltlSpecFalse  | state <- Set.toList initialStates])
    --; print (and [evaluateLTLElement state stateMap ltlSpecTrue  | state <- Set.toList initialStates])
    --; mapM_ print [Map.lookup state stateMap  | state <- Set.toList initialStates]
  }
  -- where
  --   defaultState = State 0 0 0.0 False False
  --   initialElements = [[IntegerElement (IConst 5)], [IntegerElement (IVar 0), IntegerElement (IIEqI (+) (IVar 0) (IVar 1))], [DoubleElement (DConst 3.4), DoubleElement (DDEqD (*) (DVar 2) (DConst 0.5)), DoubleElement (DConst 3.4)]]
  --   nextElements = [[IntegerElement (BIIEqI (ifThenElse) (IIEqB (<) (IVar 0) (IConst 10)) (IIEqI (+) (IVar 0) (IConst 1)) (IConst 0))]]
  --   initialStates = nextState initialElements 0 defaultState
  --   reachableStates = allStates nextElements Set.empty initialStates
  --   stateMap = constructStateMap initialElements nextElements defaultState
  --   invariants = [(IIEqB (<=) (IVar 0) (IConst 8)), (IIEqB (>) (IVar 0) (IConst 0)), (IIEqB (>=) (IVar 0) (IConst 0))]
  --   ctlSpec1 = CTLAlwaysFinally (CTLIIEqB (==) (IVar 0) (IConst 9))
  --   ctlSpec2 = CTLExistsFinally (CTLIIEqB (==) (IVar 0) (IConst 10))
  --   ctlSpec3 = CTLExistsFinally (CTLIIEqB (==) (IVar 0) (IConst 11))
