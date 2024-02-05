module V2 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )

data State = State {
  vInt1 :: Integer
  , vInt2 :: Integer
  , vDouble1 :: Double
  , vBool1 :: Bool
  , vBool2 :: Bool
  }
  deriving (Eq, Ord, Show)

type StateMap = Map.Map State (Set.Set State)

type VariableID = Integer

stateToString :: State -> String
stateToString state = "(" ++ show (vInt1 state) ++ ", " ++ show (vInt2 state) ++ ", " ++ show (vDouble1 state) ++ ", " ++ show (vBool1 state) ++ ", " ++ show (vBool2 state) ++ ")"

updateBoolByID :: State -> VariableID -> Bool -> State
updateBoolByID state 3 val = state { vBool1 = val}
updateBoolByID state 4 val = state { vBool2 = val}
updateBoolByID _ _ _ = error "illegal varID"

updateIntegerByID :: State -> VariableID -> Integer -> State
updateIntegerByID state 0 val = state { vInt1 = val}
updateIntegerByID state 1 val = state { vInt2 = val}
updateIntegerByID _ _ _ = error "illegal varID"

updateDoubleByID :: State -> VariableID -> Double -> State
updateDoubleByID state 2 val = state { vDouble1 = val}
updateDoubleByID _ _ _ = error "illegal varID"

varIDToBool :: State -> VariableID -> Bool
varIDToBool state 3 = vBool1 state
varIDToBool state 4 = vBool2 state
varIDToBool _ _ = error "illegal varID"

varIDToInteger :: State -> VariableID -> Integer
varIDToInteger state 0 = vInt1 state
varIDToInteger state 1 = vInt2 state
varIDToInteger _ _ = error "illegal varID"

varIDToDouble :: State -> VariableID -> Double
varIDToDouble state 2 = vDouble1 state
varIDToDouble _ _ = error "illegal varID"

data VarType = VarInteger | VarDouble | VarBool
  deriving (Enum, Eq)

varIDToType :: VariableID -> VarType
varIDToType 0 = VarInteger
varIDToType 1 = VarInteger
varIDToType 2 = VarDouble
varIDToType 3 = VarBool
varIDToType 4 = VarBool
varIDToType _ = error "illegal varID"

data Element =
  BoolElement BoolElement
  | IntegerElement IntegerElement
  | DoubleElement DoubleElement

data BoolElement =
  BConst Bool
  | BVar VariableID
  | BEqB (Bool -> Bool) BoolElement
  | IEqB (Integer -> Bool) IntegerElement
  | DEqB (Double -> Bool) DoubleElement
  | BBEqB (Bool -> Bool -> Bool) BoolElement BoolElement
  | IIEqB (Integer -> Integer -> Bool) IntegerElement IntegerElement
  | DDEqB (Double -> Double -> Bool) DoubleElement DoubleElement
  | BBBEqB (Bool -> Bool -> Bool -> Bool) BoolElement BoolElement BoolElement
  
data IntegerElement =
  IConst Integer
  | IVar VariableID
  | BEqI (Bool -> Integer) BoolElement
  | IEqI (Integer -> Integer) IntegerElement
  | DEqI (Double -> Integer) DoubleElement
  | BBEqI (Bool -> Bool -> Integer) BoolElement BoolElement
  | IIEqI (Integer -> Integer -> Integer) IntegerElement IntegerElement
  | DDEqI (Double -> Double -> Integer) DoubleElement DoubleElement
  | BIIEqI (Bool -> Integer -> Integer -> Integer) BoolElement IntegerElement IntegerElement

data DoubleElement =
  DConst Double
  | DVar VariableID
  | BEqD (Bool -> Double) BoolElement
  | IEqD (Integer -> Double) IntegerElement
  | DEqD (Double -> Double) DoubleElement
  | BBEqD (Bool -> Bool -> Double) BoolElement BoolElement
  | IIEqD (Integer -> Integer -> Double) IntegerElement IntegerElement
  | DDEqD (Double -> Double -> Double) DoubleElement DoubleElement
  | BDDEqD (Bool -> Double -> Double -> Double) BoolElement DoubleElement DoubleElement

data CTLElement =
  CTLAlwaysNext CTLElement
  | CTLExistsNext CTLElement
  | CTLAlwaysFinally CTLElement
  | CTLExistsFinally CTLElement
  | CTLAlwaysGlobally CTLElement
  | CTLExistsGlobally CTLElement
  | CTLBEqB (Bool -> Bool) CTLElement
  | CTLBBEqB (Bool -> Bool -> Bool) CTLElement CTLElement
  | CTLIIEqB (Integer -> Integer -> Bool) IntegerElement IntegerElement
  | CTLDDEqB (Double -> Double -> Bool) DoubleElement DoubleElement
  | CTLBVar VariableID
  | CTLBConst Bool

