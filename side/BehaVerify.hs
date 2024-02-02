module BehaVerify where


data ConstantValue = ConstantInteger Integer | ConstantBool Bool | ConstantDouble Double
data State = State {
  vInt1 :: Integer
  , vInt2 :: Integer
  , vBool1 :: Bool
  , vBool2 :: Bool
  }

type VariableID = Integer

stateToString :: State -> String
stateToString state = "(" ++ show (vInt1 state) ++ ", " ++ show (vInt2 state) ++ ", " ++ show (vBool1 state) ++ ", " ++ show (vBool2 state) ++ ")"

updateByID :: State -> VariableID -> ConstantValue -> State
updateByID state 0 (ConstantInteger val) = state { vInt1 = val}
updateByID state 1 (ConstantInteger val) = state { vInt2 = val}
updateByID state 2 (ConstantBool val) = state { vBool1 = val}
updateByID state 3 (ConstantBool val) = state { vBool2 = val}
updateByID _ _ _ = error "illegal varID"

varIDToVarVal :: VariableID -> State -> ConstantValue
varIDToVarVal 0 state = ConstantInteger (vInt1 state)
varIDToVarVal 1 state = ConstantInteger (vInt2 state)
varIDToVarVal 2 state = ConstantBool (vBool1 state)
varIDToVarVal 3 state = ConstantBool (vBool2 state)
varIDToVarVal _ _ = error "illegal varID"

type OneArgFunc = Element -> State -> ConstantValue
type TwoArgFunc = Element -> Element -> State -> ConstantValue


numToBool2 :: ((RealFrac a, RealFrac b) => a -> b -> Bool) -> ConstantValue -> ConstantValue -> ConstantValue
numToBool2 function (ConstantInteger cArg1) (ConstantInteger cArg2) = ConstantBool (function cArg1 cArg2)
numToBool2 function (ConstantInteger cArg1) (ConstantDouble cArg2) = ConstantBool (function cArg1 cArg2)
numToBool2 function (ConstantDouble cArg1) (ConstantInteger cArg2) = ConstantBool (function cArg1 cArg2)
numToBool2 function (ConstantDouble cArg1) (ConstantDouble cArg2) = ConstantBool (function cArg1 cArg2)
numToBool2 _ _ _ = error "illegal arguments"

numToNum2 :: (a -> a -> a) -> ConstantValue -> ConstantValue -> ConstantValue
numToNum2 function (ConstantInteger cArg1) (ConstantInteger cArg2) = ConstantInteger (function cArg1 cArg2)
numToNum2 function (ConstantInteger cArg1) (ConstantDouble cArg2) = ConstantDouble (function cArg1 cArg2)
numToNum2 function (ConstantDouble cArg1) (ConstantInteger cArg2) = ConstantDouble (function cArg1 cArg2)
numToNum2 function (ConstantDouble cArg1) (ConstantDouble cArg2) = ConstantDouble (function cArg1 cArg2)
numToNum2 _ _ _ = error "illegal arguments"

boolToBool2 :: (Bool -> Bool -> Bool) -> ConstantValue -> ConstantValue -> ConstantValue
boolToBool2 function (ConstantBool cArg1) (ConstantBool cArg2) = ConstantBool (function cArg1 cArg2)
boolToBool2 _ _ _ = error "illegal arguments"



eqFunc :: TwoArgFunc
eqFunc arg1 arg2 state = result
  where
    comparison :: ConstantValue -> ConstantValue -> ConstantValue
    comparison (ConstantBool cArg1) (ConstantBool cArg2) = ConstantBool (cArg1 == cArg2)
    comparison (ConstantInteger cArg1) (ConstantInteger cArg2) = ConstantBool (cArg1 == cArg2)
    comparison (ConstantInteger cArg1) (ConstantDouble cArg2) = ConstantBool (cArg1 == cArg2)
    comparison (ConstantDouble cArg1) (ConstantInteger cArg2) = ConstantBool (cArg1 == cArg2)
    comparison (ConstantDouble cArg1) (ConstantDouble cArg2) = ConstantBool (cArg1 == cArg2)
    comparison _ _ = error "illegal comparison"
    constantValue1 = evaluateElement arg1 state
    constantValue2 = evaluateElement arg2 state
    result = comparison constantValue1 constantValue2

data Element =
  ElementEquation1 OneArgFunc Element
  | ElementEquation2 TwoArgFunc Element Element
  | ElementVariable VariableID
  | ElementConstant ConstantValue

evaluateElement ::  Element -> State -> ConstantValue
evaluateElement (ElementConstant val) _ = val
evaluateElement (ElementVariable varID) state = varIDToVarVal varID state
evaluateElement (ElementEquation1 curFun arg1) state = curFun arg1 state
evaluateElement (ElementEquation2 curFun arg1 arg2) state = curFun arg1 arg2 state
--evaluateElement _ = error "invalid Predicate Equation"


getPossibleValues :: [Element] -> State -> [ConstantValue]
getPossibleValues elements state = possibleValues
  where
    result
      | falsePossible && truePossible = [True, False]
      | truePossible = [True]
      | falsePossible = [False]
      | otherwise = error "no valid value"
    --falsePossible = not (and (map (evaluateElement state) conditions))
    falsePossible = not (all (evaluateElement state) conditions)
    --truePossible = or (map (evaluateElement state) conditions)
    truePossible = any (evaluateElement state) conditions

nextState :: [[Element]] -> VariableID -> State -> [State]
nextState [] _ state = [state]
nextState (conditions:future) varID state = nxtStates
  where
    curStates = map (updateByID state varID) (nextVariable state conditions)
    nxtStates = concatMap (nextState future (varID + 1)) curStates
    


main :: IO ()
main =
  do {
    --mapM_ print (nextVariable initState [ElementConstant True, ElementConstant False])
    --mapM_ (putStrLn . stateToString) (map (updateByID initState 0) (nextVariable initState [ElementConstant True, ElementConstant False]))
    mapM_ (putStrLn . stateToString) (nextState conds 0 initState)
    --mapM_ (putStrLn . stateToString) (states)
  }
  where
    initState = State False False False False
    --initState = State False
    --states = [State False, State True]
    conds = [[ElementConstant True], [ElementConstant False, ElementConstant True], [ElementVariable 0], [ElementEquation2 3 (ElementVariable 0) (ElementVariable 1)]]
    --conds = [[ElementConstant True], [ElementConstant True], [ElementConstant True], [ElementConstant False, ElementConstant True]]
    --conds = [[ElementConstant True, ElementConstant False]]
    --conds = [[ElementConstant True]]
    --conds = [[ElementConstant False]]
