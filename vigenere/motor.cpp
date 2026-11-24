#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

// Intrare: comanda, cuvantul-cheie, alfabetul, textul.
int main()
{
    string comanda, cuvant, Alfabet, text;

    cin >> comanda >> cuvant >> Alfabet >> text;

    int m = Alfabet.length();
    if (text.length() > MAX || cuvant.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Deplasarile date de caracterele cuvantului-cheie.
    int lungimeCheie = cuvant.length();
    int cheie[MAX];
    for (int i = 0; i < lungimeCheie; i++)
        cheie[i] = Alfabet.find(cuvant[i]);

    for (int i = 0; i < text.length(); i++)
    {
        int p = Alfabet.find(text[i]);
        int k = cheie[i % lungimeCheie];
        if (comanda == "cripteaza")
            cout << Alfabet[(p + k) % m];
        else
            cout << Alfabet[(p - k + m) % m];
    }
    return 0;
}
