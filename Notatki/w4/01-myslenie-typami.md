# Jak zaprojektować typ danych

## Zacznij od wartości, które chcesz dopuścić

Wyobraź sobie wynik równania: może nie mieć rzeczywistych rozwiązań, mieć jeden pierwiastek, dwa albo nieskończenie wiele. Para typu `(Double, Double)` nie wyraża tych różnic. Nie próbuj kodować braku wyniku przez specjalną liczbę, którą trzeba pamiętać.

```haskell
data Roots = NoRoots | OneRoot Double | TwoRoots Double Double | AllReal
  deriving (Show, Eq)

describe :: Roots -> String
describe NoRoots        = "Brak rozwiazan"
describe (OneRoot x)    = "Jeden: " ++ show x
describe (TwoRoots x y) = "Dwa: " ++ show x ++ ", " ++ show y
describe AllReal        = "Wszystkie liczby rzeczywiste"
```

`TwoRoots` to funkcja dwóch argumentów; `TwoRoots 1` nadal czeka na drugi argument. `NoRoots` od razu jest wartością. `Roots` nie jest konstruktorem wartości — w tej deklaracji występuje tylko jako nazwa typu.

## Suma wariantów i iloczyn pól

Warianty odpowiadają słowu **albo**. Pola jednego wariantu odpowiadają słowu **i**. Dobry test to policzenie możliwości, gdy wszystkie pola są skończone.

```haskell
data Example = Off | On Bool Bool
```

`Off` daje jedną możliwość. W `On` każde pole ma dwie możliwości, więc razem jest ich cztery. Typ `Example` ma zatem pięć zwykłych wartości: `1 + 2 * 2`. Nie liczymy tu nieokreślonych obliczeń takich jak `undefined`.

## Dlaczego nie zawsze Maybe?

`Maybe a` jest dobre, gdy wynik może istnieć albo nie. Jeżeli nieobecność ma kilka znaczeń i chcesz je rozróżnić, własny typ przechowa tę informację. Dla równania `Nothing` nie powie, czy nie ma rozwiązań, czy wejście zostało odrzucone.

## Oddziel jednostkę od reprezentacji

```haskell
newtype Meters = Meters Double
newtype Seconds = Seconds Double

speed :: Meters -> Seconds -> Maybe Double
speed _ (Seconds 0) = Nothing
speed (Meters d) (Seconds t) = Just (d/t)
```

W `speed (Meters 100) (Seconds 10)` wynik to `Just 10.0`. Po zamianie argumentów kod nie przejdzie kontroli typów. Z `type` kompilator widziałby w obu miejscach `Double`. Natomiast dodatniość czasu to osobna reguła — samo `newtype` jej nie zapewnia.

## Pułapka: niepełna obsługa Maybe

```haskell
message :: Show a => Maybe a -> String
message (Just x) = show x
message Nothing  = "Brak wyniku"
```

Bez drugiego równania kompilacja zwykle się powiedzie, ale `message Nothing` zakończy się błędem. W GHCi włącz `:set -Wall`, żeby wcześniej zobaczyć ostrzeżenie o niepełnych wzorcach.