evaluateBoolElement :: State -> BoolElement -> Bool
evaluateBoolElement _ (BConst val) = val
evaluateBoolElement state (BVar varID) = varIDToBool state varID
evaluateBoolElement state (BEqB func bEl) = func (evaluateBoolElement state bEl)
evaluateBoolElement state (IEqB func iEl) = func (evaluateIntegerElement state iEl)
evaluateBoolElement state (DEqB func dEl) = func (evaluateDoubleElement state dEl)
evaluateBoolElement state (BBEqB func bEl1 bEl2) = func (evaluateBoolElement state bEl1) (evaluateBoolElement state bEl2)
evaluateBoolElement state (IIEqB func iEl1 iEl2) = func (evaluateIntegerElement state iEl1) (evaluateIntegerElement state iEl2)
evaluateBoolElement state (DDEqB func dEl1 dEl2) = func (evaluateDoubleElement state dEl1) (evaluateDoubleElement state dEl2)

evaluateIntegerElement :: State -> IntegerElement -> Integer
evaluateIntegerElement _ (IConst val) = val
evaluateIntegerElement state (IVar varID) = varIDToInteger state varID
evaluateIntegerElement state (BEqI func bEl) = func (evaluateBoolElement state bEl)
evaluateIntegerElement state (IEqI func iEl) = func (evaluateIntegerElement state iEl)
evaluateIntegerElement state (DEqI func dEl) = func (evaluateDoubleElement state dEl)
evaluateIntegerElement state (BBEqI func bEl1 bEl2) = func (evaluateBoolElement state bEl1) (evaluateBoolElement state bEl2)
evaluateIntegerElement state (IIEqI func iEl1 iEl2) = func (evaluateIntegerElement state iEl1) (evaluateIntegerElement state iEl2)
evaluateIntegerElement state (DDEqI func dEl1 dEl2) = func (evaluateDoubleElement state dEl1) (evaluateDoubleElement state dEl2)

evaluateDoubleElement :: State -> DoubleElement -> Double
evaluateDoubleElement _ (DConst val) = val
evaluateDoubleElement state (DVar varID) = varIDToDouble state varID
evaluateDoubleElement state (BEqD func bEl) = func (evaluateBoolElement state bEl)
evaluateDoubleElement state (IEqD func iEl) = func (evaluateIntegerElement state iEl)
evaluateDoubleElement state (DEqD func dEl) = func (evaluateDoubleElement state dEl)
evaluateDoubleElement state (BBEqD func bEl1 bEl2) = func (evaluateBoolElement state bEl1) (evaluateBoolElement state bEl2)
evaluateDoubleElement state (IIEqD func iEl1 iEl2) = func (evaluateIntegerElement state iEl1) (evaluateIntegerElement state iEl2)
evaluateDoubleElement state (DDEqD func dEl1 dEl2) = func (evaluateDoubleElement state dEl1) (evaluateDoubleElement state dEl2)

ctlAlwaysFinallyStateSearch :: CTLElement -> StateMap -> Set.Set State -> Set.Set State -> Set.Set State -> Bool
ctlAlwaysFinallyStateSearch ctlEl stateMap seenStates falseStates statesToExplore
  | Set.null unexploredStates = False -- This means we haven't reached true and have nothing left to check
  | Set.foldr ((||) . flip Set.member falseStates) False statesToExplore = False -- This means we found a state that we've already visited that didn't evaluate to true, meaning an infinite loop where we don't reach true is possible.
  | otherwise = conclusion -- This means we still have states to check and we haven't encountered an infinit loop
  where
    unexploredStates = Set.difference statesToExplore seenStates -- Make sure to remove any overlap
    unexploredFalseStates = Set.filter (not . evaluateCTLElementReorder stateMap ctlEl) unexploredStates -- Filter so we only have states where the condition is false.
    conclusion
      | Set.null unexploredFalseStates = True -- If the condition was true for all the states we were exploring, then we've proved that we always reach true.
      | otherwise = ctlAlwaysFinallyStateSearch ctlEl stateMap (Set.union seenStates unexploredStates) (Set.union falseStates unexploredFalseStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredFalseStates) -- more searching required.

