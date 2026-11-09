# Wykład 2 — funkcje, listy, leniwość i rekurencja

[Wszystkie materiały](../README.md) · [Wykład 1](../w1/README.md)

Opracowanie `_MConverter.eu_fp-w2-min.md`. Poprawiono zniekształconą składnię po konwersji i dodano objaśnienia. Przykłady są niezależnymi fragmentami: alternatywnych definicji tej samej nazwy nie wklejaj razem do jednego modułu.

## Kolejność nauki

1. [Funkcje wielu argumentów](01-funkcje.md) — krotki, currying, aplikacja częściowa, sekcje, curry, uncurry i flip.
2. [Listy](02-listy.md) — struktura, operacje, koszt, list comprehensions i typowe pułapki.
3. [Leniwe wartościowanie](03-leniwosc.md) — nieścisłość, thunk, wymuszanie i listy nieskończone.
4. [Rekurencja](04-rekurencja.md) — schematy, akumulatory, ścisłość, Fibonacci i sortowanie.
5. [Pytania i ćwiczenia](05-pytania-i-cwiczenia.md) — krótkie definicje, przewidywanie wyników, rozwiązania.

Najważniejsza zależność: lista ma budowę rekurencyjną, więc naturalnie przetwarzamy ją rekurencją; leniwość pozwala obliczać tylko potrzebny fragment, ale wymaga uwagi przy akumulatorach.

Nie powtarzam pomiarów czasu i pamięci ze slajdów jako ogólnych gwarancji: zależą od implementacji, konfiguracji, optymalizacji i danych. Podane koszty dotyczą standardowego modelu list i opisanych algorytmów.

