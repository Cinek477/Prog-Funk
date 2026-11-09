# 6. Narzędzia i mechanizmy Haskella — co to jest?

## Język a narzędzia

**Haskell** to język programowania. **GHC** to implementacja tego języka, obejmująca kompilator i powiązane narzędzia. **GHCi** to środowisko interaktywne. Nazwy te nie oznaczają tego samego.

| Nazwa | Co to jest? | Do czego służy? |
|---|---|---|
| **GHC** (Glasgow Haskell Compiler) | kompilator Haskella | sprawdza kod i typy oraz kompiluje program do postaci wykonywalnej |
| **GHCi** | interaktywne środowisko związane z GHC | pozwala wpisywać wyrażenia, sprawdzać typy i wczytywać moduły bez ręcznego budowania programu przy każdej próbie |
| **REPL** (Read–Eval–Print Loop) | sposób interaktywnej pracy | odczytaj wyrażenie, oblicz, pokaż wynik, powtórz; GHCi jest przykładem REPL |
| **runghc** | narzędzie do uruchamiania kodu Haskella | uruchamia plik `.hs` bez osobnego ręcznego wywołania kompilatora |
| **GHCup** | instalator i menedżer narzędzi | pomaga instalować i wybierać wersje m.in. GHC oraz innych narzędzi ekosystemu |
| **Cabal** | biblioteka i narzędzie związane z budowaniem pakietów Haskella | plik `.cabal` opisuje pakiet, a `cabal` pozwala m.in. budować projekty i obsługiwać zależności |
| **Stack** | narzędzie do pracy z projektami | organizuje budowanie, zależności i dobór środowiska kompilacji |
| **HLS** (Haskell Language Server) | serwer językowy dla edytora | dostarcza m.in. informacje o typach i diagnostykę w edytorze |
| **VS Code** | edytor kodu | służy do pisania kodu; rozszerzenie Haskell może współpracować z HLS |
| **Prelude** | standardowy moduł importowany domyślnie w zwykłym kodzie | udostępnia m.in. `map`, `filter`, `sum`, `not`, podstawowe typy i operatory |

Kompilator przetwarza kod przed uruchomieniem programu. Środowisko interaktywne pozwala szybko eksperymentować. GHCi również sprawdza typy — praca interaktywna nie oznacza dynamicznego typowania.

Przykładowe zastosowania:

```text
ghc Main.hs -o program   — zbuduj program
runghc Main.hs           — uruchom plik
ghci                    — rozpocznij pracę interaktywną
```

W GHCi wpisujesz np. `2 + 3`, `:type map`, `:load Main.hs` i `:reload`.

## Najważniejsze mechanizmy języka

### Czystość i przezroczystość referencyjna

Czysta funkcja oblicza wynik z argumentów bez obserwowalnych efektów ubocznych. Wyrażenie można zastąpić jego wartością bez zmiany znaczenia programu — to przezroczystość referencyjna.

```haskell
double x = 2 * x
-- double 4 można zastąpić przez 8
```

Haskell pozwala wykonywać efekty, np. wypisywanie tekstu, ale opisuje je jawnie w typach, np. przez `IO`. „Czysto funkcyjny” nie oznacza „nie może czytać plików”.

### Niezmienność wartości

Wiązanie `x = 5` nadaje nazwę wartości; nie tworzy zmiennej aktualizowanej przypisaniami. Nowy wynik powstaje przez obliczenie nowej wartości. Wewnętrzne implementacje mogą używać mutacji, ale nie zmienia to znaczenia zwykłych czystych definicji.

### Statyczne typowanie i inferencja typów

**Statyczne typowanie:** zgodność typów jest sprawdzana przed wykonaniem danego kodu.

**Inferencja typów:** kompilator potrafi wywnioskować typ na podstawie definicji, więc często nie trzeba go zapisywać ręcznie.

```haskell
square x = x * x
-- wywnioskowany typ: Num a => a -> a
```

Brak jawnej sygnatury nie oznacza braku typu. Typ nie jest zgadywany na podstawie pierwszego uruchomienia funkcji.

### Polimorfizm i klasy typów

**Polimorfizm parametryczny:** ta sama definicja działa dla różnych typów bez wymagania szczególnych operacji na nich.

```haskell
identity :: a -> a
identity x = x
```

**Klasy typów:** określają dostępne operacje dla typów. Ograniczenie `Eq a` wymaga możliwości sprawdzania równości wartości typu `a`.

```haskell
same :: Eq a => a -> a -> Bool
same x y = x == y
```

Klasy typów umożliwiają przeciążanie operacji: `(==)` ma implementacje dla różnych typów. Nie należy utożsamiać ich z klasami obiektowymi i dziedziczeniem obiektów.

### Funkcje jako wartości i funkcje wyższego rzędu

**Funkcje pierwszorzędne:** funkcje można przekazywać, zwracać i przechowywać jak inne wartości.

**Funkcja wyższego rzędu:** przyjmuje funkcję jako argument lub zwraca funkcję.

```haskell
map (\x -> x + 1) [1,2,3] -- [2,3,4]
```

`map` jest funkcją wyższego rzędu, ponieważ otrzymuje funkcję do zastosowania na elementach listy.