ctlExistsFinallyStateSearch :: CTLElement -> StateMap -> Set.Set State -> Set.Set State -> Bool
ctlExistsFinallyStateSearch ctlEl stateMap seenStates statesToExplore  -- we don't have a falseStates here because the infinite negative loop is possible, only if it's forced.
  | Set.null unexploredStates = False -- This means we haven't reached true and have nothing left to check
  | otherwise = conclusion -- This means we still have things to explore.
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    foundTrue = Set.foldr ((||) . evaluateCTLElementReorder stateMap ctlEl) False unexploredStates -- check if the condition holds for any of the new states
    conclusion
      | foundTrue = True -- if the condition holds for any of the new states, then we're done.
      | otherwise = ctlExistsFinallyStateSearch ctlEl stateMap (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredStates) -- more searching required.

ctlAlwaysGloballyStateSearch :: CTLElement -> StateMap -> Set.Set State -> Set.Set State -> Bool
ctlAlwaysGloballyStateSearch ctlEl stateMap seenStates statesToExplore -- we don't have a falseStates because if we find any false states we proved it was false.
  | Set.null unexploredStates = True -- we ran out of states and found nothing wrong, return true.
  | otherwise = conclusion
  where
    unexploredStates = Set.difference statesToExplore seenStates  -- make sure to remove any overlap.
    allTrue = Set.foldr ((&&) . evaluateCTLElementReorder stateMap ctlEl) True unexploredStates -- check if the condition holds for all of the new states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't hold globally.
      | otherwise = ctlAlwaysGloballyStateSearch ctlEl stateMap (Set.union seenStates unexploredStates) (Set.foldr (Set.union . reversedMapLookup stateMap) Set.empty unexploredStates) -- keep searching

ctlExistsGloballyStateSearch :: CTLElement -> StateMap -> Set.Set State -> Set.Set State -> Bool
ctlExistsGloballyStateSearch ctlEl stateMap seenStates statesToExplore = not (ctlAlwaysFinallyStateSearch (CTLBEqB (not) ctlEl) stateMap seenStates Set.empty statesToExplore)

evaluateCTLElement :: State -> StateMap -> CTLElement -> Bool
evaluateCTLElement startState stateMap (CTLAlwaysNext ctlEl) = Set.foldr ((&&) . evaluateCTLElementReorder stateMap ctlEl) True (fromJust (Map.lookup startState stateMap))
evaluateCTLElement startState stateMap (CTLExistsNext ctlEl) = Set.foldr ((||) . evaluateCTLElementReorder stateMap ctlEl) False (fromJust (Map.lookup startState stateMap))
evaluateCTLElement startState stateMap (CTLAlwaysFinally ctlEl) = ctlAlwaysFinallyStateSearch ctlEl stateMap Set.empty Set.empty (Set.singleton startState)
evaluateCTLElement startState stateMap (CTLExistsFinally ctlEl) = ctlExistsFinallyStateSearch ctlEl stateMap Set.empty (Set.singleton startState)
evaluateCTLElement startState stateMap (CTLAlwaysGlobally ctlEl) = ctlAlwaysGloballyStateSearch ctlEl stateMap Set.empty (Set.singleton startState)
evaluateCTLElement startState stateMap (CTLExistsGlobally ctlEl) = ctlExistsGloballyStateSearch ctlEl stateMap Set.empty (Set.singleton startState)
evaluateCTLElement startState stateMap (CTLBEqB func ctlEl) = func (evaluateCTLElement startState stateMap ctlEl)
evaluateCTLElement startState stateMap (CTLBBEqB func ctlEl1 ctlEl2) = func (evaluateCTLElement startState stateMap ctlEl1) (evaluateCTLElement startState stateMap ctlEl2)
evaluateCTLElement startState _ (CTLIIEqB func iEl1 iEl2) = func (evaluateIntegerElement startState iEl1) (evaluateIntegerElement startState iEl2)
evaluateCTLElement startState _ (CTLDDEqB func dEl1 dEl2) = func (evaluateDoubleElement startState dEl1) (evaluateDoubleElement startState dEl2)
evaluateCTLElement _ _ (CTLBConst val) = val
evaluateCTLElement startState _ (CTLBVar varID) = varIDToBool startState varID

evaluateCTLElementReorder :: StateMap -> CTLElement -> State -> Bool
evaluateCTLElementReorder stateMap ctlEl state = evaluateCTLElement state stateMap ctlEl

reversedMapLookup :: StateMap -> State -> Set.Set State
reversedMapLookup stateMap state = fromJust (Map.lookup state stateMap)

evaluateCTLAllInitial :: Set.Set State -> StateMap -> CTLElement -> Bool
evaluateCTLAllInitial initialStates stateMap ctlEl = Set.foldr ((&&) . evaluateCTLElementReorder stateMap ctlEl) True initialStates

ifThenElse :: Bool -> a -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val

