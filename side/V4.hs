module V4 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array.IArray as IArray

data State = State {
  varA :: Integer
  , varB :: Array Integer Integer
  }
  deriving (Eq, Ord, Show)


type StateMap = Map.Map State (Set.Set State)


ifThenElse :: Bool -> a -> a -> a
ifThenElse True val _ = val
ifThenElse False _ val = val

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
        guardFunc :: (Array Integer Integer) -> Integer -> Bool
        guardFunc varB_val varA_val = (/=) (varB_val ! varA_val) (0)
        guardVals = [guardFunc varB_val varA_val | varA_val <- Set.toList varA_stage1, varB_val <- Set.toList varB_stage0]
        valueFunc1 :: (Array Integer Integer) -> Set.Set (Array Integer Integer)
        valueFunc1 varB_val = Set.singleton varB_val
        resultTrue = Set.unions [valueFunc1 varB_val
                                | varB_val <- Set.toList varB_stage0]
        resultFalse = varB_stage1_func 1
    varB_stage1_func _ = resultTrue
      where
        valueFunc1 :: (Array Integer Integer) -> Integer -> Set.Set (Array Integer Integer)
        valueFunc1 varB_val varA_val = Set.singleton (IArray.array (0, 3) [(index, (ifThenElse (index == varA_val) ((*) ((+) varA_val 1) (-1)) (varB_val ! index))) | index <- [0..3]])
        valueFunc2 :: (Array Integer Integer) -> Integer -> Set.Set (Array Integer Integer)
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
    
reachableStates = reachableStatesFunc Set.empty initialStates
  where
    reachableStatesFunc :: Set.Set State -> Set.Set State -> Set.Set State
    reachableStatesFunc seenStates statesToExplore
      | Set.null unvisitedStates = seenStates
      | otherwise = reachable
      where
        unvisitedStates = Set.difference statesToExplore seenStates
        reachable = reachableStatesFunc (Set.union seenStates unvisitedStates) (Set.unions (Set.map nextStates unvisitedStates))

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


ctl1 = Set.foldr ((&&) . ctlFunc0) True initialStates
  where
    ctlFunc0 :: State -> Bool
    ctlFunc0 state = Set.foldr ((&&) . ctlFunc1) True (fromJust (Map.lookup state stateMap))
    ctlFunc1 :: State -> Bool
    ctlFunc1 state = (<) (varA state) 10

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
