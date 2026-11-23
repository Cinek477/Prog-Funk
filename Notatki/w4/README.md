# Wykład 4 — algebraiczne typy danych i klasy typów

[Materiały online](../materialy/index.html#w4) · [Quiz z wykładu 4](../quizy/index.html?wyklad=4)

Opracowanie wykładu Romana Dębskiego, slajdy 3–23. Zacznij od konstruktorów i wzorców, potem przejdź do instancji i modułów.

## 1. `type`, `newtype` i `data` (slajdy 3–8)

| Deklaracja | Co tworzy? | Kiedy użyć? |
|---|---|---|
| `type Polar = (Double, Double)` | synonim istniejącego typu | Chcesz nazwać znaczenie pary, ale akceptujesz, że kompilator nie odróżni jej od innych par typu `(Double, Double)`. |
| `newtype Meters = Meters Double` | odrębny typ, jeden konstruktor z jednym polem | Chcesz odróżniać metry od sekund bez dodatkowego opakowania w reprezentacji. |
| `data Shape = Circle Double \| Rect Double Double` | odrębny typ, dowolna liczba wariantów i pól | Chcesz opisać różne postacie danych lub zgrupować pola. |

```haskell
data Point = Point Double Double deriving Show
data Pair a = Pair a a deriving Show
```

Po lewej `Point` jest nazwą typu, a z prawej konstruktorem wartości o typie `Double -> Double -> Point`. `Point 1` nadal jest funkcją: `Double -> Point`. Konstruktor `Pair` ma typ `a -> a -> Pair a`; oba argumenty muszą mieć ten sam typ.

```haskell
data Person = Person { firstName :: String, city :: String }
  deriving (Show, Eq)

moveTo :: String -> Person -> Person
moveTo place p = p { city = place }
```

`city :: Person -> String` to selektor. Aktualizacja tworzy nową wartość; oryginalna osoba nadal ma poprzednie miasto. W zwykłej składni selektory zajmują nazwy w module (rozszerzenia GHC mogą zmienić te zasady).

## 2. Warianty, Maybe i typy rekurencyjne (slajdy 9–13)

`Circle Double` i `Rect Double Double` to dwa warianty jednego typu `Shape`: mogą występować razem w `[Shape]`. Alternatywa konstruktorów to **suma**, a pola jednego konstruktora tworzą **iloczyn**. Przy pisaniu funkcji rozpatrz każdy wariant; GHC z `-Wall` ostrzega o niepełnych wzorcach.

```haskell
safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

describeHead :: Show a => [a] -> String
describeHead xs = case safeHead xs of
  Nothing -> "pusta lista"
  Just x  -> show x
```

`Just 3` nie jest liczbą, lecz wartością opakowaną w `Maybe`. Wynikiem `safeHead []` jest `Nothing` zamiast wyjątku. Podobnie dzielenie może zwrócić `Nothing` dla zera, a funkcja szukająca pierwiastków dla ujemnej delty. Przy typie `Int` skrajny przypadek `minBound \`div\` (-1)` może dodatkowo przepełnić wynik; do prostego przykładu bez tego przypadku możesz użyć `Integer`.

```haskell
data Tree a = Empty | Node (Tree a) a (Tree a)
  deriving (Show, Eq)

size :: Tree a -> Int
size Empty = 0
size (Node l _ r) = 1 + size l + size r

insert :: Ord a => a -> Tree a -> Tree a
insert x Empty = Node Empty x Empty
insert x (Node l y r)
  | x < y     = Node (insert x l) y r
  | x > y     = Node l y (insert x r)
  | otherwise = Node l y r

data Expr = Lit Int | Add Expr Expr | Mul Expr Expr deriving Show

eval :: Expr -> Int
eval (Lit n) = n
eval (Add l r) = eval l + eval r
eval (Mul l r) = eval l * eval r
```

`size` przechodzi oba poddrzewa. `insert` w BST wybiera jedną gałąź i w tej wersji ignoruje duplikaty. Sam typ `Tree` nie gwarantuje porządku BST. Dla `Expr` struktura wyznacza kolejność działań: `Mul (Add (Lit 1) (Lit 2)) (Lit 3)` daje 9. Gdy wypisujesz drzewo wyrażeń, nawiasuj oba rodzaje operacji albo uwzględnij priorytety i łączność; samo nawiasowanie dodawania nie zachowa każdej struktury.

## 3. Klasy i instancje (slajdy 14–20)

- **Klasa** określa dostępne metody, np. `Eq` udostępnia `==` i `/=`. **Instancja** określa sposób ich wykonania dla danego typu. `MINIMAL` wskazuje wymagany zestaw metod; dla `Eq` wystarczy zdefiniować jedną z dwóch.
- `deriving Show` daje standardowy zapis konstruktora i jego pól. `deriving Eq` porównuje konstruktory i pola, a w drzewie także kształt. `deriving Ord` porównuje najpierw kolejność konstruktorów **w deklaracji**, potem pola od lewej. Dlatego `maximum [Circle 3, Rect 1 1]` wybierze `Rect`, jeżeli `Circle` zadeklarowano wcześniej. To nie jest porównanie pól powierzchni. `Ord` wymaga też `Eq`.
- Dla wyliczenia `data Day = Mon | Tue | Wed | Thu | Fri | Sat | Sun deriving (Show, Eq, Ord, Enum, Bounded)` można zapisać `[Mon..Fri]` i `minBound :: Day`.
- Ręczna instancja może porównać temperatury po sprowadzeniu do wspólnej jednostki. Przy `Double` pamiętaj o zaokrągleniach. Dla parametrycznego drzewa potrzebujesz `instance Eq a => Eq (Tree a)`, bo porównujesz także wartości typu `a`. Wybierz ręczną instancję **albo** `deriving Eq`.
- W instancji `Num V2` ze slajdu działania wykonuje się po współrzędnych, a `fromInteger 2 = V2 2 2` (dla konkretnego wejścia 2). Stąd `V2 1 2 * 2` daje `V2 2 4`. Podobna reprezentacja nie daje automatycznie instancji `Num` dla `Meters`.

```haskell
class HasArea a where
  area :: a -> Double
  describeArea :: a -> String
  describeArea a = "pole: " ++ show (area a)

newtype Disk = Disk Double
instance HasArea Disk where
  area (Disk r) = pi*r*r
```

`reverse :: [a] -> [a]` działa tak samo niezależnie od typu elementów (**polimorfizm parametryczny**). `area :: HasArea a => a -> Double` korzysta z implementacji przypisanej typowi (**ad hoc**). Ograniczenie klasy nie tworzy heterogenicznej listy. Gdy spodziewasz się głównie nowych operacji na ustalonych wariantach, wybierz wspólny typ sumy. Gdy spodziewasz się nowych typów obsługujących ten sam zestaw operacji, rozważ klasę. Rozszerzanie w obu kierunkach to tzw. *expression problem*.

## 4. Moduły i abstrakcyjny stos (slajdy 21–23)

```haskell
module Stack (Stack, empty, push, pop) where

newtype Stack a = Stack [a]

empty :: Stack a
empty = Stack []

push :: a -> Stack a -> Stack a
push x (Stack xs) = Stack (x:xs)

pop :: Stack a -> Maybe (a, Stack a)
pop (Stack []) = Nothing
pop (Stack (x:xs)) = Just (x, Stack xs)
```

Zapisz moduł jako `Stack.hs`. W innym pliku `import Stack` pozwala użyć typu i funkcji, ale nie konstruktora w wyrażeniu lub wzorcu. `Stack(..)` na liście eksportu ujawniłoby konstruktor. Po `push 2 (push 1 empty)` pierwsze `pop` oddaje 2 i pozostały stos (LIFO). Wartości się nie mutują.

`import qualified Data.Map as Map` daje nazwę `Map.lookup`, bez kolizji z `lookup` z Prelude. **Algebraiczny** typ opisuje warianty i pola. **Abstrakcyjny** typ opisuje publiczne operacje i ukrywa reprezentację. Skrót ADT może oznaczać oba pojęcia.

## Sprawdź się

1. Czy `type Seconds = Double` i `type Meters = Double` pozwolą wykryć zamianę argumentów? **Nie: oba są synonimami Double.**
2. Jaki typ ma `Rect 2`? **`Double -> Shape`.**
3. Czy dwa drzewa z tymi samymi elementami są zawsze równe przy `deriving Eq`? **Nie: kształt też musi być identyczny.**
4. Czy `deriving Show` wystarczy, by użyć `==`? **Nie: potrzeba instancji Eq.**
5. Czemu `pop` zwraca parę wewnątrz `Maybe`? **W przypadku sukcesu oddaje zdjęty element i nowy stos; dla pustego zwraca Nothing.**
