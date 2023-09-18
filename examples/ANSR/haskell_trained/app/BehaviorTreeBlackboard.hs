module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardPrevDestX :: Integer
  , boardPrevDestY :: Integer
  , boardCurX :: Integer
  , boardCurY :: Integer
  , boardDestX :: Integer
  , boardDestY :: Integer
  , boardDir :: Integer
  , boardVictory :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardPrevDestX: " ++ show (boardPrevDestX blackboard) ++ ", " ++ "boardPrevDestY: " ++ show (boardPrevDestY blackboard) ++ ", " ++ "boardCurX: " ++ show (boardCurX blackboard) ++ ", " ++ "boardCurY: " ++ show (boardCurY blackboard) ++ ", " ++ "boardDestX: " ++ show (boardDestX blackboard) ++ ", " ++ "boardDestY: " ++ show (boardDestY blackboard) ++ ", " ++ "boardDir: " ++ show (boardDir blackboard) ++ ", " ++ "boardVictory: " ++ show (boardVictory blackboard) ++ ", " ++ "boardXNetWeightFrom00: " ++ "[" ++ show (boardXNetWeightFrom00 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom00 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom01: " ++ "[" ++ show (boardXNetWeightFrom01 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom01 9 blackboard)++ "]" ++ ", " ++ "boardXNetBiasFrom0: " ++ "[" ++ show (boardXNetBiasFrom0 0 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 1 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 2 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 3 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 4 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 5 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 6 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 7 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 8 blackboard) ++ ", " ++ show (boardXNetBiasFrom0 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom10: " ++ "[" ++ show (boardXNetWeightFrom10 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom10 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom11: " ++ "[" ++ show (boardXNetWeightFrom11 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom11 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom12: " ++ "[" ++ show (boardXNetWeightFrom12 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom12 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom13: " ++ "[" ++ show (boardXNetWeightFrom13 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom13 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom14: " ++ "[" ++ show (boardXNetWeightFrom14 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom14 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom15: " ++ "[" ++ show (boardXNetWeightFrom15 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom15 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom16: " ++ "[" ++ show (boardXNetWeightFrom16 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom16 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom17: " ++ "[" ++ show (boardXNetWeightFrom17 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom17 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom18: " ++ "[" ++ show (boardXNetWeightFrom18 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom18 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom19: " ++ "[" ++ show (boardXNetWeightFrom19 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom19 9 blackboard)++ "]" ++ ", " ++ "boardXNetBiasFrom1: " ++ "[" ++ show (boardXNetBiasFrom1 0 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 1 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 2 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 3 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 4 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 5 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 6 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 7 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 8 blackboard) ++ ", " ++ show (boardXNetBiasFrom1 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom20: " ++ "[" ++ show (boardXNetWeightFrom20 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom20 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom21: " ++ "[" ++ show (boardXNetWeightFrom21 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom21 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom22: " ++ "[" ++ show (boardXNetWeightFrom22 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom22 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom23: " ++ "[" ++ show (boardXNetWeightFrom23 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom23 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom24: " ++ "[" ++ show (boardXNetWeightFrom24 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom24 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom25: " ++ "[" ++ show (boardXNetWeightFrom25 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom25 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom26: " ++ "[" ++ show (boardXNetWeightFrom26 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom26 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom27: " ++ "[" ++ show (boardXNetWeightFrom27 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom27 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom28: " ++ "[" ++ show (boardXNetWeightFrom28 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom28 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom29: " ++ "[" ++ show (boardXNetWeightFrom29 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom29 9 blackboard)++ "]" ++ ", " ++ "boardXNetBiasFrom2: " ++ "[" ++ show (boardXNetBiasFrom2 0 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 1 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 2 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 3 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 4 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 5 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 6 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 7 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 8 blackboard) ++ ", " ++ show (boardXNetBiasFrom2 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom30: " ++ "[" ++ show (boardXNetWeightFrom30 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom30 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom31: " ++ "[" ++ show (boardXNetWeightFrom31 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom31 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom32: " ++ "[" ++ show (boardXNetWeightFrom32 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom32 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom33: " ++ "[" ++ show (boardXNetWeightFrom33 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom33 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom34: " ++ "[" ++ show (boardXNetWeightFrom34 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom34 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom35: " ++ "[" ++ show (boardXNetWeightFrom35 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom35 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom36: " ++ "[" ++ show (boardXNetWeightFrom36 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom36 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom37: " ++ "[" ++ show (boardXNetWeightFrom37 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom37 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom38: " ++ "[" ++ show (boardXNetWeightFrom38 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom38 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom39: " ++ "[" ++ show (boardXNetWeightFrom39 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom39 9 blackboard)++ "]" ++ ", " ++ "boardXNetBiasFrom3: " ++ "[" ++ show (boardXNetBiasFrom3 0 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 1 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 2 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 3 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 4 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 5 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 6 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 7 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 8 blackboard) ++ ", " ++ show (boardXNetBiasFrom3 9 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom40: " ++ "[" ++ show (boardXNetWeightFrom40 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom40 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom41: " ++ "[" ++ show (boardXNetWeightFrom41 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom41 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom42: " ++ "[" ++ show (boardXNetWeightFrom42 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom42 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom43: " ++ "[" ++ show (boardXNetWeightFrom43 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom43 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom44: " ++ "[" ++ show (boardXNetWeightFrom44 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom44 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom45: " ++ "[" ++ show (boardXNetWeightFrom45 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom45 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom46: " ++ "[" ++ show (boardXNetWeightFrom46 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom46 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom47: " ++ "[" ++ show (boardXNetWeightFrom47 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom47 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom48: " ++ "[" ++ show (boardXNetWeightFrom48 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom48 10 blackboard)++ "]" ++ ", " ++ "boardXNetWeightFrom49: " ++ "[" ++ show (boardXNetWeightFrom49 0 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 1 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 2 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 3 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 4 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 5 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 6 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 7 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 8 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 9 blackboard) ++ ", " ++ show (boardXNetWeightFrom49 10 blackboard)++ "]" ++ ", " ++ "boardXNetBiasFrom4: " ++ "[" ++ show (boardXNetBiasFrom4 0 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 1 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 2 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 3 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 4 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 5 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 6 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 7 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 8 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 9 blackboard) ++ ", " ++ show (boardXNetBiasFrom4 10 blackboard)++ "]" ++ ", " ++ "boardXNetNode00: " ++ show (boardXNetNode00 blackboard) ++ ", " ++ "boardXNetNode01: " ++ show (boardXNetNode01 blackboard) ++ ", " ++ "boardXNetNode10: " ++ show (boardXNetNode10 blackboard) ++ ", " ++ "boardXNetNode11: " ++ show (boardXNetNode11 blackboard) ++ ", " ++ "boardXNetNode12: " ++ show (boardXNetNode12 blackboard) ++ ", " ++ "boardXNetNode13: " ++ show (boardXNetNode13 blackboard) ++ ", " ++ "boardXNetNode14: " ++ show (boardXNetNode14 blackboard) ++ ", " ++ "boardXNetNode15: " ++ show (boardXNetNode15 blackboard) ++ ", " ++ "boardXNetNode16: " ++ show (boardXNetNode16 blackboard) ++ ", " ++ "boardXNetNode17: " ++ show (boardXNetNode17 blackboard) ++ ", " ++ "boardXNetNode18: " ++ show (boardXNetNode18 blackboard) ++ ", " ++ "boardXNetNode19: " ++ show (boardXNetNode19 blackboard) ++ ", " ++ "boardXNetNode20: " ++ show (boardXNetNode20 blackboard) ++ ", " ++ "boardXNetNode21: " ++ show (boardXNetNode21 blackboard) ++ ", " ++ "boardXNetNode22: " ++ show (boardXNetNode22 blackboard) ++ ", " ++ "boardXNetNode23: " ++ show (boardXNetNode23 blackboard) ++ ", " ++ "boardXNetNode24: " ++ show (boardXNetNode24 blackboard) ++ ", " ++ "boardXNetNode25: " ++ show (boardXNetNode25 blackboard) ++ ", " ++ "boardXNetNode26: " ++ show (boardXNetNode26 blackboard) ++ ", " ++ "boardXNetNode27: " ++ show (boardXNetNode27 blackboard) ++ ", " ++ "boardXNetNode28: " ++ show (boardXNetNode28 blackboard) ++ ", " ++ "boardXNetNode29: " ++ show (boardXNetNode29 blackboard) ++ ", " ++ "boardXNetNode30: " ++ show (boardXNetNode30 blackboard) ++ ", " ++ "boardXNetNode31: " ++ show (boardXNetNode31 blackboard) ++ ", " ++ "boardXNetNode32: " ++ show (boardXNetNode32 blackboard) ++ ", " ++ "boardXNetNode33: " ++ show (boardXNetNode33 blackboard) ++ ", " ++ "boardXNetNode34: " ++ show (boardXNetNode34 blackboard) ++ ", " ++ "boardXNetNode35: " ++ show (boardXNetNode35 blackboard) ++ ", " ++ "boardXNetNode36: " ++ show (boardXNetNode36 blackboard) ++ ", " ++ "boardXNetNode37: " ++ show (boardXNetNode37 blackboard) ++ ", " ++ "boardXNetNode38: " ++ show (boardXNetNode38 blackboard) ++ ", " ++ "boardXNetNode39: " ++ show (boardXNetNode39 blackboard) ++ ", " ++ "boardXNetNode40: " ++ show (boardXNetNode40 blackboard) ++ ", " ++ "boardXNetNode41: " ++ show (boardXNetNode41 blackboard) ++ ", " ++ "boardXNetNode42: " ++ show (boardXNetNode42 blackboard) ++ ", " ++ "boardXNetNode43: " ++ show (boardXNetNode43 blackboard) ++ ", " ++ "boardXNetNode44: " ++ show (boardXNetNode44 blackboard) ++ ", " ++ "boardXNetNode45: " ++ show (boardXNetNode45 blackboard) ++ ", " ++ "boardXNetNode46: " ++ show (boardXNetNode46 blackboard) ++ ", " ++ "boardXNetNode47: " ++ show (boardXNetNode47 blackboard) ++ ", " ++ "boardXNetNode48: " ++ show (boardXNetNode48 blackboard) ++ ", " ++ "boardXNetNode49: " ++ show (boardXNetNode49 blackboard) ++ ", " ++ "boardXNetNode50: " ++ show (boardXNetNode50 blackboard) ++ ", " ++ "boardXNetNode51: " ++ show (boardXNetNode51 blackboard) ++ ", " ++ "boardXNetNode52: " ++ show (boardXNetNode52 blackboard) ++ ", " ++ "boardXNetNode53: " ++ show (boardXNetNode53 blackboard) ++ ", " ++ "boardXNetNode54: " ++ show (boardXNetNode54 blackboard) ++ ", " ++ "boardXNetNode55: " ++ show (boardXNetNode55 blackboard) ++ ", " ++ "boardXNetNode56: " ++ show (boardXNetNode56 blackboard) ++ ", " ++ "boardXNetNode57: " ++ show (boardXNetNode57 blackboard) ++ ", " ++ "boardXNetNode58: " ++ show (boardXNetNode58 blackboard) ++ ", " ++ "boardXNetNode59: " ++ show (boardXNetNode59 blackboard) ++ ", " ++ "boardXNetNode510: " ++ show (boardXNetNode510 blackboard) ++ ", " ++ "boardXNetOutputMax: " ++ show (boardXNetOutputMax blackboard) ++ ", " ++ "boardXNetOutput: " ++ show (boardXNetOutput blackboard) ++ ", " ++ "boardYNet11: " ++ show (boardYNet11 blackboard) ++ ", " ++ "boardYNet12: " ++ show (boardYNet12 blackboard) ++ ", " ++ "boardYNet13: " ++ show (boardYNet13 blackboard) ++ ", " ++ "boardYNet14: " ++ show (boardYNet14 blackboard) ++ ", " ++ "boardYNet15: " ++ show (boardYNet15 blackboard) ++ ", " ++ "boardYNet21: " ++ show (boardYNet21 blackboard) ++ ", " ++ "boardYNet22: " ++ show (boardYNet22 blackboard) ++ ", " ++ "boardYNet23: " ++ show (boardYNet23 blackboard) ++ ", " ++ "boardYNet24: " ++ show (boardYNet24 blackboard) ++ ", " ++ "boardYNet31: " ++ show (boardYNet31 blackboard) ++ ", " ++ "boardYNet32: " ++ show (boardYNet32 blackboard) ++ ", " ++ "boardYNet33: " ++ show (boardYNet33 blackboard) ++ ", " ++ "boardYNetOutput: " ++ show (boardYNetOutput blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardXNetNode00 :: BTreeBlackboard -> Integer
boardXNetNode00 blackboard = (boardDestX blackboard)
boardXNetNode01 :: BTreeBlackboard -> Integer
boardXNetNode01 blackboard = (boardPrevDestX blackboard)
boardXNetNode10 :: BTreeBlackboard -> Integer
boardXNetNode10 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 0 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 0 blackboard)) + (boardXNetBiasFrom0 0 blackboard))) 0)
boardXNetNode11 :: BTreeBlackboard -> Integer
boardXNetNode11 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 1 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 1 blackboard)) + (boardXNetBiasFrom0 1 blackboard))) 0)
boardXNetNode12 :: BTreeBlackboard -> Integer
boardXNetNode12 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 2 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 2 blackboard)) + (boardXNetBiasFrom0 2 blackboard))) 0)
boardXNetNode13 :: BTreeBlackboard -> Integer
boardXNetNode13 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 3 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 3 blackboard)) + (boardXNetBiasFrom0 3 blackboard))) 0)
boardXNetNode14 :: BTreeBlackboard -> Integer
boardXNetNode14 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 4 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 4 blackboard)) + (boardXNetBiasFrom0 4 blackboard))) 0)
boardXNetNode15 :: BTreeBlackboard -> Integer
boardXNetNode15 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 5 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 5 blackboard)) + (boardXNetBiasFrom0 5 blackboard))) 0)
boardXNetNode16 :: BTreeBlackboard -> Integer
boardXNetNode16 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 6 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 6 blackboard)) + (boardXNetBiasFrom0 6 blackboard))) 0)
boardXNetNode17 :: BTreeBlackboard -> Integer
boardXNetNode17 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 7 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 7 blackboard)) + (boardXNetBiasFrom0 7 blackboard))) 0)
boardXNetNode18 :: BTreeBlackboard -> Integer
boardXNetNode18 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 8 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 8 blackboard)) + (boardXNetBiasFrom0 8 blackboard))) 0)
boardXNetNode19 :: BTreeBlackboard -> Integer
boardXNetNode19 blackboard = (max (((boardXNetNode00 blackboard) * (boardXNetWeightFrom00 9 blackboard)) + (((boardXNetNode01 blackboard) * (boardXNetWeightFrom01 9 blackboard)) + (boardXNetBiasFrom0 9 blackboard))) 0)
boardXNetNode20 :: BTreeBlackboard -> Integer
boardXNetNode20 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 0 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 0 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 0 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 0 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 0 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 0 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 0 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 0 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 0 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 0 blackboard)) + (boardXNetBiasFrom1 0 blackboard))))))))))) 0)
boardXNetNode21 :: BTreeBlackboard -> Integer
boardXNetNode21 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 1 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 1 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 1 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 1 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 1 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 1 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 1 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 1 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 1 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 1 blackboard)) + (boardXNetBiasFrom1 1 blackboard))))))))))) 0)
boardXNetNode22 :: BTreeBlackboard -> Integer
boardXNetNode22 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 2 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 2 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 2 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 2 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 2 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 2 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 2 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 2 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 2 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 2 blackboard)) + (boardXNetBiasFrom1 2 blackboard))))))))))) 0)
boardXNetNode23 :: BTreeBlackboard -> Integer
boardXNetNode23 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 3 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 3 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 3 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 3 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 3 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 3 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 3 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 3 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 3 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 3 blackboard)) + (boardXNetBiasFrom1 3 blackboard))))))))))) 0)
boardXNetNode24 :: BTreeBlackboard -> Integer
boardXNetNode24 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 4 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 4 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 4 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 4 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 4 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 4 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 4 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 4 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 4 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 4 blackboard)) + (boardXNetBiasFrom1 4 blackboard))))))))))) 0)
boardXNetNode25 :: BTreeBlackboard -> Integer
boardXNetNode25 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 5 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 5 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 5 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 5 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 5 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 5 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 5 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 5 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 5 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 5 blackboard)) + (boardXNetBiasFrom1 5 blackboard))))))))))) 0)
boardXNetNode26 :: BTreeBlackboard -> Integer
boardXNetNode26 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 6 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 6 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 6 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 6 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 6 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 6 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 6 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 6 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 6 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 6 blackboard)) + (boardXNetBiasFrom1 6 blackboard))))))))))) 0)
boardXNetNode27 :: BTreeBlackboard -> Integer
boardXNetNode27 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 7 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 7 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 7 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 7 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 7 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 7 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 7 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 7 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 7 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 7 blackboard)) + (boardXNetBiasFrom1 7 blackboard))))))))))) 0)
boardXNetNode28 :: BTreeBlackboard -> Integer
boardXNetNode28 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 8 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 8 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 8 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 8 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 8 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 8 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 8 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 8 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 8 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 8 blackboard)) + (boardXNetBiasFrom1 8 blackboard))))))))))) 0)
boardXNetNode29 :: BTreeBlackboard -> Integer
boardXNetNode29 blackboard = (max (((boardXNetNode10 blackboard) * (boardXNetWeightFrom10 9 blackboard)) + (((boardXNetNode11 blackboard) * (boardXNetWeightFrom11 9 blackboard)) + (((boardXNetNode12 blackboard) * (boardXNetWeightFrom12 9 blackboard)) + (((boardXNetNode13 blackboard) * (boardXNetWeightFrom13 9 blackboard)) + (((boardXNetNode14 blackboard) * (boardXNetWeightFrom14 9 blackboard)) + (((boardXNetNode15 blackboard) * (boardXNetWeightFrom15 9 blackboard)) + (((boardXNetNode16 blackboard) * (boardXNetWeightFrom16 9 blackboard)) + (((boardXNetNode17 blackboard) * (boardXNetWeightFrom17 9 blackboard)) + (((boardXNetNode18 blackboard) * (boardXNetWeightFrom18 9 blackboard)) + (((boardXNetNode19 blackboard) * (boardXNetWeightFrom19 9 blackboard)) + (boardXNetBiasFrom1 9 blackboard))))))))))) 0)
boardXNetNode30 :: BTreeBlackboard -> Integer
boardXNetNode30 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 0 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 0 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 0 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 0 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 0 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 0 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 0 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 0 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 0 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 0 blackboard)) + (boardXNetBiasFrom2 0 blackboard))))))))))) 0)
boardXNetNode31 :: BTreeBlackboard -> Integer
boardXNetNode31 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 1 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 1 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 1 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 1 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 1 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 1 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 1 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 1 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 1 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 1 blackboard)) + (boardXNetBiasFrom2 1 blackboard))))))))))) 0)
boardXNetNode32 :: BTreeBlackboard -> Integer
boardXNetNode32 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 2 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 2 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 2 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 2 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 2 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 2 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 2 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 2 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 2 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 2 blackboard)) + (boardXNetBiasFrom2 2 blackboard))))))))))) 0)
boardXNetNode33 :: BTreeBlackboard -> Integer
boardXNetNode33 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 3 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 3 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 3 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 3 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 3 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 3 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 3 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 3 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 3 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 3 blackboard)) + (boardXNetBiasFrom2 3 blackboard))))))))))) 0)
boardXNetNode34 :: BTreeBlackboard -> Integer
boardXNetNode34 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 4 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 4 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 4 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 4 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 4 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 4 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 4 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 4 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 4 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 4 blackboard)) + (boardXNetBiasFrom2 4 blackboard))))))))))) 0)
boardXNetNode35 :: BTreeBlackboard -> Integer
boardXNetNode35 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 5 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 5 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 5 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 5 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 5 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 5 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 5 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 5 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 5 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 5 blackboard)) + (boardXNetBiasFrom2 5 blackboard))))))))))) 0)
boardXNetNode36 :: BTreeBlackboard -> Integer
boardXNetNode36 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 6 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 6 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 6 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 6 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 6 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 6 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 6 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 6 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 6 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 6 blackboard)) + (boardXNetBiasFrom2 6 blackboard))))))))))) 0)
boardXNetNode37 :: BTreeBlackboard -> Integer
boardXNetNode37 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 7 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 7 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 7 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 7 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 7 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 7 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 7 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 7 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 7 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 7 blackboard)) + (boardXNetBiasFrom2 7 blackboard))))))))))) 0)
boardXNetNode38 :: BTreeBlackboard -> Integer
boardXNetNode38 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 8 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 8 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 8 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 8 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 8 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 8 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 8 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 8 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 8 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 8 blackboard)) + (boardXNetBiasFrom2 8 blackboard))))))))))) 0)
boardXNetNode39 :: BTreeBlackboard -> Integer
boardXNetNode39 blackboard = (max (((boardXNetNode20 blackboard) * (boardXNetWeightFrom20 9 blackboard)) + (((boardXNetNode21 blackboard) * (boardXNetWeightFrom21 9 blackboard)) + (((boardXNetNode22 blackboard) * (boardXNetWeightFrom22 9 blackboard)) + (((boardXNetNode23 blackboard) * (boardXNetWeightFrom23 9 blackboard)) + (((boardXNetNode24 blackboard) * (boardXNetWeightFrom24 9 blackboard)) + (((boardXNetNode25 blackboard) * (boardXNetWeightFrom25 9 blackboard)) + (((boardXNetNode26 blackboard) * (boardXNetWeightFrom26 9 blackboard)) + (((boardXNetNode27 blackboard) * (boardXNetWeightFrom27 9 blackboard)) + (((boardXNetNode28 blackboard) * (boardXNetWeightFrom28 9 blackboard)) + (((boardXNetNode29 blackboard) * (boardXNetWeightFrom29 9 blackboard)) + (boardXNetBiasFrom2 9 blackboard))))))))))) 0)
boardXNetNode40 :: BTreeBlackboard -> Integer
boardXNetNode40 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 0 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 0 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 0 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 0 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 0 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 0 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 0 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 0 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 0 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 0 blackboard)) + (boardXNetBiasFrom3 0 blackboard))))))))))) 0)
boardXNetNode41 :: BTreeBlackboard -> Integer
boardXNetNode41 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 1 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 1 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 1 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 1 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 1 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 1 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 1 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 1 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 1 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 1 blackboard)) + (boardXNetBiasFrom3 1 blackboard))))))))))) 0)
boardXNetNode42 :: BTreeBlackboard -> Integer
boardXNetNode42 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 2 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 2 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 2 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 2 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 2 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 2 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 2 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 2 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 2 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 2 blackboard)) + (boardXNetBiasFrom3 2 blackboard))))))))))) 0)
boardXNetNode43 :: BTreeBlackboard -> Integer
boardXNetNode43 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 3 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 3 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 3 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 3 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 3 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 3 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 3 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 3 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 3 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 3 blackboard)) + (boardXNetBiasFrom3 3 blackboard))))))))))) 0)
boardXNetNode44 :: BTreeBlackboard -> Integer
boardXNetNode44 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 4 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 4 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 4 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 4 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 4 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 4 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 4 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 4 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 4 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 4 blackboard)) + (boardXNetBiasFrom3 4 blackboard))))))))))) 0)
boardXNetNode45 :: BTreeBlackboard -> Integer
boardXNetNode45 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 5 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 5 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 5 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 5 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 5 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 5 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 5 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 5 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 5 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 5 blackboard)) + (boardXNetBiasFrom3 5 blackboard))))))))))) 0)
boardXNetNode46 :: BTreeBlackboard -> Integer
boardXNetNode46 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 6 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 6 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 6 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 6 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 6 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 6 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 6 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 6 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 6 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 6 blackboard)) + (boardXNetBiasFrom3 6 blackboard))))))))))) 0)
boardXNetNode47 :: BTreeBlackboard -> Integer
boardXNetNode47 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 7 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 7 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 7 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 7 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 7 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 7 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 7 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 7 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 7 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 7 blackboard)) + (boardXNetBiasFrom3 7 blackboard))))))))))) 0)
boardXNetNode48 :: BTreeBlackboard -> Integer
boardXNetNode48 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 8 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 8 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 8 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 8 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 8 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 8 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 8 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 8 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 8 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 8 blackboard)) + (boardXNetBiasFrom3 8 blackboard))))))))))) 0)
boardXNetNode49 :: BTreeBlackboard -> Integer
boardXNetNode49 blackboard = (max (((boardXNetNode30 blackboard) * (boardXNetWeightFrom30 9 blackboard)) + (((boardXNetNode31 blackboard) * (boardXNetWeightFrom31 9 blackboard)) + (((boardXNetNode32 blackboard) * (boardXNetWeightFrom32 9 blackboard)) + (((boardXNetNode33 blackboard) * (boardXNetWeightFrom33 9 blackboard)) + (((boardXNetNode34 blackboard) * (boardXNetWeightFrom34 9 blackboard)) + (((boardXNetNode35 blackboard) * (boardXNetWeightFrom35 9 blackboard)) + (((boardXNetNode36 blackboard) * (boardXNetWeightFrom36 9 blackboard)) + (((boardXNetNode37 blackboard) * (boardXNetWeightFrom37 9 blackboard)) + (((boardXNetNode38 blackboard) * (boardXNetWeightFrom38 9 blackboard)) + (((boardXNetNode39 blackboard) * (boardXNetWeightFrom39 9 blackboard)) + (boardXNetBiasFrom3 9 blackboard))))))))))) 0)
boardXNetNode50 :: BTreeBlackboard -> Integer
boardXNetNode50 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 0 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 0 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 0 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 0 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 0 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 0 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 0 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 0 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 0 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 0 blackboard)) + (boardXNetBiasFrom4 0 blackboard)))))))))))
boardXNetNode51 :: BTreeBlackboard -> Integer
boardXNetNode51 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 1 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 1 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 1 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 1 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 1 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 1 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 1 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 1 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 1 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 1 blackboard)) + (boardXNetBiasFrom4 1 blackboard)))))))))))
boardXNetNode52 :: BTreeBlackboard -> Integer
boardXNetNode52 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 2 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 2 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 2 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 2 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 2 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 2 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 2 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 2 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 2 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 2 blackboard)) + (boardXNetBiasFrom4 2 blackboard)))))))))))
boardXNetNode53 :: BTreeBlackboard -> Integer
boardXNetNode53 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 3 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 3 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 3 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 3 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 3 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 3 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 3 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 3 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 3 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 3 blackboard)) + (boardXNetBiasFrom4 3 blackboard)))))))))))
boardXNetNode54 :: BTreeBlackboard -> Integer
boardXNetNode54 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 4 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 4 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 4 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 4 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 4 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 4 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 4 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 4 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 4 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 4 blackboard)) + (boardXNetBiasFrom4 4 blackboard)))))))))))
boardXNetNode55 :: BTreeBlackboard -> Integer
boardXNetNode55 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 5 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 5 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 5 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 5 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 5 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 5 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 5 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 5 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 5 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 5 blackboard)) + (boardXNetBiasFrom4 5 blackboard)))))))))))
boardXNetNode56 :: BTreeBlackboard -> Integer
boardXNetNode56 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 6 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 6 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 6 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 6 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 6 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 6 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 6 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 6 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 6 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 6 blackboard)) + (boardXNetBiasFrom4 6 blackboard)))))))))))
boardXNetNode57 :: BTreeBlackboard -> Integer
boardXNetNode57 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 7 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 7 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 7 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 7 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 7 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 7 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 7 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 7 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 7 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 7 blackboard)) + (boardXNetBiasFrom4 7 blackboard)))))))))))
boardXNetNode58 :: BTreeBlackboard -> Integer
boardXNetNode58 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 8 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 8 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 8 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 8 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 8 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 8 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 8 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 8 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 8 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 8 blackboard)) + (boardXNetBiasFrom4 8 blackboard)))))))))))
boardXNetNode59 :: BTreeBlackboard -> Integer
boardXNetNode59 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 9 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 9 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 9 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 9 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 9 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 9 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 9 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 9 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 9 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 9 blackboard)) + (boardXNetBiasFrom4 9 blackboard)))))))))))
boardXNetNode510 :: BTreeBlackboard -> Integer
boardXNetNode510 blackboard = (((boardXNetNode40 blackboard) * (boardXNetWeightFrom40 10 blackboard)) + (((boardXNetNode41 blackboard) * (boardXNetWeightFrom41 10 blackboard)) + (((boardXNetNode42 blackboard) * (boardXNetWeightFrom42 10 blackboard)) + (((boardXNetNode43 blackboard) * (boardXNetWeightFrom43 10 blackboard)) + (((boardXNetNode44 blackboard) * (boardXNetWeightFrom44 10 blackboard)) + (((boardXNetNode45 blackboard) * (boardXNetWeightFrom45 10 blackboard)) + (((boardXNetNode46 blackboard) * (boardXNetWeightFrom46 10 blackboard)) + (((boardXNetNode47 blackboard) * (boardXNetWeightFrom47 10 blackboard)) + (((boardXNetNode48 blackboard) * (boardXNetWeightFrom48 10 blackboard)) + (((boardXNetNode49 blackboard) * (boardXNetWeightFrom49 10 blackboard)) + (boardXNetBiasFrom4 10 blackboard)))))))))))
boardXNetOutputMax :: BTreeBlackboard -> Integer
boardXNetOutputMax blackboard = (max (boardXNetNode510 blackboard) (max (boardXNetNode59 blackboard) (max (boardXNetNode58 blackboard) (max (boardXNetNode57 blackboard) (max (boardXNetNode56 blackboard) (max (boardXNetNode55 blackboard) (max (boardXNetNode54 blackboard) (max (boardXNetNode53 blackboard) (max (boardXNetNode52 blackboard) (max (boardXNetNode51 blackboard) (boardXNetNode50 blackboard)))))))))))
boardXNetOutput :: BTreeBlackboard -> Integer
boardXNetOutput blackboard
  | ((boardXNetOutputMax blackboard) == (boardXNetNode50 blackboard)) = 0
  | ((boardXNetOutputMax blackboard) == (boardXNetNode51 blackboard)) = 1
  | ((boardXNetOutputMax blackboard) == (boardXNetNode52 blackboard)) = 2
  | ((boardXNetOutputMax blackboard) == (boardXNetNode53 blackboard)) = 3
  | ((boardXNetOutputMax blackboard) == (boardXNetNode54 blackboard)) = 4
  | ((boardXNetOutputMax blackboard) == (boardXNetNode55 blackboard)) = 5
  | ((boardXNetOutputMax blackboard) == (boardXNetNode56 blackboard)) = 6
  | ((boardXNetOutputMax blackboard) == (boardXNetNode57 blackboard)) = 7
  | ((boardXNetOutputMax blackboard) == (boardXNetNode58 blackboard)) = 8
  | ((boardXNetOutputMax blackboard) == (boardXNetNode59 blackboard)) = 9
  | ((boardXNetOutputMax blackboard) == (boardXNetNode510 blackboard)) = 10
  | otherwise = (-1)
