module Behavior_tree_core where
import Behavior_tree_environment

data NodeStatus = Success | Running | Failure | Invalid
  deriving (Enum, Eq, Show)

data MemoryTree = MemoryTree {
  val :: NodeStatus
  , subTree :: [MemoryTree]
  } deriving (Show)

type Codes = [Environment -> Environment]

type TreeOutput = (NodeStatus, Codes, Environment, MemoryTree, MemoryTree)

type NodeOutput = (NodeStatus, Codes, Environment, [MemoryTree], [MemoryTree])

data Node =  Node
  { evalFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
  , children :: [Node]
  }
  
----------------------------End of data declarations

getStatus :: (a, b, c, d, e) -> a
getStatus (status, _, _, _, _) = status

getCodes :: (a, b, c, d, e) -> b
getCodes (_, codes, _, _, _) = codes

getTreeEnvironment :: (a, b, c, d, e) -> c
getTreeEnvironment (_, _, environment, _, _) = environment

getMemory :: (a, b, c, d, e) -> d
getMemory (_, _, _, memory, _) = memory

getPartial :: (a, b, c, d, e) -> e
getPartial (_, _, _, _,  partial) = partial

allInvalid :: Node -> MemoryTree
allInvalid node
  | null (children node) = MemoryTree Invalid []
  | otherwise = MemoryTree Invalid (map allInvalid (children node))


childrenInvalid :: Node -> NodeStatus -> MemoryTree
childrenInvalid node status
  | null (children node) = MemoryTree status []
  | otherwise = MemoryTree status (map allInvalid (children node))

----------------------------End of data manipulators



evaluateTree :: Node -> MemoryTree -> MemoryTree -> Environment -> TreeOutput
evaluateTree node memoryTree partialTree environment = evaluateNode node memoryTree partialTree environment []


evaluateNode :: Node -> MemoryTree -> MemoryTree -> Environment -> Codes -> TreeOutput
evaluateNode node memoryTree partialTree environment codes = (newStatus, newCodes, newEnvironment, newMemory, newPartial)
  where result = evalFunc node (children node) (val memoryTree) (subTree memoryTree) (val partialTree) (subTree partialTree) environment codes
        newStatus = getStatus result
        newCodes = getCodes result
        newEnvironment = getTreeEnvironment result
        newMemory = MemoryTree newStatus (getMemory result)
        newPartial
          | newStatus == Running = MemoryTree newStatus (getPartial result)
          | otherwise = childrenInvalid node newStatus


--START OF SELECTOR

selectorFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
selectorFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Failure, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        nextResult
          | getStatus result == Failure = selectorFunc (tail children) memoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial


selectorMemoryFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
selectorMemoryFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Failure, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | memoryStatus == Running && val (head memoryTree) /= Running = (val (head memoryTree), codes, environment, head memoryTree, head partialTree) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        newMemoryStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | memoryStatus == Running && val (head memoryTree) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = memoryStatus
        nextResult
          | getStatus result == Failure = selectorMemoryFunc (tail children) newMemoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial


selectorPartialFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
selectorPartialFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Failure, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | partialStatus == Running && val (head partialTree) /= Running = (val (head partialTree), codes, environment, head memoryTree, head partialTree) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        newPartialStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | partialStatus == Running && val (head partialTree) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = partialStatus
        nextResult
          | getStatus result == Failure = selectorPartialFunc (tail children) memoryStatus (tail memoryTree) newPartialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial
-- END OF SELECTOR
-- START OF SEQUENCE
sequenceFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
sequenceFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Success, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        nextResult
          | getStatus result == Success = sequenceFunc (tail children) memoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial


sequenceMemoryFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
sequenceMemoryFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Success, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | memoryStatus == Running && val (head memoryTree) /= Running = (val (head memoryTree), codes, environment, head memoryTree, head partialTree) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        newMemoryStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | memoryStatus == Running && val (head memoryTree) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = memoryStatus
        nextResult
          | getStatus result == Success = sequenceMemoryFunc (tail children) newMemoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial


sequencePartialFunc :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
sequencePartialFunc children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children  = (Success, codes, environment, [], []) -- base case of no more children
  | otherwise = (getStatus nextResult, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | partialStatus == Running && val (head partialTree) /= Running = (val (head partialTree), codes, environment, head memoryTree, head partialTree) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes --run current child
        newPartialStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | partialStatus == Running && val (head partialTree) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = partialStatus
        nextResult
          | getStatus result == Success = sequencePartialFunc (tail children) memoryStatus (tail memoryTree) newPartialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result) --run next child, because we aren't finished
          | otherwise = (getStatus result, getCodes result, getTreeEnvironment result, tail memoryTree, tail partialTree) --we finished.
        newMemory = getMemory result : getMemory nextResult --compile memory
        newPartial = getPartial result : getPartial nextResult --compile partial
