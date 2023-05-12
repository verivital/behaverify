module SereneRandomizer where
import System.Random

getGenerator :: Int -> StdGen
getGenerator = mkStdGen

getRandomInt :: StdGen -> Int -> (Int, StdGen)
getRandomInt generator maxValue = randomR (0, maxValue) generator

