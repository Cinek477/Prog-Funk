# 1. Funkcje wyższego rzędu, lambdy i domknięcia

[Spis wykładu 3](README.md) · Slajdy 4–7

## Problem: podobne funkcje i reguła DRY

Funkcje sumujące elementy, ich kwadraty, sześciany lub wartości bezwzględne różnią się tylko tym, co robimy z pojedynczym elementem. Kopiowanie całego schematu rekurencji utrudnia poprawki.

**DRY — Don't Repeat Yourself:** wydziel wspólny schemat, a różnice przekaż jako parametr.

```haskell
sumWith :: Num a => (a -> a) -> [a] -> a
sumWith _ [] = 0
sumWith f (x:xs) = f x + sumWith f xs
```

Jak czytać typ:

1. `(a -> a)` — pierwszy argument jest funkcją przekształcającą jeden element.
2. `[a]` — drugi argument jest listą.
3. `a` — wynikiem jest liczba.
4. `Num a` — potrzebujemy dodawania i zera.

Nawiasy wokół `(a -> a)` są kluczowe. Bez nich `a -> a -> [a] -> a` opisywałoby inne argumenty.

```haskell
sumWith id [1,2,3]    -- 6
sumWith (^2) [1,2,3]  -- 14
sumWith (^3) [1,2,3]  -- 36
sumWith abs [-2,3,-4] -- 9
```

`id x = x`. Operator `(^2)` jest sekcją, która podnosi argument do kwadratu.

Rozwinięcie:

```text
sumWith (^2) [2,3]
= 2^2 + sumWith (^2) [3]
= 4 + (3^2 + sumWith (^2) [])
= 4 + (9 + 0)
= 13
```

**Funkcja wyższego rzędu** przyjmuje funkcję jako argument lub zwraca funkcję. `sumWith`, `map` i `filter` to przykłady. Funkcje mogą być wartościami: przekazujemy `abs`, a nie koniecznie wynik `abs x`.

## Funkcje anonimowe, czyli lambdy

```haskell
\x -> x*x
\x y -> x+y
\(x,y) -> x+y
```

Backslash `\` rozpoczyna funkcję, a `->` oddziela argumenty od ciała. Druga lambda przyjmuje argumenty kolejno; trzecia jedną parę.

```haskell
(\x y -> x+y) 1 2 -- 3
(\(x,y) -> x+y) (1,2) -- 3
```

Równoważne sposoby zapisania tej samej transformacji:

```haskell
square x = x^2
-- funkcja anonimowa: \x -> x^2
-- sekcja: (^2)
```

Użyj nazwy, gdy funkcja jest dłuższa lub wielokrotnie używana. Krótka lambda jest wygodna przy pojedynczym użyciu. Nie każdą funkcję można sensownie zastąpić sekcją.

## Funkcja jako wynik: przybliżona pochodna

```haskell
df :: (Double -> Double) -> Double -> (Double -> Double)
df f h = \x -> (f (x+h) - f (x-h)) / (2*h)
```

`df` przyjmuje funkcję `f`, krok `h` i zwraca funkcję zmiennej `x`. To centralny iloraz różnicowy, czyli przybliżenie pochodnej.

```haskell
dSquare :: Double -> Double
dSquare = df (\x -> x*x) 1e-5
-- dSquare 3 jest bliskie 6, niekoniecznie dokładnie 6
```

Wymagamy `h /= 0`. Zbyt mały krok nie musi poprawić wyniku: odejmowanie bliskich liczb zmiennoprzecinkowych może zwiększyć błąd. `Double` jest reprezentacją przybliżoną.

**Domknięcie = funkcja wraz ze środowiskiem**, z którego korzysta. Zwrócona lambda pamięta dostęp do `f` i `h`, choć po lewej stronie jej definicji widzimy tylko `x`.

Prostszy przykład:

```haskell
makeAdder :: Int -> (Int -> Int)
makeAdder n = \x -> n+x
-- makeAdder 5 zwraca funkcję dodającą 5
```

## Ile argumentów już podano?

```haskell
absErr :: Num a => (t -> a) -> (t -> a) -> t -> a
absErr exact approximate x = abs (exact x - approximate x)
```

To błąd bezwzględny dwóch wyników obliczonych dla tego samego `x`.

```haskell
absErr (\x -> 2*x) (df (\x -> x*x) 1e-5)
-- :: Double -> Double
```

Podano dwie funkcje. Brakuje punktu `x`, więc wynikiem jest funkcja. Użycie jej w `map` dostarczy kolejne punkty:

```haskell
map (absErr (\x -> 2*x) dSquare) [0,0.5,1]
```

Częściowa aplikacja nie jest funkcją częściową: pierwsza oznacza niepodanie wszystkich argumentów, druga brak poprawnego wyniku dla niektórych wejść.
