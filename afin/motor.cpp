#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

// Numarul x pentru care (a * x) mod m = 1, sau 0 daca nu exista (a nu este prim cu m).
int inversModular(int a, int m)
{
    for (int x = 1; x < m; x++)
        if ((a * x) % m == 1)
            return x;
    return 0;
}

// Intrare: comanda, a si b (lipsesc la atac), alfabetul, textul.
int main()
{
    string comanda, Alfabet, text;
    int a = 0, b = 0;

    cin >> comanda;
    if (comanda != "atac")
        cin >> a >> b;
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
        // Toate perechile (a, b) cu a prim cu m; pe fiecare rand: a, b, textul obtinut.
        for (a = 1; a < m; a++)
        {
            int inversA = inversModular(a, m);
            if (inversA == 0)
                continue;
            for (b = 0; b < m; b++)
            {
                cout << a << "\t" << b << "\t";
                for (int i = 0; i < n; i++)
                {
                    int p = Alfabet.find(text[i]);
                    cout << Alfabet[(inversA * (p - b + m)) % m];
                }
                cout << endl;
            }
        }
        return 0;
    }

    a = ((a % m) + m) % m;
    b = ((b % m) + m) % m;
    int inversA = inversModular(a, m);
    if (inversA == 0)
    {
        cerr << "afin_a";
        return 1;
    }

    for (int i = 0; i < n; i++)
    {
        int p = Alfabet.find(text[i]);
        if (comanda == "cripteaza")
            cout << Alfabet[(a * p + b) % m];
        else
            cout << Alfabet[(inversA * (p - b + m)) % m];
    }
    return 0;
}