--END OF SEQUENCE
--START OF PARALLEL BASE
parallelBase :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> ([NodeStatus], Codes, Environment, [MemoryTree], [MemoryTree])
parallelBase children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children = ([], codes, environment, [], [])
  | otherwise = (newStatuses, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes
        nextResult = parallelBase (tail children) memoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result)
        newStatuses = getStatus result : getStatus nextResult
        newMemory = getMemory result : getMemory nextResult
        newPartial = getPartial result : getPartial nextResult


parallelMemoryBase :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> ([NodeStatus], Codes, Environment, [MemoryTree], [MemoryTree])
parallelMemoryBase children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children = ([], codes, environment, [], [])
  | otherwise = (newStatuses, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | memoryStatus == Running && val (head memoryTree) /= Running = (val (head memoryTree), codes, environment, head memoryTree, head partialTree)
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes
        nextResult = parallelMemoryBase (tail children) memoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result)
        newStatuses = getStatus result : getStatus nextResult
        newMemory = getMemory result : getMemory nextResult
        newPartial = getPartial result : getPartial nextResult


parallelPartialBase :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> ([NodeStatus], Codes, Environment, [MemoryTree], [MemoryTree])
parallelPartialBase children memoryStatus memoryTree partialStatus partialTree environment codes
  | null children = ([], codes, environment, [], [])
  | otherwise = (newStatuses, getCodes nextResult, getTreeEnvironment nextResult, newMemory, newPartial)
  where result
          | partialStatus == Running && val (head partialTree) /= Running = (val (head partialTree), codes, environment, head memoryTree, head partialTree)
          | otherwise = evaluateNode (head children) (head memoryTree) (head partialTree) environment codes
        nextResult = parallelPartialBase (tail children) memoryStatus (tail memoryTree) partialStatus (tail partialTree) (getTreeEnvironment result) (getCodes result)
        newStatuses = getStatus result : getStatus nextResult
        newMemory = getMemory result : getMemory nextResult
        newPartial = getPartial result : getPartial nextResult

        
parallelCreator :: ([NodeStatus] -> NodeStatus) -> ([Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput)
parallelCreator conditionFunction = parallelFunc
  where parallelFunc children memoryStatus memoryTree partialStatus partialTree environment codes = (conditionFunction (getStatus result),
                                                                                                     getCodes result,
                                                                                                     getTreeEnvironment result,
                                                                                                     getMemory result,
                                                                                                     getPartial result)
          where result = parallelBase children memoryStatus memoryTree partialStatus partialTree environment codes

parallelMemoryCreator :: ([NodeStatus] -> NodeStatus) -> ([Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput)
parallelMemoryCreator conditionFunction = parallelFunc
  where parallelFunc children memoryStatus memoryTree partialStatus partialTree environment codes = (conditionFunction (getStatus result),
                                                                                                     getCodes result,
                                                                                                     getTreeEnvironment result,
                                                                                                     getMemory result,
                                                                                                     getPartial result)
          where result = parallelMemoryBase children memoryStatus memoryTree partialStatus partialTree environment codes

parallelPartialCreator :: ([NodeStatus] -> NodeStatus) -> ([Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput)
parallelPartialCreator conditionFunction = parallelFunc
  where parallelFunc children memoryStatus memoryTree partialStatus partialTree environment codes = (conditionFunction (getStatus result),
                                                                                                     getCodes result,
                                                                                                     getTreeEnvironment result,
                                                                                                     getMemory result,
                                                                                                     getPartial result)
          where result = parallelPartialBase children memoryStatus memoryTree partialStatus partialTree environment codes

--END OF PARALLEL
--start of basic parallel templates

isFailure :: NodeStatus -> Bool
isFailure status
  | status == Failure = True
  | otherwise = False

isRunning :: NodeStatus -> Bool
isRunning status
  | status == Running = True
  | otherwise = False

isSuccess :: NodeStatus -> Bool
isSuccess status
  | status == Success = True
  | otherwise = False

successOnAllFailureOne :: [NodeStatus] -> NodeStatus
successOnAllFailureOne statuses
  | null statuses = Running
  | any isFailure statuses = Failure
  | any isRunning statuses = Running
  | otherwise = Success

successOnOneFailureOne :: [NodeStatus] -> NodeStatus
successOnOneFailureOne statuses
  | null statuses = Running
  | any isFailure statuses = Failure
  | any isSuccess statuses = Success
  | otherwise = Running

successOnOneFailureOnImpossible :: [NodeStatus] -> NodeStatus
successOnOneFailureOnImpossible statuses
  | null statuses = Running
  | any isSuccess statuses = Success
  | any isRunning statuses = Running
  | otherwise = Failure