### Lambdy i domknięcia

**Lambda** to zapis funkcji anonimowej: `\x -> x + 1`.

**Domknięcie** to funkcja wraz z dostępem do wartości z otaczającego zakresu.

```haskell
makeAdder n = \x -> n + x
-- makeAdder 5 zwraca funkcję, która dodaje zachowane n = 5
```

### Currying i częściowa aplikacja

**Currying** oznacza przedstawienie funkcji wielu argumentów jako funkcji jednego argumentu, która zwraca kolejną funkcję.

```haskell
add :: Int -> Int -> Int
add x y = x + y
```

Typ czytamy jako `Int -> (Int -> Int)`.

**Częściowa aplikacja** to podanie części argumentów i uzyskanie funkcji czekającej na pozostałe:

```haskell
addTen :: Int -> Int
addTen = add 10
-- addTen 3 = 13
```

Currying opisuje postać funkcji, a częściowa aplikacja jest sposobem jej użycia.

### Leniwe wartościowanie

Obliczenia są wykonywane w miarę zapotrzebowania na ich wynik. W typowym modelu wykonania GHC odroczone obliczenie jest reprezentowane przez **thunk**; po obliczeniu jego wynik może być współdzielony.

```haskell
take 3 [1..] -- [1,2,3]
```

Nie trzeba obliczać całej nieskończonej listy. Leniwość nie oznacza wykonywania wszystkiego równolegle ani automatycznej oszczędności pamięci.

### Dopasowanie wzorców

Wybiera równanie funkcji lub gałąź `case` na podstawie struktury danych. Może też rozpakować dane i nadać nazwy ich częściom.

```haskell
isEmpty [] = True
isEmpty (_:_) = False
```

Pierwszy pasujący wzorzec wygrywa. Wzorzec `x:xs` pasuje tylko do niepustej listy.

### Rekurencja i rekurencja ogonowa

**Rekurencja:** funkcja wywołuje samą siebie.

```haskell
sumList [] = 0
sumList (x:xs) = x + sumList xs
```

**Rekurencja ogonowa:** wynik wywołania rekurencyjnego jest bezpośrednio wynikiem danej gałęzi — po powrocie nie pozostaje dodatkowe działanie.

```haskell
sumAcc acc [] = acc
sumAcc acc (x:xs) = sumAcc (acc + x) xs
```

`sumList` nie jest ogonowa, bo po wywołaniu pozostaje dodawanie. `sumAcc` jest ogonowa, ale w leniwym Haskellu sam ten fakt nie gwarantuje stałego zużycia pamięci: akumulator może zawierać odłożone dodawania. W praktyce do ścisłego składania skończonej listy często służy `foldl'` z `Data.List`.

### List comprehensions i składanie funkcji

**List comprehension** tworzy listę na podstawie generatorów i warunków:

```haskell
[x * x | x <- [1..5], odd x] -- [1,9,25]
```

**Składanie funkcji** łączy przekształcenia: `(f . g) x = f (g x)`. Na przykład `sum . filter even` najpierw wybiera liczby parzyste, a następnie je sumuje.

### Typy algebraiczne — podstawowe rozpoznanie pojęcia

Pozwalają opisywać własne dane przez konstruktory i ich pola.

```haskell
data Shape = Circle Double | Rectangle Double Double
```

Wartość typu `Shape` jest kołem z promieniem albo prostokątem z dwoma wymiarami. `|` rozdziela warianty. Konstruktory zaczynają się wielką literą i mogą być używane we wzorcach.

```haskell
area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rectangle a b) = a * b
```

To krótki dodatek pojęciowy; pełne definiowanie typów jest kolejnym etapem nauki.

## Krótkie odpowiedzi do powtórzenia

| Pytanie | Odpowiedź |
|---|---|
| Czym jest GHC? | Kompilatorem Haskella: sprawdza i tłumaczy kod na program wykonywalny. |
| Czym jest GHCi? | Interaktywnym środowiskiem do obliczania wyrażeń, sprawdzania typów i wczytywania kodu Haskella. |
| Czym jest GHCup? | Narzędziem do instalowania i zarządzania narzędziami Haskella. |
| Czy Haskell jest statycznie typowany? | Tak. Inferencja pozwala pomijać część jawnych sygnatur, ale typy nadal są sprawdzane. |
| Co znaczy „leniwie”? | Wyrażenie jest obliczane dopiero w zakresie potrzebnym do uzyskania wyniku. |
| Co znaczy „czysta funkcja”? | Wynik zależy od argumentów, a obliczenie nie ma obserwowalnych efektów ubocznych. |
| Co to funkcja wyższego rzędu? | Funkcja przyjmująca lub zwracająca funkcję. |
| Co to currying? | Zapis wielu argumentów jako kolejnych funkcji jednoargumentowych. |
| Co to pattern matching? | Rozpoznawanie struktury danych i wybieranie pasującego przypadku. |
| Co to Prelude? | Domyślnie importowany standardowy moduł z podstawowymi definicjami. |
| Czym różni się kompilator od edytora? | Kompilator przetwarza kod, a edytor służy do jego pisania. |

