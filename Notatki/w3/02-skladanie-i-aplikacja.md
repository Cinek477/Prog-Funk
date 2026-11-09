# 2. Składanie funkcji oraz operatory . i $

[Spis wykładu 3](README.md) · Slajd 8

## Złożenie: wynik jednej funkcji trafia do drugiej

```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
(f . g) x = f (g x)
```

Najpierw działa funkcja po prawej. Typ wyniku `g` musi pasować do typu argumentu `f`.

```haskell
double x = 2*x
square x = x*x

(double . square) 3 -- double (square 3) = 18
(square . double) 3 -- square (double 3) = 36
```

Złożenie zwykle nie jest przemienne. `f . g . h` opisuje proces od prawej do lewej: h, potem g, potem f.

## Kropka tworzy funkcję, dolar ją stosuje

```haskell
($) :: (a -> b) -> a -> b
f $ x = f x
```

`$` ma priorytet 0 i wiąże w prawo. Pozwala objąć argumentem całe wyrażenie po prawej:

```haskell
sum $ map (^2) [1,2,3]
-- sum (map (^2) [1,2,3]) = 14
```

Porównaj:

```haskell
sum . map (^2)   -- funkcja oczekująca na listę
sum $ map (^2) [1,2,3] -- liczba 14
```

Nie zamieniaj automatycznie `.` na `$`. `f . g` przekazuje do f przyszły wynik g, a `f $ x` przekazuje do f obecny argument x.

## Priorytety na przykładzie z wykładu

```haskell
f x y = x^2+y^2

f 1 2 + 3   -- (f 1 2)+3 = 8
f 1 $ 2 + 3 -- f 1 (2+3) = 26
```

Aplikacja przez spacje wiąże najmocniej. Kropka ma priorytet 9, a `$` 0. Oba operatory są prawostronnie łączne.

```haskell
sum . map (^2) . filter even $ [1..5]
-- sum (map (^2) (filter even [1..5])) = 20
```

Przy czytaniu dopisz najpierw nawiasy, a dopiero potem licz wynik.

## Styl bez jawnego argumentu: point-free

```haskell
sumEvenSquares xs = sum (map (^2) (filter even xs))
-- alternatywa:
sumEvenSquares = sum . map (^2) . filter even
```

Oba zapisy są równoważne. Nie usuwaj nazw argumentów kosztem czytelności. Na początku bezpiecznie jest zapisać pełną wersję i dopiero przekształcić ją w złożenie.

## Sekcja ($ 2)

```haskell
($ 2) f = f 2
map ($ 2) [(^2),(^3),(^4),(^5)] -- [4,8,16,32]
```

Tutaj lista przechowuje funkcje, a `map` stosuje każdą z nich do tej samej wartości `2`. `($ 2)` ma typ `(a -> b) -> b`, przy odpowiednio ustalonym typie dwójki. To nie jest funkcja dodająca 2.

## Ścisła aplikacja: $!

`f $! x` wymusza argument `x` do WHNF przed zastosowaniem `f`. WHNF oznacza zewnętrzną postać wartości, nie pełne obliczenie wszystkich pól i elementów.

```haskell
const 7 $ undefined  -- 7
const 7 $! undefined -- błąd
const 7 $! [undefined] -- 7: konstruktor niepustej listy jest znany
```

Ścisłość zmienia zapotrzebowanie na obliczenia. Nie traktuj `$!` jako automatycznej optymalizacji każdego wywołania.
