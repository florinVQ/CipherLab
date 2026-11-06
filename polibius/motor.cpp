// Patratul lui Polibius: fiecare litera devine perechea (linie, coloana) dintr-un patrat 5x5.
// Litera J se scrie ca I. Literele cuvantului-cheie completeaza primele casute ale patratului
// (cu cuvantul-cheie A se obtine patratul standard).
// Date citite de la tastatura (sau de la interfata Python):
//   cripteaza cuvant   |   decripteaza cuvant
//   textul pe o singura linie: litere majuscule la criptare, perechi de cifre (11 44 ...) la decriptare
#include <iostream>
using namespace std;

const int MAX = 10000;

int main()
{
    string comanda, cuvant, text;
    char litere[25];
    char patrat[5][5];

    cin >> comanda >> cuvant;
    getline(cin >> ws, text);

    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Aflam cele 25 de litere ale patratului: cuvantul-cheie, apoi restul alfabetului.
    string sir = cuvant + "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    int nr = 0;
    for (int i = 0; i < sir.length(); i++)
    {
        char c = sir[i];
        if (c == 'J')
            c = 'I';
        bool esteLitera = c >= 'A' && c <= 'Z';
        bool existaDeja = false;
        for (int j = 0; j < nr; j++)
            if (litere[j] == c)
                existaDeja = true;

        if (esteLitera && !existaDeja)
        {
            litere[nr] = c;
            nr++;
        }
    }
    for (int i = 0; i < 25; i++)
        patrat[i / 5][i % 5] = litere[i];

    if (comanda == "cripteaza")
    {
        for (int i = 0; i < text.length(); i++)
        {
            char c = text[i];
            if (c == 'J')
                c = 'I';
            for (int linie = 0; linie < 5; linie++)
                for (int coloana = 0; coloana < 5; coloana++)
                    if (patrat[linie][coloana] == c)
                        cout << linie + 1 << coloana + 1 << " ";
        }
        return 0;
    }

    // Decriptare: strangem cifrele 1-5 si le citim doua cate doua.
    int cifre[MAX];
    int nrCifre = 0;
    for (int i = 0; i < text.length(); i++)
    {
        if (text[i] >= '1' && text[i] <= '5')
        {
            cifre[nrCifre] = text[i] - '0';
            nrCifre++;
        }
    }
    if (nrCifre % 2 != 0)
    {
        cerr << "polibius_cifre";
        return 1;
    }
    for (int i = 0; i < nrCifre; i += 2)
        cout << patrat[cifre[i] - 1][cifre[i + 1] - 1];
    return 0;
}
