#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

// Intrare: comanda, cheia k (lipseste la atac), alfabetul, textul.
// Alfabetul si textul vin codate (vezi comun/alfabet.py): fiecare caracter este un octet,
// iar numarul unui caracter este pozitia lui in sirul Alfabet.
int main()
{
    string comanda, Alfabet, text;
    int k = 0;

    cin >> comanda;
    if (comanda != "atac")
        cin >> k;
    cin >> Alfabet >> text;

    int m = Alfabet.length();
    int n = text.length();
    if (n > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    if (comanda == "atac")
    {
        // Toate cele m chei posibile; pe fiecare rand: cheia, apoi textul obtinut.
        for (int cheie = 0; cheie < m; cheie++)
        {
            cout << cheie << "\t";
            for (int i = 0; i < n; i++)
            {
                int p = Alfabet.find(text[i]);
                cout << Alfabet[(p - cheie + m) % m];
            }
            cout << endl;
        }
        return 0;
    }

    if (comanda == "decripteaza")
        k = -k;
    k = ((k % m) + m) % m;

    for (int i = 0; i < n; i++)
    {
        int p = Alfabet.find(text[i]);
        cout << Alfabet[(p + k) % m];
    }
    return 0;
}
