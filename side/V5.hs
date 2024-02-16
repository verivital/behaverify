module V5 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array.IArray as IArray ( (!), array, Array )

data State = State {
  varA :: Integer
  , varB :: Integer
  , sel :: NodeStatus
  , check :: NodeStatus
  , act :: NodeStatus
  }
  deriving (Eq, Ord, Show)

data NodeStatus = Success | Running | Failure | Invalid
  deriving (Enum, Eq, Ord, Show)

type StateMap = Map.Map State (Set.Set State)

ifThenElse :: Bool -> a -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val
  
initialStates :: Set.Set State
initialStates = next_func
  where
    varA_val = 0
    varB_val = 0
    next_func :: Set.Set State
    next_func = result
      where
        value1 = 1
        value2 = 3
        varA_vals = Set.fromList [value1, value2]
        result = Set.foldr (Set.union . next_func) Set.empty varA_vals
          where
            next_func :: Integer -> Set.Set State
            next_func varA_val = result
              where
                value1 = (-) varA_val 1
                varB_vals = Set.fromList [value1]
                result = Set.foldr (Set.union . next_func) Set.empty varB_vals
                  where
                    next_func :: Integer -> Set.Set State
                    next_func varB_val = result
                      where
                        result = Set.singleton (State varA_val varB_val Invalid Invalid Invalid)

nextStates :: State -> Set.Set State
nextStates state = next_func
  where
    varA_val = varA state
    varB_val = varB state
    sel_val = sel state
    check_val = check state
    act_val = act state
    next_func :: Set.Set State
    next_func = result
      where
        value1 = ifThenElse ((<) varA_val varB_val) Success Failure
        check_vals = Set.fromList [value1]
        result = Set.foldr (Set.union . next_func) Set.empty check_vals
          where
            next_func :: NodeStatus -> Set.Set State
            next_func check_val = result
              where
                value1_1 = 3
                value1_2 = 4
                value2_1 = (+) varA_val 1
                varA_vals
                  | (/=) check_val Failure = Set.singleton varA_val
                  | (==) varA_val 5 = Set.fromList [value1_1, value1_2]
                  | otherwise = Set.fromList [value2_1]
                result = Set.foldr (Set.union . next_func) Set.empty varA_vals
                  where
                    next_func :: Integer -> Set.Set State
                    next_func varA_val = result
                      where
                        varB_vals
                          | check_val /= Failure = Set.singleton varB_val
                          | otherwise = Set.fromList [(+) varB_val 1, (*) varB_val 2]
                        result = Set.foldr (Set.union . next_func) Set.empty varB_vals
                          where
                            next_func :: Integer -> Set.Set State
                            next_func varB_val = result
                              where
                                act_vals
                                  | check_val /= Failure = Set.singleton Invalid
                                  | otherwise = Set.fromList [Success]
                                result = Set.foldr (Set.union . next_func) Set.empty act_vals
                                  where
                                    sel_val
                                      | elem Success [check_val, act_val] = Success
                                      | elem Running [check_val, act_val] = Running
                                      | otherwise = Failure
                                    next_func :: NodeStatus -> Set.Set State
                                    next_func act_val = Set.singleton (State varA_val varB_val sel_val check_val act_val)
    
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
ctlAF function = ctlAFStateSearch function Set.empty
ctlAFStateSearch :: (State -> Bool) -> Set.Set State -> State -> Bool
ctlAFStateSearch function seenStates state
  | function state = True
  | Set.member state seenStates = False -- This means we haven't reached true and have nothing left to check
  | otherwise = Set.foldr ((&&) . ctlAFStateSearch function (Set.insert state seenStates)) True (fromJust (Map.lookup state stateMap)) -- more searching required.


ctlEF :: (State -> Bool) -> State -> Bool
ctlEF function state = (||) (function state) (ctlEFStateSearch function (Set.singleton state) (fromJust (Map.lookup state stateMap)))
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
ctlAG function state = (&&) (function state) (ctlAGStateSearch function (Set.singleton state) (fromJust (Map.lookup state stateMap)))
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
ctlEG function = ctlEGStateSearch function Set.empty
ctlEGStateSearch :: (State -> Bool) -> Set.Set State -> State -> Bool
ctlEGStateSearch function seenStates state
  | not (function state) = False -- it doesn't hold for the state, so it's not true.
  | Set.member state seenStates = True -- we've looped!
  | otherwise = Set.foldr ((||) . ctlEGStateSearch function (Set.insert state seenStates)) False (fromJust (Map.lookup state stateMap)) -- more searching required.


