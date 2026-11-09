# 5. Praca z kodem i ściąga

## Plik a konsola GHCi

Kod źródłowy zapisujesz w plikach `.hs`. GHC jest kompilatorem, GHCi interaktywną konsolą, a `runghc` pozwala uruchomić plik bez osobnego kroku budowania programu.

Po udostępnieniu tych narzędzi w środowisku uruchom w terminalu:

```text
ghci
```

W GHCi można obliczać wyrażenia i sprawdzać typy:

```text
:type not
:type map
:info Int
:load Lab1.hs
:reload
main
:quit
```

`:type` (skrót `:t`) pokazuje typ, `:info` informacje o nazwie, `:load` (`:l`) ładuje plik, a `:reload` (`:r`) wczytuje go po zmianach. W razie problemu ze znalezieniem pliku użyj pełnej ścieżki w cudzysłowie.

W GHCi można utworzyć krótką definicję przez `let square x = x * x`. W pliku na najwyższym poziomie piszesz po prostu `square x = x * x`, bez `let`.

Samą funkcję `square` można wczytać bez definiowania `main`. Uruchamialny program potrzebuje punktu wejścia:

```haskell
main :: IO ()
main = putStrLn "Czesc!"
```

`IO ()` opisuje akcję wejścia/wyjścia, która po wykonaniu nie dostarcza użytecznego wyniku obliczeniowego. `putStrLn` wypisuje tekst i kończy linię.

```haskell
main :: IO ()
main = do
  putStrLn "Podaj imie:"
  name <- getLine
  putStrLn ("Czesc, " ++ name ++ "!")
```

`do` pozwala zapisać sekwencję akcji. Tutaj `<-` wiąże nazwę `name` z wynikiem akcji `getLine`. Nie jest przypisaniem zmieniającym istniejącą zmienną. W pliku może być tylko jedna z pokazanych definicji `main`.

Uruchomienie pliku w terminalu:

```text
runghc Lab1.hs
```

Kompilacja i uruchomienie w PowerShell:

```text
ghc Lab1.hs -o lab1
.\lab1.exe
```

## Najczęstsze błędy

| Problem | Poprawny zapis lub wyjaśnienie |
|---|---|
| `f(x,y)` przy definicji `f x y` | `f x y`; krotka jest jednym argumentem |
| `x = 3` użyte jako test | test równości to `x == 3` |
| `if p then a` | potrzebne jest również `else b` |
| `if p then 1 else False` | gałęzie muszą mieć zgodny typ |
| `[1, True]` | elementy listy muszą mieć jeden typ; użyj krotki, jeśli opisujesz różne pola |
| `1 ++ [2,3]` | `1 : [2,3]` lub `[1] ++ [2,3]` |
| `square -3` | ujemny argument zapisz jako `square (-3)` |
| `Int` dodany do `Double` | jawna konwersja, np. `fromIntegral n + x` |
| nieobsłużona pusta lista | dodaj przypadek `[]` |
| błędne wcięcia | wyrównaj definicje należące do tego samego bloku |

## Ściąga ze składni

```haskell
-- sygnatura i definicja
inc :: Int -> Int
inc x = x + 1

-- warunek
absolute x = if x >= 0 then x else -x

-- guards
sign x
  | x < 0     = -1
  | x == 0    = 0
  | otherwise = 1

-- wzorce list
isEmpty [] = True
isEmpty _  = False

-- definicja lokalna
squarePlusOne x = y + 1
  where
    y = x * x

-- lokalne wyrażenie
example = let x = 2 in x + 3

-- lambda
squares = map (\x -> x * x) [1..5]
```

## Ćwiczenia

Spróbuj rozwiązać je przed przeczytaniem odpowiedzi.

1. Jaka jest różnica między `f x y` i `f (x,y)`?
2. Oblicz `map (+1) (filter even [1..6])`.
3. Zapisz funkcję `maxTwo`, która zwraca większy z dwóch argumentów. Użyj `if`.
4. Zapisz rekurencyjną funkcję mnożącą elementy listy. Dla pustej listy przyjmij wynik `1`.
5. Wywnioskuj typ `pair x = (x, x)`.
6. Wyjaśnij, dlaczego `bad x = if x then 1 else "nie"` jest błędne.
7. Zapisz funkcję obliczającą sumę kwadratów nieparzystych liczb z listy.
8. Jaki wynik daje `take 3 (map (*2) [1..])` i dlaczego obliczenie się kończy?

## Odpowiedzi

1. Pierwszy zapis podaje argumenty kolejno; drugi podaje jedną krotkę. Wymagają różnych typów funkcji.
2. Najpierw `[2,4,6]`, następnie `[3,5,7]`.
3. Przykładowa definicja:

```haskell
maxTwo :: Ord a => a -> a -> a
maxTwo x y = if x >= y then x else y
```

4. Iloczyn pustej listy to element neutralny mnożenia:

```haskell
productList :: Num a => [a] -> a
productList []     = 1
productList (x:xs) = x * productList xs
```

5. `pair :: a -> (a, a)`. Oba pola zawierają wartość tego samego typu.
6. Warunek wymusza `x :: Bool`, ale problemem są różne typy gałęzi: liczba i `String`.
7. Przykładowa definicja:

```haskell
sumOddSquares :: [Int] -> Int
sumOddSquares xs = sum (map (\x -> x * x) (filter odd xs))
```

8. `[2,4,6]`. Dzięki leniwemu obliczaniu potrzebny jest tylko początek nieskończonej listy.

## Co powinno być jasne po przeczytaniu

- Dlaczego `=` definiuje wartość, a `==` ją porównuje.
- Jak przeczytać `Eq a => a -> a -> Bool`.
- Jak wywołać funkcję i kiedy użyć nawiasów.
- Jak rozdzielić dane wzorcami oraz warunkami.
- Jak definiować pomocnicze wartości przez `where` i `let`.
- Jak rozbić listę na `[]` i `x:xs`.
- Jak zastąpić prostą pętlę przez rekurencję, `map`, `filter` lub składanie funkcji.
- Jak sprawdzić typ i wczytać plik w GHCi.
