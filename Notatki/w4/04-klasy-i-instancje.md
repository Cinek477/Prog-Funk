# Klasy typów: od sygnatury do instancji

## Przeczytaj ograniczenie przed strzałką

`Eq a => a -> a -> Bool` znaczy: funkcja działa dla takiego typu `a`, który ma równość. Dwie wartości muszą mieć **ten sam** typ, a konkretna instancja mówi, co znaczy ich porównanie. `Eq` nie jest typem wartości: nie można deklarować listy `[Eq]` jako kolekcji dowolnych porównywalnych elementów.

## Własne znaczenie równości

```haskell
data Distance = Meters Integer | Centimeters Integer
  deriving Show

toCentimeters :: Distance -> Integer
toCentimeters (Meters m)      = 100 * m
toCentimeters (Centimeters c) = c

instance Eq Distance where
  x == y = toCentimeters x == toCentimeters y

instance Ord Distance where
  compare x y = compare (toCentimeters x) (toCentimeters y)
```

`Meters 2 == Centimeters 200` daje `True`, choć jeden wynik `show` to `"Meters 2"`, a drugi to `"Centimeters 200"`. Zwykłe `deriving Eq` uznałoby różne konstruktory za nierówne. Zapis `x == y = x == y` wewnątrz instancji nie rozwiązuje problemu: wywołuje tę samą metodę na tych samych argumentach.

`Ord` ma nadklasę `Eq`. Własne porównania powinny być zgodne: jeśli `compare x y == EQ`, to `x == y` powinno dać `True`. Dlatego obie instancje używają tej samej jednostki.

## Instancja z warunkiem dla parametru

```haskell
data Box a = Box a

instance Eq a => Eq (Box a) where
  Box x == Box y = x == y
```

Po lewej od `=>` podajemy warunek potrzebny, żeby napisać ciało: `x` i `y` mają typ `a`, więc potrzebujemy `Eq a`. Po prawej określamy, dla jakiego typu dostarczamy instancję: `Eq (Box a)`.

## Co wygeneruje deriving

| Klasa | Praktyczne znaczenie |
| --- | --- |
| `Show` | Tekst prezentujący konstruktor i pola. |
| `Eq` | Porównanie konstruktora, a potem odpowiadających pól. |
| `Ord` | Najpierw kolejność konstruktorów w deklaracji, potem porównanie pól od lewej. |
| `Enum` | Dla wyliczenia pozwala przechodzić po konstruktorach, np. `[Mon..Fri]`. |
| `Bounded` | Dla wyliczenia `minBound` i `maxBound` dają skrajne warianty. |

**Pułapka:** dla `data Shape = Circle Double | Rect Double Double deriving (Eq, Ord)` nawet ogromny okrąg jest mniejszy od małego prostokąta. Jeżeli zadanie mówi o powierzchni, porównuj `area x` i `area y`, nie wartości `Shape` przez automatyczne `Ord`.

## Po co fromInteger w Num?

Literał całkowity `3` jest interpretowany przez `fromInteger 3` na podstawie typu oczekiwanego w danym miejscu. Jeśli instancja `Num V2` powiela liczbę na obie współrzędne, to w `V2 2 5 + 3` prawa strona zachowuje się jak `V2 3 3`, a wynik to `V2 5 8`. Nie oznacza to, że każdy typ z dwoma liczbami automatycznie jest instancją `Num`.
