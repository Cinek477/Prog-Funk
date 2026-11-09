# 5. Collection Pipeline — proces z małych funkcji

[Spis wykładu 3](README.md) · Slajd 16

## Zadanie z wykładu

Z tekstu z imionami usuń jednoliterowe słowa, a pozostałe zapisz z wielkiej litery, oddzielone pojedynczymi spacjami.

```text
tomasz t bogdan anna Jerzy j maria
→ Tomasz Bogdan Anna Jerzy Maria
```

**Collection Pipeline** to sekwencja przekształceń: wynik jednego etapu jest wejściem następnego. Rozdzielenie etapów ułatwia sprawdzanie typów i znajdowanie błędów.

## Etap 1: podział tekstu na słowa

```haskell
words "tomasz t bogdan"
-- ["tomasz","t","bogdan"]
-- words :: String -> [String]
```

`words` rozpoznaje białe znaki, więc wielokrotne spacje i przejścia wiersza nie tworzą pustych słów. Nie jest parserem interpunkcji: np. przecinek zostaje częścią słowa.

## Etap 2: odrzucenie krótkich słów

```haskell
filter (\w -> length w > 1) ["tomasz","t","bogdan"]
-- ["tomasz","bogdan"]
```

Predykat przyjmuje String i zwraca Bool. Cały filtr ma typ `[String] -> [String]`.

## Etap 3: normalizacja liter

```haskell
import Data.Char (toUpper, toLower)

capitalize :: String -> String
capitalize [] = []
capitalize (x:xs) = toUpper x : map toLower xs
```

```haskell
capitalize "jERZY" -- "Jerzy"
map capitalize ["tomasz","bogdan"] -- ["Tomasz","Bogdan"]
```

`toUpper` i `toLower` działają na pojedynczych znakach. `map toLower` działa na całym ogonie tekstu. To prosty formatter, nie pełny model pisowni wszystkich nazwisk i imion.

## Etap 4: połączenie słów

Wersja ze slajdu:

```haskell
foldr1 (\w rest -> w ++ " " ++ rest) ["Tomasz","Bogdan"]
-- "Tomasz Bogdan"
```

**Pułapka:** po wejściu `"a b c"` filtr usunie wszystkie słowa, a `foldr1` dostanie `[]` i zgłosi błąd. Podobnie dla pustego tekstu.

Bezpieczna operacja biblioteczna:

```haskell
unwords ["Tomasz","Bogdan"] -- "Tomasz Bogdan"
unwords [] -- ""
-- unwords :: [String] -> String
```

## Całość w trzech zapisach

Najpierw wersja z nazwami etapów:

```haskell
formatNames :: String -> String
formatNames s =
  let tokens = words s
      longWords = filter (\w -> length w > 1) tokens
      normalized = map capitalize longWords
  in unwords normalized
```

Wersja z nawiasami:

```haskell
formatNames s = unwords (map capitalize (filter (\w -> length w > 1) (words s)))
```

Wersja przez złożenie:

```haskell
formatNames = unwords . map capitalize . filter (\w -> length w > 1) . words
```

To alternatywne definicje. W pliku wybierz jedną.

## Kontrola typów etapów

```text
String
  -- words --> [String]
  -- filter --> [String]
  -- map capitalize --> [String]
  -- unwords --> String
```

Jeżeli pomylisz kolejność i użyjesz `words` na `[String]`, typy wykryją problem. Część błędów logicznych, np. wybieranie `length w < 1`, nadal jest poprawna typowo — dlatego potrzebne są przykłady wejścia i oczekiwane wyniki.

## Przykłady brzegowe

| Wejście | Wynik poprawionej wersji |
|---|---|
| `""` | `""` |
| `"a b c"` | `""` |
| `"  aNNA   bOGDAN "` | `"Anna Bogdan"` |
| `"JAN"` | `"Jan"` |

## Kolejny pipeline: suma kwadratów dodatnich

```haskell
sumPositiveSquares :: [Int] -> Int
sumPositiveSquares = sum . map (^2) . filter (>0)
-- sumPositiveSquares [-2,0,3,4] = 25
```

Tutaj kolejność też ma znaczenie. Jeśli najpierw podniesiesz do kwadratu, liczby ujemne staną się dodatnie i mogą zostać zachowane przez filtr.
