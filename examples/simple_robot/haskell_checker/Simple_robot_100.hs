module Simple_robot_100 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array.IArray as IArray ( (!), array, Array )

data STATE = STATE {
    x_true___ :: Integer
    , y_true___ :: Integer
    , x_goal___ :: Integer
    , y_goal___ :: Integer
    , remaining_goals___ :: Integer
    , goal_reached___ :: Bool
    , move_robot___ :: NODE_STATUS
    , try_right___ :: NODE_STATUS
    , x_too_small___ :: NODE_STATUS
    , go_right___ :: NODE_STATUS
    , try_left___ :: NODE_STATUS
    , x_too_big___ :: NODE_STATUS
    , go_left___ :: NODE_STATUS
    , try_up___ :: NODE_STATUS
    , y_too_small___ :: NODE_STATUS
    , go_up___ :: NODE_STATUS
    , try_down___ :: NODE_STATUS
    , y_too_big___ :: NODE_STATUS
    , go_down___ :: NODE_STATUS
    }
    deriving (Eq, Ord, Show)

initial_states :: Set.Set STATE
initial_states = next_func
    where
        x_true___VAL = 0
        y_true___VAL = 0
        x_goal___VAL = 0
        y_goal___VAL = 0
        remaining_goals___VAL = 0
        goal_reached___VAL = True
        next_func :: Set.Set STATE
        next_func = result
            where
                -- for x_true___VAL
                guard_0 = True
                value_0_0 = (0)
                value_0_1 = (1)
                value_0_2 = (2)
                value_0_3 = (3)
                value_0_4 = (4)
                value_0_5 = (5)
                value_0_6 = (6)
                value_0_7 = (7)
                value_0_8 = (8)
                value_0_9 = (9)
                value_0_10 = (10)
                value_0_11 = (11)
                value_0_12 = (12)
                value_0_13 = (13)
                value_0_14 = (14)
                value_0_15 = (15)
                value_0_16 = (16)
                value_0_17 = (17)
                value_0_18 = (18)
                value_0_19 = (19)
                value_0_20 = (20)
                value_0_21 = (21)
                value_0_22 = (22)
                value_0_23 = (23)
                value_0_24 = (24)
                value_0_25 = (25)
                value_0_26 = (26)
                value_0_27 = (27)
                value_0_28 = (28)
                value_0_29 = (29)
                value_0_30 = (30)
                value_0_31 = (31)
                value_0_32 = (32)
                value_0_33 = (33)
                value_0_34 = (34)
                value_0_35 = (35)
                value_0_36 = (36)
                value_0_37 = (37)
                value_0_38 = (38)
                value_0_39 = (39)
                value_0_40 = (40)
                value_0_41 = (41)
                value_0_42 = (42)
                value_0_43 = (43)
                value_0_44 = (44)
                value_0_45 = (45)
                value_0_46 = (46)
                value_0_47 = (47)
                value_0_48 = (48)
                value_0_49 = (49)
                value_0_50 = (50)
                value_0_51 = (51)
                value_0_52 = (52)
                value_0_53 = (53)
                value_0_54 = (54)
                value_0_55 = (55)
                value_0_56 = (56)
                value_0_57 = (57)
                value_0_58 = (58)
                value_0_59 = (59)
                value_0_60 = (60)
                value_0_61 = (61)
                value_0_62 = (62)
                value_0_63 = (63)
                value_0_64 = (64)
                value_0_65 = (65)
                value_0_66 = (66)
                value_0_67 = (67)
                value_0_68 = (68)
                value_0_69 = (69)
                value_0_70 = (70)
                value_0_71 = (71)
                value_0_72 = (72)
                value_0_73 = (73)
                value_0_74 = (74)
                value_0_75 = (75)
                value_0_76 = (76)
                value_0_77 = (77)
                value_0_78 = (78)
                value_0_79 = (79)
                value_0_80 = (80)
                value_0_81 = (81)
                value_0_82 = (82)
                value_0_83 = (83)
                value_0_84 = (84)
                value_0_85 = (85)
                value_0_86 = (86)
                value_0_87 = (87)
                value_0_88 = (88)
                value_0_89 = (89)
                value_0_90 = (90)
                value_0_91 = (91)
                value_0_92 = (92)
                value_0_93 = (93)
                value_0_94 = (94)
                value_0_95 = (95)
                value_0_96 = (96)
                value_0_97 = (97)
                value_0_98 = (98)
                value_0_99 = (99)
                value_0_100 = (100)
                values
                    | False = Set.singleton x_true___VAL
                    | guard_0 = Set.fromList [value_0_0, value_0_1, value_0_2, value_0_3, value_0_4, value_0_5, value_0_6, value_0_7, value_0_8, value_0_9, value_0_10, value_0_11, value_0_12, value_0_13, value_0_14, value_0_15, value_0_16, value_0_17, value_0_18, value_0_19, value_0_20, value_0_21, value_0_22, value_0_23, value_0_24, value_0_25, value_0_26, value_0_27, value_0_28, value_0_29, value_0_30, value_0_31, value_0_32, value_0_33, value_0_34, value_0_35, value_0_36, value_0_37, value_0_38, value_0_39, value_0_40, value_0_41, value_0_42, value_0_43, value_0_44, value_0_45, value_0_46, value_0_47, value_0_48, value_0_49, value_0_50, value_0_51, value_0_52, value_0_53, value_0_54, value_0_55, value_0_56, value_0_57, value_0_58, value_0_59, value_0_60, value_0_61, value_0_62, value_0_63, value_0_64, value_0_65, value_0_66, value_0_67, value_0_68, value_0_69, value_0_70, value_0_71, value_0_72, value_0_73, value_0_74, value_0_75, value_0_76, value_0_77, value_0_78, value_0_79, value_0_80, value_0_81, value_0_82, value_0_83, value_0_84, value_0_85, value_0_86, value_0_87, value_0_88, value_0_89, value_0_90, value_0_91, value_0_92, value_0_93, value_0_94, value_0_95, value_0_96, value_0_97, value_0_98, value_0_99, value_0_100]
                result = Set.foldr (Set.union . next_func) Set.empty values
                    where
                        next_func :: Integer -> Set.Set STATE
                        next_func x_true___VAL = result
                            where
                
                                -- for y_true___VAL
                                guard_0 = True
                                value_0_0 = (0)
                                value_0_1 = (1)
                                value_0_2 = (2)
                                value_0_3 = (3)
                                value_0_4 = (4)
                                value_0_5 = (5)
                                value_0_6 = (6)
                                value_0_7 = (7)
                                value_0_8 = (8)
                                value_0_9 = (9)
                                value_0_10 = (10)
                                value_0_11 = (11)
                                value_0_12 = (12)
                                value_0_13 = (13)
                                value_0_14 = (14)
                                value_0_15 = (15)
                                value_0_16 = (16)
                                value_0_17 = (17)
                                value_0_18 = (18)
                                value_0_19 = (19)
                                value_0_20 = (20)
                                value_0_21 = (21)
                                value_0_22 = (22)
                                value_0_23 = (23)
                                value_0_24 = (24)
                                value_0_25 = (25)
                                value_0_26 = (26)
                                value_0_27 = (27)
                                value_0_28 = (28)
                                value_0_29 = (29)
                                value_0_30 = (30)
                                value_0_31 = (31)
                                value_0_32 = (32)
                                value_0_33 = (33)
                                value_0_34 = (34)
                                value_0_35 = (35)
                                value_0_36 = (36)
                                value_0_37 = (37)
                                value_0_38 = (38)
                                value_0_39 = (39)
                                value_0_40 = (40)
                                value_0_41 = (41)
                                value_0_42 = (42)
                                value_0_43 = (43)
                                value_0_44 = (44)
                                value_0_45 = (45)
                                value_0_46 = (46)
                                value_0_47 = (47)
                                value_0_48 = (48)
                                value_0_49 = (49)
                                value_0_50 = (50)
                                value_0_51 = (51)
                                value_0_52 = (52)
                                value_0_53 = (53)
                                value_0_54 = (54)
                                value_0_55 = (55)
                                value_0_56 = (56)
                                value_0_57 = (57)
                                value_0_58 = (58)
                                value_0_59 = (59)
                                value_0_60 = (60)
                                value_0_61 = (61)
                                value_0_62 = (62)
                                value_0_63 = (63)
                                value_0_64 = (64)
                                value_0_65 = (65)
                                value_0_66 = (66)
                                value_0_67 = (67)
                                value_0_68 = (68)
                                value_0_69 = (69)
                                value_0_70 = (70)
                                value_0_71 = (71)
                                value_0_72 = (72)
                                value_0_73 = (73)
                                value_0_74 = (74)
                                value_0_75 = (75)
                                value_0_76 = (76)
                                value_0_77 = (77)
                                value_0_78 = (78)
                                value_0_79 = (79)
                                value_0_80 = (80)
                                value_0_81 = (81)
                                value_0_82 = (82)
                                value_0_83 = (83)
                                value_0_84 = (84)
                                value_0_85 = (85)
                                value_0_86 = (86)
                                value_0_87 = (87)
                                value_0_88 = (88)
                                value_0_89 = (89)
                                value_0_90 = (90)
                                value_0_91 = (91)
                                value_0_92 = (92)
                                value_0_93 = (93)
                                value_0_94 = (94)
                                value_0_95 = (95)
                                value_0_96 = (96)
                                value_0_97 = (97)
                                value_0_98 = (98)
                                value_0_99 = (99)
                                value_0_100 = (100)
                                values
                                    | False = Set.singleton y_true___VAL
                                    | guard_0 = Set.fromList [value_0_0, value_0_1, value_0_2, value_0_3, value_0_4, value_0_5, value_0_6, value_0_7, value_0_8, value_0_9, value_0_10, value_0_11, value_0_12, value_0_13, value_0_14, value_0_15, value_0_16, value_0_17, value_0_18, value_0_19, value_0_20, value_0_21, value_0_22, value_0_23, value_0_24, value_0_25, value_0_26, value_0_27, value_0_28, value_0_29, value_0_30, value_0_31, value_0_32, value_0_33, value_0_34, value_0_35, value_0_36, value_0_37, value_0_38, value_0_39, value_0_40, value_0_41, value_0_42, value_0_43, value_0_44, value_0_45, value_0_46, value_0_47, value_0_48, value_0_49, value_0_50, value_0_51, value_0_52, value_0_53, value_0_54, value_0_55, value_0_56, value_0_57, value_0_58, value_0_59, value_0_60, value_0_61, value_0_62, value_0_63, value_0_64, value_0_65, value_0_66, value_0_67, value_0_68, value_0_69, value_0_70, value_0_71, value_0_72, value_0_73, value_0_74, value_0_75, value_0_76, value_0_77, value_0_78, value_0_79, value_0_80, value_0_81, value_0_82, value_0_83, value_0_84, value_0_85, value_0_86, value_0_87, value_0_88, value_0_89, value_0_90, value_0_91, value_0_92, value_0_93, value_0_94, value_0_95, value_0_96, value_0_97, value_0_98, value_0_99, value_0_100]
                                result = Set.foldr (Set.union . next_func) Set.empty values
                                    where
                                        next_func :: Integer -> Set.Set STATE
                                        next_func y_true___VAL = result
                                            where
                                
                                                -- for x_goal___VAL
                                                guard_0 = True
                                                value_0_0 = (0)
                                                value_0_1 = (1)
                                                value_0_2 = (2)
                                                value_0_3 = (3)
                                                value_0_4 = (4)
                                                value_0_5 = (5)
                                                value_0_6 = (6)
                                                value_0_7 = (7)
                                                value_0_8 = (8)
                                                value_0_9 = (9)
                                                value_0_10 = (10)
                                                value_0_11 = (11)
                                                value_0_12 = (12)
                                                value_0_13 = (13)
                                                value_0_14 = (14)
                                                value_0_15 = (15)
                                                value_0_16 = (16)
                                                value_0_17 = (17)
                                                value_0_18 = (18)
                                                value_0_19 = (19)
                                                value_0_20 = (20)
                                                value_0_21 = (21)
                                                value_0_22 = (22)
                                                value_0_23 = (23)
                                                value_0_24 = (24)
                                                value_0_25 = (25)
                                                value_0_26 = (26)
                                                value_0_27 = (27)
                                                value_0_28 = (28)
                                                value_0_29 = (29)
                                                value_0_30 = (30)
                                                value_0_31 = (31)
                                                value_0_32 = (32)
                                                value_0_33 = (33)
                                                value_0_34 = (34)
                                                value_0_35 = (35)
                                                value_0_36 = (36)
                                                value_0_37 = (37)
                                                value_0_38 = (38)
                                                value_0_39 = (39)
                                                value_0_40 = (40)
                                                value_0_41 = (41)
                                                value_0_42 = (42)
                                                value_0_43 = (43)
                                                value_0_44 = (44)
                                                value_0_45 = (45)
                                                value_0_46 = (46)
                                                value_0_47 = (47)
                                                value_0_48 = (48)
                                                value_0_49 = (49)
                                                value_0_50 = (50)
                                                value_0_51 = (51)
                                                value_0_52 = (52)
                                                value_0_53 = (53)
                                                value_0_54 = (54)
                                                value_0_55 = (55)
                                                value_0_56 = (56)
                                                value_0_57 = (57)
                                                value_0_58 = (58)
                                                value_0_59 = (59)
                                                value_0_60 = (60)
                                                value_0_61 = (61)
                                                value_0_62 = (62)
                                                value_0_63 = (63)
                                                value_0_64 = (64)
                                                value_0_65 = (65)
                                                value_0_66 = (66)
                                                value_0_67 = (67)
                                                value_0_68 = (68)
                                                value_0_69 = (69)
                                                value_0_70 = (70)
                                                value_0_71 = (71)
                                                value_0_72 = (72)
                                                value_0_73 = (73)
                                                value_0_74 = (74)
                                                value_0_75 = (75)
                                                value_0_76 = (76)
                                                value_0_77 = (77)
                                                value_0_78 = (78)
                                                value_0_79 = (79)
                                                value_0_80 = (80)
                                                value_0_81 = (81)
                                                value_0_82 = (82)
                                                value_0_83 = (83)
                                                value_0_84 = (84)
                                                value_0_85 = (85)
                                                value_0_86 = (86)
                                                value_0_87 = (87)
                                                value_0_88 = (88)
                                                value_0_89 = (89)
                                                value_0_90 = (90)
                                                value_0_91 = (91)
                                                value_0_92 = (92)
                                                value_0_93 = (93)
                                                value_0_94 = (94)
                                                value_0_95 = (95)
                                                value_0_96 = (96)
                                                value_0_97 = (97)
                                                value_0_98 = (98)
                                                value_0_99 = (99)
                                                value_0_100 = (100)
                                                values
                                                    | False = Set.singleton x_goal___VAL
                                                    | guard_0 = Set.fromList [value_0_0, value_0_1, value_0_2, value_0_3, value_0_4, value_0_5, value_0_6, value_0_7, value_0_8, value_0_9, value_0_10, value_0_11, value_0_12, value_0_13, value_0_14, value_0_15, value_0_16, value_0_17, value_0_18, value_0_19, value_0_20, value_0_21, value_0_22, value_0_23, value_0_24, value_0_25, value_0_26, value_0_27, value_0_28, value_0_29, value_0_30, value_0_31, value_0_32, value_0_33, value_0_34, value_0_35, value_0_36, value_0_37, value_0_38, value_0_39, value_0_40, value_0_41, value_0_42, value_0_43, value_0_44, value_0_45, value_0_46, value_0_47, value_0_48, value_0_49, value_0_50, value_0_51, value_0_52, value_0_53, value_0_54, value_0_55, value_0_56, value_0_57, value_0_58, value_0_59, value_0_60, value_0_61, value_0_62, value_0_63, value_0_64, value_0_65, value_0_66, value_0_67, value_0_68, value_0_69, value_0_70, value_0_71, value_0_72, value_0_73, value_0_74, value_0_75, value_0_76, value_0_77, value_0_78, value_0_79, value_0_80, value_0_81, value_0_82, value_0_83, value_0_84, value_0_85, value_0_86, value_0_87, value_0_88, value_0_89, value_0_90, value_0_91, value_0_92, value_0_93, value_0_94, value_0_95, value_0_96, value_0_97, value_0_98, value_0_99, value_0_100]
                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                    where
                                                        next_func :: Integer -> Set.Set STATE
                                                        next_func x_goal___VAL = result
                                                            where
                                                
                                                                -- for y_goal___VAL
                                                                guard_0 = True
                                                                value_0_0 = (0)
                                                                value_0_1 = (1)
                                                                value_0_2 = (2)
                                                                value_0_3 = (3)
                                                                value_0_4 = (4)
                                                                value_0_5 = (5)
                                                                value_0_6 = (6)
                                                                value_0_7 = (7)
                                                                value_0_8 = (8)
                                                                value_0_9 = (9)
                                                                value_0_10 = (10)
                                                                value_0_11 = (11)
                                                                value_0_12 = (12)
                                                                value_0_13 = (13)
                                                                value_0_14 = (14)
                                                                value_0_15 = (15)
                                                                value_0_16 = (16)
                                                                value_0_17 = (17)
                                                                value_0_18 = (18)
                                                                value_0_19 = (19)
                                                                value_0_20 = (20)
                                                                value_0_21 = (21)
                                                                value_0_22 = (22)
                                                                value_0_23 = (23)
                                                                value_0_24 = (24)
                                                                value_0_25 = (25)
                                                                value_0_26 = (26)
                                                                value_0_27 = (27)
                                                                value_0_28 = (28)
                                                                value_0_29 = (29)
                                                                value_0_30 = (30)
                                                                value_0_31 = (31)
                                                                value_0_32 = (32)
                                                                value_0_33 = (33)
                                                                value_0_34 = (34)
                                                                value_0_35 = (35)
                                                                value_0_36 = (36)
                                                                value_0_37 = (37)
                                                                value_0_38 = (38)
                                                                value_0_39 = (39)
                                                                value_0_40 = (40)
                                                                value_0_41 = (41)
                                                                value_0_42 = (42)
                                                                value_0_43 = (43)
                                                                value_0_44 = (44)
                                                                value_0_45 = (45)
                                                                value_0_46 = (46)
                                                                value_0_47 = (47)
                                                                value_0_48 = (48)
                                                                value_0_49 = (49)
                                                                value_0_50 = (50)
                                                                value_0_51 = (51)
                                                                value_0_52 = (52)
                                                                value_0_53 = (53)
                                                                value_0_54 = (54)
                                                                value_0_55 = (55)
                                                                value_0_56 = (56)
                                                                value_0_57 = (57)
                                                                value_0_58 = (58)
                                                                value_0_59 = (59)
                                                                value_0_60 = (60)
                                                                value_0_61 = (61)
                                                                value_0_62 = (62)
                                                                value_0_63 = (63)
                                                                value_0_64 = (64)
                                                                value_0_65 = (65)
                                                                value_0_66 = (66)
                                                                value_0_67 = (67)
                                                                value_0_68 = (68)
                                                                value_0_69 = (69)
                                                                value_0_70 = (70)
                                                                value_0_71 = (71)
                                                                value_0_72 = (72)
                                                                value_0_73 = (73)
                                                                value_0_74 = (74)
                                                                value_0_75 = (75)
                                                                value_0_76 = (76)
                                                                value_0_77 = (77)
                                                                value_0_78 = (78)
                                                                value_0_79 = (79)
                                                                value_0_80 = (80)
                                                                value_0_81 = (81)
                                                                value_0_82 = (82)
                                                                value_0_83 = (83)
                                                                value_0_84 = (84)
                                                                value_0_85 = (85)
                                                                value_0_86 = (86)
                                                                value_0_87 = (87)
                                                                value_0_88 = (88)
                                                                value_0_89 = (89)
                                                                value_0_90 = (90)
                                                                value_0_91 = (91)
                                                                value_0_92 = (92)
                                                                value_0_93 = (93)
                                                                value_0_94 = (94)
                                                                value_0_95 = (95)
                                                                value_0_96 = (96)
                                                                value_0_97 = (97)
                                                                value_0_98 = (98)
                                                                value_0_99 = (99)
                                                                value_0_100 = (100)
                                                                values
                                                                    | False = Set.singleton y_goal___VAL
                                                                    | guard_0 = Set.fromList [value_0_0, value_0_1, value_0_2, value_0_3, value_0_4, value_0_5, value_0_6, value_0_7, value_0_8, value_0_9, value_0_10, value_0_11, value_0_12, value_0_13, value_0_14, value_0_15, value_0_16, value_0_17, value_0_18, value_0_19, value_0_20, value_0_21, value_0_22, value_0_23, value_0_24, value_0_25, value_0_26, value_0_27, value_0_28, value_0_29, value_0_30, value_0_31, value_0_32, value_0_33, value_0_34, value_0_35, value_0_36, value_0_37, value_0_38, value_0_39, value_0_40, value_0_41, value_0_42, value_0_43, value_0_44, value_0_45, value_0_46, value_0_47, value_0_48, value_0_49, value_0_50, value_0_51, value_0_52, value_0_53, value_0_54, value_0_55, value_0_56, value_0_57, value_0_58, value_0_59, value_0_60, value_0_61, value_0_62, value_0_63, value_0_64, value_0_65, value_0_66, value_0_67, value_0_68, value_0_69, value_0_70, value_0_71, value_0_72, value_0_73, value_0_74, value_0_75, value_0_76, value_0_77, value_0_78, value_0_79, value_0_80, value_0_81, value_0_82, value_0_83, value_0_84, value_0_85, value_0_86, value_0_87, value_0_88, value_0_89, value_0_90, value_0_91, value_0_92, value_0_93, value_0_94, value_0_95, value_0_96, value_0_97, value_0_98, value_0_99, value_0_100]
                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                    where
                                                                        next_func :: Integer -> Set.Set STATE
                                                                        next_func y_goal___VAL = result
                                                                            where
                                                                
                                                                                -- for remaining_goals___VAL
                                                                                guard_0 = True
                                                                                value_0_0 = (3)
                                                                                values
                                                                                    | False = Set.singleton remaining_goals___VAL
                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                    where
                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                        next_func remaining_goals___VAL = result
                                                                                            where
                                                                                
                                                                                                -- for goal_reached___VAL
                                                                                                guard_0 = True
                                                                                                value_0_0 = False
                                                                                                values
                                                                                                    | False = Set.singleton goal_reached___VAL
                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                    where
                                                                                                        next_func :: Bool -> Set.Set STATE
                                                                                                        next_func goal_reached___VAL = result
                                                                                                            where
                                                                                                
                                                                                                                result = Set.singleton (STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID)

