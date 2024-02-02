module V2 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map

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

updateIntegerByID :: State -> VariableID -> Integer -> State
updateIntegerByID state 0 val = state { vInt1 = val}
updateIntegerByID state 1 val = state { vInt2 = val}
updateIntegerByID _ _ _ = error "illegal varID"
updateDoubleByID :: State -> VariableID -> Double -> State
updateDoubleByID state 2 val = state { vDouble1 = val}
updateDoubleByID _ _ _ = error "illegal varID"
updateBoolByID :: State -> VariableID -> Bool -> State
updateBoolByID state 3 val = state { vBool1 = val}
updateBoolByID state 4 val = state { vBool2 = val}
updateBoolByID _ _ _ = error "illegal varID"

varIDToInteger :: State -> VariableID -> Integer
varIDToInteger state 0 = vInt1 state
varIDToInteger state 1 = vInt2 state
varIDToInteger _ _ = error "illegal varID"

varIDToDouble :: State -> VariableID -> Double
varIDToDouble state 2 = vDouble1 state
varIDToDouble _ _ = error "illegal varID"

varIDToBool :: State -> VariableID -> Bool
varIDToBool state 3 = vBool1 state
varIDToBool state 4 = vBool2 state
varIDToBool _ _ = error "illegal varID"


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
  IntegerElement IntegerElement
  | DoubleElement DoubleElement
  | BoolElement BoolElement

data BoolElement =
  BConst Bool
  | BVar VariableID
  | BEqB (Bool -> Bool) BoolElement
  | IIEqB (Integer -> Integer -> Bool) IntegerElement IntegerElement
  
data IntegerElement =
  IConst Integer
  | IVar VariableID
  | IEqI (Integer -> Integer) IntegerElement
  | IIEqI (Integer -> Integer -> Integer) IntegerElement IntegerElement
  | BIIEqI (Bool -> Integer -> Integer -> Integer) BoolElement IntegerElement IntegerElement
  | DEqI (Double -> Integer) DoubleElement

data DoubleElement =
  DConst Double
  | DVar VariableID
  | DEqD (Double -> Double) DoubleElement
  | DDEqD (Double -> Double -> Double) DoubleElement DoubleElement
  | IEqD (Integer -> Double) IntegerElement


data LTLElement =
  LTLGlobally BoolElement
  | LTLFinally BoolElement
  | LTLNext BoolElement
  | LTLUntil BoolElement BoolElement

evaluateIntegerElement :: State -> IntegerElement -> Integer
evaluateIntegerElement _ (IConst val) = val
evaluateIntegerElement state (IVar varID) = varIDToInteger state varID
evaluateIntegerElement state (IEqI func iEl) = func (evaluateIntegerElement state iEl)
evaluateIntegerElement state (IIEqI func iEl iEl2) = func (evaluateIntegerElement state iEl) (evaluateIntegerElement state iEl2)
evaluateIntegerElement state (BIIEqI func bEl iEl iEl2) = func (evaluateBoolElement state bEl) (evaluateIntegerElement state iEl) (evaluateIntegerElement state iEl2)
evaluateIntegerElement state (DEqI func dEl) = func (evaluateDoubleElement state dEl)

evaluateBoolElement :: State -> BoolElement -> Bool
evaluateBoolElement _ (BConst val) = val
evaluateBoolElement state (BVar varID) = varIDToBool state varID
evaluateBoolElement state (BEqB func bEl) = func (evaluateBoolElement state bEl)
evaluateBoolElement state (IIEqB func iEl iEl2) = func (evaluateIntegerElement state iEl) (evaluateIntegerElement state iEl2)


evaluateDoubleElement :: State -> DoubleElement -> Double
evaluateDoubleElement state (DEqD func dEl) = func (evaluateDoubleElement state dEl)
evaluateDoubleElement state (DDEqD func dEl dEl2) = func (evaluateDoubleElement state dEl) (evaluateDoubleElement state dEl2)
evaluateDoubleElement state (IEqD func iEl) = func (evaluateIntegerElement state iEl)
evaluateDoubleElement state (DVar varID) = varIDToDouble state varID
evaluateDoubleElement _ (DConst val) = val


-- evaluateLTLElement :: State -> StateMap -> LTLElement -> Bool
-- evaluateLTLElement startState stateMap (LTLNext bEl) = and ([evaluateBoolElement state bEl | state <- stepStateMap startState 1]) 


ifThenElse :: Bool -> a -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val


-- evaluateElement ::  Element -> State -> Element
-- evaluateElement (IntegerElement el) state = IConst (evaluateIntegerElement el state)
-- evaluateElement (DoubleElement el) state = DConst (evaluateDoubleElement el state)


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
    newSeenStates = Set.union exploreStates seenStates
    reachableStates = allStates elements newSeenStates nextStates


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
    mapM_ print (constructStateMap initialElements nextElements defaultState)
  }
  where
    defaultState = State 0 0 0.0 False False
    initialElements = [[IntegerElement (IConst 5)], [IntegerElement (IVar 0), IntegerElement (IIEqI (+) (IVar 0) (IVar 1))], [DoubleElement (DConst 3.4), DoubleElement (DDEqD (*) (DVar 2) (DConst 0.5)), DoubleElement (DConst 3.4)]]
    nextElements = [[IntegerElement (BIIEqI (ifThenElse) (IIEqB (<) (IVar 0) (IConst 10)) (IIEqI (+) (IVar 0) (IConst 1)) (IConst 0))]]
    initialStates = nextState initialElements 0 defaultState
    reachableStates = allStates nextElements Set.empty initialStates
    invariants = [(IIEqB (<=) (IVar 0) (IConst 8)), (IIEqB (>) (IVar 0) (IConst 0)), (IIEqB (>=) (IVar 0) (IConst 0))]
    
