# Moduły w praktyce: bezpieczne saldo

## Oddziel reguły od implementacji

Załóżmy, że na koncie nie może być ujemnego salda, a wpłata ma być dodatnia. Sam typ `Int` pozwala na dowolną liczbę; regułę chroni **interfejs modułu**, który chowa konstruktor i oferuje tylko bezpieczne operacje.

Zapisz w pliku `Balance.hs`:

```haskell
module Balance (Balance, empty, amount, deposit, withdraw) where

newtype Balance = Balance Integer

empty :: Balance
empty = Balance 0

amount :: Balance -> Integer
amount (Balance n) = n

deposit :: Integer -> Balance -> Maybe Balance
deposit x (Balance n)
  | x > 0     = Just (Balance (n + x))
  | otherwise = Nothing

withdraw :: Integer -> Balance -> Maybe Balance
withdraw x (Balance n)
  | 0 < x && x <= n = Just (Balance (n - x))
  | otherwise       = Nothing
```

Kod z innego modułu może wywołać `deposit 30 empty`, ale nie może zapisać `Balance (-10)`. Wewnątrz modułu konstruktor jest dostępny. Nie eksportujemy pola rekordowego pozwalającego aktualizować saldo; `amount` jest osobnym odczytem.

## Użycie z innego pliku

Zapisz obok jako `Main.hs`:

```haskell
module Main where

import qualified Balance as B

main :: IO ()
main =
  case B.deposit 30 B.empty of
    Nothing -> putStrLn "Wplata odrzucona"
    Just b  -> do
      print (B.amount b)
      case B.withdraw 40 b of
        Nothing -> putStrLn "Wyplata odrzucona"
        Just b2 -> print (B.amount b2)
```

Uruchom w katalogu zawierającym oba pliki: `runghc Main.hs`. Zobaczysz `30` i informację o odrzuconej wypłacie. Zmiana kwoty wypłaty na 10 da na końcu `20`. Nazwa `B.amount` jest kwalifikowana: prefiks odróżnia ją od ewentualnej lokalnej funkcji `amount`.

## Eksport i import to dwie osobne decyzje

- `module Balance (Balance, empty) where` eksportuje nazwę typu oraz wartość `empty`, bez konstruktora.
- `module Balance (Balance(..), empty) where` eksportuje też konstruktor. Dla tego przykładu zniszczyłoby to gwarancję salda nieujemnego.
- `import Balance (Balance, empty)` wybiera, których spośród wyeksportowanych nazw używa klient. Nie pozwala odzyskać ukrytego konstruktora.
- `import qualified Balance as B` zmienia sposób odwoływania się do nazw. Samo `qualified` niczego nie eksportuje.

To jest **abstrakcyjny** typ danych: użytkownik korzysta z publicznych operacji. `newtype Balance = Balance Integer` używa natomiast konstrukcji typu **algebraicznego**. To dwa różne aspekty tego samego przykładu.
