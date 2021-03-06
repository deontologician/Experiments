module Groups where

import Data.List (find)
import Prelude hiding ((*))
import Data.Maybe (isJust)

type Groupoid a = ([a], a->a->a)

data Magma a = Semigroup (Groupoid a) 
             | Monoid (Groupoid a)
             | Group (Groupoid a)
             | AbelianGroup (Groupoid a)
             | Magma (Groupoid a)

data Property = Associative | Unital | Idempotent | Commutative | Unipotent 
              | ZeroPotent | Alternative | PowerAssociative | Mediality Mediality 
              | Distributivity Distributivity | Cancellativity Cancellativity
              | Nullity Nullity

data Mediality = LeftSemiMedial | RightSemiMedial | SemiMedial | Medial 
               | NonMedial

data Distributivity = LeftDistributive | RightDistributive | AutoDistributive 
                    | NonDistributive

data Cancellativity = LeftCancellative | RightCancellative | Cancellative 
                    | NonCancellative

data Nullity = HasLeftZeroes | HasRightZeroes | Null | NonNull

instance Show Property where
    show Associative = "associative"
    show Commutative = "commutative"
    show Unital = "unital"
    show (Mediality LeftSemiMedial) = "left-semimedial"
    show (Mediality RightSemiMedial) = "right-semimedial"
    show (Mediality SemiMedial) = "semimedial"
    show (Mediality Medial) = "medial"
    show (Mediality NonMedial) = ""
    show (Distributivity LeftDistributive) = "left-distributive"
    show (Distributivity RightDistributive) = "right-distributive"
    show (Distributivity AutoDistributive) = "autodistributive"
    show (Distributivity NonDistributive) = ""
    show Idempotent = "idempotent"
    show Unipotent = "unipotent"
    show ZeroPotent = "zeropotent"
    show Alternative = "alternative"
    show PowerAssociative = "power-associative"
    show (Cancellativity LeftCancellative) = "left-cancellative"
    show (Cancellativity RightCancellative) = "right-cancellative"
    show (Cancellativity Cancellative) = "cancellative"
    show (Cancellativity NonCancellative) = ""
    show (Nullity HasLeftZeroes) = "has left zeroes"
    show (Nullity HasRightZeroes) = "has right zeroes"
    show (Nullity Null) = "null"
    show (Nullity NonNull) = ""

instance Show (Magma a) where
    show (Semigroup g) = "Semigroup of order " ++ show (order g)
    show (Monoid g) = "Monoid of order " ++ show (order g)
    show (Group g) = "Group of order " ++ show (order g)
    show (AbelianGroup g) = "Abelian Group of order " ++ show (order g)
    show (Magma g) = "Magma of order " ++ show (order g)

           
order :: Groupoid a -> Int
order (s, _) = length s

isEmpty :: Groupoid a -> Bool
isEmpty ([], _) = True
isEmpty (_:_, _) = False

isAssociative :: (Eq a) => Groupoid a -> Bool
isAssociative (s,(*)) = satisfy3 s (\(a,b,c) -> (a * b) * c == a * (b * c))

isCommutative :: (Eq a) => Groupoid a -> Bool
isCommutative (s,(*)) = satisfy2 s (\(a,b) -> a * b == b * a)

isIdempotent :: (Eq a) => Groupoid a -> Bool
isIdempotent (s,(*)) = all (\a -> a * a == a) s

isClosed :: (Eq a) => Groupoid a -> Bool
isClosed (s,(*)) = satisfy2 s(\(a,b) -> (a * b) `elem` s) 

-- http://en.wikipedia.org/wiki/Medial
isMedial :: (Eq a) => Groupoid a -> Bool
isMedial (s,(*)) = satisfy4 s (\(x,y,u,v) -> (x * y) * (u * v) == 
                                             (x * u) * (y * v))

isSemiMedial :: (Eq a) => Groupoid a -> Bool
isSemiMedial = isLeftSemiMedial &&&> isRightSemiMedial

isLeftSemiMedial :: (Eq a) => Groupoid a -> Bool
isLeftSemiMedial (s,(*)) = satisfy3 s (\(x,y,z) -> (x * x) * (y * z) ==
                                                   (x * y) * (x * z))

isRightSemiMedial :: (Eq a) => Groupoid a -> Bool
isRightSemiMedial (s,(*)) = satisfy3 s (\(x,y,z) -> (y * z) * (x * x) ==
                                                    (y * x) * (z * x))

mediality :: (Eq a) => Groupoid a -> Mediality
mediality g 
    | isMedial g = Medial
    | isSemiMedial g = SemiMedial
    | isLeftSemiMedial g = LeftSemiMedial
    | isRightSemiMedial g = RightSemiMedial
    | otherwise  = NonMedial

isLeftDistributive :: (Eq a) => Groupoid a -> Bool
isLeftDistributive (s,(*)) = satisfy3 s (\(x,y,z) -> x * (y * z) == 
                                                     (x * y) * (x * z))

isRightDistributive :: (Eq a) => Groupoid a -> Bool
isRightDistributive (s,(*)) = satisfy3 s (\(x,y,z) -> (y * z) * x == 
                                                      (y * x) * (z * x))

isAutoDistributive :: (Eq a) => Groupoid a -> Bool
isAutoDistributive = isLeftDistributive &&&> isRightDistributive

distributivity :: (Eq a) => Groupoid a -> Distributivity
distributivity g
    | isAutoDistributive g = AutoDistributive
    | isLeftDistributive g = LeftDistributive
    | isRightDistributive g = RightDistributive
    | otherwise = NonDistributive

