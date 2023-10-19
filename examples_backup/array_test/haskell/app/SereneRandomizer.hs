module SereneRandomizer where
import System.Random

getGenerator :: Integer -> StdGen
getGenerator seed = mkStdGen (fromInteger seed)

getRandomInteger :: StdGen -> Integer -> (Integer, StdGen)
getRandomInteger generator maxValue = (toInteger randomValue, newGenerator)
  where
    (randomValue, newGenerator) = randomR (0, maxValue) generator

