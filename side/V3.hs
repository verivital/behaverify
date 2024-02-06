module V3 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )

data State = State {
  varA :: Integer
  , varB :: Integer
  , varC :: Integer
  }
  deriving (Eq, Ord, Show)


ifThenElse :: Bool -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val

initalStates = iStates
  where
    varA_init_func :: Integer -> Set.Set Integer
    varA_init_func _ = result_true
      where
        result_true = Set.fromList [1, 2, 3]
    varA_init = varA_init_func 0
    varB_init_func :: Integer -> Set.Set Integer
    varB_init_func _ = result_true
      where
        valueFunc :: Integer -> Set.Set Integer
        valueFunc varA_val = Set.fromList [0, (*) varA_val 2]
        result_true = Set.unions [valueFunc varA_val | varA_val <- Set.toList varA_init]
    varB_init = varB_init_func 0
    varC_init_func :: Integer -> Set.Set Integer
    varC_init_func _ = result_true
      where
        valueFunc :: Integer -> Set.Set Integer
        valueFunc varB_val = Set.fromList [0, (*) varB_val 2]
        result_true = Set.unions [valueFunc varB_val | varB_val <- Set.toList varB_init]
    varC_init = varC_init_func 0
    iStates = Set.fromList [state varA_val varB_val varC_val | varA_val <- Set.toList varA_init, varB_val <- Set.toList varB_init, varC_val <- Set.toList varC_init]
      

