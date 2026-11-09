# 5. Pytania i ćwiczenia

## Krótkie odpowiedzi

| Pytanie | Odpowiedź |
|---|---|
| Co oznacza `a -> b -> c`? | `a -> (b -> c)`: funkcja zwracająca kolejną funkcję. |
| Czym jest aplikacja częściowa? | Podaniem części argumentów i otrzymaniem funkcji na pozostałe. |
| Czym jest sekcja? | Częściową aplikacją operatora z ustaleniem jednego argumentu. |
| Czy `(- 5)` odejmuje 5? | Nie, oznacza ujemną liczbę; użyj `subtract 5` lub lambdy. |
| Jak jest zbudowana lista? | Jest pusta `[]` albo ma postać `x:xs`. |
| Dlaczego indeksowanie listy kosztuje? | Trzeba przejść od początku do wskazanego ogniwa. |
| Co to thunk? | Odłożone obliczenie wraz ze środowiskiem potrzebnym do jego wykonania. |
| Co to nieścisłość? | Możliwość uzyskania wyniku bez obliczania niepotrzebnego argumentu. |
| Co wymusza `seq`? | Pierwszy argument do WHNF, czyli zewnętrznej postaci. |
| Dlaczego nieskończona lista bywa użyteczna? | Można obliczyć tylko potrzebny skończony fragment. |
| Co to akumulator? | Argument przenoszący wynik dotychczasowych kroków. |
| Co to rekurencja ogonowa? | Taka, w której wynik wywołania rekurencyjnego jest bezpośrednio wynikiem gałęzi. |
| Czy ogonowa oznacza stałą pamięć? | Nie; mogą gromadzić się thunki, a rozmiar danych może rosnąć. |
| Po co `!acc`? | Żeby wymuszać akumulator do WHNF i ograniczać odkładanie obliczeń. |
| Dlaczego naiwne `fib` jest wolne? | Wielokrotnie rozwiązuje te same podproblemy. |

## Przewidź wynik lub błąd

1. `(^2) 5` oraz `(2^) 5`.
2. `subtract 5 12` oraz `(5-) 12`.
3. `zip [1,2,3] "ab"`.
4. `take 10 [1,2]` oraz `[1,2] !! 2`.
5. `[(x,y) | x <- [1,2], y <- [x..2]]`.
6. `take 3 [x | x <- [1..], even x]`.
7. `length (takeWhile (<5) [1..])`.
8. `length [x | x <- [1..], x < 5]`.
9. `seq (Just undefined) ()`.
10. Dlaczego `reverseSlow` z poprzedniego rozdziału ma koszt kwadratowy?

## Odpowiedzi

1. `25` i `32`: kwadrat argumentu kontra potęga dwójki.
2. `7` i `-7`: znaczenie zależy od kolejności argumentów.
3. `[(1,'a'),(2,'b')]`: kończymy na krótszej liście.
4. `[1,2]` i błąd: ostatni poprawny indeks to `1`.
5. `[(1,1),(1,2),(2,2)]`.
6. `[2,4,6]`.
7. `4`: `takeWhile` ustala koniec po napotkaniu `5`.
8. Nie kończy się: po czterech elementach nadal szuka następnych spełniających warunek.
9. `()`: zewnętrzny konstruktor `Just` jest znany; wnętrze nie jest wymuszane.
10. Każde `++ [x]` przechodzi lewą listę; suma kosztów wynosi około `0 + 1 + ... + (n-1)`, czyli O(n²).

## Samodzielne definicje

A. Napisz funkcję `timesThree` przez sekcję i podaj jej typ.

B. Napisz funkcję sprawdzającą, czy dwa pierwsze elementy listy są równe, bez błędu dla krótkiej listy.

C. Napisz rekurencyjną funkcję liczącą elementy spełniające warunek.

Przykładowe rozwiązania:

```haskell
timesThree :: Num a => a -> a
timesThree = (*3)

firstTwoEqual :: Eq a => [a] -> Bool
firstTwoEqual (x:y:_) = x == y
firstTwoEqual _ = False

countIf :: (a -> Bool) -> [a] -> Int
countIf _ [] = 0
countIf p (x:xs)
  | p x = 1 + countIf p xs
  | otherwise = countIf p xs
```

Dla `countIf` ograniczenie `Eq a` ani `Num a` nie jest potrzebne: operacje na elementach opisuje przekazany predykat. Wynik ma konkretny typ `Int`.
