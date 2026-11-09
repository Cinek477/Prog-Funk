# 4. Rekurencja

## Schemat przetwarzania listy

Lista jest pusta albo ma głowę i ogon. Naturalna definicja obsługuje oba przypadki:

```haskell
sumList :: Num a => [a] -> a
sumList [] = 0
sumList (x:xs) = x + sumList xs
```

`sumList [1,2,3] = 1 + (2 + (3 + 0))`. Przypadek bazowy kończy obliczenie; krok rekurencyjny przechodzi do ogona listy. Dla nieskończonej listy sumowanie nie dochodzi do końca.

Wzorzec musi być w nawiasach: `sumList (x:xs)`, a nie `sumList x:xs`.

## Trzy podstawowe schematy

Jedna wartość z całej listy — później uogólniana przez funkcje `fold`:

```haskell
productList :: Num a => [a] -> a
productList [] = 1
productList (x:xs) = x * productList xs
```

Przekształcenie każdego elementu — schemat `map`:

```haskell
doubleAll :: Num a => [a] -> [a]
doubleAll [] = []
doubleAll (x:xs) = (2*x) : doubleAll xs
```

Wybór elementów — schemat `filter`:

```haskell
selectEven :: Integral a => [a] -> [a]
selectEven [] = []
selectEven (x:xs)
  | even x    = x : selectEven xs
  | otherwise = selectEven xs
```

## Wzorce i guards razem

```haskell
firstTwoEqual :: Eq a => [a] -> Bool
firstTwoEqual (x:y:_)
  | x == y = True
firstTwoEqual _ = False
```

Wzorzec pasuje do listy o co najmniej dwóch elementach. Jeśli guard jest fałszywy, sprawdzane jest następne równanie. Wyniki: `[3,3,1]` → `True`, `[3,4]` → `False`, `[3]` → `False`, `[]` → `False`.

## Akumulator i rekurencja ogonowa

```haskell
sumAcc :: Num a => [a] -> a
sumAcc xs = loop 0 xs
  where
    loop acc [] = acc
    loop acc (y:ys) = loop (acc + y) ys
```

Akumulator `acc` przenosi dotychczasowy wynik. Wywołanie rekurencyjne jest ostatnią operacją — to **rekurencja ogonowa**, na slajdach nazywana też końcową. Nie zmieniamy jednej zmiennej: każde wywołanie otrzymuje nowe argumenty.

Można napisać `sumAcc = loop 0` z tą samą sygnaturą i blokiem `where`.

## Dlaczego akumulator może nadal zajmować pamięć?

Bez wymuszania możliwy przebieg wygląda tak:

```text
loop 0 [1,2,3]
loop (0+1) [2,3]
loop ((0+1)+2) [3]
loop (((0+1)+2)+3) []
```

Wywołania są ogonowe, ale rośnie łańcuch odłożonych dodawań. Nie należy utożsamiać rekurencji ogonowej z gwarancją stałej pamięci w leniwym języku.

Wersja wymuszająca akumulator:

```haskell
{-# LANGUAGE BangPatterns #-}

sumStrict :: Num a => [a] -> a
sumStrict = loop 0
  where
    loop !acc [] = acc
    loop !acc (y:ys) = loop (acc + y) ys
```

`!acc` to **bang pattern**: wymusza argument do WHNF. Dla zwykłych liczb zapobiega opisanemu łańcuchowi nieobliczonych dodawań. Przy akumulatorze złożonym z wielu pól samo WHNF nie musi wymusić pól.

Alternatywa biblioteczna:

```haskell
import Data.List (foldl')

sumStrict :: Num a => [a] -> a
sumStrict = foldl' (+) 0
```

To alternatywna definicja, nie druga definicja do tego samego pliku. `foldl'` wymusza kolejne akumulatory do WHNF. Optymalizator może sam wykryć część ścisłości, ale nie traktuj tego jako ogólnej gwarancji dla każdej funkcji. Rozmiar liczb `Integer` także może rosnąć — ścisłość nie usuwa kosztu przechowywania wyniku.

## Rekurencja drzewiasta: Fibonacci

```haskell
fib :: Int -> Integer
fib n
  | n < 0 = error "Argument musi byc nieujemny"
  | n < 2 = fromIntegral n
  | otherwise = fib (n-2) + fib (n-1)
```

Dwa wywołania wielokrotnie powtarzają te same podproblemy. Liczba wywołań rośnie wykładniczo. Leniwość sama nie zapamiętuje automatycznie wyników wszystkich `fib k`.

Wersja z dwoma akumulatorami:

```haskell
fibLinear :: Int -> Integer
fibLinear n
  | n < 0 = error "Argument musi byc nieujemny"
  | otherwise = go n 0 1
  where
    go 0 a _ = a
    go k a b = go (k-1) b (a+b)
```

`fibLinear 4`: `go 4 0 1 → go 3 1 1 → go 2 1 2 → go 1 2 3 → go 0 3 5 → 3`. To liniowa liczba kroków; koszt operacji na rosnących `Integer` nie jest stały. Jak wcześniej, leniwe akumulatory mogą wymagać wymuszania, gdy zależy nam na pamięci.

## Sortowanie przez podział

```haskell
qSort :: Ord a => [a] -> [a]
qSort [] = []
qSort (x:xs) = qSort smaller ++ [x] ++ qSort larger
  where
    smaller = [y | y <- xs, y <= x]
    larger  = [y | y <- xs, y > x]
```

Punkt podziału to pierwszy element. Sortujemy osobno mniejsze lub równe i większe, następnie sklejamy. Powtórzenia nie znikają. To sortowanie tworzące listy, bez przestawiania tablicy w miejscu. Przy niekorzystnych podziałach ma koszt O(n²), np. dla uporządkowanych danych lub listy jednakowych elementów; przy zrównoważonych podziałach O(n log n).

## Odwracanie listy: pułapka ++

```haskell
reverseSlow [] = []
reverseSlow (x:xs) = reverseSlow xs ++ [x]
```

Kolejne doklejanie na końcu przechodzi coraz dłuższe lewe listy: łączny koszt O(n²).

```haskell
reverseFast :: [a] -> [a]
reverseFast = go []
  where
    go acc [] = acc
    go acc (x:xs) = go (x:acc) xs
```

Dodawanie na początek przez `(:)` jest stałokosztowe, więc ta wersja ma koszt O(n).

## Nazwy rodzajów rekurencji

| Rodzaj | Znaczenie | Przykład |
|---|---|---|
| liniowa | najwyżej jedno wywołanie rekurencyjne w kroku | `sumList` |
| ogonowa / końcowa | po wywołaniu nie pozostaje dalsza operacja | `sumAcc` |
| drzewiasta | kilka wywołań w kroku | naiwne `fib` |
| wzajemna | funkcje wywołują się nawzajem | własne `isEven` i `isOdd` |
| zagnieżdżona | wynik wywołania rekurencyjnego jest argumentem kolejnego | funkcja Ackermanna |
| korekursja | generowanie kolejnych fragmentów struktury | lista `fibs` z rozdziału o leniwości |

Kategorie nie są rozłączne: rekurencja ogonowa może być zarazem liniowa. Zakończenie, zużycie stosu i pamięci zależą od algorytmu, zapotrzebowania na wynik oraz sposobu wykonania.
