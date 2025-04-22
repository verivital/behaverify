'''
This was written by Serena Serafina Serbinowska.
'''
from bt_verification import Behaviour, combine, entails, preconditions
import spot
spot.setup()

'''
Here we create some behaviors, as presented in Table 1. The arguments of this constructor are: name, success conditions, failure conditions, guarantee. We use Spot's LTL syntax: G globally (always), F eventually, X next, ! Boolean not, & Boolean and, | Boolean or and -> as implication.
'''
send = Behaviour('send','false','!data','F(sent & !data)')
panels = Behaviour('panels','false','false','charge & (day -> F!lowpower)')
hibernate = Behaviour('hibernate','false','false','hibernating')
getdata = Behaviour('getData','data','false','Fdata')

# cell 3
print('NOW ON: cell 03')
'''
We also construct a behavior for the environment, E.
'''
E = Behaviour('env','false','false',"""GFday & FG!storm & (FGlowpower | FG!lowpower) & (dead -> (lowpower & !(charge | hibernating))) & (damaged -> (storm & !hibernating))""")

# cell 4
print('NOW ON: cell 04')
'''
Now we use the operators defined in the paper to construct a behavior modelling the entire tree T, which we now call B. For this we use the combine function, which takes a string giving the structure of the tree and a list of behaviors contained in the tree. Behaviors modelling conditions are implicitly created where necessary.
'''
B = combine('(lowpower->panels)?(storm->hibernate)?(getData->send)',
            [panels,hibernate,getdata,send])

# cell 5
print('NOW ON: cell 05')
'''
Here we construct formulas to give the sets of logical runs of B and E. Also, we construct the formula representing the desired specification.
'''
log_run_B = spot.formula.G(spot.formula.Or((B.success,B.failure,B.guarantee)))
log_run_E = spot.formula.G(spot.formula.Or((E.success,E.failure,E.guarantee)))
specification = spot.formula('G!damaged & G!dead & Fsent')

# cell 6
print('NOW ON: cell 06')
'''
Now we need only check that log_run_B & log_run_E entails specification, which is done with the following function entails.
'''
entails(spot.formula.And((log_run_B,log_run_E)),specification)

# cell 7
print('NOW ON: cell 07')
'''
By observing the generated counterexample, we note that the robot is damaged as lowpower and storm are simultaneously true in the initial state but the robot chooses to charge rather than hibernate. To correct this, we swap the order of these two subtrees and try again:
'''
B = combine('(storm->hibernate)?(lowpower->panels)?(getData->send)',
            [panels,hibernate,getdata,send])

log_run_B = spot.formula.G(spot.formula.Or((B.success,B.failure,B.guarantee)))
log_run_E = spot.formula.G(spot.formula.Or((E.success,E.failure,E.guarantee)))
specification = spot.formula('G!damaged & G!dead & Fsent')

entails(spot.formula.And((log_run_B,log_run_E)),specification)

# cell 8
print('NOW ON: cell 08')
'''
So now this tree is correct. Now suppose we wish to replace the Action GetData with a new subtree. We introduce some new behaviors:
'''
gotobase = Behaviour('goToBase','atBase','false','FatBase & ((holding & Xholding)|(!holding & X!holding))')
place = Behaviour('place','false','!holding','atBase -> F(!holding & sample)')
getrock = Behaviour('getRock','holding','false','Fholding')
analyse = Behaviour('analyse','false','!sample','!broken -> Fdata')
fix = Behaviour('fix','!broken','false','F!broken')


# cell 9
print('NOW ON: cell 09')
'''
And combine these to form a new behavior `G`:
'''
G = combine('data?(((sample ? (((holding ? getRock) -> (atBase ? goToBase)) -> place)) -> ((!broken) ? fix)) -> analyse)',
            [gotobase,place,getrock,analyse,fix])
print("Success:",G.success)
print("Failure:",G.failure)

# cell 10
print('NOW ON: cell 10')
'''
We observe that the success and failure conditions are the same as that of getData. Now, to check if the modified tree is still correct, we firstly check the safety conditions. To do this, we construct a behavior idle which is strongly refined by G and check if the safety conditions are still satisfied.
'''
idle = Behaviour('idle','data','false','true')
safety = spot.formula('G!damaged & G!dead')
B_id = combine('(storm->hibernate)?(lowpower->panels)?(idle->send)',
                [panels,hibernate,send,idle])

log_run_B_id = spot.formula.G(spot.formula.Or((B_id.success,B_id.failure,B_id.guarantee)))
log_run_E = spot.formula.G(spot.formula.Or((E.success,E.failure,E.guarantee)))
B_id_and_E = spot.formula.And((log_run_B_id,log_run_E))

entails(B_id_and_E,safety)

# cell 11
print('NOW ON: cell 11')
'''
Now that we know that the safety conditions must hold in any strong refinement of idle. As any refinement of getData is a strong refinement of idle, we need only check whether the liveness condition F sent still holds. Firstly, we will prove that FG prec_K holds, and then show that G refines getData.
'''
preconditions('(storm->hibernate)?(lowpower->panels)?(getData->send)',
              'getData',
              [panels,hibernate,send,getdata])
entails(B_id_and_E,spot.formula('FG(!lowpower & !storm)'))

# cell 12
print('NOW ON: cell 12')
'''
Then, for any strong refinement of idle, we can conclude that G!dead & G!dead & FG!lowpower & FG!storm holds. Now to show that the modified tree with G works we need only show that G refines getData, when run against the environment. Many of the variables, such as day, lowpower, storm, etc. cannot affect whether this is true because they do not exist in the new behavior or the new specification F data, so we can remove them from the environment. We create a new environment behavior E2:
'''
E2 = Behaviour('env','false','false','FG broken | FG!broken')

# cell 13
print('NOW ON: cell 13')
'''
Now we need to check that this behavior satisfies G(data | false | F data). If this is satisfied, then we can replace getData by G in the original tree above and it will remain correct, as proved in the paper.
'''
log_run_G = spot.formula.G(spot.formula.Or((G.success,G.failure,G.guarantee)))
log_run_E2 = spot.formula.G(spot.formula.Or((E2.success,E2.failure,E2.guarantee)))

entails(spot.formula.And((log_run_G,log_run_E2)),spot.formula('data | Fdata'))

# cell 14
print('NOW ON: cell 14')
'''
So G refines getData, as required.
'''


print('FINISHED')
