# Ćwiczenia do wykładu 4

Przed odsłonięciem odpowiedzi zapisz typ, dokładny wynik lub brakujący kod. W pytaniach o błędy odróżniaj to, co odrzuci kompilator, od tego, co zgłosi problem dopiero przy obliczaniu.

## A. Typy i modelowanie

1. Jaki typ ma konstruktor `Tagged` w `data Tagged a b = Tagged a b`? Jaki typ ma `Tagged True`?
2. Ile zwykłych wartości ma `data Flag = Single Bool | Both Bool Bool | Unknown`? Pomiń nieokreślone wyniki.
3. Czy kompilator odróżni `type UserId = Int` od `type OrderId = Int`? Jak zmieniłbyś deklaracje, żeby wykrywać pomyłki?
4. Dlaczego `Just (3 :: Int) + 1` nie daje `Just 4`? Zapisz funkcję, która zwiększa liczbę tylko dla `Just`.

## Rozwiązania A

1. `Tagged :: a -> b -> Tagged a b`. Po podaniu `True`: `Tagged True :: b -> Tagged Bool b`.
2. **7**: dwie możliwości dla `Single`, cztery dla `Both` i jedna dla `Unknown`.
3. Oba synonimy to dla kompilatora ten sam typ. Użyj `newtype UserId = UserId Int` i `newtype OrderId = OrderId Int`.
4. `(+)` potrzebuje instancji `Num`, a `Maybe Int` nie ma standardowej instancji `Num`. Rozpakuj wartość wzorcem:

```haskell
incMaybe :: Maybe Int -> Maybe Int
incMaybe Nothing  = Nothing
incMaybe (Just n) = Just (n + 1)
```

## B. Drzewa i instancje

5. Jakie `size` i `inorder` daje `Node (Node Empty 2 Empty) 5 (Node Empty 7 Empty)`?
6. Oblicz `eval (Mul (Add (Lit 2) (Lit 4)) (Add (Lit 3) (Lit 1)))`.
7. Co większe przy automatycznym `Ord`: `Circle 100` czy `Rect 1 1`, jeśli `Circle` zadeklarowano wcześniej?
8. Dlaczego dla `data Box a = Box a` potrzebujesz `Eq a`, jeśli w instancji `Eq (Box a)` porównujesz zawartość?
9. Zdefiniuj funkcję liczącą wysokość drzewa w **węzłach**. Puste drzewo ma wysokość zero.

## Rozwiązania B

5. `size` daje **3**, `inorder` daje **[2,5,7]**. Pierwsze liczy wszystkie węzły; drugie przechodzi je w kolejności lewo, korzeń, prawo.
6. **24**: lewe podwyrażenie daje 6, prawe daje 4.
7. **Rect 1 1**. Kolejność konstruktorów ma pierwszeństwo, powierzchnia nie bierze udziału.
8. Wzorce wiążą pola typu `a`, więc operator `==` na polach musi mieć instancję `Eq a`. To warunek z nagłówka `instance Eq a => Eq (Box a)`.
9. Liczy się najdłuższa ścieżka w dół, więc wybierasz maksimum, nie sumę:

```haskell
height :: Tree a -> Int
height Empty        = 0
height (Node l _ r) = 1 + max (height l) (height r)
```

## C. Moduły i pułapki

10. Jak wyeksportować typ `Stack` i operacje `empty`, `push`, `pop`, chowając konstruktor?
11. Co zwróci pierwsze `pop` po `push 'b' (push 'a' empty)`? A co jeśli wykonasz `pop` ponownie na **tym samym** stosie?
12. Co stanie się dla `email Guest` przy definicji `data Account = Guest | Member { email :: String }`?
13. Jak zaimportować `lookup` z `Data.Map`, żeby nie pomylić go z `lookup` z Prelude?

## Rozwiązania C

10. `module Stack (Stack, empty, push, pop) where`. Samo `Stack` na liście eksportu oznacza typ bez konstruktorów.
11. Oba wywołania zdejmą **'b'**, bo wejściowa wartość się nie zmienia. Jeśli chcesz zdjąć następny element, przekaż stos zwrócony w parze przez pierwsze `pop`.
12. Wywołanie ma poprawny typ, lecz zgłosi błąd podczas obliczania wyniku. Wariant `Guest` nie posiada pola `email`.
13. `import qualified Data.Map as Map`, a potem `Map.lookup key dict`.

[Przejdź do quizu z wykładu 4](../quizy/index.html?wyklad=4)
