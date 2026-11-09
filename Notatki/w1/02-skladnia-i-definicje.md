# 2. Składnia i definicje

## Definicja i wywołanie funkcji

```haskell
square :: Int -> Int
square x = x * x

add :: Int -> Int -> Int
add x y = x + y
```

`::` czytamy „ma typ”. Linia z `=` podaje definicję. Małe litery rozpoczynają nazwy funkcji i wartości; wielkie litery rozpoczynają m.in. nazwy typów i konstruktorów, takich jak `Int` i `True`.

```haskell
square 3         -- 9
add 2 3          -- 5
square (add 2 3) -- 25
```

Argumenty rozdziela się spacjami. `add (2,3)` przekazuje jedną krotkę i nie pasuje do powyższej definicji. Funkcja przyjmująca krotkę wygląda tak:

```haskell
addPair :: (Int, Int) -> Int
addPair (x, y) = x + y
```

## Kolejność wiązania

Wywołanie funkcji wiąże mocniej niż operatory i łączy się w lewo:

```haskell
square 2 + 3    -- (square 2) + 3 = 7
square (2 + 3)  -- 25
add 2 3        -- (add 2) 3
```

Iloczyn zapisuj jawnie: `f x * g y`. Spacja oznacza aplikację funkcji, nie mnożenie. Ujemny argument najczytelniej przekazać w nawiasie: `square (-3)`.

## Operatory

| Zapis | Znaczenie |
|---|---|
| `+`, `-`, `*` | dodawanie, odejmowanie, mnożenie |
| `/` | dzielenie w typach obsługujących ułamki |
| `div`, `mod` | dzielenie całkowite i reszta |
| `^` | potęga o nieujemnym całkowitym wykładniku |
| `**` | potęgowanie dla typów zmiennoprzecinkowych |
| `==`, `/=` | równość i nierówność |
| `<`, `>`, `<=`, `>=` | porównania |
| `&&`, `\|\|`, `not` | logiczne „i”, „lub”, negacja |

```haskell
7 `div` 2       -- 3
7 `mod` 2       -- 1
7 / 2           -- 3.5
(+) 2 3         -- 5
not (True && False) -- True
```

Zwykłą funkcję można zapisać między argumentami w odwrotnych apostrofach: ``7 `mod` 2``. Operator w nawiasach staje się funkcją: `(+) 2 3`.

## Warunki: if oraz guards

```haskell
absolute :: Int -> Int
absolute n = if n >= 0 then n else -n
```

Przy kilku warunkach czytelne są **strażniki (guards)**:

```haskell
sign :: Int -> Int
sign n
  | n < 0     = -1
  | n == 0    = 0
  | otherwise = 1
```

Warunki sprawdzane są od góry. `otherwise` jest nazwą wartości `True`. Przy pominięciu pasującej gałęzi funkcja może zakończyć się błędem podczas obliczania wyniku.

## Dopasowanie wzorców

```haskell
myNot :: Bool -> Bool
myNot True  = False
myNot False = True

isAla :: String -> Bool
isAla "Ala" = True
isAla _     = False
```

Wzorce rozpoznają postać danych. `_` pasuje do dowolnej wartości, ale nie nadaje jej nazwy. Pierwszy pasujący wzorzec wygrywa, więc ogólne przypadki umieszczaj na końcu.

`_` jest wzorcem, a `otherwise` wartością logiczną używaną w warunku — pełnią podobną rolę końcowego przypadku, ale mają inną składnię i znaczenie.

To samo rozgałęzienie można zapisać jako wyrażenie `case`:

```haskell
myNot b = case b of
  True  -> False
  False -> True
```

W `case` używa się `->`, a w równaniach funkcji `=`. Wzorzec `n > 0` nie jest poprawny; do sprawdzenia nierówności służy guard lub `if`.

## Definicje lokalne: where i let

```haskell
circleArea :: Double -> Double
circleArea r = pi * radiusSquared
  where
    radiusSquared = r * r
```

`where` dołącza lokalne definicje do równania funkcji. Mogą one korzystać z jego argumentów.

```haskell
circleArea r =
  let radiusSquared = r * r
  in pi * radiusSquared
```

`let ... in ...` jest wyrażeniem, którego wartością jest wynik części po `in`. Można go użyć wewnątrz większego wyrażenia. Lokalna nazwa może przesłonić zewnętrzną:

```haskell
factor = 10
scaled x = x * factor
  where
    factor = 2
-- scaled 3 = 6; zewnętrzne factor nadal wynosi 10
```

## Wcięcia i komentarze

Definicje najwyższego poziomu zaczynaj w tej samej kolumnie. Definicje w jednym bloku `where` lub `let` wyrównuj do siebie; podobnie alternatywy po `of`. Używaj spacji zamiast tabulatorów.

```haskell
volume :: Double -> Double
volume r = coefficient * pi * r ^ 3
  where
    coefficient = 4 / 3

-- Komentarz do końca linii
{- Komentarz blokowy.
   {- Może zawierać zagnieżdżony komentarz. -}
-}
```

Wcięcia są częścią składni. Możliwe są też jawne bloki, np. `let { x = 2; y = 3 } in x + y`, ale na początku lepiej stosować zwykłe wcięcia.
