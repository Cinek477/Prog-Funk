# 4. Foldy — foldr, foldl, foldl' i wersje bez wartości początkowej

[Spis wykładu 3](README.md) · Slajdy 12–13

## Co to znaczy „złożyć listę”?

Fold zastępuje wspólny schemat rekurencji. Określasz operację łączenia i wynik przypadku pustego. „Redukcja” nie oznacza, że wynik musi być pojedynczą liczbą — może być też listą, parą lub funkcją.

## foldr — nawiasy od prawej

Wersja dla list:

```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr f z [] = z
foldr f z (x:xs) = f x (foldr f z xs)
```

- `a`: typ elementu listy.
- `b`: typ wyniku składania.
- `f`: dostaje bieżący element i wynik przetworzenia ogona.
- `z`: wynik pustej listy.

```text
foldr f z [x1,x2,x3]
= f x1 (f x2 (f x3 z))
```

Możesz myśleć o zastępowaniu `(:)` przez `f`, a końcowego `[]` przez `z`.

```haskell
foldr (+) 0 [1,2,3] -- 1+(2+(3+0)) = 6
foldr (*) 1 [2,3,4] -- 2*(3*(4*1)) = 24
foldr (:) [] [1,2,3] -- [1,2,3]
foldr (\_ n -> 1+n) 0 [7,8,9] -- 3
```

Dlaczego `0` dla sumy i `1` dla iloczynu? To elementy neutralne tych operacji. Inne wartości początkowe też są możliwe, ale zmienią wynik.

## foldl — akumulator po lewej

```haskell
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl f z [] = z
foldl f z (x:xs) = foldl f (f z x) xs
```

Tutaj `f` otrzymuje najpierw akumulator, potem element.

```text
foldl f z [x1,x2,x3]
= f (f (f z x1) x2) x3
```

Typowy błąd to przestawienie tych argumentów. Na slajdzie z pomocniczym schematem rekurencji kolejność działania jest zapisana inaczej niż w właściwej definicji `foldl`. Ucz się definicji `foldl f (f z x) xs` i sprawdzaj kolejność na odejmowaniu.

## Porównanie: operacja niełączna ujawnia różnicę

```haskell
foldr (-) 0 [1,2,3] -- 1-(2-(3-0)) = 2
foldl (-) 0 [1,2,3] -- ((0-1)-2)-3 = -6
```

Nie wybieraj kierunku na podstawie przykładu z dodawaniem. Dla zwykłych małych liczb oba sumowania wyglądają tak samo, ale operacje niełączne dają inne wyniki. Dla liczb zmiennoprzecinkowych także samo grupowanie sumy może wpływać na zaokrąglenia.

| Cecha | foldr | foldl |
|---|---|---|
| Funkcja kroku | element → wynik ogona → wynik | akumulator → element → akumulator |
| Typ kroku | `a -> b -> b` | `b -> a -> b` |
| Układ nawiasów | `f x1 (f x2 z)` | `f (f z x1) x2` |
| Pusta lista | `z` | `z` |
| Nieskończone wejście | czasem produktywne / krótkie spięcie | nie zwraca końcowego wyniku |

Układ nawiasów opisuje zależności, nie bezwarunkową kolejność obliczania wszystkich argumentów. Haskell pozostaje leniwy.

## Fold może budować listę

```haskell
mapOwn f = foldr (\x acc -> f x : acc) []
filterOwn p = foldr (\x acc -> if p x then x:acc else acc) []

reverseSlow = foldr (\x acc -> acc ++ [x]) []
reverseFast = foldl (\acc x -> x:acc) []
```

Pierwsze dwa przykłady odtwarzają `map` i `filter`. Odwracanie z `++ [x]` ma koszt kwadratowy, bo wielokrotnie przechodzi lewą listę. Wersja odkładająca na początek ma liniową liczbę kroków listowych. Sam wybór folda nie gwarantuje wydajności: znaczenie ma też funkcja kroku.

## Leniwość i krótkie spięcie w foldr

```haskell
foldr (||) False [False,True,undefined] -- True
foldr (&&) True [False,undefined] -- False
foldr (\x _ -> x) 0 [1..] -- 1
```

Funkcja kroku może nie potrzebować wyniku ogona. `foldr` może wtedy zakończyć się bez przejścia całego wejścia.

```haskell
foldr (+) 0 [1..] -- nie zwraca skończonego wyniku
```

**Nieprawda:** „foldr zawsze obsługuje listy nieskończone”. Działa tylko wtedy, gdy konkretna funkcja kroku i sposób użycia wyniku pozwalają uniknąć niekończącej się pracy.

## foldl' — ścisły akumulator

Zwykłe `foldl (+) 0 xs` może gromadzić odłożone dodawania. Ścisła wersja ogranicza ten problem:

```haskell
import Data.List (foldl')

sumStrict :: Num a => [a] -> a
sumStrict = foldl' (+) 0
```

`foldl'` wymusza kolejne akumulatory do WHNF. To nie oznacza głębokiego obliczenia wszystkich pól złożonego akumulatora. Nie daje też końcowego wyniku dla nieskończonej listy.

Praktycznie: do pełnego sumowania skończonej listy liczb często wybiera się `foldl'`; do budowania list i krótkiego spięcia naturalne jest `foldr`.

## foldl1 i foldr1

Nie podajemy `z`. Dla niepustej listy wartość bazowa pochodzi z listy.

```haskell
foldl1 (-) [1,2,3] -- (1-2)-3 = -4
foldr1 (-) [1,2,3] -- 1-(2-3) = 2
foldl1 (+) [7] -- 7
foldr1 (+) [7] -- 7
```

Dla `[]` obie funkcje zgłaszają błąd. Typ dla list to `(a -> a -> a) -> [a] -> a`; w GHCi może pojawić się ogólniejsze ograniczenie `Foldable t`.

## Jak rozwiązywać pytania o foldy?

1. Zapisz funkcję kroku i `z`.
2. Rozwiń wszystkie nawiasy według kierunku.
3. Podstaw definicję kroku, pilnując kolejności argumentów.
4. Dopiero wtedy policz.
5. Przy `undefined` sprawdź, czy krok rzeczywiście potrzebuje dalszego wyniku.
