# Drzewa, instancje i granice modułów

## Ręcznie prześledź wstawianie do BST

Wstaw kolejno 5, 2 i 7. Najpierw nie ma korzenia, więc tworzysz węzeł 5. Potem 2 jest mniejsze od 5, więc zastępujesz puste lewe poddrzewo nowym węzłem. Wartość 7 trafia po prawej. Drugi raz wstawione 2 niczego nie zmienia w wersji ignorującej duplikaty.

```text
       5
      / \
     2   7
```

`size` musi zajrzeć w obie strony. Wyszukiwanie w poprawnym BST wybiera jedną gałąź; to nie znaczy zawsze logarytmicznie. Niezrównoważone drzewo, np. po wstawianiu uporządkowanych danych, może przypominać listę.

```haskell
data Tree a = Empty | Node (Tree a) a (Tree a)

member :: Ord a => a -> Tree a -> Bool
member _ Empty = False
member x (Node l y r) = case compare x y of
  LT -> member x l
  EQ -> True
  GT -> member x r

inorder :: Tree a -> [a]
inorder t = go t []
  where
    go Empty acc = acc
    go (Node l x r) acc = go l (x : go r acc)
```

Przejście `inorder` czyta lewe poddrzewo, korzeń, a potem prawe. Nie wymaga `Ord`: nie porównuje wartości. Dla poprawnego BST otrzymasz listę uporządkowaną. Dwa różne drzewa mogą mieć identyczne przejście; automatyczne `Eq` nadal porówna także ich strukturę.

## Domyślna instancja czy własne porównanie?

```haskell
data Shape = Circle Double | Rect Double Double
  deriving (Show, Eq, Ord)

area :: Shape -> Double
area (Circle r) = pi*r*r
area (Rect w h) = w*h
```

`Circle 100 < Rect 1 1` daje `True`, bo w automatycznym `Ord` pozycja konstruktora jest ważniejsza od pól. Jeśli w zadaniu chodzi o pole powierzchni, porównuj `area x` i `area y`, albo użyj `sortOn area` z `Data.List`. Nie zmieniaj znaczenia całej instancji tylko dla jednego sortowania.

## Typ abstrakcyjny: przeprojektuj reprezentację bez zmiany użytkowników

Jeśli moduł eksportuje `Stack`, ale nie `Stack(..)`, kod wywołujący opiera się na sygnaturach `empty`, `push` i `pop`. Może wykonać `pop (push 7 empty)`, ale nie może tworzyć wartości przez `Stack [7]`. Implementację można potem zmienić, o ile zachowasz publiczne typy i zachowanie.

Podobnie dla BST: eksportuj typ, twórcę pustego drzewa i bezpieczne operacje. Ukrycie `Node` sprawia, że użytkownik modułu nie stworzy dowolnego nieuporządkowanego węzła za pomocą tego konstruktora. To konkretna korzyść z modułu, nie tylko porządek w plikach.

## Połącz to w zadaniu

1. Zapisz konstruktor dla wyrażenia zmiany znaku: `Neg Expr`. Dopisz jego przypadek w `eval`: `eval (Neg e) = negate (eval e)`.
2. Czy samo `deriving Show` pozwala porównać wyrażenia przez `==`? Nie, potrzeba instancji `Eq`.
3. Czy `member` zachowa się poprawnie dla dowolnego drzewa? Nie. Odrzucenie połowy kandydatów opiera się na niezmienniku BST.