ctlAU :: (State -> Bool) -> (State -> Bool) -> State -> Bool
ctlAU function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctlAUStateSearch function_hold function_release (Set.singleton state) (fromJust (Map.lookup state stateMap))))
ctlAUStateSearch :: (State -> Bool) -> (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlAUStateSearch function_hold function_release seenStates statesToExplore
  | Set.null unexploredStates = False -- we ran out of states and at least one path didn't terminate with the release.
  | otherwise = conclusion
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    notReleasedStates = Set.filter (not . function_release) unexploredStates -- Filter so we only have states where the release condition is false.
    allTrue = Set.foldr ((&&) . function_hold) True notReleasedStates -- check if the condition holds for all of the not released states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctlAUStateSearch function_hold function_release (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty notReleasedStates) -- keep searching


ctlEU :: (State -> Bool) -> (State -> Bool) -> State -> Bool
ctlEU function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctlEUStateSearch function_hold function_release (Set.singleton state) (fromJust (Map.lookup state stateMap))))
ctlEUStateSearch :: (State -> Bool) -> (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlEUStateSearch function_hold function_release seenStates statesToExplore
  | Set.null unexploredStates = False -- we ran out of states and no path terminated with the release.
  | otherwise = conclusion
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    releaseFound = Set.foldr ((||) . function_release) False unexploredStates -- check if the condition holds for all of the not released states
    holdingStates = Set.filter function_hold unexploredStates -- Filter so we only have states where the release condition is false.
    conclusion
      | releaseFound = True -- we managed to reach the release
      | otherwise = ctlEUStateSearch function_hold function_release (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty holdingStates) -- keep searching


ctlAW :: (State -> Bool) -> (State -> Bool) -> State -> Bool
ctlAW function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctlAWStateSearch function_hold function_release Set.empty (fromJust (Map.lookup state stateMap))))
ctlAWStateSearch :: (State -> Bool) -> (State -> Bool) -> Set.Set State -> Set.Set State -> Bool
ctlAWStateSearch function_hold function_release seenStates statesToExplore
  | Set.null unexploredStates = True -- we ran out of states and there were no problems
  | otherwise = conclusion
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    notReleasedStates = Set.filter (not . function_release) unexploredStates -- Filter so we only have states where the release condition is false.
    allTrue = Set.foldr ((&&) . function_hold) True notReleasedStates -- check if the condition holds for all of the not released states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctlAWStateSearch function_hold function_release (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty notReleasedStates) -- keep searching


ctlEW :: (State -> Bool) -> (State -> Bool) -> State -> Bool
ctlEW function_hold function_release = ctlEWStateSearch function_hold function_release Set.empty
ctlEWStateSearch :: (State -> Bool) -> (State -> Bool) -> Set.Set State -> State -> Bool
ctlEWStateSearch function_hold function_release seenStates state
  | function_release state = True
  | not (function_hold state) = False
  | otherwise = Set.foldr ((||) . ctlEWStateSearch function_hold function_release (Set.insert state seenStates)) False (fromJust (Map.lookup state stateMap)) -- more searching required.


ctl1 :: Bool
ctl1 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlAF (\state -> (>) (varB state) (varA state)) state

ctl2 :: Bool
ctl2 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlEF (\state -> (>) (varB state) (varA state)) state

ctl3 :: Bool
ctl3 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = (||) (ctlAF (\state -> (>) (varB state) (varA state)) state) (ctlAG (\state -> (==) (varB state) 0) state)

ctl4 :: Bool
ctl4 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlAG (\state -> (||) (ctlAF (\state -> (>) (varB state) (varA state)) state) ((==) (varB state) 0)) state

    

ctl5 :: Bool
ctl5 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlAW (\state -> (==) (varB state) 0) (\state -> (ctlAF (\state -> (<) (varA state) (varB state)) state)) state


ctl6 :: Bool
ctl6 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlAW (\state -> (==) (varB state) 0) (\state -> (>) (varB state) 0) state

ctl7 ::Bool
ctl7 = Set.foldr ((&&) . ctl_func) True initialStates
  where
    ctl_func :: State -> Bool
    ctl_func state = ctlAF (\state -> (>) (varA state) 1) state

main :: IO ()
main =
  do {
    -- print reachableStates
    -- print stateMap
    print initialStates
    ; print ctl1
    ; print ctl2
    ; print ctl3
    ; print ctl4
    ; print ctl5
    ; print ctl6
    ; print ctl7
  }
