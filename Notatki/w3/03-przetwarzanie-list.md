# 3. map, filter, zipWith, unzip i concat

[Spis wykładu 3](README.md) · Slajdy 10–11 i 14–15

## Dobierz właściwy schemat

| Potrzeba | Funkcja | Co się dzieje z elementami? |
|---|---|---|
| Zmień każdy element | `map` | każdy daje jeden nowy element |
| Wybierz niektóre elementy | `filter` | zachowane elementy nie zmieniają typu |
| Połącz odpowiadające elementy dwóch list | `zipWith` | po jednym elemencie z każdej listy |
| Połącz w pary | `zip` | wynik to lista par |
| Rozdziel pary na dwie listy | `unzip` | wynik to para list |
| Usuń jedną warstwę list | `concat` | listy wewnętrzne zostają sklejone |
| Zbierz listę w jeden wynik | fold | wynik może być liczbą, listą, Bool itd. |

## map — przekształcanie

```haskell
map :: (a -> b) -> [a] -> [b]
map _ [] = []
map f (x:xs) = f x : map f xs
```

Pierwszy argument to funkcja jednego elementu. Może zmienić jego typ.

```haskell
map (^2) [1..5]             -- [1,4,9,16,25]
map even [1,2,3]           -- [False,True,False]
map length ["a","kot",""] -- [1,3,0]
map (\s -> (s,length s)) ["My","name","is"]
-- [("My",2),("name",4),("is",2)]
```

Dla skończonej listy pełnych wartości długość wyniku jest taka sama jak wejścia. Typy `a` i `b` mogą być różne, ale mogą też być takie same.

Odpowiednik comprehension:

```haskell
map f xs = [f x | x <- xs]
```

## filter — wybór

```haskell
filter :: (a -> Bool) -> [a] -> [a]
filter _ [] = []
filter p (x:xs)
  | p x = x : filter p xs
  | otherwise = filter p xs
```

`p` jest predykatem: zwraca Bool dla pojedynczego elementu.

```haskell
filter even [1..6]                    -- [2,4,6]
filter (\x -> x > 1 && x < 5) [1..10] -- [2,3,4]
filter (\s -> length s == 2) ["a","aa","bbb","bb"]
-- ["aa","bb"]
filter (\(x,y) -> x > y) [(1,2),(2,2),(3,2)]
-- [(3,2)]
```

`filter even` nie zwraca listy Bool. Listę wyników predykatu daje `map even`.

```haskell
filter p xs = [x | x <- xs, p x]
```

Kolejność nie zmienia się. Filtr nie sortuje i nie usuwa automatycznie powtórzeń.

## Kolejność map i filter ma znaczenie

```haskell
map (*2) (filter (>2) [1..4]) -- [6,8]
filter (>2) (map (*2) [1..4]) -- [4,6,8]
```

W pierwszym przypadku warunek sprawdza oryginalne wartości, w drugim już podwojone. Nie wolno przestawiać etapów bez sprawdzenia znaczenia.

## zipWith — dwie listy i funkcja

```haskell
zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
zipWith _ [] _ = []
zipWith _ _ [] = []
zipWith f (x:xs) (y:ys) = f x y : zipWith f xs ys
```

```haskell
zipWith (+) [1..5] [5,4..1] -- [6,6,6,6,6]
zipWith (*) [1,2,3] [10,20] -- [10,40]
zipWith (++) ["A","B"] ["la","ar"] -- ["Ala","Bar"]
```

Funkcja `f` przyjmuje dwa argumenty kolejno. `zipWith` kończy na krótszej liście. Nie tworzy wszystkich kombinacji par; to zadanie dla dwóch generatorów comprehension.

## zip i unzip

```haskell
zip :: [a] -> [b] -> [(a,b)]
unzip :: [(a,b)] -> ([a],[b])
```

```haskell
zip [1,2,3] "ab" -- [(1,'a'),(2,'b')]
unzip [(1,'a'),(2,'b')] -- ([1,2],"ab")
```

**Pułapka:** `unzip (zip xs ys)` nie zawsze odtwarza całe wejście. Jeżeli listy miały różne długości, nadmiar końcowych elementów został utracony.

W drugą stronę, dla skończonej listy zwykłych par, `uncurry zip (unzip pairs)` odtwarza `pairs`.

## concat — spłaszczenie o jedną warstwę

```haskell
concat :: [[a]] -> [a]
concat = foldr (++) []

concat [[1,2],[],[3,4]] -- [1,2,3,4]
concat ["ab","cd"] -- "abcd"
concat [[[1],[2]],[[3]]] -- [[1],[2],[3]]
(concat . concat) [[[1],[2]],[[3]]] -- [1,2,3]
```

Każde użycie usuwa dokładnie jedną warstwę list. Nie spłaszcza dowolnie głębokiej struktury.

## Leniwość w tych operacjach

```haskell
take 3 (map (^2) [1..]) -- [1,4,9]
take 3 (filter even [1..]) -- [2,4,6]
```

Można pracować na nieskończonych listach, jeśli potrzebny wynik powstaje po skończonej pracy. `head (filter (<0) [1..])` nie znajduje wyniku. `concat (repeat [])` również nie wytworzy pierwszego elementu.
