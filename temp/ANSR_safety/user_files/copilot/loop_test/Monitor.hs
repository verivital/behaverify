{-# LANGUAGE DataKinds        #-}
{-# LANGUAGE RebindableSyntax #-}

module Main where

import Language.Copilot
import Copilot.Compile.C99
import Copilot.Library.LTL


actions :: Stream Int32
actions = [4, 4] ++ current_action

current_action :: Stream Int32
current_action = extern "current_action" Nothing

-- pad :: Stream Int32 -> Int32 -> Stream Bool
-- pad a c = [False, False] ++ (a == (constant c))

-- opposingCardinality :: Stream Int32 -> Stream Bool
-- opposingCardinality a = (((pad a 0) && (next (pad a 1))) || ((pad a 1) && (next (pad a 0))) || ((pad a 2) && (next (pad a 3))) || ((pad a 3) && (next (pad a 2))))

-- this version doesn't use ltl
opposingCardinality :: Stream Int32 -> Stream Bool
opposingCardinality act = (((prev == (constant 0)) && (act == (constant 1))) || ((prev == (constant 1)) && (act == (constant 0))) || ((prev == (constant 2)) && (act == (constant 3))) || ((prev == (constant 3)) && (act == (constant 2))))
  where
    prev = drop 1 act


spec = do
  trigger "go_slow" (opposingCardinality actions) [] -- for non-ltl version
  --trigger "go_slow" (opposingCardinality current_action) [] -- for ltl version
  

-- Compile the spec
main = reify spec >>= compile "monitor"
