module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
    envGenerator :: StdGen
  , envEnvVAR1 :: (String, String)
  , envEnvVAR2 :: Integer
  , envEnvVAR3 :: Integer
  , envEnvFROZENVAR4 :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "env = {" ++ "envEnvVAR1: " ++ (show (envEnvVAR1 environment)) ++ ", " ++ "envEnvVAR2: " ++ (show (envEnvVAR2 environment)) ++ ", " ++ "envEnvVAR3: " ++ (show (envEnvVAR3 environment)) ++ ", " ++ "envEnvFROZENVAR4: " ++ (show (envEnvFROZENVAR4 environment)) ++ ", " ++ "envEnvDEFINE6: " ++ (show (envEnvDEFINE6 blackboard environment)) ++ ", " ++ "envEnvDEFINE7: " ++ (show (envEnvDEFINE7 blackboard environment)) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE6 :: BTreeBlackboard -> BTreeEnvironment -> (Bool, Bool)
envEnvDEFINE6 blackboard environment = newVal
  where
    newUpdate0 = True
    newUpdate1 = True
    newUpdate2 = True
    newUpdate3 = True
    newUpdate4 = True
    newUpdate5 = True
    newUpdate6 = True
    newUpdate7 = True
    newUpdate8 = True
    newUpdate9 = True
    newUpdate10 = True
    newUpdate11 = True
    defaultValue0
      | False = (sereneXNOR True False)
      | (((-47) > 14) == ((False && False) == False)) = (sereneXOR True True)
      | otherwise = ((indexIntoEnvVAR1 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvVAR1 environment)) == "both")
    defaultValue1
      | False = (sereneXNOR True False)
      | (((-47) > 14) == ((False && False) == False)) = (sereneXOR True True)
      | otherwise = ((indexIntoEnvVAR1 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvVAR1 environment)) == "both")
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayEnvDEFINE6 defaultValue [((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate0), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate1), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate2), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate3), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate4), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate5), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate6), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate7), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate8), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate9), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate10), ((max 0 (min 1 (if (27 < 43) then (-33) else 41))), newUpdate11)]
envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> (Integer, Integer)
envEnvDEFINE7 blackboard environment = newVal
  where
    newUpdate0
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate1
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate2
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate3
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate4
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate5
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate6
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate7
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate8
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate9
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate10
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    newUpdate11
      | ((envEnvVAR3 environment) > ((min 50 (max (-50) (max (-30) (envEnvVAR2 environment)))))) = (min (-2) (max (-5) (if (((min 50 (max (-50) (max (-5) (envEnvVAR3 environment))))) > (-24)) then ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR3 environment))))) else (if ((envEnvVAR2 environment) < (-41)) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))
      | (indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR2 environment))) (envEnvDEFINE6 blackboard environment)) = (min (-2) (max (-5) (envEnvVAR2 environment)))
      | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( ((min 50 (max (-50) ((if (sereneXOR True False) then (envEnvVAR2 environment) else (envEnvVAR3 environment)) + (if (False && False) then (envEnvVAR2 environment) else (-34))))))+((-25) + (if ((-36) >= 14) then (envEnvVAR3 environment) else (envEnvVAR3 environment)))))))))
    defaultValue0 = (min (-2) (max (-5) ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR2 environment)))))))
    defaultValue1 = (min (-2) (max (-5) ((min 50 (max (-50) (max (envEnvVAR2 environment) (envEnvVAR2 environment)))))))
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayEnvDEFINE7 defaultValue [((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate0), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate1), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate2), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate2), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate3), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate3), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate4), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate4), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate5), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate5), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate6), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate6), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate7), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate7), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate8), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate8), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate9), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate9), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate10), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate10), ((max 0 (min 1 ((min 50 (max (-50) ( ((min 50 (max (-50) (max 45 (envEnvVAR3 environment)))))+ ( (if (46 <= 32) then (envEnvVAR2 environment) else 7)+(((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))) + ((min 50 (max (-50) (max (envEnvVAR3 environment) (envEnvVAR3 environment))))))))))))), newUpdate11), ((max 0 (min 1 ((sereneCOUNT (sereneXOR (True && False) False) ((indexIntoEnvDEFINE6 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE6 blackboard environment)) || (sereneIMPLIES True True)))))), newUpdate11)]

-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoEnvVAR1 :: Integer -> (String, String) -> String
indexIntoEnvVAR1 0 (value, _) = value
indexIntoEnvVAR1 1 (_, value) = value
indexIntoEnvVAR1 _ _ = error "indexIntoEnvVAR1 illegal index value"
indexIntoEnvDEFINE6 :: Integer -> (Bool, Bool) -> Bool
indexIntoEnvDEFINE6 0 (value, _) = value
indexIntoEnvDEFINE6 1 (_, value) = value
indexIntoEnvDEFINE6 _ _ = error "indexIntoEnvDEFINE6 illegal index value"
indexIntoEnvDEFINE7 :: Integer -> (Integer, Integer) -> Integer
indexIntoEnvDEFINE7 0 (value, _) = value
indexIntoEnvDEFINE7 1 (_, value) = value
indexIntoEnvDEFINE7 _ _ = error "indexIntoEnvDEFINE7 illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayEnvVAR1 :: (String, String) -> [(Integer, String)] -> (String, String)
newArrayEnvVAR1 values  []  = values
newArrayEnvVAR1 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, String)] -> (String, String)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues
newArrayEnvDEFINE6 :: (Bool, Bool) -> [(Integer, Bool)] -> (Bool, Bool)
newArrayEnvDEFINE6 values  []  = values
newArrayEnvDEFINE6 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues
newArrayEnvDEFINE7 :: (Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer)
newArrayEnvDEFINE7 values  []  = values
newArrayEnvDEFINE7 (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF UPDATES

envUpdate :: BTreeEnvironment -> StdGen -> BTreeEnvironment
envUpdate environment newGen = environment { envGenerator = newGen }
envUpdateEnvVAR1 :: BTreeEnvironment -> StdGen -> (String, String) -> BTreeEnvironment
envUpdateEnvVAR1 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR1 = newVal }
envUpdateEnvVAR2 :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateEnvVAR2 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR2 = newVal }
envUpdateEnvVAR3 :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateEnvVAR3 environment newGen newVal = environment { envGenerator = newGen, envEnvVAR3 = newVal }

