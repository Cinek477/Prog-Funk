module Main where

import Data.Char (toLower, toUpper)
import Data.List (foldl')

sumWith :: Num a => (a -> a) -> [a] -> a
sumWith _ [] = 0
sumWith f (x:xs) = f x + sumWith f xs

df :: (Double -> Double) -> Double -> (Double -> Double)
df f h = \x -> (f (x+h)-f (x-h))/(2*h)

absErr :: Num a => (t -> a) -> (t -> a) -> t -> a
absErr exact approximate x = abs (exact x - approximate x)

mapOwn :: (a -> b) -> [a] -> [b]
mapOwn _ [] = []
mapOwn f (x:xs) = f x : mapOwn f xs

filterOwn :: (a -> Bool) -> [a] -> [a]
filterOwn _ [] = []
filterOwn p (x:xs)
  | p x = x : filterOwn p xs
  | otherwise = filterOwn p xs

foldrOwn :: (a -> b -> b) -> b -> [a] -> b
foldrOwn _ z [] = z
foldrOwn f z (x:xs) = f x (foldrOwn f z xs)

foldlOwn :: (b -> a -> b) -> b -> [a] -> b
foldlOwn _ z [] = z
foldlOwn f z (x:xs) = foldlOwn f (f z x) xs

zipWithOwn :: (a -> b -> c) -> [a] -> [b] -> [c]
zipWithOwn _ [] _ = []
zipWithOwn _ _ [] = []
zipWithOwn f (x:xs) (y:ys) = f x y : zipWithOwn f xs ys

unzipOwn :: [(a,b)] -> ([a],[b])
unzipOwn [] = ([],[])
unzipOwn ((x,y):rest) = (x:xs,y:ys)
  where (xs,ys) = unzipOwn rest

concatOwn :: [[a]] -> [a]
concatOwn = foldrOwn (++) []

capitalize :: String -> String
capitalize [] = []
capitalize (x:xs) = toUpper x : map toLower xs

formatNames :: String -> String
formatNames = unwords . map capitalize . filter (\w -> length w > 1) . words

-- Wersja dydaktyczna ze slajdu: czesciowa dla pustego wyniku filtrowania.
formatNamesSlide :: String -> String
formatNamesSlide s = foldr1 (\w rest -> w ++ " " ++ rest)
                  . map capitalize . filter (\w -> length w > 1) $ words s

sumPositiveSquares :: [Int] -> Int
sumPositiveSquares = sum . map (^2) . filter (>0)

sumStrict :: Num a => [a] -> a
sumStrict = foldl' (+) 0

checks :: [(String, Bool)]
checks =
  [ ("sumWith", sumWith (^2) [2,3 :: Integer] == 13)
  , ("mapOwn", mapOwn even [1,2,3 :: Int] == [False,True,False])
  , ("filterOwn", filterOwn even [1..6 :: Int] == [2,4,6])
  , ("foldr subtraction", foldrOwn (-) 0 [1,2,3 :: Int] == 2)
  , ("foldl subtraction", foldlOwn (-) 0 [1,2,3 :: Int] == -6)
  , ("foldr short circuit", foldrOwn (&&) True [False,undefined] == False)
  , ("zipWithOwn", zipWithOwn (+) [1,2,3 :: Int] [10,20] == [11,22])
  , ("unzipOwn", unzipOwn [(1,'a'),(2,'b')] == ([1,2 :: Int],"ab"))
  , ("concatOwn", concatOwn [[1,2],[],[3 :: Int]] == [1,2,3])
  , ("capitalize empty", capitalize "" == "")
  , ("capitalize", capitalize "aNNA" == "Anna")
  , ("format names", formatNames "tomasz t bogdan anna Jerzy j maria" == "Tomasz Bogdan Anna Jerzy Maria")
  , ("format empty", formatNames "" == "")
  , ("format removed", formatNames "a b c" == "")
  , ("format whitespace", formatNames "  aNNA   bOGDAN " == "Anna Bogdan")
  , ("pipeline", sumPositiveSquares [-2,0,3,4] == 25)
  , ("sumStrict", sumStrict [1..100 :: Integer] == 5050)
  , ("derivative approximate", absErr (\x -> 2*x) (df (\x -> x*x) 1e-5) 3 < 1e-7)
  ]

main :: IO ()
main = do
  mapM_ (\(name,ok) -> putStrLn ((if ok then "OK: " else "BLAD: ") ++ name)) checks
  if all snd checks
    then putStrLn "Wszystkie 18 przykladow poprawne."
    else error "Co najmniej jeden przyklad wymaga poprawki."