nextStates :: State -> Set.Set State
nextStates state = nextStates
  where
    varA_stage0 = Set.singleton (varA state)
    varB_stage0 = Set.singleton (varB state)
    varC_stage0 = Set.singleton (varC state)
    varA_stage1_func :: Integer -> Set.Set Integer
    varA_stage1_func 0
      | guardTrue && guardFalse = Set.union resultTrue resultFalse
      | guardTrue = resultTrue
      | otherwise = resultFalse
      where
        guardTrue = any guardVals
        guardFalse = not (all guardVals)
        guardFunc :: Integer -> Integer -> Bool
        guardFunc varA_val varB_val = (<) (varA_val) (varB_val)
        guardVals = [guardFunc varA_val varB_val | varA_val <- Set.toList varA_stage0, varB_val <- Set.toList varB_stage0]
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varA_val = Set.singleton varA_val
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <- Set.toList varA_stage0]
          )
        resultFalse = varA_stage1_func 1
    varA_stage1_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc varA_val = Set.fromSingleton ((+) varA_val 1)
        valueFunc2 :: Integer -> Set.Set Integer
        valueFunc varB_val = Set.fromSingleton ((-) varB_val 1)
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <-Set.toList  varA_stage0]
          ++
          [valueFunc2 varB_val
          | varB_val <- Set.toList varB_stage0]
    varA_stage1 = varA_stage1_func 0
    varB_stage1_func :: Integer -> Set.Set Integer
    varB_stage1_func 0
      | guardTrue && guardFalse = Set.union resultTrue resultFalse
      | guardTrue = resultTrue
      | otherwise = resultFalse
      where
        guardTrue = any guardVals
        guardFalse = not (all guardVals)
        guardFunc :: Integer -> Integer -> Bool
        guardFunc varA_val varB_val = (<) (varA_val) (varB_val)
        guardVals = [guardFunc varA_val varB_val | varA_val <- Set.toList varA_stage1, varB_val <- Set.toList varB_stage0]
        valueFunc :: Integer -> Set.Set Integer
        valueFunc varC_val = Set.singleton varC_val
        resultTrue = Set.unions [valueFunc varC_val
                                | varC_val <- Set.toList varC_stage0]
        resultFalse = varB_stage1_func 1
    varB_stage1_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varA_val = Set.singleton ((+) varA_val 1)
        valueFunc2 ::  Integer -> Set.Set Integer
        valueFunc2 varB_val = Set.singleton ((*) varB_val 3)
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <- Set.toList varA_stage1]
          ++
          [valueFunc2 varB_val
          | varB_val <- Set.toList varB_stage0]
          )
    varB_stage1 = varB_stage1_func 0
    varC_stage1_func :: Integer -> Set.Set Integer
    varC_stage1_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc varA_val = Set.singleton varA_val
        valueFunc2 :: Integer -> Set.Set Integer
        valueFunc varB_val = Set.singleton varB_val
        valueFunc3 :: Integer -> Set.Set Integer
        valueFunc varC_val = Set.singleton varC_val
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <- Set.toList varA_stage1]
          ++
          [valueFunc2 varB_val
          | varB_val <- Set.toList varB_stage1]
          ++
          [valueFunc3 varC_val
          | varC_val <- Set.toList varC_stage1]
          )
    varC_stage1 = varC_stage1_func 0
    varA_stage2_func :: Integer -> Set.Set Integer
    varA_stage2_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varA_val = Set.singleton (min 15 (max varA_val 0))
        resultTrue = Set.unions (
          [valueFunc1 varA_val
          | varA_val <- Set.toList varA_stage1]
          )
    varA_stage2 = varA_stage2_func 0
    varB_stage2_func :: Integer -> Set.Set Integer
    varB_stage2_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varB_val = Set.singleton (min 15 (max varB_val 0))
        resultTrue = Set.unions (
          [valueFunc1 varB_val
          | varB_val <- Set.toList varB_stage1]
          )
    varB_stage2 = varB_stage2_func 0
    varC_stage2_func :: Integer -> Set.Set Integer
    varC_stage2_func _ = resultTrue
      where
        valueFunc1 :: Integer -> Set.Set Integer
        valueFunc1 varC_val = Set.singleton (min 15 (max varC_val 0))
        resultTrue = Set.unions (
          [valueFunc1 varC_val
          | varC_val <- Set.toList varC_stage1]
          )
    varC_stage2 = varC_stage2_func 0
    nextStates = Set.fromList [state varA_val varB_val varC_val | varA_val <- Set.toList varA_stage2, varB_val <- Set.toList varB_stage2, varC_val <- Set.toList varC_stage2]
    
    -- varA_stage1_func :: Integer -> [Integer]
    -- varA_stage1 = foldr concat [
    --   (ifThenElse
    --    ((<) (varA_val) (varB_val))
    --    [varA_val]
    --    [((+) varA_val 1), ((-) varB_val 1)])
    --   | varA_val <- varA_stage0
    --   , varB_val <- varB_stage0]
    -- varB_stage1 = foldr concat [
    --   (ifThenElse
    --    ((<) (varA_val) (varB_val))
    --    [varC_val]
    --    [((+) varA_val 1), ((*) varB_val 3)])
    --   | varA_val <- varA_stage1
    --   , varB_val <- varB_stage0
    --   , varC_val <- varC_stage0]
    -- varC_stage1 = foldr concat [
    --   [varA_val, varB_val, varC_val]
    --   | varA_val <- varA_stage1
    --   , varB_val <- varB_stage1
    --   , varC_val <- varC_stage0]
    -- varA_stage2 = foldr concat [
    --   (min 15 (max varA_val 0))
    --   | varA_val <- varA_stage1]
    -- varB_stage2 = foldr concat [
    --   (min 15 (max varB_val 0))
    --   | varB_val <- varB_stage1]
    -- varC_stage2 = foldr concat [
    --   (min 15 (max varC_val 0))
    --   | varC_val <- varC_stage1]
    -- nextStates = Set.fromList [state varA_val varB_val varC_val | varA_val <- varA_stage2, varB_val <- varB_stage2, varC_val <- varC_stage2]
    
reachableStates = reachableStatesFunc Set.empty initialStates
  where
    reachableStatesFunc :: Set.Set State -> Set.Set State -> Set.Set State
    reachableStatesFunc seenStates statesToExplore
      | Set.null unvisitedStates = seenStates
      | otherwise = reachable
      where
        unvisitedStates = Set.difference statesToExplore seenStates
        reachable = reachableStatesFunc (Set.union seenStates unvisitedStates) (Set.unions (Set.map nextStates unvisitedStates))

stateMap = constructStateMap
  where
    constructStateMap :: StateMap -> StateMap -> StateMap
    constructStateMap seenMap toExploreMap
      | Map.null unvisitedMap = seenMap
      | otherwise = fullMap
      where
        unvisitedMap = Map.difference toExploreMap seenMap
        exploredMap = Map.mapWithKey (dummyNextState nextElements 0) unvisitedMap
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
