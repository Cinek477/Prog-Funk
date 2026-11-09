# Wykład 3 — funkcje wyższego rzędu i przetwarzanie kolekcji

[Wszystkie wykłady](../README.md) · [Wykład 2](../w2/README.md) · [Quizy](../quizy/index.html)

Materiały opracowane na podstawie `fp-w3.pdf` (17 slajdów, ułożonych na 3 stronach PDF). Wyjaśnienia i ćwiczenia są rozszerzeniem treści slajdów, bez historii i spraw organizacyjnych.

## Od czego zacząć?

| Kolejność | Materiał | Po przeczytaniu potrafisz… |
|---|---|---|
| 1 | [Funkcje wyższego rzędu, lambdy, domknięcia](01-funkcje-wyzszego-rzedu.md) | przekazać funkcję jako argument i odczytać jej typ |
| 2 | [Składanie funkcji, operatory . i $](02-skladanie-i-aplikacja.md) | odróżnić tworzenie funkcji od jej wywołania |
| 3 | [map, filter, zipWith i concat](03-przetwarzanie-list.md) | dobrać operację do przekształcenia danych |
| 4 | [foldr, foldl i foldl\'](04-foldy.md) | ręcznie rozwinąć fold i dobrać akumulator |
| 5 | [Collection Pipeline — przykład krok po kroku](05-pipeline.md) | złożyć cały proces i sprawdzić przypadki brzegowe |
| 6 | [Ćwiczenia i rozwiązania](06-cwiczenia.md) | przećwiczyć typy, wyniki i uzupełnianie kodu |
| Powtórka | [Ściąga](07-sciaga.md) | szybko przypomnieć typy, kolejność argumentów i pułapki |

## Najważniejsza idea

Zamiast pisać nową rekurencję dla każdego zadania, przekazujemy różnicę jako funkcję:

```haskell
sumSquares xs = sum (map (^2) xs)
```

`map` odpowiada za przechodzenie listy, `(^2)` za pojedynczą zmianę, a `sum` za zebranie wyniku. Dalej nauczysz się zapisywać i czytać takie procesy.

## Gotowy kod

[Przyklady.hs](Przyklady.hs) zawiera działające definicje oraz sprawdzane przykłady. W terminalu, z głównego folderu projektu:

```text
runghc Notatki/w3/Przyklady.hs
```

W GHCi:

```text
:load Notatki/w3/Przyklady.hs
:type sumWith
:type foldrOwn
formatNames "tomasz t bogdan anna"
main
```

Przykłady w rozdziałach są niezależne; nie kopiuj alternatywnych definicji tej samej nazwy razem. Typy funkcji bibliotecznych podajemy głównie w wersji dla list. GHCi może pokazać szerszy typ z `Foldable`, np. dla `foldr`, `sum` czy `concat` — nie jest to sprzeczność.

## Plan nauki na około godzinę

- 15 minut: rozdziały 1–2; rozpisz ręcznie dwa wywołania i dwa typy.
- 20 minut: `map`/`filter` i foldy; koniecznie porównaj odejmowanie w `foldr` i `foldl`.
- 10 minut: prześledź formatowanie tekstu na kolejnych etapach.
- 15 minut: rozwiąż ćwiczenia bez podglądania, potem zrób quiz z wyborem „Wykład 3”.
