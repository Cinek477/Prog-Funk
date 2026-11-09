# 1. Funkcje wielu argumentów

## Krotka a argumenty podawane kolejno

```haskell
addPair :: Num a => (a, a) -> a
addPair (x, y) = x + y

add :: Num a => a -> a -> a
add x y = x + y
```

`addPair (1,2)` i `add 1 2` dają `3`. `add (1,2)` oraz `addPair 1 2` nie pasują do tych definicji. Para jest jedną wartością; dwa sposoby zapisu wymagają różnych typów.

Strzałki łączą się w prawo: `a -> a -> a` oznacza `a -> (a -> a)`. Funkcja otrzymuje pierwszy argument i zwraca funkcję oczekującą na drugi. To **currying**. Aplikacja łączy się w lewo: `add 1 2` to `(add 1) 2`.

## Aplikacja częściowa

```haskell
addOne :: Num a => a -> a
addOne = add 1
-- addOne 5 = 6

pair :: a -> b -> (a,b)
pair x y = (x,y)
-- pair 'a' :: b -> (Char,b)

combine :: Num a => a -> a -> a -> a
combine x y z = x * y + z
-- combine 1 2 :: Num a => a -> a
```

Podanie argumentu konsumuje jedną strzałkę typu i może ustalić część zmiennych typu.

**Aplikacja częściowa** to podanie części argumentów. **Funkcja częściowa** to funkcja, która dla niektórych argumentów nie daje poprawnego wyniku, np. `head []`. Te pojęcia są niezależne.

## Sekcje operatorów

Sekcja ustala jeden argument operatora:

| Sekcja | Odpowiednik | Przykład |
|---|---|---|
| `(+ 3)` | `\x -> x + 3` | `(+ 3) 4 == 7` |
| `(3 +)` | `\x -> 3 + x` | `(3 +) 4 == 7` |
| `(^ 2)` | `\x -> x ^ 2` | `(^ 2) 10 == 100` |
| `(2 ^)` | `\n -> 2 ^ n` | `(2 ^) 10 == 1024` |
| ``(`div` 2)`` | ``\x -> x `div` 2`` | wynik dla `7`: `3` |
| `(> 0)` | `\x -> x > 0` | wynik dla `5`: `True` |
| `(++ "!")` | `\s -> s ++ "!"` | wynik dla `"Hej"`: `"Hej!"` |

`(^ 2) :: Num a => a -> a`, natomiast `(2 ^) :: (Num a, Integral b) => b -> a`. W drugim przypadku argument jest wykładnikiem całkowitym.

**Wyjątek składniowy:** `(- 5)` to ujemna liczba, a nie funkcja odejmująca 5.

```haskell
subtract 5 12 -- 7: od drugiego argumentu odejmij pierwszy
(5 -) 12     -- -7: od pięciu odejmij argument
-- funkcja odejmująca 5:
-- \x -> x - 5
```

## curry, uncurry, flip

To istniejące funkcje biblioteczne; poniżej ich typy i przykłady użycia:

```haskell
curry   :: ((a,b) -> c) -> a -> b -> c
uncurry :: (a -> b -> c) -> (a,b) -> c
flip    :: (a -> b -> c) -> b -> a -> c
```

- `curry` zmienia funkcję na parze w funkcję z kolejnymi argumentami: `curry addPair 1 2` daje `3`.
- `uncurry` wykonuje zmianę odwrotną: `uncurry add (1,2)` daje `3`.
- `flip` zamienia kolejność dwóch pierwszych argumentów: `flip (-) 3 10` daje `7`.

`flip (^) 2 10` daje `10 ^ 2`, czyli `100`.

## Sygnatury i ograniczenie monomorfizmu

```haskell
toPower5 :: Num a => a -> a
toPower5 = (^ 5)
```

Definicje bez jawnych parametrów po lewej stronie, zawierające przeciążone operacje, mogą podlegać **ograniczeniu monomorfizmu**. Bez sygnatury typ takiego wiązania może zostać zawężony przez domyślny wybór typu liczbowego. Zachowanie zależy też od ustawień; GHCi i moduł mogą mieć inne ustawienia. Nie oznacza to, że każda definicja bez parametrów jest monomorficzna. Jawna sygnatura wyraża zamierzoną ogólność.

Nazwy zwykłych funkcji zaczynaj małą literą: `myFun x = 2 * x`. Wielka litera oznacza m.in. konstruktor danych, więc `MyFun x = ...` nie definiuje zwykłej funkcji.
