module Behavior_tree_core where
import Behavior_tree_environment
import Behavior_tree_blackboard

-- Data Declarations

data BTreeNodeStatus = Success | Running | Failure | Invalid
  deriving (Enum, Eq, Show)

data BTreeStatusTree = BTreeStatusTree
  {
  val :: BTreeNodeStatus
  , subTree :: [BTreeStatusTree]
  } deriving (Show)

data BTreeNode =  BTreeNode
  { nodeFunction :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
  -- Node Function has seperate status and [BTreeStatusTree] so that it's easier to recurse.
  , nodeChildren :: [BTreeNode]
  , locationInTree :: TreeLocation
  }

----------------------------End of data declarations
-- Type Declarations

type MemoryStorage = BTreeStatusTree

type MemoryStatus = BTreeNodeStatus

type PartialMemoryStorage = BTreeStatusTree

type PartialMemoryStatus = BTreeNodeStatus

type FutureChanges = [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)]

type TreeLocation = Int

type TreeOutput = (BTreeNodeStatus, MemoryStorage, PartialMemoryStorage, BTreeBlackboard, BTreeEnvironment, FutureChanges)

type BTreeNodeOutput = (BTreeNodeStatus, [MemoryStorage], [PartialMemoryStorage], BTreeBlackboard, BTreeEnvironment, FutureChanges)

----------------------------End of Type declarations
-- Blank slate memory creation

allInvalid :: BTreeNode -> BTreeStatusTree
allInvalid node
  | null (nodeChildren node) = BTreeStatusTree Invalid []
  | otherwise = BTreeStatusTree Invalid (map allInvalid (nodeChildren node))


nodeChildrenInvalid :: BTreeNode -> BTreeNodeStatus -> BTreeStatusTree
nodeChildrenInvalid node status
  | null (nodeChildren node) = BTreeStatusTree status []
  | otherwise = BTreeStatusTree status (map allInvalid (nodeChildren node))

----------------------------End of Blank Slate Memory Creation
-- unpack tuples

getBTreeNodeStatus :: (a, b, c, d, e, f) -> a
getBTreeNodeStatus (status, _, _, _, _, _) = status

getBTreeMemory :: (a, b, c, d, e, f) -> b
getBTreeMemory (_, memory, _, _, _, _) = memory

getBTreePartial :: (a, b, c, d, e, f) -> c
getBTreePartial (_, _, partial, _, _, _) = partial

getBTreeBlackboard :: (a, b, c, d, e, f) -> d
getBTreeBlackboard (_, _, _, blackboard, _, _) = blackboard

getBTreeEnvironment :: (a, b, c, d, e, f) -> e
getBTreeEnvironment (_, _, _, _, environment, _) = environment

getFutureChanges :: (a, b, c, d, e, f) -> f
getFutureChanges (_, _, _, _, _, changes) = changes

----------------------------End of unpack tuples



evaluateTree :: BTreeNode -> BTreeStatusTree -> BTreeStatusTree -> BTreeBlackboard -> BTreeEnvironment -> TreeOutput
evaluateTree node memoryStorage partialMemoryStorage blackboard environment = evaluateBTreeNode node memoryStorage partialMemoryStorage blackboard environment []


evaluateBTreeNode :: BTreeNode -> BTreeStatusTree -> BTreeStatusTree -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> TreeOutput
evaluateBTreeNode node memoryStorage partialMemoryStorage blackboard environment futureChanges = (newStatus, newMemory, newPartial, newBlackboard, newEnvironment, newFutureChanges)
  where result = nodeFunction node (nodeChildren node) (locationInTree node) (val memoryStorage) (subTree memoryStorage) (val partialMemoryStorage) (subTree partialMemoryStorage) blackboard environment futureChanges
        newStatus = getBTreeNodeStatus result
        newMemory = BTreeStatusTree newStatus (getBTreeMemory result)
        newPartial
          | newStatus == Running = BTreeStatusTree newStatus (getBTreePartial result)
          | otherwise = nodeChildrenInvalid node newStatus
        newBlackboard = getBTreeBlackboard result
        newEnvironment = getBTreeEnvironment result
        newFutureChanges = getFutureChanges result


--START OF SELECTOR

selectorFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
selectorFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Failure, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        nextResult
          | getBTreeNodeStatus result == Failure = selectorFunc (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial


selectorMemoryFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
selectorMemoryFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Failure, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | memoryStatus == Running && val (head memoryStorage) /= Running = (val (head memoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        newMemoryStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | memoryStatus == Running && val (head memoryStorage) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = memoryStatus
        nextResult
          | getBTreeNodeStatus result == Failure = selectorMemoryFunc (tail nodeChildren) nodeLocation newMemoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial


selectorPartialFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
selectorPartialFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Failure, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | partialStatus == Running && val (head partialMemoryStorage) /= Running = (val (head partialMemoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        newPartialStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | partialStatus == Running && val (head partialMemoryStorage) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = partialStatus
        nextResult
          | getBTreeNodeStatus result == Failure = selectorPartialFunc (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) newPartialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial
-- END OF SELECTOR
-- START OF SEQUENCE
sequenceFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
sequenceFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Success, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        nextResult
          | getBTreeNodeStatus result == Success = sequenceFunc (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial


sequenceMemoryFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
sequenceMemoryFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Success, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | memoryStatus == Running && val (head memoryStorage) /= Running = (val (head memoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        newMemoryStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | memoryStatus == Running && val (head memoryStorage) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = memoryStatus
        nextResult
          | getBTreeNodeStatus result == Success = sequenceMemoryFunc (tail nodeChildren) nodeLocation newMemoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial


sequencePartialFunc :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
sequencePartialFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren  = (Success, [], [], blackboard, environment, futureChanges) -- base case of no more nodeChildren
  | otherwise = (getBTreeNodeStatus nextResult, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | partialStatus == Running && val (head partialMemoryStorage) /= Running = (val (head partialMemoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges) --skip this child because we need to resume from the child that returned running
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
        newPartialStatus -- this is used to ensure we stop skipping after we find the child that returned running
          | partialStatus == Running && val (head partialMemoryStorage) == Running = Invalid --since we found the child that returned running, we now swap this to invalid
          | otherwise = partialStatus
        nextResult
          | getBTreeNodeStatus result == Success = sequencePartialFunc (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) newPartialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result) --run next child, because we aren't finished
          | otherwise = (getBTreeNodeStatus result, tail memoryStorage, tail partialMemoryStorage, getBTreeBlackboard result, getBTreeEnvironment result, getFutureChanges result) --we finished.
        newMemory = getBTreeMemory result : getBTreeMemory nextResult --compile memory
        newPartial = getBTreePartial result : getBTreePartial nextResult --compile partial
--END OF SEQUENCE
--START OF PARALLEL BASE
parallelBase :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> ([BTreeNodeStatus], [BTreeStatusTree], [BTreeStatusTree], BTreeBlackboard, BTreeEnvironment, FutureChanges)
parallelBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren = ([], [], [], blackboard, environment, futureChanges)
  | otherwise = (newStatuses, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges
        nextResult = parallelBase (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result)
        newStatuses = getBTreeNodeStatus result : getBTreeNodeStatus nextResult
        newMemory = getBTreeMemory result : getBTreeMemory nextResult
        newPartial = getBTreePartial result : getBTreePartial nextResult


parallelMemoryBase :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> ([BTreeNodeStatus], [BTreeStatusTree], [BTreeStatusTree], BTreeBlackboard, BTreeEnvironment, FutureChanges)
parallelMemoryBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren = ([], [], [], blackboard, environment, futureChanges)
  | otherwise = (newStatuses, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | memoryStatus == Running && val (head memoryStorage) /= Running = (val (head memoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges)
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges
        nextResult = parallelMemoryBase (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result)
        newStatuses = getBTreeNodeStatus result : getBTreeNodeStatus nextResult
        newMemory = getBTreeMemory result : getBTreeMemory nextResult
        newPartial = getBTreePartial result : getBTreePartial nextResult


parallelPartialBase :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> ([BTreeNodeStatus], [BTreeStatusTree], [BTreeStatusTree], BTreeBlackboard, BTreeEnvironment, FutureChanges)
parallelPartialBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | null nodeChildren = ([], [], [], blackboard, environment, futureChanges)
  | otherwise = (newStatuses, newMemory, newPartial, getBTreeBlackboard nextResult, getBTreeEnvironment nextResult, getFutureChanges nextResult)
  where result
          | partialStatus == Running && val (head partialMemoryStorage) /= Running = (val (head partialMemoryStorage), head memoryStorage, head partialMemoryStorage, blackboard, environment, futureChanges)
          | otherwise = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges
        nextResult = parallelPartialBase (tail nodeChildren) nodeLocation memoryStatus (tail memoryStorage) partialStatus (tail partialMemoryStorage) (getBTreeBlackboard result) (getBTreeEnvironment result) (getFutureChanges result)
        newStatuses = getBTreeNodeStatus result : getBTreeNodeStatus nextResult
        newMemory = getBTreeMemory result : getBTreeMemory nextResult
        newPartial = getBTreePartial result : getBTreePartial nextResult

        
parallelCreator :: ([BTreeNodeStatus] -> BTreeNodeStatus) -> ([BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
parallelCreator conditionFunction = parallelFunc
  where parallelFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
          = (conditionFunction (getBTreeNodeStatus result),
              getBTreeMemory result,
              getBTreePartial result,
              getBTreeBlackboard result,
              getBTreeEnvironment result,
              getFutureChanges result)
          where result = parallelBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges

parallelMemoryCreator :: ([BTreeNodeStatus] -> BTreeNodeStatus) -> ([BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
parallelMemoryCreator conditionFunction = parallelFunc
  where parallelFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
          = (conditionFunction (getBTreeNodeStatus result),
              getBTreeMemory result,
              getBTreePartial result,
              getBTreeBlackboard result,
              getBTreeEnvironment result,
              getFutureChanges result)
          where result = parallelMemoryBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges

parallelPartialCreator :: ([BTreeNodeStatus] -> BTreeNodeStatus) -> ([BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
parallelPartialCreator conditionFunction = parallelFunc
  where parallelFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
          = (conditionFunction (getBTreeNodeStatus result),
              getBTreeMemory result,
              getBTreePartial result,
              getBTreeBlackboard result,
              getBTreeEnvironment result,
              getFutureChanges result)
          where result = parallelPartialBase nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges

--END OF PARALLEL
--start of basic parallel templates

isFailure :: BTreeNodeStatus -> Bool
isFailure status
  | status == Failure = True
  | otherwise = False

isRunning :: BTreeNodeStatus -> Bool
isRunning status
  | status == Running = True
  | otherwise = False

isSuccess :: BTreeNodeStatus -> Bool
isSuccess status
  | status == Success = True
  | otherwise = False

successOnAllFailureOne :: [BTreeNodeStatus] -> BTreeNodeStatus
successOnAllFailureOne statuses
  | null statuses = Running
  | any isFailure statuses = Failure
  | any isRunning statuses = Running
  | otherwise = Success

successOnOneFailureOne :: [BTreeNodeStatus] -> BTreeNodeStatus
successOnOneFailureOne statuses
  | null statuses = Running
  | any isFailure statuses = Failure
  | any isSuccess statuses = Success
  | otherwise = Running

successOnOneFailureOnImpossible :: [BTreeNodeStatus] -> BTreeNodeStatus
successOnOneFailureOnImpossible statuses
  | null statuses = Running
  | any isSuccess statuses = Success
  | any isRunning statuses = Running
  | otherwise = Failure



---


xISyCreator :: BTreeNodeStatus -> BTreeNodeStatus -> (BTreeNodeStatus -> BTreeNodeStatus)
xISyCreator x y = xISyFunc
  where
    xISyFunc :: BTreeNodeStatus -> BTreeNodeStatus
    xISyFunc status
      | status == x = y
      | otherwise = status


inverterCreator = inverterFunc
  where
    inverterFunc :: BTreeNodeStatus -> BTreeNodeStatus
    inverterFunc Success = Failure
    inverterFunc Failure = Success
    inverterFunc x = x



--type BTreeNodeOutput = (BTreeNodeStatus, [MemoryStorage], [PartialMemoryStorage], BTreeBlackboard, BTreeEnvironment, FutureChanges)

decoratorCreator :: (BTreeNodeStatus -> BTreeNodeStatus) -> ([BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)
decoratorCreator statusFunc nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges =
  (statusFunc (getBTreeNodeStatus result),
   [getBTreeMemory result],
   [getBTreePartial result],
   getBTreeBlackboard result,
   getBTreeEnvironment result,
   getFutureChanges result)
  where
    result = evaluateBTreeNode (head nodeChildren) (head memoryStorage) (head partialMemoryStorage) blackboard environment futureChanges --run current child
