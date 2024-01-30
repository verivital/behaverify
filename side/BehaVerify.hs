module BehaVerify where

data State = State {
  x_stage_0 :: Bool
  , x_stage_1 :: Bool
  , y_stage_0 :: Bool
  , y_stage_1 :: Bool
  }

stateToString :: State -> String
stateToString state = "(" ++ (show (x_stage_0 state)) ++ (show (x_stage_1 state)) ++ (show (y_stage_0 state)) ++ (show (y_stage_1 state)) ++ ")"

updateByID :: State -> VariableID -> Bool -> State
updateByID state 0 val = state { x_stage_0 = val}
updateByID state 1 val = state { x_stage_1 = val}
updateByID state 2 val = state { y_stage_0 = val}
updateByID state 3 val = state { y_stage_1 = val}

varIDToVarVal :: VariableID -> State -> Bool
varIDToVarVal 0 state = x_stage_0 state
varIDToVarVal 1 state = x_stage_1 state
varIDToVarVal 2 state = y_stage_0 state
varIDToVarVal 3 state = y_stage_1 state
varIDToVarVal _ _ = error "illegal varID"

data Function = EQ | NE | OR | AND
  deriving (Enum)

convertFunction :: FunctionID -> (Bool -> Bool -> Bool)
convertFunction 1 = sereneEQ
convertFunction 2 = sereneNE
convertFunction 3 = sereneOR
convertFunction 4 = sereneAND
convertFunction _ = error "illegal function"

sereneEQ :: Bool -> Bool -> Bool
sereneEQ a b = a == b

sereneNE :: Bool -> Bool -> Bool
sereneNE a b = a /= b

sereneOR :: Bool -> Bool -> Bool
sereneOR a b = a || b

sereneAND :: Bool -> Bool -> Bool
sereneAND a b = a && b


type FunctionID = Integer -- 1=eq, 2=ne, 3=or, 4=and
type ElementType = Integer -- 1=Condition, 2=Variable, 3=Constant
type VariableID = Integer
type ConstantVal = Bool

type PredicateValue = (ElementType, PredicateEquation, VariableID, ConstantVal) -- Element type determines which one is relevant, Condition is more code, first Integer is 

data PredicateEquation = PredicateEquation {
  function :: FunctionID
  , arg1 :: PredicateValue
  , arg2 :: PredicateValue
  }

evaluatePredicate :: State -> PredicateValue -> Bool
evaluatePredicate _ (3, _, _, a) = a
evaluatePredicate state (2, _, a, _) = varIDToVarVal a state
evaluatePredicate state (1, pred, _, _) = (convertFunction (function pred)) (evaluatePredicate state (arg1 pred)) (evaluatePredicate state (arg2 pred))
evaluatePredicate _ _ = error "invalid Predicate Equation"


nextVariable :: State -> [PredicateValue] -> [Bool]
nextVariable state conditions = result
  where
    result
      | falsePossible && truePossible = [True, False]
      | truePossible = [True]
      | falsePossible = [False]
      | otherwise = error "no valid value"
    falsePossible = not (and (map evaluatePredicate conditions))
    truePossible = or (map evaluatePredicate conditions)

nextState :: [[PredicateValue]] -> VariableID -> State -> [State]
nextState (conditions:future) varID state = nxtStates
  where
    curStates = map (updateById state varID) (nextVariable state conditions)
    nxtStates = map (nextState future (varID + 1)) curStates
    


main :: IO ()
main =
  do {
    mapM_ putStrLn (map stateToString (nextState conds 0 initState))
  }
  where
    emptyEq = PredicateEquation {0
    initState = State False False False False
    conds = [[(True], [True, 
