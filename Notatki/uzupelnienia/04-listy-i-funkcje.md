# 4. Listy, rekurencja i funkcje wyższego rzędu

Ten rozdział uzupełnia pierwszy wykład o praktyczne podstawy przetwarzania danych.

## Budowanie list

```haskell
[]               -- pusta lista
[1,2,3]          -- lista trzech liczb
1 : [2,3]        -- [1,2,3]
[1,2] ++ [3,4]   -- [1,2,3,4]
[1..5]           -- [1,2,3,4,5]
[2,4..10]        -- [2,4,6,8,10]
```

`(:)` dodaje jeden element na początek listy. `(++)` skleja dwie listy. Dlatego `1 ++ [2,3]` jest błędem: lewa strona też musi być listą.

Lista `[1,2,3]` ma strukturę `1 : (2 : (3 : []))`. Wzorzec `x:xs` rozdziela niepustą listę na pierwszy element `x` i pozostałą listę `xs`. Nazwy są umowne.

## Rekurencja

Funkcja rekurencyjna korzysta z samej siebie dla mniejszego lub prostszego problemu.

```haskell
sumList :: Num a => [a] -> a
sumList []     = 0
sumList (x:xs) = x + sumList xs
```

Obliczenie:

```text
sumList [1,2,3]
= 1 + sumList [2,3]
= 1 + (2 + sumList [3])
= 1 + (2 + (3 + sumList []))
= 1 + (2 + (3 + 0))
= 6
```

Potrzebne są przypadek bazowy (`[]`) i krok przybliżający do niego (`xs`). Ten wzorzec kończy się dla skończonych list. Dla nieskończonej listy sumowanie nie dojdzie do końca.

```haskell
lengthList :: [a] -> Int
lengthList []     = 0
lengthList (_:xs) = 1 + lengthList xs
```

Nie odczytujemy wartości elementów, więc typ `a` nie potrzebuje ograniczeń.

## map, filter i foldr

```haskell
map :: (a -> b) -> [a] -> [b]
filter :: (a -> Bool) -> [a] -> [a]
foldr :: (a -> b -> b) -> b -> [a] -> b
```

To sygnatury istniejących funkcji z biblioteki standardowej — nie trzeba ich samodzielnie deklarować w pliku.

```haskell
map (*2) [1,2,3]         -- [2,4,6]
filter even [1..6]       -- [2,4,6]
foldr (+) 0 [1,2,3]      -- 6
foldr (*) 1 [2,3,4]      -- 24
```

- `map` przekształca każdy element; może zmienić typ elementów.
- `filter` zachowuje elementy spełniające warunek.
- `foldr` zastępuje konstruktory listy operacją i wartością początkową: `foldr f z [x,y] = f x (f y z)`.

`(*2)` to sekcja operatora, czyli funkcja mnożąca argument przez 2. Dla odejmowania uważaj: `(-2)` oznacza liczbę ujemną; funkcję odejmującą 2 zapisz jako `\x -> x - 2`.

## Lambdy i domknięcia

Lambda to funkcja bez nadawania jej osobnej nazwy:

```haskell
\x -> x * x
\x y -> x + y

map (\x -> x * x) [1,2,3]  -- [1,4,9]
```

Funkcja może korzystać z wartości otaczającego zakresu:

```haskell
makeAdder :: Int -> (Int -> Int)
makeAdder n = \x -> n + x

-- (makeAdder 5) 3 = 8
```

Zwrócona funkcja zachowuje dostęp do `n`. Taką funkcję wraz z jej środowiskiem nazywamy domknięciem. To samo można krócej zapisać `makeAdder n x = n + x`.

## Składanie funkcji i operator $

```haskell
(f . g) x = f (g x)
```

To równanie wyjaśnia działanie istniejącego operatora `(.)`. Najpierw działa `g`, potem `f`.

```haskell
sumEvenSquares :: [Int] -> Int
sumEvenSquares xs = sum (map (\x -> x * x) (filter even xs))

-- alternatywna definicja:
sumEvenSquares = sum . map (\x -> x * x) . filter even
-- sumEvenSquares [1,2,3,4] = 20
```

W ten sposób powstaje ciąg przekształceń kolekcji: wybierz parzyste, podnieś do kwadratu, zsumuj.

`$` oznacza aplikację funkcji o bardzo niskim priorytecie. Pomaga ograniczać nawiasy:

```haskell
sum $ map (*2) [1,2,3]
-- to samo co sum (map (*2) [1,2,3])
```

`.` tworzy złożoną funkcję, a `$` przekazuje argument do funkcji. Nie są zamienne.

## List comprehensions

```haskell
[x * x | x <- [1..5]]              -- [1,4,9,16,25]
[x * x | x <- [1..5], even x]      -- [4,16]
[(x,y) | x <- [1,2], y <- [3,4]]   -- [(1,3),(1,4),(2,3),(2,4)]
```

Po lewej stronie `|` opisujesz wynikowy element. Po prawej podajesz generatory (`x <- lista`) i warunki. W tym zapisie `<-` pobiera kolejne elementy listy.

## Przykład z wykładu: sortowanie

```haskell
qsort :: Ord a => [a] -> [a]
qsort [] = []
qsort (x:xs) = qsort smaller ++ [x] ++ qsort larger
  where
    smaller = filter (<= x) xs
    larger  = filter (> x) xs
```

Pierwszy element jest punktem podziału. Reszta trafia do dwóch list, które są sortowane rekurencyjnie. Powtórzenia pozostają w wyniku.

To dydaktyczne sortowanie list: tworzy nowe listy, nie przestawia elementów tablicy w miejscu. Wybór pierwszego elementu może dać czas kwadratowy, np. dla już uporządkowanych danych. Przykład pokazuje składnię i rekurencję, nie stanowi wzorca wydajnego sortowania.

## Unikaj niepełnych przypadków

`head []` i `tail []` powodują błąd. Można jawnie opisać brak wyniku:

```haskell
safeHead :: [a] -> Maybe a
safeHead []    = Nothing
safeHead (x:_) = Just x
```

`Maybe a` opisuje opcjonalną wartość: `Nothing` oznacza jej brak, `Just x` jej obecność. W ten sposób oba przypadki są częścią typu wyniku.