isUnipotent :: (Eq a) => Groupoid a -> Bool
isUnipotent (s,(*)) = satisfy2 s (\(x,y) -> (x*x) == (y*y))

isZeroPotent :: (Eq a) => Groupoid a -> Bool
isZeroPotent (s,(*)) = satisfy2 s (\(x,y)-> let r1 = (x*x)*y
                                                r2 = (y*y)*x
                                                r3 = (x*x)
                                            in
                                              r1 == r2 && r2 == r3)

isAlternative :: (Eq a) => Groupoid a -> Bool
isAlternative (s,(*)) = satisfy2 s (\(x,y) -> let r1 = (x*x)*y
                                                  r2 = x*(x*y)
                                                  r3 = x*(y*y)
                                                  r4 = (x*y)*y
                                              in
                                                r1 == r2 && r3 == r4)

isUnital :: (Eq a) => Groupoid a -> Bool
isUnital = isJust . identityOf

isInvertible :: (Eq a) => Groupoid a -> Bool
isInvertible g@(s,(*)) = maybe False 
                         (\e -> all 
                          (\a -> any 
                           (\b -> (a * b == e) && 
                                  (b * a == e) ) s ) s)
                         $ identityOf g

isPowerAssociative :: (Eq a) => Groupoid a -> Bool
isPowerAssociative (s,(*)) = all isAssociative [([a],(*)) | a <- s]

isLeftCancellative :: (Eq a) => Groupoid a -> Bool
isLeftCancellative (s,(*)) = satisfy3 s (\(x,y,z) -> ((x*y) == (x*z)) ==> (y == z))

isRightCancellative :: (Eq a) => Groupoid a -> Bool
isRightCancellative (s,(*)) = satisfy3 s (\(x,y,z) -> ((y*x) == (z*x)) ==> (y == z))

isCancellative :: (Eq a) => Groupoid a -> Bool
isCancellative = isLeftCancellative &&&> isRightCancellative

cancellativity :: (Eq a) => Groupoid a -> Cancellativity
cancellativity g
    | isCancellative g = Cancellative
    | isRightCancellative g = RightCancellative
    | isLeftCancellative g = LeftCancellative
    | otherwise = NonCancellative

hasRightZeroes :: (Eq a) => Groupoid a -> Bool
hasRightZeroes (s,(*)) = satisfy2 s (\(x,y) -> y == (x*y))

hasLeftZeroes :: (Eq a) => Groupoid a -> Bool
hasLeftZeroes (s,(*)) = satisfy2 s (\(x,y) -> x == (x*y))

isNull :: (Eq a) => Groupoid a -> Bool
isNull = hasLeftZeroes &&&> hasRightZeroes

nullity :: (Eq a) => Groupoid a -> Nullity
nullity g
    | hasLeftZeroes g = HasLeftZeroes
    | hasRightZeroes g = HasRightZeroes
    | isNull g = Null
    | otherwise = NonNull

identityOf :: (Eq a) => Groupoid a -> Maybe a 
identityOf (s,(*)) = find (\e -> all (\a -> (e * a == a) && 
                                            (a * e == a)
                                    ) s
                          ) s

-- Tests for classification

isSemigroup :: (Eq a) => Groupoid a -> Bool
isSemigroup = isClosed &&&> isAssociative

isMonoid :: (Eq a) => Groupoid a -> Bool
isMonoid = isSemigroup &&&> (not . isEmpty) &&&> isUnital

isGroup :: (Eq a) => Groupoid a -> Bool
isGroup = isMonoid &&&> isInvertible

isAbelianGroup :: (Eq a) => Groupoid a -> Bool
isAbelianGroup = isGroup &&&> isCommutative

classify :: (Eq a) => Groupoid a -> Magma a
classify g 
    | isAbelianGroup g = AbelianGroup g
    | isGroup g        = Group g
    | isMonoid g       = Monoid g
    | isSemigroup g    = Semigroup g
    | otherwise        = Magma g

--getProperties :: (Eq a) => Groupoid a -> [Property]

-- Some ways of creating different magmas

createZMod :: Int -> Groupoid Int
createZMod 0 = ([0], \x _ -> x)
createZMod n = ([0..(n-1)], \x y -> mod (x + y) n)

-- Helper stuffs
allDoubles :: [a] -> [(a,a)]
allDoubles s = [(a,b) | a <- s, b <- s]

allTriples :: [a] -> [(a,a,a)]
allTriples s = [(a,b,c) | (a,b) <- allDoubles s, c <-s]

all4Tuples :: [a] -> [(a,a,a,a)]
all4Tuples s = [(a,b,c,d) | (a,b,c) <- allTriples s, d <- s]

satisfy :: [a] -> (a -> Bool) -> Bool
satisfy = flip all

satisfy2 :: [a] -> ((a,a) -> Bool) -> Bool
satisfy2 = satisfy . allDoubles

satisfy3 :: [a] -> ((a,a,a) -> Bool) -> Bool
satisfy3 = satisfy . allTriples

satisfy4 :: [a] -> ((a,a,a,a) -> Bool) -> Bool
satisfy4 = satisfy . all4Tuples

-- logical implication boolean operator
(==>) :: Bool -> Bool -> Bool
a ==> b = not a || b

-- This seems pretty general
bowleg :: (b -> c -> d) -> (a -> b) -> (a -> c) ->  a -> d
bowleg combine opA opB a = opA a `combine` opB a

-- Hey it turns out we can chain these, that's pretty sweet
(&&&>) :: (a -> Bool) -> (a -> Bool) -> a -> Bool
(&&&>) = bowleg (&&)