-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

-- START OF FUTURE CHANGES

applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)

-- START OF BETWEEN TICK CHANGES

betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, environment) = (newBlackboard, newEnvironment)
  where
    (newBlackboard, newEnvironment) = (statement1 (statement0 (blackboard, environment)))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate1
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate2
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate3
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate4
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate5
          | ((sereneXNOR True True) || (sereneXOR (indexIntoEnvDEFINE6 (max 0 (min 1 (-17))) (envEnvDEFINE6 blackboard environment)) (True || True))) = (boardBlVAR0 blackboard)
          | otherwise = "yes"
        newUpdate6
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate7
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate8
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate9
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate10
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate11
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate12
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate13
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate14
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate15
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate16
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        newUpdate17
          | (((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (envEnvVAR3 environment))) (envEnvDEFINE7 blackboard environment)))))) < ((min 50 (max (-50) ( 26+ ( 26+(26 + 26))))))) = (envEnvFROZENVAR4 environment)
          | otherwise = (boardBlVAR0 blackboard)
        defaultValue = (envEnvVAR1 environment)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate0), ((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate1), ((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate2), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate2), ((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate3), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate3), ((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate4), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate4), ((max 0 (min 1 ((min 50 (max (-50) (max (-47) (-1))))))), newUpdate5), ((max 0 (min 1 ((min 50 (max (-50) (abs (indexIntoEnvDEFINE7 (max 0 (min 1 (-5))) (envEnvDEFINE7 blackboard environment)))))))), newUpdate5), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate6), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate6), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate7), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate7), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate8), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate8), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate9), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate9), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate10), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate10), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate11), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate11), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate12), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate12), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate13), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate13), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate14), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate14), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate15), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate15), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate16), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate16), ((max 0 (min 1 ((min 50 (max (-50) ((envEnvVAR2 environment) - (envEnvVAR2 environment))))))), newUpdate17), ((max 0 (min 1 ((min 50 (max (-50) (abs 33)))))), newUpdate17)]
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR2 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | ((indexIntoEnvDEFINE6 (max 0 (min 1 23)) (envEnvDEFINE6 blackboard environment)) == (((min 50 (max (-50) (min (-18) 19)))) == ((min 50 (max (-50) (min (envEnvVAR3 environment) (envEnvVAR3 environment))))))) = (min 5 (max 2 ((min 50 (max (-50) (min 17 ((min 50 (max (-50) (min 25 42))))))))))
          | otherwise = (min 5 (max 2 (if ((envEnvVAR3 environment) <= (-14)) then 7 else (envEnvVAR3 environment))))

-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = newEnvironment
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    envUpdateEnvFROZENVAR4 :: BTreeEnvironment -> StdGen -> String -> BTreeEnvironment
    envUpdateEnvFROZENVAR4 environment newGen newVal = environment { envGenerator = newGen, envEnvFROZENVAR4 = newVal }
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeEnvironment firstGen (" ", " ") 0 0 " "
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateEnvVAR1 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newUpdate0 = "both"
        newUpdate1 = "both"
        defaultValue0
          | (sereneXNOR (sereneXOR False False) (sereneXOR True False)) = (boardBlVAR0 blackboard)
          | otherwise = "no"
        defaultValue1
          | (sereneXNOR (sereneXOR False False) (sereneXOR True False)) = (boardBlVAR0 blackboard)
          | otherwise = "no"
        defaultValue = (defaultValue0, defaultValue1)
        newGenerator = snd randomPair0
        newVal = newArrayEnvVAR1 defaultValue [((max 0 (min 1 5)), newUpdate0), ((max 0 (min 1 5)), newUpdate1)]
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateEnvVAR2 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | False = (min 5 (max 2 ((min 50 (max (-50) (((min 50 (max (-50) (2 * (-22))))) + 13))))))
          | (4 <= (if (sereneXOR False True) then 19 else 5)) = (min 5 (max 2 ((min 50 (max (-50) (((min 50 (max (-50) ( 25+ ( 25+(36 + 36)))))) - ((min 50 (max (-50) (min 4 4))))))))))
          | otherwise = (min 5 (max 2 ((min 50 (max (-50) ((-49) - ((sereneCOUNT (sereneIMPLIES False False) ((-38) /= 3)) + (sereneCOUNT (True == False) (False && True)))))))))
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (blackboard, envUpdateEnvVAR3 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | False = (min (-2) (max (-5) (envEnvVAR2 environment)))
          | otherwise = (min (-2) (max (-5) ((min 50 (max (-50) ( (envEnvVAR2 environment)+ ( (envEnvVAR2 environment)+(21 + (envEnvVAR2 environment)))))))))
    statement3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement3 (blackboard, environment)  = (blackboard, envUpdateEnvFROZENVAR4 environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | (((min 50 (max (-50) (- (envEnvVAR2 environment))))) >= (if ((envEnvVAR3 environment) > (envEnvVAR3 environment)) then 25 else (envEnvVAR2 environment))) = "both"
          | otherwise = "both"
    (_, newEnvironment) = (statement3 (statement2 (statement1 (statement0 (blackboard, dummy)))))