boardYNet11 :: BTreeBlackboard -> Integer
boardYNet11 blackboard = (max (boardDestY blackboard) 0)
boardYNet12 :: BTreeBlackboard -> Integer
boardYNet12 blackboard = (max ((boardDestY blackboard) - (boardPrevDestY blackboard)) 0)
boardYNet13 :: BTreeBlackboard -> Integer
boardYNet13 blackboard = (max ((boardPrevDestY blackboard) - (boardDestY blackboard)) 0)
boardYNet14 :: BTreeBlackboard -> Integer
boardYNet14 blackboard = (max (boardDir blackboard) 0)
boardYNet15 :: BTreeBlackboard -> Integer
boardYNet15 blackboard = (max (- (boardDir blackboard)) 0)
boardYNet21 :: BTreeBlackboard -> Integer
boardYNet21 blackboard = (max (boardYNet11 blackboard) 0)
boardYNet22 :: BTreeBlackboard -> Integer
boardYNet22 blackboard = (max ((- (boardYNet12 blackboard)) + ((- (boardYNet13 blackboard)) + 1)) 0)
boardYNet23 :: BTreeBlackboard -> Integer
boardYNet23 blackboard = (max (boardYNet14 blackboard) 0)
boardYNet24 :: BTreeBlackboard -> Integer
boardYNet24 blackboard = (max (boardYNet15 blackboard) 0)
boardYNet31 :: BTreeBlackboard -> Integer
boardYNet31 blackboard = (max (boardYNet21 blackboard) 0)
boardYNet32 :: BTreeBlackboard -> Integer
boardYNet32 blackboard = (max ((boardYNet22 blackboard) + ((boardYNet23 blackboard) + (-1))) 0)
boardYNet33 :: BTreeBlackboard -> Integer
boardYNet33 blackboard = (max ((boardYNet22 blackboard) + ((boardYNet24 blackboard) + (-1))) 0)
boardYNetOutput :: BTreeBlackboard -> Integer
boardYNetOutput blackboard = (max ((boardYNet31 blackboard) + ((2 * (boardYNet32 blackboard)) + ((-1) * (2 * (boardYNet33 blackboard))))) 0)
boardXNetWeightFrom00 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom00 0 blackboard = 82
boardXNetWeightFrom00 1 blackboard = 93
boardXNetWeightFrom00 2 blackboard = 125
boardXNetWeightFrom00 3 blackboard = 23
boardXNetWeightFrom00 4 blackboard = (-69)
boardXNetWeightFrom00 5 blackboard = (-1)
boardXNetWeightFrom00 6 blackboard = 41
boardXNetWeightFrom00 7 blackboard = 87
boardXNetWeightFrom00 8 blackboard = (-8)
boardXNetWeightFrom00 9 blackboard = 67
boardXNetWeightFrom00 _ _ = error "boardXNetWeightFrom00 illegal index value"
boardXNetWeightFrom01 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom01 0 blackboard = 3
boardXNetWeightFrom01 1 blackboard = 39
boardXNetWeightFrom01 2 blackboard = 25
boardXNetWeightFrom01 3 blackboard = (-31)
boardXNetWeightFrom01 4 blackboard = (-31)
boardXNetWeightFrom01 5 blackboard = 88
boardXNetWeightFrom01 6 blackboard = 98
boardXNetWeightFrom01 7 blackboard = (-88)
boardXNetWeightFrom01 8 blackboard = (-49)
boardXNetWeightFrom01 9 blackboard = (-67)
boardXNetWeightFrom01 _ _ = error "boardXNetWeightFrom01 illegal index value"
boardXNetBiasFrom0 :: Integer -> BTreeBlackboard -> Integer
boardXNetBiasFrom0 0 blackboard = (-84)
boardXNetBiasFrom0 1 blackboard = (-46)
boardXNetBiasFrom0 2 blackboard = (-65)
boardXNetBiasFrom0 3 blackboard = 151
boardXNetBiasFrom0 4 blackboard = 0
boardXNetBiasFrom0 5 blackboard = 126
boardXNetBiasFrom0 6 blackboard = 154
boardXNetBiasFrom0 7 blackboard = 0
boardXNetBiasFrom0 8 blackboard = 0
boardXNetBiasFrom0 9 blackboard = (-1)
boardXNetBiasFrom0 _ _ = error "boardXNetBiasFrom0 illegal index value"
boardXNetWeightFrom10 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom10 0 blackboard = 87
boardXNetWeightFrom10 1 blackboard = 82
boardXNetWeightFrom10 2 blackboard = (-3)
boardXNetWeightFrom10 3 blackboard = 13
boardXNetWeightFrom10 4 blackboard = 49
boardXNetWeightFrom10 5 blackboard = (-411)
boardXNetWeightFrom10 6 blackboard = 20
boardXNetWeightFrom10 7 blackboard = (-29)
boardXNetWeightFrom10 8 blackboard = 48
boardXNetWeightFrom10 9 blackboard = (-29)
boardXNetWeightFrom10 _ _ = error "boardXNetWeightFrom10 illegal index value"
boardXNetWeightFrom11 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom11 0 blackboard = 36
boardXNetWeightFrom11 1 blackboard = 40
boardXNetWeightFrom11 2 blackboard = (-33)
boardXNetWeightFrom11 3 blackboard = 67
boardXNetWeightFrom11 4 blackboard = (-16)
boardXNetWeightFrom11 5 blackboard = (-141)
boardXNetWeightFrom11 6 blackboard = (-29)
boardXNetWeightFrom11 7 blackboard = 36
boardXNetWeightFrom11 8 blackboard = (-51)
boardXNetWeightFrom11 9 blackboard = 1
boardXNetWeightFrom11 _ _ = error "boardXNetWeightFrom11 illegal index value"
boardXNetWeightFrom12 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom12 0 blackboard = 83
boardXNetWeightFrom12 1 blackboard = 55
boardXNetWeightFrom12 2 blackboard = 18
boardXNetWeightFrom12 3 blackboard = 72
boardXNetWeightFrom12 4 blackboard = 38
boardXNetWeightFrom12 5 blackboard = (-305)
boardXNetWeightFrom12 6 blackboard = (-17)
boardXNetWeightFrom12 7 blackboard = 40
boardXNetWeightFrom12 8 blackboard = (-43)
boardXNetWeightFrom12 9 blackboard = (-141)
boardXNetWeightFrom12 _ _ = error "boardXNetWeightFrom12 illegal index value"
boardXNetWeightFrom13 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom13 0 blackboard = (-58)
boardXNetWeightFrom13 1 blackboard = 141
boardXNetWeightFrom13 2 blackboard = 127
boardXNetWeightFrom13 3 blackboard = (-149)
boardXNetWeightFrom13 4 blackboard = (-114)
boardXNetWeightFrom13 5 blackboard = (-119)
boardXNetWeightFrom13 6 blackboard = 18
boardXNetWeightFrom13 7 blackboard = 82
boardXNetWeightFrom13 8 blackboard = (-22)
boardXNetWeightFrom13 9 blackboard = (-35)
boardXNetWeightFrom13 _ _ = error "boardXNetWeightFrom13 illegal index value"
boardXNetWeightFrom14 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom14 0 blackboard = 7
boardXNetWeightFrom14 1 blackboard = 45
boardXNetWeightFrom14 2 blackboard = (-41)
boardXNetWeightFrom14 3 blackboard = 1
boardXNetWeightFrom14 4 blackboard = 3
boardXNetWeightFrom14 5 blackboard = 44
boardXNetWeightFrom14 6 blackboard = 19
boardXNetWeightFrom14 7 blackboard = (-30)
boardXNetWeightFrom14 8 blackboard = (-39)
boardXNetWeightFrom14 9 blackboard = 23
boardXNetWeightFrom14 _ _ = error "boardXNetWeightFrom14 illegal index value"
boardXNetWeightFrom15 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom15 0 blackboard = (-28)
boardXNetWeightFrom15 1 blackboard = (-73)
boardXNetWeightFrom15 2 blackboard = 72
boardXNetWeightFrom15 3 blackboard = (-28)
boardXNetWeightFrom15 4 blackboard = 21
boardXNetWeightFrom15 5 blackboard = 89
boardXNetWeightFrom15 6 blackboard = (-33)
boardXNetWeightFrom15 7 blackboard = 89
boardXNetWeightFrom15 8 blackboard = (-29)
boardXNetWeightFrom15 9 blackboard = 13
boardXNetWeightFrom15 _ _ = error "boardXNetWeightFrom15 illegal index value"
boardXNetWeightFrom16 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom16 0 blackboard = 0
boardXNetWeightFrom16 1 blackboard = 3
boardXNetWeightFrom16 2 blackboard = 70
boardXNetWeightFrom16 3 blackboard = 63
boardXNetWeightFrom16 4 blackboard = 4
boardXNetWeightFrom16 5 blackboard = 103
boardXNetWeightFrom16 6 blackboard = (-19)
boardXNetWeightFrom16 7 blackboard = 45
boardXNetWeightFrom16 8 blackboard = (-3)
boardXNetWeightFrom16 9 blackboard = 58
boardXNetWeightFrom16 _ _ = error "boardXNetWeightFrom16 illegal index value"
boardXNetWeightFrom17 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom17 0 blackboard = (-43)
boardXNetWeightFrom17 1 blackboard = (-78)
boardXNetWeightFrom17 2 blackboard = (-68)
boardXNetWeightFrom17 3 blackboard = 18
boardXNetWeightFrom17 4 blackboard = 49
boardXNetWeightFrom17 5 blackboard = (-199)
boardXNetWeightFrom17 6 blackboard = 23
boardXNetWeightFrom17 7 blackboard = 88
boardXNetWeightFrom17 8 blackboard = 27
boardXNetWeightFrom17 9 blackboard = (-84)
boardXNetWeightFrom17 _ _ = error "boardXNetWeightFrom17 illegal index value"
boardXNetWeightFrom18 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom18 0 blackboard = (-35)
boardXNetWeightFrom18 1 blackboard = 54
boardXNetWeightFrom18 2 blackboard = 7
boardXNetWeightFrom18 3 blackboard = 0
boardXNetWeightFrom18 4 blackboard = 10
boardXNetWeightFrom18 5 blackboard = 40
boardXNetWeightFrom18 6 blackboard = (-39)
boardXNetWeightFrom18 7 blackboard = 3
boardXNetWeightFrom18 8 blackboard = 49
boardXNetWeightFrom18 9 blackboard = (-36)
boardXNetWeightFrom18 _ _ = error "boardXNetWeightFrom18 illegal index value"
boardXNetWeightFrom19 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom19 0 blackboard = 34
boardXNetWeightFrom19 1 blackboard = (-20)
boardXNetWeightFrom19 2 blackboard = (-64)
boardXNetWeightFrom19 3 blackboard = 53
boardXNetWeightFrom19 4 blackboard = 10
boardXNetWeightFrom19 5 blackboard = (-126)
boardXNetWeightFrom19 6 blackboard = 3
boardXNetWeightFrom19 7 blackboard = 103
boardXNetWeightFrom19 8 blackboard = 10
boardXNetWeightFrom19 9 blackboard = (-62)
boardXNetWeightFrom19 _ _ = error "boardXNetWeightFrom19 illegal index value"
boardXNetBiasFrom1 :: Integer -> BTreeBlackboard -> Integer
boardXNetBiasFrom1 0 blackboard = (-81)
boardXNetBiasFrom1 1 blackboard = (-47)
boardXNetBiasFrom1 2 blackboard = 123
boardXNetBiasFrom1 3 blackboard = (-99)
boardXNetBiasFrom1 4 blackboard = (-158)
boardXNetBiasFrom1 5 blackboard = (-10)
boardXNetBiasFrom1 6 blackboard = (-3)
boardXNetBiasFrom1 7 blackboard = 174
boardXNetBiasFrom1 8 blackboard = (-1)
boardXNetBiasFrom1 9 blackboard = (-30)
boardXNetBiasFrom1 _ _ = error "boardXNetBiasFrom1 illegal index value"
boardXNetWeightFrom20 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom20 0 blackboard = 104
boardXNetWeightFrom20 1 blackboard = (-48)
boardXNetWeightFrom20 2 blackboard = 81
boardXNetWeightFrom20 3 blackboard = 88
boardXNetWeightFrom20 4 blackboard = 33
boardXNetWeightFrom20 5 blackboard = (-50)
boardXNetWeightFrom20 6 blackboard = (-135)
boardXNetWeightFrom20 7 blackboard = 43
boardXNetWeightFrom20 8 blackboard = (-7)
boardXNetWeightFrom20 9 blackboard = (-53)
boardXNetWeightFrom20 _ _ = error "boardXNetWeightFrom20 illegal index value"
boardXNetWeightFrom21 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom21 0 blackboard = 70
boardXNetWeightFrom21 1 blackboard = (-18)
boardXNetWeightFrom21 2 blackboard = (-46)
boardXNetWeightFrom21 3 blackboard = 97
boardXNetWeightFrom21 4 blackboard = (-29)
boardXNetWeightFrom21 5 blackboard = (-24)
boardXNetWeightFrom21 6 blackboard = (-17)
boardXNetWeightFrom21 7 blackboard = (-29)
boardXNetWeightFrom21 8 blackboard = 69
boardXNetWeightFrom21 9 blackboard = (-73)
boardXNetWeightFrom21 _ _ = error "boardXNetWeightFrom21 illegal index value"
boardXNetWeightFrom22 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom22 0 blackboard = (-19)
boardXNetWeightFrom22 1 blackboard = (-25)
boardXNetWeightFrom22 2 blackboard = (-15)
boardXNetWeightFrom22 3 blackboard = 9
boardXNetWeightFrom22 4 blackboard = 14
boardXNetWeightFrom22 5 blackboard = 15
boardXNetWeightFrom22 6 blackboard = (-22)
boardXNetWeightFrom22 7 blackboard = (-93)
boardXNetWeightFrom22 8 blackboard = (-81)
boardXNetWeightFrom22 9 blackboard = 70
boardXNetWeightFrom22 _ _ = error "boardXNetWeightFrom22 illegal index value"
boardXNetWeightFrom23 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom23 0 blackboard = 72
boardXNetWeightFrom23 1 blackboard = (-54)
boardXNetWeightFrom23 2 blackboard = 68
boardXNetWeightFrom23 3 blackboard = (-29)
boardXNetWeightFrom23 4 blackboard = (-45)
boardXNetWeightFrom23 5 blackboard = (-21)
boardXNetWeightFrom23 6 blackboard = (-60)
boardXNetWeightFrom23 7 blackboard = 62
boardXNetWeightFrom23 8 blackboard = (-33)
boardXNetWeightFrom23 9 blackboard = 7
boardXNetWeightFrom23 _ _ = error "boardXNetWeightFrom23 illegal index value"
boardXNetWeightFrom24 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom24 0 blackboard = 31
boardXNetWeightFrom24 1 blackboard = 3
boardXNetWeightFrom24 2 blackboard = 23
boardXNetWeightFrom24 3 blackboard = (-134)
boardXNetWeightFrom24 4 blackboard = (-35)
boardXNetWeightFrom24 5 blackboard = (-64)
boardXNetWeightFrom24 6 blackboard = 105
boardXNetWeightFrom24 7 blackboard = 117
boardXNetWeightFrom24 8 blackboard = 3
boardXNetWeightFrom24 9 blackboard = (-105)
boardXNetWeightFrom24 _ _ = error "boardXNetWeightFrom24 illegal index value"
boardXNetWeightFrom25 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom25 0 blackboard = (-296)
boardXNetWeightFrom25 1 blackboard = 45
boardXNetWeightFrom25 2 blackboard = (-233)
boardXNetWeightFrom25 3 blackboard = 213
boardXNetWeightFrom25 4 blackboard = 6
boardXNetWeightFrom25 5 blackboard = (-218)
boardXNetWeightFrom25 6 blackboard = 96
boardXNetWeightFrom25 7 blackboard = (-53)
boardXNetWeightFrom25 8 blackboard = (-51)
boardXNetWeightFrom25 9 blackboard = 419
boardXNetWeightFrom25 _ _ = error "boardXNetWeightFrom25 illegal index value"
boardXNetWeightFrom26 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom26 0 blackboard = (-33)
boardXNetWeightFrom26 1 blackboard = (-38)
boardXNetWeightFrom26 2 blackboard = (-1)
boardXNetWeightFrom26 3 blackboard = (-38)
boardXNetWeightFrom26 4 blackboard = 1
boardXNetWeightFrom26 5 blackboard = 12
boardXNetWeightFrom26 6 blackboard = 16
boardXNetWeightFrom26 7 blackboard = (-20)
boardXNetWeightFrom26 8 blackboard = (-36)
boardXNetWeightFrom26 9 blackboard = (-26)
boardXNetWeightFrom26 _ _ = error "boardXNetWeightFrom26 illegal index value"
boardXNetWeightFrom27 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom27 0 blackboard = 17
boardXNetWeightFrom27 1 blackboard = (-16)
boardXNetWeightFrom27 2 blackboard = 75
boardXNetWeightFrom27 3 blackboard = 26
boardXNetWeightFrom27 4 blackboard = (-27)
boardXNetWeightFrom27 5 blackboard = 72
boardXNetWeightFrom27 6 blackboard = 27
boardXNetWeightFrom27 7 blackboard = (-15)
boardXNetWeightFrom27 8 blackboard = 53
boardXNetWeightFrom27 9 blackboard = 71
boardXNetWeightFrom27 _ _ = error "boardXNetWeightFrom27 illegal index value"
boardXNetWeightFrom28 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom28 0 blackboard = 46
boardXNetWeightFrom28 1 blackboard = (-31)
boardXNetWeightFrom28 2 blackboard = (-37)
boardXNetWeightFrom28 3 blackboard = 53
boardXNetWeightFrom28 4 blackboard = 45
boardXNetWeightFrom28 5 blackboard = (-38)
boardXNetWeightFrom28 6 blackboard = (-52)
boardXNetWeightFrom28 7 blackboard = (-32)
boardXNetWeightFrom28 8 blackboard = 21
boardXNetWeightFrom28 9 blackboard = 0
boardXNetWeightFrom28 _ _ = error "boardXNetWeightFrom28 illegal index value"
boardXNetWeightFrom29 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom29 0 blackboard = (-19)
boardXNetWeightFrom29 1 blackboard = 22
boardXNetWeightFrom29 2 blackboard = 8
boardXNetWeightFrom29 3 blackboard = (-51)
boardXNetWeightFrom29 4 blackboard = 31
boardXNetWeightFrom29 5 blackboard = (-12)
boardXNetWeightFrom29 6 blackboard = 199
boardXNetWeightFrom29 7 blackboard = (-44)
boardXNetWeightFrom29 8 blackboard = 19
boardXNetWeightFrom29 9 blackboard = 171
boardXNetWeightFrom29 _ _ = error "boardXNetWeightFrom29 illegal index value"
boardXNetBiasFrom2 :: Integer -> BTreeBlackboard -> Integer
boardXNetBiasFrom2 0 blackboard = (-74)
boardXNetBiasFrom2 1 blackboard = (-4)
boardXNetBiasFrom2 2 blackboard = (-51)
boardXNetBiasFrom2 3 blackboard = 82
boardXNetBiasFrom2 4 blackboard = (-16)
boardXNetBiasFrom2 5 blackboard = 159
boardXNetBiasFrom2 6 blackboard = 19
boardXNetBiasFrom2 7 blackboard = (-117)
boardXNetBiasFrom2 8 blackboard = 64
boardXNetBiasFrom2 9 blackboard = 184
boardXNetBiasFrom2 _ _ = error "boardXNetBiasFrom2 illegal index value"
boardXNetWeightFrom30 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom30 0 blackboard = 59
boardXNetWeightFrom30 1 blackboard = (-31)
boardXNetWeightFrom30 2 blackboard = (-47)
boardXNetWeightFrom30 3 blackboard = (-92)
boardXNetWeightFrom30 4 blackboard = 44
boardXNetWeightFrom30 5 blackboard = (-38)
boardXNetWeightFrom30 6 blackboard = 26
boardXNetWeightFrom30 7 blackboard = 3
boardXNetWeightFrom30 8 blackboard = 90
boardXNetWeightFrom30 9 blackboard = (-66)
boardXNetWeightFrom30 _ _ = error "boardXNetWeightFrom30 illegal index value"
boardXNetWeightFrom31 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom31 0 blackboard = (-5)
boardXNetWeightFrom31 1 blackboard = (-7)
boardXNetWeightFrom31 2 blackboard = (-29)
boardXNetWeightFrom31 3 blackboard = 0
boardXNetWeightFrom31 4 blackboard = (-7)
boardXNetWeightFrom31 5 blackboard = 53
boardXNetWeightFrom31 6 blackboard = 47
boardXNetWeightFrom31 7 blackboard = (-5)
boardXNetWeightFrom31 8 blackboard = (-54)
boardXNetWeightFrom31 9 blackboard = 41
boardXNetWeightFrom31 _ _ = error "boardXNetWeightFrom31 illegal index value"
boardXNetWeightFrom32 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom32 0 blackboard = 22
boardXNetWeightFrom32 1 blackboard = (-5)
boardXNetWeightFrom32 2 blackboard = (-9)
boardXNetWeightFrom32 3 blackboard = (-66)
boardXNetWeightFrom32 4 blackboard = (-40)
boardXNetWeightFrom32 5 blackboard = 64
boardXNetWeightFrom32 6 blackboard = (-8)
boardXNetWeightFrom32 7 blackboard = 41
boardXNetWeightFrom32 8 blackboard = 44
boardXNetWeightFrom32 9 blackboard = 35
boardXNetWeightFrom32 _ _ = error "boardXNetWeightFrom32 illegal index value"
boardXNetWeightFrom33 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom33 0 blackboard = 21
boardXNetWeightFrom33 1 blackboard = 11
boardXNetWeightFrom33 2 blackboard = (-48)
boardXNetWeightFrom33 3 blackboard = 69
boardXNetWeightFrom33 4 blackboard = (-48)
boardXNetWeightFrom33 5 blackboard = (-12)
boardXNetWeightFrom33 6 blackboard = (-35)
boardXNetWeightFrom33 7 blackboard = (-69)
boardXNetWeightFrom33 8 blackboard = 94
boardXNetWeightFrom33 9 blackboard = 16
boardXNetWeightFrom33 _ _ = error "boardXNetWeightFrom33 illegal index value"
boardXNetWeightFrom34 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom34 0 blackboard = 30
boardXNetWeightFrom34 1 blackboard = (-4)
boardXNetWeightFrom34 2 blackboard = (-32)
boardXNetWeightFrom34 3 blackboard = (-19)
boardXNetWeightFrom34 4 blackboard = (-6)
boardXNetWeightFrom34 5 blackboard = 39
boardXNetWeightFrom34 6 blackboard = 22
boardXNetWeightFrom34 7 blackboard = 18
boardXNetWeightFrom34 8 blackboard = (-2)
boardXNetWeightFrom34 9 blackboard = 41
boardXNetWeightFrom34 _ _ = error "boardXNetWeightFrom34 illegal index value"
boardXNetWeightFrom35 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom35 0 blackboard = 37
boardXNetWeightFrom35 1 blackboard = (-11)
boardXNetWeightFrom35 2 blackboard = 11
boardXNetWeightFrom35 3 blackboard = 83
boardXNetWeightFrom35 4 blackboard = (-45)
boardXNetWeightFrom35 5 blackboard = 27
boardXNetWeightFrom35 6 blackboard = (-31)
boardXNetWeightFrom35 7 blackboard = 79
boardXNetWeightFrom35 8 blackboard = (-86)
boardXNetWeightFrom35 9 blackboard = 191
boardXNetWeightFrom35 _ _ = error "boardXNetWeightFrom35 illegal index value"
boardXNetWeightFrom36 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom36 0 blackboard = (-95)
boardXNetWeightFrom36 1 blackboard = 14
boardXNetWeightFrom36 2 blackboard = (-16)
boardXNetWeightFrom36 3 blackboard = 58
boardXNetWeightFrom36 4 blackboard = (-37)
boardXNetWeightFrom36 5 blackboard = 119
boardXNetWeightFrom36 6 blackboard = (-45)
boardXNetWeightFrom36 7 blackboard = 35
boardXNetWeightFrom36 8 blackboard = 23
boardXNetWeightFrom36 9 blackboard = (-192)
boardXNetWeightFrom36 _ _ = error "boardXNetWeightFrom36 illegal index value"
boardXNetWeightFrom37 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom37 0 blackboard = 65
boardXNetWeightFrom37 1 blackboard = 39
boardXNetWeightFrom37 2 blackboard = (-26)
boardXNetWeightFrom37 3 blackboard = 72
boardXNetWeightFrom37 4 blackboard = 25
boardXNetWeightFrom37 5 blackboard = (-200)
boardXNetWeightFrom37 6 blackboard = (-49)
boardXNetWeightFrom37 7 blackboard = 35
boardXNetWeightFrom37 8 blackboard = 17
boardXNetWeightFrom37 9 blackboard = (-165)
boardXNetWeightFrom37 _ _ = error "boardXNetWeightFrom37 illegal index value"
boardXNetWeightFrom38 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom38 0 blackboard = 71
boardXNetWeightFrom38 1 blackboard = (-40)
boardXNetWeightFrom38 2 blackboard = 10
boardXNetWeightFrom38 3 blackboard = (-110)
boardXNetWeightFrom38 4 blackboard = 13
boardXNetWeightFrom38 5 blackboard = 136
boardXNetWeightFrom38 6 blackboard = 4
boardXNetWeightFrom38 7 blackboard = 203
boardXNetWeightFrom38 8 blackboard = (-47)
boardXNetWeightFrom38 9 blackboard = 74
boardXNetWeightFrom38 _ _ = error "boardXNetWeightFrom38 illegal index value"
boardXNetWeightFrom39 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom39 0 blackboard = (-6)
boardXNetWeightFrom39 1 blackboard = (-28)
boardXNetWeightFrom39 2 blackboard = (-40)
boardXNetWeightFrom39 3 blackboard = 130
boardXNetWeightFrom39 4 blackboard = (-21)
boardXNetWeightFrom39 5 blackboard = 92
boardXNetWeightFrom39 6 blackboard = (-33)
boardXNetWeightFrom39 7 blackboard = 14
boardXNetWeightFrom39 8 blackboard = (-72)
boardXNetWeightFrom39 9 blackboard = 123
boardXNetWeightFrom39 _ _ = error "boardXNetWeightFrom39 illegal index value"
boardXNetBiasFrom3 :: Integer -> BTreeBlackboard -> Integer
boardXNetBiasFrom3 0 blackboard = 27
boardXNetBiasFrom3 1 blackboard = (-1)
boardXNetBiasFrom3 2 blackboard = 0
boardXNetBiasFrom3 3 blackboard = 151
boardXNetBiasFrom3 4 blackboard = (-1)
boardXNetBiasFrom3 5 blackboard = (-23)
boardXNetBiasFrom3 6 blackboard = 0
boardXNetBiasFrom3 7 blackboard = 6
boardXNetBiasFrom3 8 blackboard = 7
boardXNetBiasFrom3 9 blackboard = 118
boardXNetBiasFrom3 _ _ = error "boardXNetBiasFrom3 illegal index value"
boardXNetWeightFrom40 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom40 0 blackboard = (-74)
boardXNetWeightFrom40 1 blackboard = (-181)
boardXNetWeightFrom40 2 blackboard = 13
boardXNetWeightFrom40 3 blackboard = 4
boardXNetWeightFrom40 4 blackboard = (-33)
boardXNetWeightFrom40 5 blackboard = (-28)
boardXNetWeightFrom40 6 blackboard = (-14)
boardXNetWeightFrom40 7 blackboard = (-32)
boardXNetWeightFrom40 8 blackboard = (-26)
boardXNetWeightFrom40 9 blackboard = 57
boardXNetWeightFrom40 10 blackboard = 21
boardXNetWeightFrom40 _ _ = error "boardXNetWeightFrom40 illegal index value"
boardXNetWeightFrom41 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom41 0 blackboard = (-13)
boardXNetWeightFrom41 1 blackboard = 51
boardXNetWeightFrom41 2 blackboard = 48
boardXNetWeightFrom41 3 blackboard = 18
boardXNetWeightFrom41 4 blackboard = 46
boardXNetWeightFrom41 5 blackboard = 46
boardXNetWeightFrom41 6 blackboard = (-13)
boardXNetWeightFrom41 7 blackboard = (-15)
boardXNetWeightFrom41 8 blackboard = 50
boardXNetWeightFrom41 9 blackboard = 20
boardXNetWeightFrom41 10 blackboard = 41
boardXNetWeightFrom41 _ _ = error "boardXNetWeightFrom41 illegal index value"
boardXNetWeightFrom42 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom42 0 blackboard = (-28)
boardXNetWeightFrom42 1 blackboard = 24
boardXNetWeightFrom42 2 blackboard = 1
boardXNetWeightFrom42 3 blackboard = (-10)
boardXNetWeightFrom42 4 blackboard = (-29)
boardXNetWeightFrom42 5 blackboard = 32
boardXNetWeightFrom42 6 blackboard = 12
boardXNetWeightFrom42 7 blackboard = 51
boardXNetWeightFrom42 8 blackboard = 16
boardXNetWeightFrom42 9 blackboard = (-19)
boardXNetWeightFrom42 10 blackboard = (-49)
boardXNetWeightFrom42 _ _ = error "boardXNetWeightFrom42 illegal index value"
boardXNetWeightFrom43 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom43 0 blackboard = 70
boardXNetWeightFrom43 1 blackboard = (-8)
boardXNetWeightFrom43 2 blackboard = (-84)
boardXNetWeightFrom43 3 blackboard = (-76)
boardXNetWeightFrom43 4 blackboard = (-273)
boardXNetWeightFrom43 5 blackboard = (-806)
boardXNetWeightFrom43 6 blackboard = (-398)
boardXNetWeightFrom43 7 blackboard = (-263)
boardXNetWeightFrom43 8 blackboard = (-174)
boardXNetWeightFrom43 9 blackboard = (-154)
boardXNetWeightFrom43 10 blackboard = 122
boardXNetWeightFrom43 _ _ = error "boardXNetWeightFrom43 illegal index value"
boardXNetWeightFrom44 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom44 0 blackboard = (-55)
boardXNetWeightFrom44 1 blackboard = (-57)
boardXNetWeightFrom44 2 blackboard = 16
boardXNetWeightFrom44 3 blackboard = (-16)
boardXNetWeightFrom44 4 blackboard = (-32)
boardXNetWeightFrom44 5 blackboard = (-53)
boardXNetWeightFrom44 6 blackboard = 39
boardXNetWeightFrom44 7 blackboard = 10
boardXNetWeightFrom44 8 blackboard = (-51)
boardXNetWeightFrom44 9 blackboard = (-50)
boardXNetWeightFrom44 10 blackboard = (-49)
boardXNetWeightFrom44 _ _ = error "boardXNetWeightFrom44 illegal index value"
boardXNetWeightFrom45 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom45 0 blackboard = (-88)
boardXNetWeightFrom45 1 blackboard = (-19)
boardXNetWeightFrom45 2 blackboard = (-22)
boardXNetWeightFrom45 3 blackboard = 41
boardXNetWeightFrom45 4 blackboard = 0
boardXNetWeightFrom45 5 blackboard = 14
boardXNetWeightFrom45 6 blackboard = 26
boardXNetWeightFrom45 7 blackboard = (-34)
boardXNetWeightFrom45 8 blackboard = 21
boardXNetWeightFrom45 9 blackboard = 7
boardXNetWeightFrom45 10 blackboard = (-205)
boardXNetWeightFrom45 _ _ = error "boardXNetWeightFrom45 illegal index value"
boardXNetWeightFrom46 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom46 0 blackboard = (-41)
boardXNetWeightFrom46 1 blackboard = 2
boardXNetWeightFrom46 2 blackboard = (-10)
boardXNetWeightFrom46 3 blackboard = (-45)
boardXNetWeightFrom46 4 blackboard = 27
boardXNetWeightFrom46 5 blackboard = (-31)
boardXNetWeightFrom46 6 blackboard = (-5)
boardXNetWeightFrom46 7 blackboard = 22
boardXNetWeightFrom46 8 blackboard = (-43)
boardXNetWeightFrom46 9 blackboard = (-16)
boardXNetWeightFrom46 10 blackboard = (-24)
boardXNetWeightFrom46 _ _ = error "boardXNetWeightFrom46 illegal index value"
boardXNetWeightFrom47 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom47 0 blackboard = (-93)
boardXNetWeightFrom47 1 blackboard = 88
boardXNetWeightFrom47 2 blackboard = 77
boardXNetWeightFrom47 3 blackboard = 46
boardXNetWeightFrom47 4 blackboard = 8
boardXNetWeightFrom47 5 blackboard = 24
boardXNetWeightFrom47 6 blackboard = 23
boardXNetWeightFrom47 7 blackboard = 43
boardXNetWeightFrom47 8 blackboard = 44
boardXNetWeightFrom47 9 blackboard = 6
boardXNetWeightFrom47 10 blackboard = 39
boardXNetWeightFrom47 _ _ = error "boardXNetWeightFrom47 illegal index value"
boardXNetWeightFrom48 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom48 0 blackboard = 90
boardXNetWeightFrom48 1 blackboard = (-251)
boardXNetWeightFrom48 2 blackboard = (-589)
boardXNetWeightFrom48 3 blackboard = (-148)
boardXNetWeightFrom48 4 blackboard = (-114)
boardXNetWeightFrom48 5 blackboard = (-60)
boardXNetWeightFrom48 6 blackboard = 5
boardXNetWeightFrom48 7 blackboard = 37
boardXNetWeightFrom48 8 blackboard = 34
boardXNetWeightFrom48 9 blackboard = (-6)
boardXNetWeightFrom48 10 blackboard = 14
boardXNetWeightFrom48 _ _ = error "boardXNetWeightFrom48 illegal index value"
boardXNetWeightFrom49 :: Integer -> BTreeBlackboard -> Integer
boardXNetWeightFrom49 0 blackboard = (-10)
boardXNetWeightFrom49 1 blackboard = 31
boardXNetWeightFrom49 2 blackboard = 48
boardXNetWeightFrom49 3 blackboard = 8
boardXNetWeightFrom49 4 blackboard = 95
boardXNetWeightFrom49 5 blackboard = 41
boardXNetWeightFrom49 6 blackboard = (-67)
boardXNetWeightFrom49 7 blackboard = (-75)
boardXNetWeightFrom49 8 blackboard = (-189)
boardXNetWeightFrom49 9 blackboard = (-625)
boardXNetWeightFrom49 10 blackboard = 12
boardXNetWeightFrom49 _ _ = error "boardXNetWeightFrom49 illegal index value"
boardXNetBiasFrom4 :: Integer -> BTreeBlackboard -> Integer
boardXNetBiasFrom4 0 blackboard = (-15)
boardXNetBiasFrom4 1 blackboard = (-39)
boardXNetBiasFrom4 2 blackboard = (-17)
boardXNetBiasFrom4 3 blackboard = 24
boardXNetBiasFrom4 4 blackboard = 42
boardXNetBiasFrom4 5 blackboard = 6
boardXNetBiasFrom4 6 blackboard = (-33)
boardXNetBiasFrom4 7 blackboard = (-23)
boardXNetBiasFrom4 8 blackboard = 7
boardXNetBiasFrom4 9 blackboard = (-8)
boardXNetBiasFrom4 10 blackboard = 23
boardXNetBiasFrom4 _ _ = error "boardXNetBiasFrom4 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardPrevDestX :: Integer -> Integer
checkValueBoardPrevDestX value
  | 0 > value || value > 10 = error "boardPrevDestX illegal value"
  | otherwise = value

