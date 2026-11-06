"""Textele de pe tabul "Noțiuni teoretice", pentru fiecare cifru, in romana / engleza / rusa.

Format: o linie care incepe cu "# " este un titlu; o linie indentata cu 4 spatii este o formula.
"""

TEORIE = {
    "cezar": {
        "ro": """
# Ce este?
Cifrul lui Cezar este unul dintre cele mai vechi sisteme de criptare simetrice. Se spune că Iulius Cezar îl folosea, cu deplasarea 3, pentru mesajele militare.

# Cum funcționează
Literele alfabetului sunt numerotate: A=0, B=1, ..., Z=25. Cheia k este numărul de poziții cu care se mută fiecare literă. La final se revine la începutul alfabetului (de aceea „mod 26”).
    Criptare:    C = (P + k) mod 26
    Decriptare:  P = (C - k) mod 26

# Exemplu cu k = 3
Fiecare literă înaintează 3 poziții: A devine D, B devine E, ..., X devine A, Y devine B, Z devine C.
    ATAC  ->  DWDF

# Cât de sigur este?
Există doar 26 de chei posibile. Un atac cu forță brută le încearcă pe toate și alege varianta care are sens. Sistemul este monoalfabetic: aceeași literă este criptată mereu la fel, deci frecvențele literelor rămân vizibile în textul criptat.

# Cum folosești aplicația
Pe tabul „Criptarea” scrii textul și cheia k, apoi apeși „Criptează”. Pe „Decriptarea” faci invers. Pe „Atac cu forță brută” lipești un text criptat și aplicația încearcă toate cele 26 de chei.
""",
        "en": """
# What is it?
The Caesar cipher is one of the oldest symmetric encryption systems. Julius Caesar is said to have used it, with a shift of 3, for military messages.

# How it works
The letters of the alphabet are numbered: A=0, B=1, ..., Z=25. The key k is the number of positions each letter is moved. At the end of the alphabet you wrap around to the beginning (that is why "mod 26").
    Encryption:  C = (P + k) mod 26
    Decryption:  P = (C - k) mod 26

# Example with k = 3
Every letter moves forward 3 positions: A becomes D, B becomes E, ..., X becomes A, Y becomes B, Z becomes C.
    ATTACK  ->  DWWDFN

# How secure is it?
There are only 26 possible keys. A brute-force attack tries all of them and picks the result that makes sense. The system is monoalphabetic: the same letter is always encrypted the same way, so letter frequencies stay visible in the encrypted text.

# How to use the app
On the "Encryption" tab you type the text and the key k, then press "Encrypt". "Decryption" works the other way round. On the "Brute-force attack" tab you paste an encrypted text and the app tries all 26 keys.
""",
        "ru": """
# Что это?
Шифр Цезаря — одна из старейших симметричных систем шифрования. Говорят, что Юлий Цезарь использовал его со сдвигом 3 для военных сообщений.

# Как это работает
Буквы латинского алфавита нумеруются: A=0, B=1, ..., Z=25. Ключ k — число позиций, на которое сдвигается каждая буква. В конце алфавита счёт возвращается к началу (поэтому «mod 26»).
    Шифрование:   C = (P + k) mod 26
    Расшифровка:  P = (C - k) mod 26

# Пример при k = 3
Каждая буква сдвигается на 3 позиции вперёд: A → D, B → E, ..., X → A, Y → B, Z → C.
    ATTACK  ->  DWWDFN

# Насколько это надёжно?
Возможных ключей всего 26. Атака полным перебором проверяет их все и выбирает вариант, имеющий смысл. Система моноалфавитная: одна и та же буква всегда шифруется одинаково, поэтому частоты букв остаются видны в шифртексте.

# Как пользоваться приложением
На вкладке «Шифрование» введите текст и ключ k, затем нажмите «Зашифровать». «Расшифровка» работает наоборот. На вкладке «Атака полным перебором» вставьте шифртекст — приложение проверит все 26 ключей.
""",
    },
    "cezar_cheie": {
        "ro": """
# Ce este?
Cezar cu cheie este o variantă mai puternică a cifrului Cezar. Alfabetul de criptare nu mai este simplu A, B, C, ..., ci începe cu un cuvânt-cheie, iar apoi este deplasat cu k poziții.

# Cum construiești alfabetul
1) Scrii cuvântul-cheie fără litere repetate.
2) Adaugi restul literelor, în ordine alfabetică.
3) Litera cu numărul i din alfabetul normal se înlocuiește cu litera de pe poziția (i + k) din alfabetul nou.
Exemplu pentru cuvântul CODE și k = 0:
    Normal:   A B C D E F G H I J K L M ...
    Criptat:  C O D E A B F G H I J K L ...
    ATAC  ->  CTCD

# Formule
Dacă alfabetul nou este S (un șir de 26 de litere):
    Criptare:    C = S[(P + k) mod 26]
    Decriptare:  P = (poziția lui C în S - k) mod 26

# Cât de sigur este?
Sunt 26! (aproximativ 4 · 10^26) alfabete posibile, așa că forța brută pură nu mai are sens. Atacul de pe ultimul tab încearcă însă cuvintele-cheie pe care le bănuiești (de exemplu numele unei persoane), fiecare cu toate cele 26 de deplasări.

# Cum folosești aplicația
Scrii cuvântul-cheie și numărul k, apoi apeși „Criptează”. La atac, scrii în câmp mai multe cuvinte bănuite, despărțite prin virgulă (de exemplu: ion,maria,code).
""",
        "en": """
# What is it?
Caesar with a key is a stronger variant of the Caesar cipher. The encryption alphabet is no longer plain A, B, C, ... but starts with a keyword and is then shifted by k positions.

# How to build the alphabet
1) Write the keyword without repeated letters.
2) Add the remaining letters in alphabetical order.
3) The letter with number i in the normal alphabet is replaced by the letter at position (i + k) of the new alphabet.
Example for the keyword CODE and k = 0:
    Normal:     A B C D E F G H I J K L M ...
    Encrypted:  C O D E A B F G H I J K L ...
    ATTACK  ->  CTTCDJ

# Formulas
If the new alphabet is S (a string of 26 letters):
    Encryption:  C = S[(P + k) mod 26]
    Decryption:  P = (position of C in S - k) mod 26

# How secure is it?
There are 26! (about 4 · 10^26) possible alphabets, so pure brute force makes no sense. The attack on the last tab instead tries the keywords you suspect (for example a person's name), each with all 26 shifts.

# How to use the app
Type the keyword and the number k, then press "Encrypt". For the attack, type several guessed words in the field, separated by commas (for example: ion,mary,code).
""",
        "ru": """
# Что это?
Шифр Цезаря с ключом — усиленный вариант шифра Цезаря. Алфавит шифрования уже не простой A, B, C, ..., а начинается с ключевого слова и затем сдвигается на k позиций.

# Как построить алфавит
1) Запишите ключевое слово без повторяющихся букв.
2) Добавьте остальные буквы в алфавитном порядке.
3) Буква с номером i обычного алфавита заменяется буквой на позиции (i + k) нового алфавита.
Пример для слова CODE и k = 0:
    Обычный:   A B C D E F G H I J K L M ...
    Шифр:      C O D E A B F G H I J K L ...
    ATTACK  ->  CTTCDJ

# Формулы
Если новый алфавит — S (строка из 26 букв):
    Шифрование:   C = S[(P + k) mod 26]
    Расшифровка:  P = (позиция C в S - k) mod 26

# Насколько это надёжно?
Возможных алфавитов 26! (около 4 · 10^26), поэтому чистый перебор бессмыслен. Атака на последней вкладке проверяет ключевые слова, которые вы предполагаете (например, имя человека), каждое со всеми 26 сдвигами.

# Как пользоваться приложением
Введите ключевое слово и число k, затем нажмите «Зашифровать». Для атаки впишите в поле несколько предполагаемых слов через запятую (например: ion,mary,code).
""",
    },
    "afin": {
        "ro": """
# Ce este?
Cifrul afin generalizează cifrul Cezar: litera nu doar se mută, ci mai întâi se înmulțește cu o cheie a. Cheia este o pereche de numere (a, b).

# Formule (literele sunt numerotate A=0, ..., Z=25)
    Criptare:    C = (a · P + b) mod 26
    Decriptare:  P = a^-1 · (C - b) mod 26
Aici a^-1 este inversul lui a modulo 26, adică numărul x cu a · x = 1 (mod 26).

# Ce valori poate avea a?
Pentru ca decriptarea să existe, a trebuie să fie prim cu 26 (cel mai mare divizor comun al lor este 1). Valorile permise sunt:
    1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
Cheia b poate fi orice număr de la 0 la 25.

# Exemplu cu a = 5, b = 8
Litera A (0) devine 5·0+8 = 8, adică I. Litera T (19) devine 5·19+8 = 103, iar 103 mod 26 = 25, adică Z.
    ATAC  ->  IZIS
Inversul lui 5 modulo 26 este 21, pentru că 5 · 21 = 105 = 4·26 + 1.

# Cât de sigur este?
Există doar 12 · 26 = 312 chei posibile. Un atac cu forță brută le încearcă pe toate foarte repede. Pentru a = 1 cifrul afin devine cifrul Cezar.

# Cum folosești aplicația
Completezi a și b, apoi apeși „Criptează”. Dacă a nu este prim cu 26, aplicația te anunță. Pe tabul de atac vezi toate cele 312 variante.
""",
        "en": """
# What is it?
The affine cipher generalizes the Caesar cipher: a letter is not only moved, it is first multiplied by a key a. The key is a pair of numbers (a, b).

# Formulas (letters are numbered A=0, ..., Z=25)
    Encryption:  C = (a · P + b) mod 26
    Decryption:  P = a^-1 · (C - b) mod 26
Here a^-1 is the inverse of a modulo 26, that is the number x with a · x = 1 (mod 26).

# Which values can a have?
For decryption to exist, a must be coprime with 26 (their greatest common divisor is 1). The allowed values are:
    1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
Key b can be any number from 0 to 25.

# Example with a = 5, b = 8
The letter A (0) becomes 5·0+8 = 8, which is I. The letter T (19) becomes 5·19+8 = 103, and 103 mod 26 = 25, which is Z.
    ATTACK  ->  IZZISG
The inverse of 5 modulo 26 is 21, because 5 · 21 = 105 = 4·26 + 1.

# How secure is it?
There are only 12 · 26 = 312 possible keys. A brute-force attack tries them all very quickly. For a = 1 the affine cipher becomes the Caesar cipher.

# How to use the app
Fill in a and b, then press "Encrypt". If a is not coprime with 26, the app tells you. On the attack tab you see all 312 candidates.
""",
        "ru": """
# Что это?
Аффинный шифр обобщает шифр Цезаря: буква не только сдвигается, но сначала умножается на ключ a. Ключ — пара чисел (a, b).

# Формулы (буквы нумеруются A=0, ..., Z=25)
    Шифрование:   C = (a · P + b) mod 26
    Расшифровка:  P = a^-1 · (C - b) mod 26
Здесь a^-1 — число, обратное a по модулю 26, то есть число x, для которого a · x = 1 (mod 26).

# Какие значения может иметь a?
Чтобы расшифровка существовала, a должно быть взаимно простым с 26 (их наибольший общий делитель равен 1). Допустимые значения:
    1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
Ключ b может быть любым числом от 0 до 25.

# Пример при a = 5, b = 8
Буква A (0) превращается в 5·0+8 = 8, то есть I. Буква T (19) превращается в 5·19+8 = 103, а 103 mod 26 = 25, то есть Z.
    ATTACK  ->  IZZISG
Число, обратное 5 по модулю 26, равно 21, так как 5 · 21 = 105 = 4·26 + 1.

# Насколько это надёжно?
Возможных ключей всего 12 · 26 = 312. Атака полным перебором проверяет их все очень быстро. При a = 1 аффинный шифр превращается в шифр Цезаря.

# Как пользоваться приложением
Заполните a и b, затем нажмите «Зашифровать». Если a не взаимно просто с 26, приложение сообщит об этом. На вкладке атаки видны все 312 вариантов.
""",
    },
    "vigenere": {
        "ro": """
# Ce este?
Cifrul Vigenère este un sistem polialfabetic: nu mai folosește o singură deplasare, ci mai multe. Cheia este un cuvânt, iar fiecare literă a cuvântului este o deplasare Cezar (A=0, B=1, ..., Z=25).

# Cum funcționează
Cuvântul-cheie se repetă sub text, iar fiecare literă din text este deplasată cu litera de sub ea.
    Cheia KEY înseamnă deplasările 10, 4, 24, 10, 4, 24, ...
    Criptare:    C = (P + K) mod 26
    Decriptare:  P = (C - K) mod 26

# Exemplu cu cheia KEY
    Text clar:     A T T A C K
    Cheia:         K E Y K E Y
    Text criptat:  K X R K G I
Observă că cele două litere T din text sunt criptate diferit (X și R). Asta ascunde frecvențele literelor.

# Cât de sigur este?
Dacă cheia are m litere, există 26^m chei: 26 pentru m=1, 17 576 pentru m=3, 456 976 pentru m=4. Cu cât cheia este mai lungă, cu atât cifrul este mai greu de spart; metodele profesionale (testul Kasiski) găsesc lungimea cheii analizând repetițiile din text.

# Cum folosești aplicația
Scrii un cuvânt-cheie (doar litere) și apeși „Criptează”. Spațiile și semnele din text rămân neschimbate.
""",
        "en": """
# What is it?
The Vigenère cipher is a polyalphabetic system: it does not use a single shift but several. The key is a word, and each letter of the word is a Caesar shift (A=0, B=1, ..., Z=25).

# How it works
The keyword is repeated under the text, and each letter of the text is shifted by the letter below it.
    The key KEY means the shifts 10, 4, 24, 10, 4, 24, ...
    Encryption:  C = (P + K) mod 26
    Decryption:  P = (C - K) mod 26

# Example with the key KEY
    Plain text:      A T T A C K
    Key:             K E Y K E Y
    Encrypted text:  K X R K G I
Notice that the two letters T in the text are encrypted differently (X and R). This hides the letter frequencies.

# How secure is it?
If the key has m letters, there are 26^m keys: 26 for m=1, 17,576 for m=3, 456,976 for m=4. The longer the key, the harder the cipher is to break; professional methods (the Kasiski test) find the key length by analyzing repetitions in the text.

# How to use the app
Type a keyword (letters only) and press "Encrypt". Spaces and punctuation in the text stay unchanged.
""",
        "ru": """
# Что это?
Шифр Виженера — полиалфавитная система: используется не один сдвиг, а несколько. Ключ — слово, а каждая его буква задаёт сдвиг Цезаря (A=0, B=1, ..., Z=25).

# Как это работает
Ключевое слово повторяется под текстом, и каждая буква текста сдвигается на букву, стоящую под ней.
    Ключ KEY означает сдвиги 10, 4, 24, 10, 4, 24, ...
    Шифрование:   C = (P + K) mod 26
    Расшифровка:  P = (C - K) mod 26

# Пример с ключом KEY
    Открытый текст:  A T T A C K
    Ключ:            K E Y K E Y
    Шифртекст:       K X R K G I
Обратите внимание: две буквы T в тексте шифруются по-разному (X и R). Это скрывает частоты букв.

# Насколько это надёжно?
Если в ключе m букв, существует 26^m ключей: 26 при m=1, 17 576 при m=3, 456 976 при m=4. Чем длиннее ключ, тем труднее взломать шифр; профессиональные методы (тест Казиски) находят длину ключа, анализируя повторы в тексте.

# Как пользоваться приложением
Введите ключевое слово (только буквы) и нажмите «Зашифровать». Пробелы и знаки препинания в тексте не меняются.
""",
    },
    "polibius": {
        "ro": """
# Ce este?
Pătratul lui Polibius (istoricul grec Polibius, secolul II î.Hr.) înlocuiește fiecare literă cu două cifre: rândul și coloana ei dintr-un pătrat 5 × 5. Alfabetul are 26 de litere, deci J și I împart aceeași căsuță.

# Pătratul standard
    1 2 3 4 5
    1 A B C D E
    2 F G H I K
    3 L M N O P
    4 Q R S T U
    5 V W X Y Z
Litera T se află pe rândul 4, coloana 4, deci devine 44.
    ATAC  ->  11 44 11 13

# Cu cuvânt-cheie
Literele cuvântului-cheie (fără repetări) completează primele căsuțe ale pătratului, iar restul alfabetului urmează în ordine. Cu cuvântul-cheie A se obține chiar pătratul standard de mai sus.

# Cât de sigur este?
Fără cuvânt-cheie, sistemul nu are nicio taină: oricine știe pătratul decriptează mesajul. Cu cuvânt-cheie, sistemul rămâne monoalfabetic (aceeași literă dă mereu aceleași două cifre), deci poate fi spart cu analiza frecvențelor.

# Cum folosești aplicația
Din text se păstrează doar literele A-Z; spațiile dispar. Rezultatul este o înșiruire de perechi de cifre între 1 și 5. Pentru decriptare lipești aceste perechi, cu același cuvânt-cheie.
""",
        "en": """
# What is it?
The Polybius square (named after the Greek historian Polybius, 2nd century BC) replaces each letter with two digits: its row and column in a 5 × 5 square. The alphabet has 26 letters, so J and I share the same cell.

# The standard square
    1 2 3 4 5
    1 A B C D E
    2 F G H I K
    3 L M N O P
    4 Q R S T U
    5 V W X Y Z
The letter T is in row 4, column 4, so it becomes 44.
    ATTACK  ->  11 44 44 11 13 25

# With a keyword
The letters of the keyword (without repeats) fill the first cells of the square, and the rest of the alphabet follows in order. With the keyword A you get exactly the standard square above.

# How secure is it?
Without a keyword the system has no secret: anyone who knows the square can decrypt the message. With a keyword it stays monoalphabetic (the same letter always gives the same two digits), so it can be broken with frequency analysis.

# How to use the app
Only the letters A-Z are kept from the text; spaces disappear. The result is a series of digit pairs between 1 and 5. To decrypt, paste these pairs and use the same keyword.
""",
        "ru": """
# Что это?
Квадрат Полибия (назван по имени греческого историка Полибия, II век до н. э.) заменяет каждую букву двумя цифрами: номером строки и столбца в квадрате 5 × 5. В алфавите 26 букв, поэтому J и I занимают одну клетку.

# Стандартный квадрат
    1 2 3 4 5
    1 A B C D E
    2 F G H I K
    3 L M N O P
    4 Q R S T U
    5 V W X Y Z
Буква T находится в строке 4, столбце 4, поэтому становится 44.
    ATTACK  ->  11 44 44 11 13 25

# С ключевым словом
Буквы ключевого слова (без повторов) заполняют первые клетки квадрата, а остальной алфавит идёт по порядку. С ключевым словом A получается именно стандартный квадрат, показанный выше.

# Насколько это надёжно?
Без ключевого слова у системы нет секрета: любой, кто знает квадрат, расшифрует сообщение. С ключевым словом система остаётся моноалфавитной (одна буква всегда даёт одни и те же две цифры), поэтому её можно взломать частотным анализом.

# Как пользоваться приложением
Из текста остаются только буквы A-Z; пробелы исчезают. Результат — последовательность пар цифр от 1 до 5. Для расшифровки вставьте эти пары и используйте то же ключевое слово.
""",
    },
    "homofonic": {
        "ro": """
# Ce este?
Cifrul homofonic încearcă să ascundă frecvența literelor. O literă foarte des folosită (cum este E) nu are un singur înlocuitor, ci mai multe numere, numite omofoane. Fiecare apariție a literei folosește pe rând alt număr.

# Cum funcționează în această aplicație
Avem 100 de numere (00 ... 99), împărțite literelor după frecvența lor:
    E primește 12 numere, A și I câte 11, R 7, N 6, T 6, U 6
    literele rare (J, K, Q, W, X, Y, Z ...) primesc câte un singur număr
Cheia este un număr de la 0 la 9999: ea amestecă tabelul, deci stabilește care numere aparțin cărei litere.

# Exemplu
Dacă E are numerele 13, 25, 74, ..., prima literă E din text devine 13, a doua devine 25, a treia 74 și tot așa. Textul criptat arată ca o înșiruire de numere:
    13 25 74 69 55 20 ...

# Cât de sigur este?
Cifrul este mai greu de spart cu frecvențe, deoarece fiecare număr apare aproximativ la fel de des. Cheia din această aplicație are doar 10 000 de valori; sistemele reale folosesc tabele mult mai mari.

# Cum folosești aplicația
Din text se păstrează doar literele A-Z. La decriptare lipești numerele separate prin spații și folosești aceeași cheie.
""",
        "en": """
# What is it?
The homophonic cipher tries to hide letter frequencies. A very common letter (like E) does not have a single substitute but several numbers, called homophones. Each occurrence of the letter uses a different number in turn.

# How it works in this app
There are 100 numbers (00 ... 99), divided among the letters according to their frequency:
    E gets 12 numbers, A and I get 11 each, R 7, N 6, T 6, U 6
    rare letters (J, K, Q, W, X, Y, Z ...) get a single number each
The key is a number from 0 to 9999: it shuffles the table, so it decides which numbers belong to which letter.

# Example
If E has the numbers 13, 25, 74, ..., the first E in the text becomes 13, the second becomes 25, the third 74, and so on. The encrypted text looks like a series of numbers:
    13 25 74 69 55 20 ...

# How secure is it?
The cipher is harder to break with frequencies because every number appears about equally often. The key in this app has only 10,000 values; real systems use much larger tables.

# How to use the app
Only the letters A-Z are kept from the text. To decrypt, paste the numbers separated by spaces and use the same key.
""",
        "ru": """
# Что это?
Омофонический шифр пытается скрыть частоты букв. У очень частой буквы (например, E) не один заменитель, а несколько чисел — омофонов. Каждое появление буквы использует по очереди другое число.

# Как это работает в этом приложении
Есть 100 чисел (00 ... 99), распределённых между буквами по их частоте:
    E получает 12 чисел, A и I — по 11, R — 7, N, T, U — по 6
    редкие буквы (J, K, Q, W, X, Y, Z ...) получают по одному числу
Ключ — число от 0 до 9999: он перемешивает таблицу и определяет, какие числа принадлежат какой букве.

# Пример
Если у E числа 13, 25, 74, ..., то первая E в тексте превращается в 13, вторая — в 25, третья — в 74 и так далее. Шифртекст выглядит как последовательность чисел:
    13 25 74 69 55 20 ...

# Насколько это надёжно?
Шифр труднее взломать по частотам, потому что каждое число встречается примерно одинаково часто. У ключа в этом приложении всего 10 000 значений; настоящие системы используют гораздо большие таблицы.

# Как пользоваться приложением
Из текста остаются только буквы A-Z. Для расшифровки вставьте числа, разделённые пробелами, и используйте тот же ключ.
""",
    },
    "hill": {
        "ro": """
# Ce este?
Cifrul Hill (Lester Hill, 1929) criptează literele în blocuri, nu una câte una. Aici folosim blocuri de 2 litere și o matrice cheie 2 × 2, cu elementele a, b, c, d.

# Criptarea
Perechea de litere (P1, P2) devine (C1, C2) prin înmulțire cu matricea, modulo 26 (A=0, ..., Z=25):
    C1 = (a · P1 + b · P2) mod 26
    C2 = (c · P1 + d · P2) mod 26
Dacă textul are un număr impar de litere, se adaugă un X la final.

# Decriptarea (matricea inversă o calculezi tu)
Aplicația nu calculează inversa. O afli singur, pe hârtie:
    det = (a · d - b · c) mod 26
    m = numărul cu det · m = 1 (mod 26), adică inversul lui det modulo 26
    matricea inversată = [ d  -b ; -c  a ]   (valorile aduse între 0 și 25)
Cheia este bună doar dacă det este prim cu 26 (altfel m nu există). La decriptare introduci numărul modular m și matricea inversată; programul calculează P = m · (matricea · C) mod 26. Dacă ai înmulțit deja matricea cu m, pune m = 1.

# Exemplu cu matricea a=3, b=3, c=2, d=5
det = 3·5 - 3·2 = 9, iar inversul lui 9 modulo 26 este m = 3 (9 · 3 = 27 = 1 mod 26). Matricea inversată este [5 -3 ; -2 3] = [5 23 ; 24 3].
    HELP  ->  HIAT
Verificare: (7, 4) devine (3·7+3·4, 2·7+5·4) = (33, 34) = (7, 8) = HI.

# Cum folosești aplicația
Din text se păstrează doar literele A-Z. La criptare introduci numerele a, b, c, d. La decriptare introduci numărul modular m și cele patru numere ale matricii inversate (de exemplu m=3 și 5, 23, 24, 3).
""",
        "en": """
# What is it?
The Hill cipher (Lester Hill, 1929) encrypts letters in blocks, not one at a time. Here we use blocks of 2 letters and a 2 × 2 key matrix with the elements a, b, c, d.

# Encryption
The pair of letters (P1, P2) becomes (C1, C2) by multiplying with the matrix, modulo 26 (A=0, ..., Z=25):
    C1 = (a · P1 + b · P2) mod 26
    C2 = (c · P1 + d · P2) mod 26
If the text has an odd number of letters, an X is added at the end.

# Decryption (you calculate the inverse matrix)
The app does not calculate the inverse. You find it yourself, on paper:
    det = (a · d - b · c) mod 26
    m = the number with det · m = 1 (mod 26), i.e. the inverse of det modulo 26
    inverted matrix = [ d  -b ; -c  a ]   (values brought between 0 and 25)
The key is good only if det is coprime with 26 (otherwise m does not exist). For decryption you enter the modular number m and the inverted matrix; the program computes P = m · (matrix · C) mod 26. If you already multiplied the matrix by m, put m = 1.

# Example with the matrix a=3, b=3, c=2, d=5
det = 3·5 - 3·2 = 9, and the inverse of 9 modulo 26 is m = 3 (9 · 3 = 27 = 1 mod 26). The inverted matrix is [5 -3 ; -2 3] = [5 23 ; 24 3].
    HELP  ->  HIAT
Check: (7, 4) becomes (3·7+3·4, 2·7+5·4) = (33, 34) = (7, 8) = HI.

# How to use the app
Only the letters A-Z are kept from the text. For encryption enter the numbers a, b, c, d. For decryption enter the modular number m and the four numbers of the inverted matrix (for example m=3 and 5, 23, 24, 3).
""",
        "ru": """
# Что это?
Шифр Хилла (Лестер Хилл, 1929) шифрует буквы блоками, а не по одной. Здесь используются блоки из 2 букв и ключевая матрица 2 × 2 с элементами a, b, c, d.

# Шифрование
Пара букв (P1, P2) превращается в (C1, C2) умножением на матрицу по модулю 26 (A=0, ..., Z=25):
    C1 = (a · P1 + b · P2) mod 26
    C2 = (c · P1 + d · P2) mod 26
Если в тексте нечётное число букв, в конец добавляется X.

# Расшифровка (обратную матрицу вычисляете вы)
Приложение не вычисляет обратную матрицу. Вы находите её сами, на бумаге:
    det = (a · d - b · c) mod 26
    m = число, для которого det · m = 1 (mod 26), то есть обратное к det по модулю 26
    обращённая матрица = [ d  -b ; -c  a ]   (значения приводятся к диапазону 0-25)
Ключ годится, только если det взаимно прост с 26 (иначе m не существует). При расшифровке вы вводите модульное число m и обращённую матрицу; программа считает P = m · (матрица · C) mod 26. Если вы уже умножили матрицу на m, введите m = 1.

# Пример для матрицы a=3, b=3, c=2, d=5
det = 3·5 - 3·2 = 9, а число, обратное 9 по модулю 26, равно m = 3 (9 · 3 = 27 = 1 mod 26). Обращённая матрица: [5 -3 ; -2 3] = [5 23 ; 24 3].
    HELP  ->  HIAT
Проверка: (7, 4) превращается в (3·7+3·4, 2·7+5·4) = (33, 34) = (7, 8) = HI.

# Как пользоваться приложением
Из текста остаются только буквы A-Z. Для шифрования введите числа a, b, c, d. Для расшифровки введите модульное число m и четыре числа обращённой матрицы (например, m=3 и 5, 23, 24, 3).
""",
    },
}
