# 1. Myślenie funkcyjne

## Program jako obliczanie wartości

W podejściu imperatywnym opisujesz kolejne zmiany stanu, np. zwiększanie licznika i aktualizowanie sumy. W podejściu funkcyjnym opisujesz wartości oraz funkcje, które przekształcają jedne wartości w inne.

```haskell
sum [1..10]  -- 55
```

`[1..10]` oznacza listę liczb od 1 do 10, a `sum` oblicza sumę jej elementów. Nie trzeba samodzielnie tworzyć zmiennej akumulatora i pętli.

## Czyste funkcje

Czysta funkcja wyznacza wynik na podstawie argumentów, bez obserwowalnych efektów ubocznych. Dla tych samych argumentów daje ten sam wynik, o ile obliczenie kończy się poprawnie.

```haskell
double :: Int -> Int
double x = 2 * x
```

`double 4` daje `8`. Obliczenie nie zmienia globalnej zmiennej ani nie wypisuje tekstu. Odczyt pliku, komunikacja z użytkownikiem i losowanie wymagają osobnego opisania efektów; w Haskellu służy do tego m.in. typ `IO`.

**Przezroczystość referencyjna:** wyrażenie można zastąpić jego wartością bez zmiany znaczenia programu. Zamiast `double 4 + 1` można rozważyć `8 + 1`.

## Niezmienność

```haskell
x = 5
y = x + 1
```

`x = 5` wiąże nazwę z wartością. Nie jest poleceniem zmiany zawartości komórki pamięci. Nie można potem przypisać tej samej nazwie w tym samym zakresie wartości `6`.

Dlatego zapis `x = x + 1` nie zwiększa licznika. Jest definicją rekurencyjną, która dla zwykłych liczb nie daje użytecznego wyniku. Kolejne etapy obliczeń opisuje się nowymi wartościami, wywołaniami funkcji i rekurencją.

## Funkcje są wartościami

Funkcję można przekazać jako argument, zwrócić jako wynik i umieścić w strukturze danych.

```haskell
map double [1, 2, 3]  -- [2,4,6]
```

`map` przyjmuje funkcję i listę. Stosuje przekazaną funkcję do każdego elementu. Takie funkcje nazywamy **funkcjami wyższego rzędu**.

## Leniwe obliczanie

Haskell domyślnie oblicza wyrażenia wtedy, gdy ich wartość jest potrzebna.

```haskell
first x _ = x
first 7 (1 `div` 0)  -- 7

take 5 [1..]        -- [1,2,3,4,5]
```

`_` oznacza ignorowany argument. Pierwsza funkcja nie potrzebuje drugiego argumentu, więc nie wykonuje dzielenia przez zero. `[1..]` opisuje nieskończoną listę, ale `take 5` potrzebuje tylko pięciu elementów.

Leniwość nie gwarantuje zakończenia obliczeń. `sum [1..]` nie zwróci skończonego wyniku. Nie gwarantuje też małego zużycia pamięci: odkładane obliczenia mogą się gromadzić.

## Wyrażenia zamiast instrukcji

Wyrażenie ma wartość i typ. Wywołanie funkcji, `if`, `case` oraz `let ... in` są wyrażeniami.

```haskell
result = 10 + (if True then 2 else 3)  -- 12
```

Obie gałęzie `if` są obowiązkowe i muszą mieć zgodny typ, ponieważ całe wyrażenie musi mieć jeden typ.
