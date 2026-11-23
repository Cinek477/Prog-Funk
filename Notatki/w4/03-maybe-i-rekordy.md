# Maybe, rekordy i brak wyniku

## Najpierw ustal, co może pójść nie tak

Funkcja szukająca użytkownika może trafić na znany identyfikator albo nie znaleźć go w danych. Jeżeli nie ma użytkownika, nie istnieje też miasto do odczytania. Zamiast wymyślać wartości zastępcze, modelujemy brak przez `Maybe`.

```haskell
data User = User { userName :: String, city :: Maybe String }
  deriving (Show, Eq)

users :: [(Int, User)]
users = [(1, User "Ada" (Just "Krakow")), (2, User "Ola" Nothing)]

findCity :: Int -> Maybe String
findCity key = case lookup key users of
  Nothing -> Nothing
  Just u  -> city u

moveTo :: String -> User -> User
moveTo place u = u { city = Just place }
```

| Wyrażenie | Wynik | Dlaczego? |
| --- | --- | --- |
| `lookup 1 users` | `Just (User "Ada" …)` | Użytkownik istnieje. |
| `findCity 1` | `Just "Krakow"` | Po wyszukaniu odczytujemy miasto. |
| `findCity 2` | `Nothing` | Użytkownik istnieje, ale nie ma zapisanego miasta. |
| `findCity 9` | `Nothing` | Nie ma użytkownika o tym identyfikatorze. |

`lookup` z Prelude przegląda listę par i zwraca **pierwszą** pasującą wartość. Tutaj `findCity` celowo sprowadza dwa różne przypadki do tego samego wyniku. Jeżeli musisz rozróżnić brak użytkownika od braku miasta, użyj odrębnych konstruktorów, np. `data CityResult = NoUser | NoCity | FoundCity String`.

## Jak czytać selektor i aktualizację

`city :: User -> Maybe String` to funkcja wybierająca pole, więc `city u` jest zwykłą aplikacją. W zapisie `u { city = Just place }` tworzysz nową wersję użytkownika; poprzednia wartość `u` się nie zmienia.

Jeżeli nie każdy wariant posiada pole, selektor może być częściowy:

```haskell
data Account = Guest | Member { email :: String }

safeEmail :: Account -> Maybe String
safeEmail Guest      = Nothing
safeEmail (Member e) = Just e
```

`email Guest` ma poprawny typ, ale zgłasza błąd podczas obliczania wyniku. `safeEmail Guest` daje `Nothing`. To dobry przykład różnicy między błędem typu a błędem wykonania.

## Just Nothing nie oznacza tego samego co Nothing

Przy typie `Maybe (Maybe String)` odczytujesz konstruktory od zewnątrz do środka. `Nothing` oznacza brak wyniku pierwszego etapu, `Just Nothing` — że pierwszy etap się udał, lecz drugi nie dał wartości. `Just (Just "Krakow")` oznacza sukces obu.
