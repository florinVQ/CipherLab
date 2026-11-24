#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const int MAX_N = 100;

// Adevarat daca p[0..n-1] contine numerele 1..n, fiecare o singura data.
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

// Intrare: comanda, n, permutarea p1 ... pn, alfabetul, textul.
// Criptare:   y[i] = x[p(i)]   (pe pozitia i se pune caracterul de pe pozitia p(i))
// Decriptare: x[p(i)] = y[i]   (adica se aplica permutarea inversa)
int main()
{
    string comanda, Alfabet, text;
    int n, p[MAX_N];

    cin >> comanda >> n;
    if (n < 1 || n > MAX_N)
    {
        cerr << "permutare";
        return 1;
    }
    for (int i = 0; i < n; i++)
        cin >> p[i];
    cin >> Alfabet >> text;

    if (!estePermutare(p, n))
    {
        cerr << "permutare";
        return 1;
    }
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Ultimul bloc se completeaza cu ultimul caracter al alfabetului.
    while (text.length() % n != 0)
        text = text + Alfabet[Alfabet.length() - 1];

    for (int bloc = 0; bloc < text.length(); bloc += n)
    {
        string rezultat = text.substr(bloc, n);
        for (int i = 0; i < n; i++)
        {
            if (comanda == "cripteaza")
                rezultat[i] = text[bloc + p[i] - 1];
            else
                rezultat[p[i] - 1] = text[bloc + i];
        }
        cout << rezultat;
    }
    return 0;
}
