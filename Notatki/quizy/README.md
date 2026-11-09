# Quizy interaktywne

Otwórz [index.html](index.html) w przeglądarce (np. dwuklikiem w Eksploratorze).

- 337 zadań: 77 do wykładu 1, 164 do wykładu 2 i 96 do wykładu 3. Łącznie 319 zadań z kodem, w tym 65 z uzupełnianiem luk.
- Osobne zestawy wykładów lub zestaw mieszany; 10, 20, 30, 50, 100 albo wszystkie dostępne pytania.
- Filtr: zadania z kodem (domyślnie), tylko uzupełnianie kodu lub pełna baza z pytaniami pojęciowymi.
- Tryb nauki: po sprawdzeniu pytania pojawiają się rozwiązanie i wyjaśnienie.
- Tryb kartkówki: rozwiązania są widoczne dopiero po zakończeniu.
- Wybór jednej lub wielu odpowiedzi oraz uzupełnianie kodu przez listy wyboru.
- Losowanie pytań i odpowiedzi; powtórka błędnych i pominiętych pytań.
- Zapis bieżącej sesji w pamięci przeglądarki, jeśli jej ustawienia pozwalają na localStorage dla lokalnych plików.

Każde pytanie to 1 punkt; zadania wieloczęściowe wymagają poprawnych wszystkich części. Pytania inspirowano notatkami i dostarczonymi zdjęciami, nie kopiowano bezkrytycznie zaznaczonych na nich odpowiedzi. Nieczytelne fragmenty zastąpiono jednoznacznymi przykładami.

Quiz działa bez internetu i nie wysyła odpowiedzi. Na innym urządzeniu trzeba otworzyć tam ten sam plik HTML. Układ dostosowuje się do wąskiego ekranu, ale działania na fizycznym telefonie nie zweryfikowano.


## Intensywna powtórka

1. Wybierz temat **Inferencja typów**, tryb nauki i rundę 20 pytań.
2. Następnie wybierz **Uzupełnianie kodu** i rundę 20 pytań.
3. Przejdź do **Leniwości i pułapek**, a potem **List i rekurencji**.
4. Na końcu ustaw wszystkie tematy, tryb kartkówki i 30 pytań. Powtórz błędne i pominięte.

Nie musisz przechodzić całej bazy jednym ciągiem. Po błędzie przeczytaj wyjaśnienie i spróbuj samodzielnie odtworzyć rozwiązanie.

## Weryfikacja

85 nowych wyrażeń sprawdzono przez obliczenie w GHCi, a 30 nowych pytań o typy porównano z inferencją GHCi. Sprawdzono też klucze odpowiedzi, renderowanie pytań w modelu dokumentu, punktowanie i kombinacje filtrów. Nie jest to test wizualny w prawdziwej przeglądarce ani na fizycznym telefonie.

## Wykład 3

Wybierz „Wykład 3” w polu Zestaw. Dodano 96 pytań: 55 obliczeń sprawdzonych w GHCi, 15 pytań o typy, 20 zadań z uzupełnianiem kodu i 6 dodatkowych pytań o pułapki. Tematy obejmują lambdy, funkcje jako argumenty, złożenie, operatory aplikacji, map/filter, foldy, zipWith/concat oraz pipeline. Osobne filtry „Foldy” i „Pipeline i składanie” pomagają skupić się na nowym materiale.

[Materiały do wykładu 3](../w3/README.md).