checkValueBoardPrevDestY :: Integer -> Integer
checkValueBoardPrevDestY value
  | 0 > value || value > 10 = error "boardPrevDestY illegal value"
  | otherwise = value

checkValueBoardCurX :: Integer -> Integer
checkValueBoardCurX value
  | 0 > value || value > 10 = error "boardCurX illegal value"
  | otherwise = value

checkValueBoardCurY :: Integer -> Integer
checkValueBoardCurY value
  | 0 > value || value > 10 = error "boardCurY illegal value"
  | otherwise = value

checkValueBoardDestX :: Integer -> Integer
checkValueBoardDestX value
  | 0 > value || value > 10 = error "boardDestX illegal value"
  | otherwise = value

checkValueBoardDestY :: Integer -> Integer
checkValueBoardDestY value
  | 0 > value || value > 10 = error "boardDestY illegal value"
  | otherwise = value

checkValueBoardDir :: Integer -> Integer
checkValueBoardDir (-1) = (-1)
checkValueBoardDir 1 = 1
checkValueBoardDir _ = error "boardDir illegal value"

checkValueBoardVictory :: Bool -> Bool
checkValueBoardVictory value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardPrevDestX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardPrevDestX blackboard value = blackboard { boardPrevDestX = (checkValueBoardPrevDestX value)}
updateBoardPrevDestY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardPrevDestY blackboard value = blackboard { boardPrevDestY = (checkValueBoardPrevDestY value)}
updateBoardCurX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardCurX blackboard value = blackboard { boardCurX = (checkValueBoardCurX value)}
updateBoardCurY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardCurY blackboard value = blackboard { boardCurY = (checkValueBoardCurY value)}
updateBoardDestX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDestX blackboard value = blackboard { boardDestX = (checkValueBoardDestX value)}
updateBoardDestY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDestY blackboard value = blackboard { boardDestY = (checkValueBoardDestY value)}
updateBoardDir :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDir blackboard value = blackboard { boardDir = (checkValueBoardDir value)}
updateBoardVictory :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardVictory blackboard value = blackboard { boardVictory = (checkValueBoardVictory value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY newValDir newValVictory  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen8
    partialBlackboardPrevDestX = BTreeBlackboard newSereneGenerator 0 0 0 0 0 0 0 True
    initValPrevDestX :: StdGen -> (Integer, StdGen)
    initValPrevDestX curGen = (0, curGen)
      where
        blackboard = partialBlackboardPrevDestX

    (newValPrevDestX, tempGen1) = initValPrevDestX tempGen0

    partialBlackboardPrevDestY = BTreeBlackboard newSereneGenerator newValPrevDestX 0 0 0 0 0 0 True
    initValPrevDestY :: StdGen -> (Integer, StdGen)
    initValPrevDestY curGen = ((0 + 1), curGen)
      where
        blackboard = partialBlackboardPrevDestY

    (newValPrevDestY, tempGen2) = initValPrevDestY tempGen1

    partialBlackboardCurX = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY 0 0 0 0 0 True
    initValCurX :: StdGen -> (Integer, StdGen)
    initValCurX curGen = (0, curGen)
      where
        blackboard = partialBlackboardCurX

    (newValCurX, tempGen3) = initValCurX tempGen2

    partialBlackboardCurY = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX 0 0 0 0 True
    initValCurY :: StdGen -> (Integer, StdGen)
    initValCurY curGen = (0, curGen)
      where
        blackboard = partialBlackboardCurY

    (newValCurY, tempGen4) = initValCurY tempGen3

    partialBlackboardDestX = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY 0 0 0 True
    initValDestX :: StdGen -> (Integer, StdGen)
    initValDestX curGen = (0, curGen)
      where
        blackboard = partialBlackboardDestX

    (newValDestX, tempGen5) = initValDestX tempGen4

    partialBlackboardDestY = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX 0 0 True
    initValDestY :: StdGen -> (Integer, StdGen)
    initValDestY curGen = (0, curGen)
      where
        blackboard = partialBlackboardDestY

    (newValDestY, tempGen6) = initValDestY tempGen5

    partialBlackboardDir = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY 0 True
    initValDir :: StdGen -> (Integer, StdGen)
    initValDir curGen = (1, curGen)
      where
        blackboard = partialBlackboardDir

    (newValDir, tempGen7) = initValDir tempGen6

    partialBlackboardVictory = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY newValDir True
    initValVictory :: StdGen -> (Bool, StdGen)
    initValVictory curGen = (False, curGen)
      where
        blackboard = partialBlackboardVictory

    (newValVictory, tempGen8) = initValVictory tempGen7


