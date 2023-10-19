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

sereneIMPLIES :: Bool -> Bool -> Bool
sereneIMPLIES True True = True
sereneIMPLIES True False = False
sereneIMPLIES False True = True
sereneIMPLIES False False = True

sereneCOUNT :: Bool -> Bool -> Integer
sereneCOUNT True True = 2
sereneCOUNT True False = 1
sereneCOUNT False True = 1
sereneCOUNT False False = 0

