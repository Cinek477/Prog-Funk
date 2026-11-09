# 7. Ściąga — wykład 3

[Spis wykładu 3](README.md)

## Typy dla list

```haskell
map     :: (a -> b) -> [a] -> [b]
filter  :: (a -> Bool) -> [a] -> [a]
foldr   :: (a -> b -> b) -> b -> [a] -> b
foldl   :: (b -> a -> b) -> b -> [a] -> b
zip     :: [a] -> [b] -> [(a,b)]
unzip   :: [(a,b)] -> ([a],[b])
zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
concat  :: [[a]] -> [a]
(.)     :: (b -> c) -> (a -> b) -> a -> c
($)     :: (a -> b) -> a -> b
```

## Równania do zapamiętania

```text
(f . g) x = f (g x)
f $ x = f x
foldr f z [a,b,c] = f a (f b (f c z))
foldl f z [a,b,c] = f (f (f z a) b) c
```

## Szybkie przykłady

| Cel | Zapis |
|---|---|
| Kwadraty | `map (^2)` |
| Parzyste | `filter even` |
| Suma kwadratów | `sum . map (^2)` |
| Suma kwadratów dodatnich | `sum . map (^2) . filter (>0)` |
| Długości słów | `map length . words` |
| Spłaszczenie | `concat` |
| Suma par elementów | `zipWith (+)` |
| Iloczyn listy | `foldr (*) 1` |
| Długość przez fold | `foldr (\_ acc -> 1+acc) 0` |
| Odwrócenie przez akumulator | `foldl (\acc x -> x:acc) []` |
| Zastosuj funkcje do 2 | `map ($2)` |

## Pułapki

- `map even` daje Bool dla każdego elementu; `filter even` zachowuje liczby.
- `f . g` to funkcja; `f $ x` to jej zastosowanie do argumentu.
- W `foldr` krok dostaje element i wynik ogona; w `foldl` akumulator i element.
- Kierunek folda ma znaczenie przy odejmowaniu, dzieleniu i budowaniu struktur.
- `foldr1` i `foldl1` nie obsługują `[]`.
- `foldl'` i `$!` wymuszają do WHNF, nie w głąb całej struktury.
- `foldr` czasem działa z listą nieskończoną, ale nie dla każdej funkcji kroku.
- `zip` i `zipWith` obcinają wynik do krótszej listy.
- `concat` usuwa jedną warstwę list, nie wszystkie naraz.
- Nazwy `sum`, `map` i `filter` istnieją w Prelude. Przy pisaniu własnych wersji użyj np. końcówki `Own`, aby uniknąć konfliktów.
- Składanie czytaj od prawej do lewej i sprawdzaj typ na każdej granicy.

## Słownik krótkich odpowiedzi

**Funkcja wyższego rzędu:** przyjmuje lub zwraca funkcję.

**Lambda:** anonimowa funkcja, np. `\x -> x+1`.

**Domknięcie:** funkcja wraz z dostępem do środowiska, np. zachowanego kroku h.

**Predykat:** funkcja zwracająca Bool.

**Fold:** opis rekurencyjnego składania przez funkcję kroku i przypadek bazowy.

**Pipeline:** proces z kolejnych przekształceń kolekcji.

**DRY:** wspólny schemat zapisujemy raz, a zmienne zachowanie przekazujemy jako parametr.
