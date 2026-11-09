# 6. Ćwiczenia — najpierw samodzielnie, potem sprawdź

[Spis wykładu 3](README.md)

## A. Przewidź wynik

1. `map (+1) (filter even [1..6])`
2. `filter even (map (+1) [1..6])`
3. `map ($ 3) [(+1),(*2),(^2)]`
4. `foldr (-) 0 [2,3,4]`
5. `foldl (-) 0 [2,3,4]`
6. `foldr (:) [9] [1,2]`
7. `foldl (\acc x -> x:acc) [] [1,2,3]`
8. `foldr (\x acc -> acc ++ [x]) [] [1,2,3]`
9. `zipWith (-) [8,7,6] [1,2]`
10. `unzip (zip [1,2,3] "ab")`
11. `concat [[[1],[2]],[[3]]]`
12. `sum . map (^2) . filter odd $ [1..5]`
13. `foldr (&&) True [False,undefined]`
14. `const 5 $! [undefined]`
15. Co stanie się dla `foldr1 (++) []`?

## B. Typy

Podaj typ dla list, jeśli wyrażenie dotyczy przetwarzania list. Pamiętaj, że GHCi może pokazać ogólniejszy typ z `Foldable`.

16. `map even`
17. `filter even`
18. `map length` dla wejściowej listy list
19. `sum . map (^2)` dla list
20. `zipWith (==)`
21. `foldr (:) []`
22. `foldl (\acc _ -> acc+1) (0 :: Int)` dla list
23. `df f h`, jeżeli `df :: (Double -> Double) -> Double -> Double -> Double`

## C. Uzupełnij kod

24. Suma wartości bezwzględnych:

```haskell
sumAbs = sumWith _____
```

25. Własne `map` przez `foldr`:

```haskell
mapOwn f = foldr (\x acc -> _____) _____
```

26. Iloczyn przez fold:

```haskell
productOwn = foldr _____ _____
```

27. Wybór par z większą pierwszą współrzędną:

```haskell
selectPairs = filter (\(x,y) -> _____)
```

28. Suma iloczynów odpowiadających elementów:

```haskell
dot xs ys = sum (zipWith _____ xs ys)
```

29. Normalizacja słów z tekstu:

```haskell
formatNames = _____ . map capitalize . filter (\w -> length w > 1) . _____
```

30. Dlaczego zastąpienie `unwords` przez `foldr1` może zmienić zachowanie dla pustego tekstu?

---

## Rozwiązania A

1. `[3,5,7]`: wybierz parzyste, potem zwiększ.
2. `[2,4,6]`: najpierw zwiększ, dopiero potem wybierz.
3. `[4,6,9]`: każda funkcja dostaje argument 3.
4. `2-(3-(4-0)) = 3`.
5. `((0-2)-3)-4 = -9`.
6. `[1,2,9]`: bazowa lista jest końcem wyniku.
7. `[3,2,1]`: kolejne elementy trafiają na początek akumulatora.
8. `[3,2,1]`: wynik ten sam, ale ta wersja przez `++` jest kwadratowa.
9. `[7,5]`: wynik kończy się z krótszą listą.
10. `([1,2],"ab")`: trzecia liczba została utracona przez `zip`.
11. `[[1],[2],[3]]`: usuwamy jedną warstwę.
12. `35`: 1²+3²+5².
13. `False`: nie trzeba obliczać ogona po pierwszym False.
14. `5`: lista jest już w WHNF, element nie jest wymuszany.
15. Błąd: `foldr1` nie obsługuje pustej listy.

## Rozwiązania B

16. `Integral a => [a] -> [Bool]`.
17. `Integral a => [a] -> [a]`.
18. `[[a]] -> [Int]`.
19. `Num a => [a] -> a`.
20. `Eq a => [a] -> [a] -> [Bool]`.
21. `[a] -> [a]`.
22. `[a] -> Int`: wartości elementów nie są używane.
23. `Double -> Double`: zostały podane f i h, brakuje x.

## Rozwiązania C

24. `abs` lub `\x -> abs x`.
25. `f x : acc` oraz `[]`.
26. `(*)` oraz `1`.
27. `x > y`.
28. `(*)`.
29. `unwords` oraz `words`.
30. `unwords []` daje pusty tekst, a `foldr1` zgłasza błąd. Pusta lista może powstać także dla niepustego wejścia, gdy filtr usunie wszystkie słowa.

## Zadanie przekrojowe

Napisz funkcję, która z tekstu wybiera słowa dłuższe niż 2 znaki i zwraca sumę ich długości. Zapisz wersję z argumentem i wersję przez złożenie.

```haskell
totalLongLength :: String -> Int
totalLongLength s = sum (map length (filter (\w -> length w > 2) (words s)))

-- alternatywnie:
totalLongLength = sum . map length . filter (\w -> length w > 2) . words
-- totalLongLength "a kot pies i dom" = 10
```