next_states :: STATE -> Set.Set STATE
next_states state 
    | ((>) (remaining_goals___ state) (0)) = next_func
    | otherwise = Set.singleton state
    where
        x_true___VAL = x_true___ state
        y_true___VAL = y_true___ state
        x_goal___VAL = x_goal___ state
        y_goal___VAL = y_goal___ state
        remaining_goals___VAL = remaining_goals___ state
        goal_reached___VAL = goal_reached___ state
        move_robot___VAL = move_robot___ state
        try_right___VAL = try_right___ state
        x_too_small___VAL = x_too_small___ state
        go_right___VAL = go_right___ state
        try_left___VAL = try_left___ state
        x_too_big___VAL = x_too_big___ state
        go_left___VAL = go_left___ state
        try_up___VAL = try_up___ state
        y_too_small___VAL = y_too_small___ state
        go_up___VAL = go_up___ state
        try_down___VAL = try_down___ state
        y_too_big___VAL = y_too_big___ state
        go_down___VAL = go_down___ state
        next_func :: Set.Set STATE
        next_func = result
            where
                -- for x_too_small___
                value
                    | False = INVALID
                    | ((<) x_true___VAL x_goal___VAL) = SUCCESS
                    | otherwise = FAILURE
                result = next_func value
                    where
                        next_func :: NODE_STATUS -> Set.Set STATE
                        next_func x_too_small___VAL = result
                            where
                
                                -- for x_true___VAL
                                guard_0 = True
                                value_0_0 = (max (0) (min (100) ((+) x_true___VAL (1))))
                                values
                                    | ((/=) x_too_small___VAL SUCCESS) = Set.singleton x_true___VAL
                                    | guard_0 = Set.singleton value_0_0
                                result = Set.foldr (Set.union . next_func) Set.empty values
                                    where
                                        next_func :: Integer -> Set.Set STATE
                                        next_func x_true___VAL = result
                                            where
                                
                                                -- for y_true___VAL
                                                guard_0 = True
                                                value_0_0 = (max (0) (min (100) ((+) y_true___VAL (0))))
                                                values
                                                    | ((/=) x_too_small___VAL SUCCESS) = Set.singleton y_true___VAL
                                                    | guard_0 = Set.singleton value_0_0
                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                    where
                                                        next_func :: Integer -> Set.Set STATE
                                                        next_func y_true___VAL = result
                                                            where
                                                
                                                                -- for go_right___
                                                                value
                                                                    | ((/=) x_too_small___VAL SUCCESS) = INVALID
                                                                    | otherwise = SUCCESS
                                                                result = next_func value
                                                                    where
                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                        next_func go_right___VAL = result
                                                                            where
                                                                
                                                                                -- for try_right___
                                                                                children = [x_too_small___VAL, go_right___VAL]
                                                                                value
                                                                                    | False = INVALID
                                                                                    | elem FAILURE children = FAILURE
                                                                                    | elem RUNNING children = RUNNING
                                                                                    | otherwise = SUCCESS
                                                                                result = next_func value
                                                                                    where
                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                        next_func try_right___VAL = result
                                                                                            where
                                                                                
                                                                                                -- for x_too_big___
                                                                                                value
                                                                                                    | ((/=) try_right___VAL FAILURE) = INVALID
                                                                                                    | ((>) x_true___VAL x_goal___VAL) = SUCCESS
                                                                                                    | otherwise = FAILURE
                                                                                                result = next_func value
                                                                                                    where
                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                        next_func x_too_big___VAL = result
                                                                                                            where
                                                                                                
                                                                                                                -- for x_true___VAL
                                                                                                                guard_0 = True
                                                                                                                value_0_0 = (max (0) (min (100) ((+) x_true___VAL (-1))))
                                                                                                                values
                                                                                                                    | ((/=) x_too_big___VAL SUCCESS) = Set.singleton x_true___VAL
                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                    where
                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                        next_func x_true___VAL = result
                                                                                                                            where
                                                                                                                
                                                                                                                                -- for y_true___VAL
                                                                                                                                guard_0 = True
                                                                                                                                value_0_0 = (max (0) (min (100) ((+) y_true___VAL (0))))
                                                                                                                                values
                                                                                                                                    | ((/=) x_too_big___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                    where
                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                        next_func y_true___VAL = result
                                                                                                                                            where
                                                                                                                                
                                                                                                                                                -- for go_left___
                                                                                                                                                value
                                                                                                                                                    | ((/=) x_too_big___VAL SUCCESS) = INVALID
                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                result = next_func value
                                                                                                                                                    where
                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                        next_func go_left___VAL = result
                                                                                                                                                            where
                                                                                                                                                
                                                                                                                                                                -- for try_left___
                                                                                                                                                                children = [x_too_big___VAL, go_left___VAL]
                                                                                                                                                                value
                                                                                                                                                                    | ((/=) try_right___VAL FAILURE) = INVALID
                                                                                                                                                                    | elem FAILURE children = FAILURE
                                                                                                                                                                    | elem RUNNING children = RUNNING
                                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                                result = next_func value
                                                                                                                                                                    where
                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                        next_func try_left___VAL = result
                                                                                                                                                                            where
                                                                                                                                                                
                                                                                                                                                                                -- for y_too_small___
                                                                                                                                                                                value
                                                                                                                                                                                    | ((/=) try_left___VAL FAILURE) = INVALID
                                                                                                                                                                                    | ((<) y_true___VAL y_goal___VAL) = SUCCESS
                                                                                                                                                                                    | otherwise = FAILURE
                                                                                                                                                                                result = next_func value
                                                                                                                                                                                    where
                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                        next_func y_too_small___VAL = result
                                                                                                                                                                                            where
                                                                                                                                                                                
                                                                                                                                                                                                -- for x_true___VAL
                                                                                                                                                                                                guard_0 = True
                                                                                                                                                                                                value_0_0 = (max (0) (min (100) ((+) x_true___VAL (0))))
                                                                                                                                                                                                values
                                                                                                                                                                                                    | ((/=) y_too_small___VAL SUCCESS) = Set.singleton x_true___VAL
                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                    where
                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                        next_func x_true___VAL = result
                                                                                                                                                                                                            where
                                                                                                                                                                                                
                                                                                                                                                                                                                -- for y_true___VAL
                                                                                                                                                                                                                guard_0 = True
                                                                                                                                                                                                                value_0_0 = (max (0) (min (100) ((+) y_true___VAL (1))))
                                                                                                                                                                                                                values
                                                                                                                                                                                                                    | ((/=) y_too_small___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                    where
                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                        next_func y_true___VAL = result
                                                                                                                                                                                                                            where
                                                                                                                                                                                                                
                                                                                                                                                                                                                                -- for go_up___
                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                    | ((/=) y_too_small___VAL SUCCESS) = INVALID
                                                                                                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                        next_func go_up___VAL = result
                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                -- for try_up___
                                                                                                                                                                                                                                                children = [y_too_small___VAL, go_up___VAL]
                                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                                    | ((/=) try_left___VAL FAILURE) = INVALID
                                                                                                                                                                                                                                                    | elem FAILURE children = FAILURE
                                                                                                                                                                                                                                                    | elem RUNNING children = RUNNING
                                                                                                                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                                        next_func try_up___VAL = result
                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                -- for y_too_big___
                                                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                                                    | ((/=) try_up___VAL FAILURE) = INVALID
                                                                                                                                                                                                                                                                    | ((>) y_true___VAL y_goal___VAL) = SUCCESS
                                                                                                                                                                                                                                                                    | otherwise = FAILURE
                                                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                                                        next_func y_too_big___VAL = result
                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                -- for x_true___VAL
                                                                                                                                                                                                                                                                                guard_0 = True
                                                                                                                                                                                                                                                                                value_0_0 = (max (0) (min (100) ((+) x_true___VAL (0))))
                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                    | ((/=) y_too_big___VAL SUCCESS) = Set.singleton x_true___VAL
                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                                                                                        next_func x_true___VAL = result
                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                -- for y_true___VAL
                                                                                                                                                                                                                                                                                                guard_0 = True
                                                                                                                                                                                                                                                                                                value_0_0 = (max (0) (min (100) ((+) y_true___VAL (-1))))
                                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                                    | ((/=) y_too_big___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                                                                                                        next_func y_true___VAL = result
                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                -- for go_down___
                                                                                                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                                                                                                    | ((/=) y_too_big___VAL SUCCESS) = INVALID
                                                                                                                                                                                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                        next_func go_down___VAL = result
                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                -- for try_down___
                                                                                                                                                                                                                                                                                                                                children = [y_too_big___VAL, go_down___VAL]
                                                                                                                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                                                                                                                    | ((/=) try_up___VAL FAILURE) = INVALID
                                                                                                                                                                                                                                                                                                                                    | elem FAILURE children = FAILURE
                                                                                                                                                                                                                                                                                                                                    | elem RUNNING children = RUNNING
                                                                                                                                                                                                                                                                                                                                    | otherwise = SUCCESS
                                                                                                                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                        next_func try_down___VAL = result
                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                -- for move_robot___
                                                                                                                                                                                                                                                                                                                                                children = [try_right___VAL, try_left___VAL, try_up___VAL, try_down___VAL]
                                                                                                                                                                                                                                                                                                                                                value
                                                                                                                                                                                                                                                                                                                                                    | False = INVALID
                                                                                                                                                                                                                                                                                                                                                    | elem SUCCESS children = SUCCESS
                                                                                                                                                                                                                                                                                                                                                    | elem RUNNING children = RUNNING
                                                                                                                                                                                                                                                                                                                                                    | otherwise = FAILURE
                                                                                                                                                                                                                                                                                                                                                result = next_func value
                                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                                        next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                                        next_func move_robot___VAL = result
                                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                -- for goal_reached___VAL
                                                                                                                                                                                                                                                                                                                                                                guard_0 = True
                                                                                                                                                                                                                                                                                                                                                                value_0_0 = ((&&) ((==) x_goal___VAL x_true___VAL) ((==) y_goal___VAL y_true___VAL))
                                                                                                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                                                                                                    | False = Set.singleton goal_reached___VAL
                                                                                                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                                                        next_func :: Bool -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                                                        next_func goal_reached___VAL = result
                                                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                -- for remaining_goals___VAL
                                                                                                                                                                                                                                                                                                                                                                                guard_0 = goal_reached___VAL
                                                                                                                                                                                                                                                                                                                                                                                value_0_0 = (max (0) ((-) remaining_goals___VAL (1)))
                                                                                                                                                                                                                                                                                                                                                                                guard_1 = True
                                                                                                                                                                                                                                                                                                                                                                                value_1_0 = remaining_goals___VAL
                                                                                                                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                                                                                                                    | False = Set.singleton remaining_goals___VAL
                                                                                                                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                                                                                                                    | guard_1 = Set.singleton value_1_0
                                                                                                                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                                                                        next_func remaining_goals___VAL = result
                                                                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                -- for x_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                guard_0 = ((==) (0) remaining_goals___VAL)
                                                                                                                                                                                                                                                                                                                                                                                                value_0_0 = x_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                guard_1 = goal_reached___VAL
                                                                                                                                                                                                                                                                                                                                                                                                value_1_0 = (0)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_1 = (1)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_2 = (2)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_3 = (3)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_4 = (4)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_5 = (5)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_6 = (6)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_7 = (7)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_8 = (8)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_9 = (9)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_10 = (10)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_11 = (11)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_12 = (12)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_13 = (13)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_14 = (14)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_15 = (15)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_16 = (16)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_17 = (17)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_18 = (18)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_19 = (19)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_20 = (20)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_21 = (21)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_22 = (22)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_23 = (23)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_24 = (24)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_25 = (25)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_26 = (26)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_27 = (27)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_28 = (28)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_29 = (29)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_30 = (30)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_31 = (31)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_32 = (32)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_33 = (33)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_34 = (34)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_35 = (35)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_36 = (36)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_37 = (37)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_38 = (38)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_39 = (39)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_40 = (40)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_41 = (41)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_42 = (42)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_43 = (43)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_44 = (44)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_45 = (45)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_46 = (46)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_47 = (47)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_48 = (48)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_49 = (49)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_50 = (50)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_51 = (51)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_52 = (52)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_53 = (53)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_54 = (54)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_55 = (55)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_56 = (56)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_57 = (57)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_58 = (58)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_59 = (59)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_60 = (60)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_61 = (61)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_62 = (62)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_63 = (63)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_64 = (64)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_65 = (65)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_66 = (66)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_67 = (67)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_68 = (68)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_69 = (69)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_70 = (70)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_71 = (71)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_72 = (72)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_73 = (73)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_74 = (74)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_75 = (75)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_76 = (76)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_77 = (77)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_78 = (78)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_79 = (79)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_80 = (80)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_81 = (81)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_82 = (82)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_83 = (83)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_84 = (84)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_85 = (85)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_86 = (86)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_87 = (87)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_88 = (88)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_89 = (89)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_90 = (90)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_91 = (91)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_92 = (92)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_93 = (93)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_94 = (94)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_95 = (95)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_96 = (96)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_97 = (97)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_98 = (98)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_99 = (99)
                                                                                                                                                                                                                                                                                                                                                                                                value_1_100 = (100)
                                                                                                                                                                                                                                                                                                                                                                                                guard_2 = True
                                                                                                                                                                                                                                                                                                                                                                                                value_2_0 = x_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                                                                                                                                    | False = Set.singleton x_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                                                                                                                                    | guard_1 = Set.fromList [value_1_0, value_1_1, value_1_2, value_1_3, value_1_4, value_1_5, value_1_6, value_1_7, value_1_8, value_1_9, value_1_10, value_1_11, value_1_12, value_1_13, value_1_14, value_1_15, value_1_16, value_1_17, value_1_18, value_1_19, value_1_20, value_1_21, value_1_22, value_1_23, value_1_24, value_1_25, value_1_26, value_1_27, value_1_28, value_1_29, value_1_30, value_1_31, value_1_32, value_1_33, value_1_34, value_1_35, value_1_36, value_1_37, value_1_38, value_1_39, value_1_40, value_1_41, value_1_42, value_1_43, value_1_44, value_1_45, value_1_46, value_1_47, value_1_48, value_1_49, value_1_50, value_1_51, value_1_52, value_1_53, value_1_54, value_1_55, value_1_56, value_1_57, value_1_58, value_1_59, value_1_60, value_1_61, value_1_62, value_1_63, value_1_64, value_1_65, value_1_66, value_1_67, value_1_68, value_1_69, value_1_70, value_1_71, value_1_72, value_1_73, value_1_74, value_1_75, value_1_76, value_1_77, value_1_78, value_1_79, value_1_80, value_1_81, value_1_82, value_1_83, value_1_84, value_1_85, value_1_86, value_1_87, value_1_88, value_1_89, value_1_90, value_1_91, value_1_92, value_1_93, value_1_94, value_1_95, value_1_96, value_1_97, value_1_98, value_1_99, value_1_100]
                                                                                                                                                                                                                                                                                                                                                                                                    | guard_2 = Set.singleton value_2_0
                                                                                                                                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                                                                                        next_func x_goal___VAL = result
                                                                                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                -- for y_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                                guard_0 = ((==) (0) remaining_goals___VAL)
                                                                                                                                                                                                                                                                                                                                                                                                                value_0_0 = y_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                                guard_1 = goal_reached___VAL
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_0 = (0)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_1 = (1)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_2 = (2)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_3 = (3)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_4 = (4)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_5 = (5)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_6 = (6)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_7 = (7)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_8 = (8)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_9 = (9)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_10 = (10)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_11 = (11)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_12 = (12)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_13 = (13)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_14 = (14)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_15 = (15)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_16 = (16)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_17 = (17)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_18 = (18)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_19 = (19)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_20 = (20)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_21 = (21)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_22 = (22)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_23 = (23)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_24 = (24)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_25 = (25)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_26 = (26)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_27 = (27)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_28 = (28)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_29 = (29)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_30 = (30)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_31 = (31)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_32 = (32)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_33 = (33)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_34 = (34)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_35 = (35)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_36 = (36)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_37 = (37)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_38 = (38)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_39 = (39)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_40 = (40)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_41 = (41)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_42 = (42)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_43 = (43)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_44 = (44)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_45 = (45)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_46 = (46)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_47 = (47)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_48 = (48)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_49 = (49)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_50 = (50)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_51 = (51)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_52 = (52)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_53 = (53)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_54 = (54)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_55 = (55)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_56 = (56)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_57 = (57)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_58 = (58)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_59 = (59)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_60 = (60)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_61 = (61)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_62 = (62)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_63 = (63)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_64 = (64)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_65 = (65)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_66 = (66)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_67 = (67)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_68 = (68)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_69 = (69)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_70 = (70)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_71 = (71)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_72 = (72)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_73 = (73)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_74 = (74)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_75 = (75)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_76 = (76)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_77 = (77)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_78 = (78)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_79 = (79)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_80 = (80)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_81 = (81)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_82 = (82)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_83 = (83)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_84 = (84)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_85 = (85)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_86 = (86)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_87 = (87)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_88 = (88)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_89 = (89)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_90 = (90)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_91 = (91)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_92 = (92)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_93 = (93)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_94 = (94)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_95 = (95)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_96 = (96)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_97 = (97)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_98 = (98)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_99 = (99)
                                                                                                                                                                                                                                                                                                                                                                                                                value_1_100 = (100)
                                                                                                                                                                                                                                                                                                                                                                                                                guard_2 = True
                                                                                                                                                                                                                                                                                                                                                                                                                value_2_0 = y_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                                values
                                                                                                                                                                                                                                                                                                                                                                                                                    | False = Set.singleton y_goal___VAL
                                                                                                                                                                                                                                                                                                                                                                                                                    | guard_0 = Set.singleton value_0_0
                                                                                                                                                                                                                                                                                                                                                                                                                    | guard_1 = Set.fromList [value_1_0, value_1_1, value_1_2, value_1_3, value_1_4, value_1_5, value_1_6, value_1_7, value_1_8, value_1_9, value_1_10, value_1_11, value_1_12, value_1_13, value_1_14, value_1_15, value_1_16, value_1_17, value_1_18, value_1_19, value_1_20, value_1_21, value_1_22, value_1_23, value_1_24, value_1_25, value_1_26, value_1_27, value_1_28, value_1_29, value_1_30, value_1_31, value_1_32, value_1_33, value_1_34, value_1_35, value_1_36, value_1_37, value_1_38, value_1_39, value_1_40, value_1_41, value_1_42, value_1_43, value_1_44, value_1_45, value_1_46, value_1_47, value_1_48, value_1_49, value_1_50, value_1_51, value_1_52, value_1_53, value_1_54, value_1_55, value_1_56, value_1_57, value_1_58, value_1_59, value_1_60, value_1_61, value_1_62, value_1_63, value_1_64, value_1_65, value_1_66, value_1_67, value_1_68, value_1_69, value_1_70, value_1_71, value_1_72, value_1_73, value_1_74, value_1_75, value_1_76, value_1_77, value_1_78, value_1_79, value_1_80, value_1_81, value_1_82, value_1_83, value_1_84, value_1_85, value_1_86, value_1_87, value_1_88, value_1_89, value_1_90, value_1_91, value_1_92, value_1_93, value_1_94, value_1_95, value_1_96, value_1_97, value_1_98, value_1_99, value_1_100]
                                                                                                                                                                                                                                                                                                                                                                                                                    | guard_2 = Set.singleton value_2_0
                                                                                                                                                                                                                                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                                                                                                                                                                                                                                    where
                                                                                                                                                                                                                                                                                                                                                                                                                        next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                                                                                                                                                                                                                                        next_func y_goal___VAL = result
                                                                                                                                                                                                                                                                                                                                                                                                                            where
                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                result = Set.singleton (STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL move_robot___VAL try_right___VAL x_too_small___VAL go_right___VAL try_left___VAL x_too_big___VAL go_left___VAL try_up___VAL y_too_small___VAL go_up___VAL try_down___VAL y_too_big___VAL go_down___VAL)

data NODE_STATUS = SUCCESS | RUNNING | FAILURE | INVALID
  deriving (Enum, Eq, Ord, Show)

type STATE_MAP = Map.Map STATE (Set.Set STATE)

if_then_else :: Bool -> a -> a -> a
if_then_else True val _ = val
if_then_else False _ val = val
    
reachable_states :: Set.Set STATE
reachable_states = reachable_states_func Set.empty initial_states
  where
    reachable_states_func :: Set.Set STATE -> Set.Set STATE -> Set.Set STATE
    reachable_states_func seen_states states_to_explore
      | Set.null unvisited_states = seen_states
      | otherwise = reachable
      where
        unvisited_states = Set.difference states_to_explore seen_states
        reachable = reachable_states_func (Set.union seen_states unvisited_states) (Set.unions (Set.map next_states unvisited_states))

state_map :: STATE_MAP
state_map = construct_state_map Map.empty (Map.fromList [(new_state, Set.empty) | new_state <- Set.toList initial_states])
  where
    dummy_next_states :: STATE -> a -> Set.Set STATE
    dummy_next_states state _ = next_states state
    construct_state_map :: STATE_MAP -> STATE_MAP -> STATE_MAP
    construct_state_map seen_map to_explore_map
      | Map.null unvisited_map = seen_map
      | otherwise = full_map
      where
        unvisited_map = Map.difference to_explore_map seen_map
        explored_map = Map.mapWithKey dummy_next_states unvisited_map
        new_seen_map
          | Map.size seen_map > Map.size explored_map = Map.union seen_map explored_map
          | otherwise = Map.union explored_map seen_map
        nextExplore = Map.fromList [(new_state, Set.empty) | new_state <- Set.toList (Set.unions (Map.elems explored_map))]
        full_map = construct_state_map new_seen_map nextExplore

reversed_map_lookup :: STATE_MAP -> STATE -> Set.Set STATE
reversed_map_lookup state_map state = fromJust (Map.lookup state state_map)

ctl_ax :: (STATE -> Bool) -> STATE -> Bool
ctl_ax function state = Set.foldr ((&&) . function) True (fromJust (Map.lookup state state_map))

ctl_ex :: (STATE -> Bool) -> STATE -> Bool
ctl_ex function state = Set.foldr ((||) . function) False (fromJust (Map.lookup state state_map))

ctl_af :: (STATE -> Bool) -> STATE -> Bool
ctl_af function = ctl_af_state_search function Set.empty
ctl_af_state_search :: (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_af_state_search function seen_states state
  | function state = True
  | Set.member state seen_states = False -- This means we haven't reached true and have nothing left to check
  | otherwise = Set.foldr ((&&) . ctl_af_state_search function (Set.insert state seen_states)) True (fromJust (Map.lookup state state_map)) -- more searching required.


ctl_ef :: (STATE -> Bool) -> STATE -> Bool
ctl_ef function state = (||) (function state) (ctl_ef_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
ctl_ef_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_ef_state_search function seen_states states_to_explore
  | Set.null unexplored_states = False -- This means we haven't reached true and have nothing left to check
  | otherwise = conclusion -- This means we still have states to check
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    found_true = Set.foldr ((||) . function) False unexplored_states -- check if the condition holds for any of the new states
    conclusion
      | found_true = True -- if the condition holds for any of the new states, then we're done.
      | otherwise = ctl_ef_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- more searching required.


ctl_ag :: (STATE -> Bool) -> STATE -> Bool
ctl_ag function state = (&&) (function state) (ctl_ag_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
ctl_ag_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_ag_state_search function seen_states states_to_explore
  | Set.null unexplored_states = True -- we ran out of states and found nothing wrong, return true.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    all_true = Set.foldr ((&&) . function) True unexplored_states -- check if the condition holds for all of the new states
    conclusion
      | not all_true = False -- at least one of our current states failed, so it didn't hold globally.
      | otherwise = ctl_ag_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- keep searching


ctl_eg :: (STATE -> Bool) -> STATE -> Bool
ctl_eg function = ctl_eg_state_search function Set.empty
ctl_eg_state_search :: (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_eg_state_search function seen_states state
  | not (function state) = False -- it doesn't hold for the state, so it's not true.
  | Set.member state seen_states = True -- we've looped!
  | otherwise = Set.foldr ((||) . ctl_eg_state_search function (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.


ctl_au :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_au function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_au_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
ctl_au_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_au_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = False -- we ran out of states and at least one path didn't terminate with the release.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
    allTrue = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctl_au_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


ctl_eu :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_eu function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_eu_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
ctl_eu_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_eu_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = False -- we ran out of states and no path terminated with the release.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    release_found = Set.foldr ((||) . function_release) False unexplored_states -- check if the condition holds for all of the not released states
    holding_states = Set.filter function_hold unexplored_states -- Filter so we only have states where the release condition is false.
    conclusion
      | release_found = True -- we managed to reach the release
      | otherwise = ctl_eu_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty holding_states) -- keep searching


ctl_aw :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_aw function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_aw_state_search function_hold function_release Set.empty (fromJust (Map.lookup state state_map))))
ctl_aw_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_aw_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = True -- we ran out of states and there were no problems
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
    all_true = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
    conclusion
      | not all_true = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctl_aw_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


ctl_ew :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_ew function_hold function_release = ctl_ew_state_search function_hold function_release Set.empty
ctl_ew_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_ew_state_search function_hold function_release seen_states state
  | function_release state = True
  | not (function_hold state) = False
  | otherwise = Set.foldr ((||) . ctl_ew_state_search function_hold function_release (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.

ctl_0 :: Bool
ctl_0 = Set.foldr ((&&) . ctl_func) True initial_states
    where
        ctl_func :: STATE -> Bool
        ctl_func state = (ctl_af (\state -> ((==) (remaining_goals___ state) (0))) state)

main :: IO ()
main = 
    do {
        print "model checking for Simple_robot_100"
       ; print (length reachable_states)
        --; putStrLn ((++) "ctl_0 is " (show ctl_0))
    }
