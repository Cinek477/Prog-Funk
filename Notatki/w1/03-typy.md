# 3. Typy

## Podstawowe typy

| Typ | Przykład | Co opisuje |
|---|---|---|
| `Int` | `42 :: Int` | liczby całkowite o ograniczonym zakresie |
| `Integer` | `42 :: Integer` | liczby całkowite dowolnej precyzji, ograniczone dostępną pamięcią |
| `Float` | `1.5 :: Float` | przybliżone liczby zmiennoprzecinkowe pojedynczej precyzji |
| `Double` | `1.5 :: Double` | przybliżone liczby zmiennoprzecinkowe podwójnej precyzji |
| `Bool` | `True`, `False` | wartości logiczne |
| `Char` | `'a'` | pojedynczy znak |
| `String` | `"Ala"` | lista znaków, czyli `[Char]` |
| `[Int]` | `[1,2,3]` | lista elementów jednego typu |
| `(Int, Char)` | `(1,'a')` | krotka o ustalonej liczbie i typach pól |
| `()` | `()` | typ jednostkowy z jedną zwykłą wartością |

`'a'` to znak, a `"a"` to jednoelementowa lista znaków. `[1, True]` jest niepoprawne, ale `(1, True)` jest poprawną krotką. Lista może mieć różną długość; typ krotki określa liczbę jej pól.

## Czytanie sygnatur

```haskell
not :: Bool -> Bool
add :: Int -> Int -> Int
swap :: (a, b) -> (b, a)
```

`->` opisuje funkcję: po lewej jest typ argumentu, po prawej typ wyniku. Strzałki grupują się w prawo:

```haskell
Int -> Int -> Int
-- znaczy Int -> (Int -> Int)
```

`add` przyjmuje liczbę i zwraca funkcję przyjmującą kolejną liczbę. W codziennym użyciu mówimy, że przyjmuje dwa argumenty. To **currying**. Dzięki niemu można podać tylko część argumentów:

```haskell
add x y = x + y
addFive = add 5
-- addFive 3 daje 8
```

Nie myl `a -> b -> c` z `(a, b) -> c`: pierwsza funkcja otrzymuje argumenty kolejno, druga jedną parę.

## Polimorfizm parametryczny

Mała litera w typie, np. `a`, jest zmienną typu.

```haskell
identity :: a -> a
identity x = x

swap :: (a, b) -> (b, a)
swap (x, y) = (y, x)
```

`identity` działa dla różnych typów. W jednym użyciu wszystkie wystąpienia `a` oznaczają ten sam typ. W `swap` typy `a` i `b` mogą być różne, ale mogą też być takie same.

## Klasy typów i ograniczenia

```haskell
(==) :: Eq a => a -> a -> Bool
(+)  :: Num a => a -> a -> a
```

`=>` oddziela wymagania od właściwego typu funkcji. `Eq a` oznacza, że dla typu `a` dostępne jest porównanie równości. Klasa typów opisuje zestaw operacji; nie jest klasą obiektów w znaczeniu programowania obiektowego.

| Ograniczenie | Co pozwala robić |
|---|---|
| `Eq a` | porównywać przez `==`, `/=` |
| `Ord a` | porządkować przez `<`, `>`, `<=`, `>=` itd.; wymaga też `Eq` |
| `Num a` | używać m.in. `+`, `-`, `*`, literałów całkowitych |
| `Integral a` | używać m.in. `div`, `mod`, np. dla `Int` i `Integer` |
| `Fractional a` | używać `/`, np. dla `Double` |
| `Floating a` | używać m.in. `sqrt`, `sin`, `pi`, `**` |
| `Show a` | zamieniać wartość na tekst przez `show` |

```haskell
same :: Eq a => a -> a -> Bool
same x y = x == y

largerDouble :: (Num a, Ord a) => a -> a
largerDouble x = if x > 3 then 2 * x else 42
```

`Num` nie wystarcza do `/` ani do porównania `>`. `a -> a` bez ograniczeń nie pozwala zakładać, że argument jest liczbą.

## Inferencja typów

Kompilator potrafi wywnioskować typ z użytych operacji:

```haskell
square x = x * x
-- square :: Num a => a -> a

swap (x, y) = (y, x)
-- swap :: (a, b) -> (b, a)

choose x = if x > 3 then 2 * x else x / 42
-- choose :: (Fractional a, Ord a) => a -> a
```

Dla `choose`: `>` wymaga `Ord`, a `/` wymaga `Fractional`. Wymaganie `Num` jest już zawarte w `Fractional`.

```haskell
-- BŁĄD:
wrong x = if x > 3 then 2 * x else False
```

Gałąź liczbowa i gałąź logiczna nie mają zgodnego typu. Kompilator odrzuca definicję zamiast wybrać typ zależny od wartości argumentu.

Warto pisać sygnatury nawet tam, gdzie nie są konieczne: dokumentują zamiar i pomagają znaleźć błędy. Konkretna sygnatura, np. `Int -> Int`, celowo zawęża ogólniejszą funkcję.

## Literały i konwersje

Literał `3` może być użyty w różnych typach liczbowych. Nie oznacza to automatycznej konwersji już istniejących wartości:

```haskell
n :: Int
n = 3

x :: Double
x = 2.5

result :: Double
result = fromIntegral n + x  -- 5.5
```

`fromIntegral` przekształca wartość całkowitą do odpowiedniego typu liczbowego. `n + x` bez konwersji byłoby błędem. Typ literału lub wyrażenia można doprecyzować przez `::`, np. `(7 :: Double) / 2`.
