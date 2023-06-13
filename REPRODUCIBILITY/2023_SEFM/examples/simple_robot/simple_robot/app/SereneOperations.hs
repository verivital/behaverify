module SereneOperations where

sereneXOR :: Bool -> Bool -> Bool
sereneXOR True True = False
sereneXOR True False = True
sereneXOR False True = True
sereneXOR False False = False

sereneXNOR :: Bool -> Bool -> Bool
sereneXNOR True True = True
sereneXNOR True False = False
sereneXNOR False True = False
sereneXNOR False False = True

