# 2. Listy

## Budowa: pustka albo element i reszta

Lista `[a]` zawiera elementy jednego typu. Ma dwa konstruktory: `[]` oraz `(:)`.

```haskell
[1,2,3] == 1 : (2 : (3 : []))
-- (:) :: a -> [a] -> [a]
```

To lista jednokierunkowa. Pierwszy element jest dostępny bez przechodzenia poprzednich elementów; dotarcie do dalszego wymaga przejścia kolejnych ogniw.

Schematyczny zapis ze slajdów należy rozumieć jako opis budowy. Poprawny przykład własnego analogicznego typu to:

```haskell
data List a = Empty | Cons a (List a)
```

Nie redefiniuje on wbudowanej składni list.

## Najważniejsze operacje

| Wyrażenie | Wynik |
|---|---|
| `head [1,2,3]` | `1` |
| `tail [1,2,3]` | `[2,3]` |
| `last [1,2,3]` | `3` |
| `init [1,2,3]` | `[1,2]` |
| `length [1,2,3]` | `3` |
| `null []` | `True` |
| `take 2 [1,2,3]` | `[1,2]` |
| `drop 2 [1,2,3]` | `[3]` |
| `splitAt 2 [1,2,3]` | `([1,2],[3])` |
| `[1,2,3] !! 1` | `2` — indeksy od zera |
| `[1] ++ [2,3]` | `[1,2,3]` |
| `reverse [1,2,3]` | `[3,2,1]` |
| `elem 2 [1,2,3]` | `True` |
| `sum [1,2,3]` | `6` |
| `product [1,2,3]` | `6` |
| `maximum [1,3,2]` | `3` |
| `zip [1,2] "ab"` | `[(1,'a'),(2,'b')]` |
| `any even [1,3]` | `False` |
| `all odd [1,3]` | `True` |
| `filter even [1,2,3,4]` | `[2,4]` |
| `map (*2) [1,2,3]` | `[2,4,6]` |

`sort` wymaga importu:

```haskell
import Data.List (sort)
-- sort [2,3,1] daje [1,2,3]
```

`zip` kończy na krótszej liście. `take 10 [3,1,4]` daje całą dostępną listę. `takeWhile p` bierze początek do pierwszego niespełnienia `p`, a `filter p` przeszukuje dalej.

## Przypadki brzegowe

`head`, `tail`, `last`, `init` i `maximum` nie obsługują pustej listy. `!!` zgłasza błąd również dla indeksu ujemnego lub spoza zakresu.

```haskell
take 5 []  -- []
drop 5 []  -- []
sum []     -- 0
product [] -- 1
any even [] -- False
all even [] -- True
```

Brak błędu dla pustej listy nie oznacza zakończenia dla dowolnej listy nieskończonej. `length [1..]` nie kończy się. Terminem „całkowita” na slajdach opisano przede wszystkim obsługę zwykłych przypadków brzegowych; należy pamiętać także o niekończących się obliczeniach.

## Koszty list

Dla już dostępnej struktury listy, bez kosztu obliczania jej elementów:

| Operacja | Typowy koszt |
|---|---|
| `head xs`, `tail xs`, `x : xs`, `null xs` | stały, O(1), gdy przypadek jest poprawny |
| `xs !! i` | O(i + 1) |
| `length xs`, `last xs` | O(n) dla n elementów |
| pełne przejście `xs ++ ys` | O(długość xs) |
| `reverse xs` | O(n) |

Leniwość oznacza, że samo utworzenie wyrażenia `xs ++ ys` nie musi od razu przechodzić całej lewej listy. Koszt pojawia się podczas konsumowania wyniku.

Indeksowanie kolejno wszystkich elementów przez `!!` może dać O(n²). Zwykle przechodź listę bezpośrednio przez wzorce lub funkcje biblioteczne. Do intensywnego dostępu losowego służą inne struktury, np. tablice lub wektory.

## List comprehensions

```haskell
[x ^ 2 | x <- [1..10], odd x]
-- [1,9,25,49,81]

[(x,c) | x <- [1..3], c <- "ab"]
-- [(1,'a'),(1,'b'),(2,'a'),(2,'b'),(3,'a'),(3,'b')]

[(x,y) | x <- [1..3], y <- [x..3]]
-- [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
```

Przed `|` jest wynikowy element. `x <- lista` jest generatorem, a `odd x` warunkiem. Kolejny generator może korzystać ze zmiennych wcześniejszego; ostatni zmienia się najszybciej.

Trójki pitagorejskie:

```haskell
triples :: [(Int,Int,Int)]
triples = [(a,b,c) | a <- [1..10], b <- [a..10], c <- [b..10],
                     a*a + b*b == c*c]
-- [(3,4,5),(6,8,10)]
```

Zakresy wymuszają `a <= b <= c`, więc nie otrzymujemy obu przestawień przyprostokątnych.

## Pusty zakres i liczby pierwsze

`[2..0]` jest pustą listą. Brak znalezionych dzielników nie wystarcza, by uznać 1 lub liczbę ujemną za pierwszą.

```haskell
isPrime :: Int -> Bool
isPrime n = n > 1 && null [i | i <- [2..n-1], n `mod` i == 0]
```

To prosty przykład dydaktyczny. `null` pyta tylko, czy lista jest pusta, i nie wymaga klasy `Eq` dla jej elementów, w przeciwieństwie do porównania `xs == []`.