getPossibleIntegers :: State -> [IntegerElement] -> Set.Set Integer
getPossibleIntegers state elements = Set.fromList (map (evaluateIntegerElement state) elements)

getPossibleDoubles :: State -> [DoubleElement] -> Set.Set Double
getPossibleDoubles state elements = Set.fromList (map (evaluateDoubleElement state) elements)

nextState :: [[Element]] -> VariableID -> State -> Set.Set State
nextState [] _ state = Set.singleton state
nextState (curElements:nextElements) varID state = nextStates
  where
    varType = varIDToType varID
    curStates
      | varType == VarDouble = Set.map (updateDoubleByID state varID) (getPossibleDoubles state [x | DoubleElement x <- curElements])
      | otherwise = Set.map (updateIntegerByID state varID) (getPossibleIntegers state [x | IntegerElement x <- curElements])
    nextStates = Set.unions (Set.map (nextState nextElements (varID + 1)) curStates)
    

allStates :: [[Element]] -> Set.Set State -> Set.Set State -> Set.Set State
allStates elements seenStates exploreStates
  | Set.null actualExploreStates = seenStates
  | otherwise = reachableStates
  where
    actualExploreStates = Set.difference exploreStates seenStates
    nextStates = Set.unions (Set.map (nextState elements 0) actualExploreStates)
    reachableStates = allStates elements (Set.union seenStates actualExploreStates) nextStates


constructStateMap :: [[Element]] -> [[Element]] -> State -> StateMap
constructStateMap initialElements nextElements defaultState = stateMap
  where
    initialStates = nextState initialElements 0 defaultState
    dummyNextState :: [[Element]] -> VariableID -> State -> a -> Set.Set State
    dummyNextState arg1 arg2 arg3 _ = nextState arg1 arg2 arg3
    populateStateMap :: StateMap -> StateMap -> StateMap
    populateStateMap  seenMap exploreMap
      | Map.null toExploreMap = seenMap
      | otherwise = fullMap
      where
        toExploreMap = Map.difference exploreMap seenMap
        exploredMap = Map.mapWithKey (dummyNextState nextElements 0) toExploreMap
        newSeenMap = Map.union exploredMap seenMap
        nextExplore = Map.fromList [(newState, Set.empty) | newState <- Set.toList (Set.unions (Map.elems exploredMap))]
        fullMap = populateStateMap newSeenMap nextExplore
    stateMap = populateStateMap Map.empty (Map.fromList [(newState, Set.empty) | newState <- Set.toList initialStates])
    
checkInvariants :: [BoolElement] -> Set.Set State -> [Bool]
checkInvariants elements states = [and [evaluateBoolElement state element | state <- Set.toList states] | element <- elements]

main :: IO ()
main =
  do {
    --mapM_ (putStrLn . stateToString) initialStates
    --mapM_ (putStrLn . stateToString) reachableStates
    --mapM_ print (checkInvariants invariants reachableStates)
    print stateMap
    ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec1)
    ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec2)
    ; print (evaluateCTLAllInitial initialStates stateMap ctlSpec3)
    --; print (and [evaluateLTLElement state stateMap ltlSpecFalse  | state <- Set.toList initialStates])
    --; print (and [evaluateLTLElement state stateMap ltlSpecTrue  | state <- Set.toList initialStates])
    --; mapM_ print [Map.lookup state stateMap  | state <- Set.toList initialStates]
  }
  where
    defaultState = State 0 0 0.0 False False
    initialElements = [[IntegerElement (IConst 5)], [IntegerElement (IVar 0), IntegerElement (IIEqI (+) (IVar 0) (IVar 1))], [DoubleElement (DConst 3.4), DoubleElement (DDEqD (*) (DVar 2) (DConst 0.5)), DoubleElement (DConst 3.4)]]
    nextElements = [[IntegerElement (BIIEqI (ifThenElse) (IIEqB (<) (IVar 0) (IConst 10)) (IIEqI (+) (IVar 0) (IConst 1)) (IConst 0))]]
    initialStates = nextState initialElements 0 defaultState
    reachableStates = allStates nextElements Set.empty initialStates
    stateMap = constructStateMap initialElements nextElements defaultState
    invariants = [(IIEqB (<=) (IVar 0) (IConst 8)), (IIEqB (>) (IVar 0) (IConst 0)), (IIEqB (>=) (IVar 0) (IConst 0))]
    ctlSpec1 = CTLAlwaysFinally (CTLIIEqB (==) (IVar 0) (IConst 9))
    ctlSpec2 = CTLExistsFinally (CTLIIEqB (==) (IVar 0) (IConst 10))
    ctlSpec3 = CTLExistsFinally (CTLIIEqB (==) (IVar 0) (IConst 11))
