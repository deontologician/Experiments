module Main where

import Random
import Control.Monad.Random
import Control.Monad
import Control.Applicative
import Data.Tree 
import Data.List
import Data.Monoid

data Result = Result { size :: Int
                         ,height :: Int
                         ,survey :: (Int,Int,Int,Int)
                       }
                    deriving (Show, Eq, Ord)

main :: IO ()
main = do
  sg <- getStdGen
  putStrLn "How many samples?"
  times <- read <$> getLine
  let results = evalRand (createLoop times) sg
  putStrLn $ "Max height: " ++ (show $ maximum' height results)
  putStrLn $ "Max size: " ++ (show $ maximum' size results)
  putStrLn $ "Survey total: " ++ (show $ surveyResults results)
  putStrLn $ "Size histogram: " ++ (show $ histogram size results)
  putStrLn $ "Height histogram: " ++ (show $ histogram height results)

createLoop :: Int -> Rand StdGen [Result]
createLoop samples = forM  [0 .. samples] $ \_ -> do
           t <- randTree
           return $ Result (treeSize t) (treeHeight t) (treeSurvey t)

randTree :: Rand StdGen (Tree String)
randTree = do
  numBranches <- getRandomR (0, 3::Int)
  case numBranches of
    0 -> return leaf
    1 -> (\right -> Node "1" [leaf, right]) <$> randTree
    2 -> (\left -> Node "2" [left, leaf]) <$> randTree
    3 -> liftM2 (\left right -> Node "3" [left, right]) randTree randTree
    _ -> error "Shouldn't happen"
  where leaf = Node "0" []
      

treeSize :: Tree a -> Int
treeSize = length . flatten

treeHeight :: Tree a -> Int
treeHeight = length . levels

treeSurvey :: Tree String -> (Int,Int,Int,Int)
treeSurvey (Node x sub) = mappend (forestSurvey sub) $ case x of
                                                       "0" -> (1,0,0,0)
                                                       "1" -> (0,1,0,0)
                                                       "2" -> (0,0,1,0)
                                                       "3" -> (0,0,0,1)
                                                       bad -> error $ "Bad tree label: " ++ bad

forestSurvey :: [Tree String] -> (Int,Int,Int,Int)
forestSurvey = mconcat . map treeSurvey

instance Monoid Int where
    mempty = 0
    mappend = (+)

max' :: (Result -> Int) -> Int -> Result -> Int
max' f base new = max base (f new)

maximum' :: (Result -> Int) -> [Result] -> Int
maximum' f = foldl' (max' f) 0

totalSize :: [Result] -> Int
totalSize = foldl' (\a b -> a + (size b)) 0

histogram :: (Result -> Int) -> [Result] -> [(Int, Int)]
histogram f xs = [ (head l, length l) | l <- group . sort . map f $ xs ]


surveyResults :: [Result] -> (Int,Int,Int,Int)
surveyResults = mconcat . map survey