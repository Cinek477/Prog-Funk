# 3. Leniwe wartościowanie

## Czy argument jest potrzebny?

```haskell
answer :: Int -> Int -> Int
answer x y = if x > 0 then 42 else x + y

-- answer 1 undefined daje 42
-- answer 0 undefined zgłasza błąd
```

`undefined` ma dowolny wymagany typ, ale próba uzyskania jego wartości kończy się błędem. Pierwsze wywołanie nie potrzebuje `y`. W drugim trzeba obliczyć `x + y`, więc błąd staje się widoczny.

**Nieścisłość** opisuje znaczenie języka: wynik może być dostępny bez obliczania argumentu. **Leniwe wartościowanie** to sposób realizacji: odkładaj obliczenie, wykonaj je, gdy potrzeba, i współdziel wynik. To rozróżnienie między semantyką a implementacją.

## Thunk i współdzielenie

**Thunk** to reprezentacja odłożonego obliczenia wraz z potrzebnym środowiskiem. W typowym modelu wykonania GHC współdzielony thunk jest po obliczeniu aktualizowany wynikiem; nie trzeba przeliczać go przy każdym użyciu. Nie jest to automatyczna pamięć podręczna dla wszystkich wywołań funkcji z równymi argumentami.

Eksperyment w GHCi:

```text
let x = 1 + 2 :: Int
let y = x + 1
:sprint x
:sprint y
seq x ()
:sprint x
:sprint y
```

`:sprint` pokazuje stan obliczenia bez zwykłego wymuszania wartości jak przy wypisywaniu jej w konsoli. `_` może oznaczać nieobliczoną część. Po wymuszeniu `x` można zobaczyć `x = 3`, podczas gdy `y` pozostaje odłożone. Dokładny obraz zależy od kompilacji i optymalizacji — to ilustracja mechanizmu, nie gwarantowany transkrypt.

## seq i WHNF

```haskell
seq :: a -> b -> b
```

`seq a b` wymusza pierwszy argument do **WHNF**, a następnie zwraca drugi. WHNF to zewnętrzna postać wartości, niekoniecznie pełne obliczenie jej wnętrza.

```haskell
seq undefined ()   -- błąd
seq (1 + 2) ()     -- ()
seq [undefined] () -- (): wiadomo, że lista jest niepusta
seq (Just undefined) () -- (): znany konstruktor Just
```

Wymuszenie listy do WHNF nie oblicza wszystkich jej elementów. To ważne przy rozumieniu ścisłych akumulatorów.

## Własne konstrukcje sterujące

```haskell
and2 :: Bool -> Bool -> Bool
and2 False _ = False
and2 True y  = y

if' :: Bool -> a -> a -> a
if' True x _  = x
if' False _ y = y
```

- `and2 False undefined` daje `False`.
- `and2 undefined False` zgłasza błąd: trzeba rozpoznać pierwszy argument, aby wybrać równanie.
- `if' True "tak" undefined` daje `"tak"`.

Leniwość pozwala zwykłym funkcjom pomijać niepotrzebne obliczenia. Kolejność dopasowywania wzorców ma znaczenie także wtedy, gdy końcowy wynik logiczny wydaje się oczywisty.

## Listy nieskończone i produktywność

```haskell
take 5 [1..] -- [1,2,3,4,5]
takeWhile (<50) [x*x | x <- [1..]] -- [1,4,9,16,25,36,49]
head [x | x <- [1..], x `mod` 35 == 0] -- 35
```

Obliczenie może się zakończyć, jeżeli do jego wyniku wystarczy skończona praca. Samo użycie `head` lub `take` nie daje gwarancji: `head (filter (<0) [1..])` szuka bez końca.

```haskell
length [1..] -- nie kończy się
[x | x <- [1..], x < 5] -- zwraca początek 1,2,3,4, ale nigdy nie ustala końca

takeWhile (<5) [1..] -- kończy się wynikiem [1,2,3,4]
```

`filter` i comprehension z warunkiem nadal szukają kolejnych pasujących elementów. `takeWhile` kończy na pierwszym niespełnieniu warunku.

**Produktywność:** możliwość wytwarzania kolejnych fragmentów wyniku w skończonej pracy, nawet jeśli całość jest nieskończona.

## Fibonacci przez korekursję

```haskell
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- take 10 fibs = [0,1,1,2,3,5,8,13,21,34]
```

`zipWith (+)` dodaje odpowiadające sobie elementy dwóch list:

```text
fibs:       0 1 1 2 3 ...
tail fibs:  1 1 2 3 5 ...
suma:       1 2 3 5 8 ...
```

Do utworzenia kolejnego elementu wystarczają wcześniejsze. To **korekursja**: opisujemy, jak wytwarzać strukturę, zamiast koniecznie zmniejszać ją do przypadku bazowego. `Integer` zapobiega przepełnieniu typowemu dla ograniczonego `Int`.

Leniwość może oszczędzać pracę, ale thunki i zatrzymywane fragmenty struktur zajmują pamięć. Nie jest synonimem równoległego wykonania.
