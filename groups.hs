module Groups (
               order, isEmpty, isAssociative, isCommutative,
               isIdempotent, isClosed, identityOf, hasIdentity,
               isInvertible, isSemigroup, isMonoid, isGroup,
               isAbelianGroup, classify, createZMod
              ) where

import qualified Data.Set as Set
import List

type Groupoid a = ([a], a->a->a)

data Magma a = Semigroup (Groupoid a) 
             | Monoid (Groupoid a)
             | Group (Groupoid a)
             | AbelianGroup (Groupoid a)

instance Show (Magma a) where
    show (Semigroup g) = "Semigroup of order " ++ (show $ order g)
    show (Monoid g) = "Monoid of order " ++ (show $ order g)
    show (Group g) = "Group of order " ++ (show $ order g)
    show (AbelianGroup g) = "Abelian Group of order " ++ (show $ order g)
               
order :: Groupoid a -> Int
order (s, _) = length s

isEmpty :: Groupoid a -> Bool
isEmpty ([], _) = True
isEmpty (x:xs, _) = False

isAssociative :: (Eq a) => Groupoid a -> Bool
isAssociative (s, o) = all (\(a,b,c) -> (a `o` b) `o` c == a `o` (b `o` c)) 
                    [(a,b,c) | a<-s, b<-s, c<-s] 

isCommutative :: (Eq a) => Groupoid a -> Bool
isCommutative (s, o) = all (\(a,b) -> a `o` b == b `o` a)
                       [(a,b) | a<-s, b<-s]

isIdempotent :: (Eq a) => Groupoid a -> Bool
isIdempotent (s, o) = all (\a -> a `o` a == a) s

isClosed :: (Eq a) => Groupoid a -> Bool
isClosed (s, o) = all (\(a,b) -> (a `o` b) `elem` s) 
                  [(a,b) | a<-s, b<-s]

identityOf :: (Eq a) => Groupoid a -> Maybe a 
identityOf (s, o) = find (\e -> all (\a -> (e `o` a == a) && 
                                           (a `o` e == a)
                                    ) s
                         ) s

hasIdentity :: (Eq a) => Groupoid a -> Bool
hasIdentity g = case identityOf g of Just _ -> True
                                     Nothing -> False

isInvertible :: (Eq a) => Groupoid a -> Bool
isInvertible g@(s, o) = let me = identityOf g
                        in
                          case me of 
                            Just e -> 
                                all (\a ->
                                         any (\b -> (a `o` b == e) && 
                                                    (b `o` a == e)
                                             ) s
                                    ) s 
                            Nothing -> False
-- Tests for classification

isSemigroup :: (Eq a) => Groupoid a -> Bool
isSemigroup g = isClosed g && isAssociative g

isMonoid :: (Eq a) => Groupoid a -> Bool
isMonoid g = isSemigroup g && not (isEmpty g) && hasIdentity g

isGroup :: (Eq a) => Groupoid a -> Bool
isGroup g = isMonoid g && isInvertible g

isAbelianGroup :: (Eq a) => Groupoid a -> Bool
isAbelianGroup g = isGroup g && isCommutative g

classify :: (Eq a) => Groupoid a -> Maybe (Magma a)
classify g 
    | isAbelianGroup g = Just (AbelianGroup g)
    | isGroup g        = Just (Group g)
    | isMonoid g       = Just (Monoid g)
    | isSemigroup g    = Just (Semigroup g)
    | otherwise        = Nothing

-- Some ways of creating groupoids

createZMod :: Int -> Groupoid Int
createZMod n
    | n <= 0 = ([0], (\x y -> x))
    | otherwise = ([0..(n-1)], (\x y -> mod (x + y) n))
