{-# LANGUAGE DataKinds        #-}
{-# LANGUAGE RebindableSyntax #-}

module Main where

import Language.Copilot
import Copilot.Compile.C99

-- import QuPrelude hiding ((<=), (||), (&&), (+), (-), (++), (*), (!!))


-- obs_0 :: Stream Int32
-- obs_0 = 3
-- obs_1 :: Stream Int32
-- obs_1 = 3
-- obs_2 :: Stream Int32
-- obs_2 = 0
-- obs_3 :: Stream Int32
-- obs_3 = 4
-- obs_s_0 :: Stream Int32
-- obs_s_0 = 1
-- obs_s_1 :: Stream Int32
-- obs_s_1 = 0


obs :: Stream (Array 4 Int32)
obs = [array [3, 3, 0, 4]] ++ obs
obs_size :: Stream (Array 2 Int32)
obs_size = [array [1, 0]] ++ obs_size


drone_x :: Stream Int32
drone_x = extern "drone_x" Nothing
drone_y :: Stream Int32
drone_y = extern "drone_y" Nothing
drone_speed :: Stream Int32
drone_speed = extern "drone_speed" Nothing
delta_x :: Stream Int32
delta_x = extern "delta_x" Nothing
delta_y :: Stream Int32
delta_y = extern "delta_y" Nothing


moveResult :: (Stream Int32, Stream Int32) -> (Stream Int32, Stream Int32) -> (Stream Int32, Stream Int32)
moveResult (x, y) (dx, dy) = (x + dx, y + dy)

insideObs :: Stream Int32 -> Stream Int32 -> Stream Word32 -> Stream Bool
insideObs x y i = (((obs .!! (2 * i)) - (obs_size .!! i)) <= x) && (x <= (obs .!! (2 * i))) && (((obs .!! ((2 * i) + 1)) - (obs_size .!! (i))) <= y) && (y <= (obs .!! ((2 * i) + 1)))
    

dangerObs :: (Stream Int32, Stream Int32) -> (Stream Int32, Stream Int32) -> Stream Bool
--dangerObs (x, y) (dx, dy) = foldr ((||) . (insideObs nx ny)) (-1) [0, 1]
dangerObs (x, y) (dx, dy) = (insideObs nx ny (constant 0)) || (insideObs nx ny (constant 1))
  where
    (nx, ny) = moveResult (x, y) (dx, dy)

spec = do
  trigger "go_slow" (dangerObs (drone_x, drone_y) (delta_x, delta_y)) []
  --trigger "going_up" (drone_y < (snd (moveResult (drone_x, drone_y) (delta_x, delta_y)))) []

-- Compile the spec
main = reify spec >>= compile "monitor"
