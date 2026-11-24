#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const int MAX_PERMUTARI = 50;
const int MAX_N = 100;

bool estePermutare(int p[], int n)
{
    bool vazut[MAX_N + 1] = {false};
    for (int i = 0; i < n; i++)
    {
        if (p[i] < 1 || p[i] > n || vazut[p[i]])
            return false;
        vazut[p[i]] = true;
    }
    return true;
}

// Intrare: comanda, numarul de permutari, apoi fiecare permutare (lungimea ei si numerele),
// alfabetul, textul.
// Textul se imparte in segmente cu lungimile permutarilor, luate pe rand (si reluate de la
// prima daca textul este mai lung). Fiecare segment se permuta cu permutarea lui:
// la criptare y[i] = x[p(i)], la decriptare x[p(i)] = y[i].
int main()
{
    string comanda, Alfabet, text;
    int nrPermutari;
    int lungime[MAX_PERMUTARI], p[MAX_PERMUTARI][MAX_N];

    cin >> comanda >> nrPermutari;
    if (nrPermutari < 1 || nrPermutari > MAX_PERMUTARI)
    {
        cerr << "permutare";
        return 1;
    }
    for (int k = 0; k < nrPermutari; k++)
    {
        cin >> lungime[k];
        if (lungime[k] < 1 || lungime[k] > MAX_N)
        {
            cerr << "permutare";
            return 1;
        }
        for (int i = 0; i < lungime[k]; i++)
            cin >> p[k][i];
        if (!estePermutare(p[k], lungime[k]))
        {
            cerr << "permutare";
            return 1;
        }
    }
    cin >> Alfabet >> text;
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    int pozitie = 0, k = 0;
    while (pozitie < text.length())
    {
        int n = lungime[k];
        // Ultimul segment se completeaza cu ultimul caracter al alfabetului.
        while (pozitie + n > text.length())
            text = text + Alfabet[Alfabet.length() - 1];

        string segment = text.substr(pozitie, n);
        for (int i = 0; i < n; i++)
        {
            if (comanda == "cripteaza")
                segment[i] = text[pozitie + p[k][i] - 1];
            else
                segment[p[k][i] - 1] = text[pozitie + i];
        }
        cout << segment;
        pozitie += n;
        k = (k + 1) % nrPermutari;
    }
    return 0;
}
