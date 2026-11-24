#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

// Intrare: comanda, generatorul cheii fluide, alfabetul, textul.
// Generatorul este unul dintre:
//   cuvant W           sincron: cheile sunt caracterele cuvantului W, repetate (Vigenere)
//   sir L k1 ... kL    sincron: cheile sunt numerele date, repetate
//   fibonacci F1 F2    sincron: K1 = F1, K2 = F2, Ki = K(i-1) + K(i-2)
//   asincron k1        auto-sincronizant: K1 = k1, apoi K(i+1) = y(i), caracterul criptat anterior
// Iesire: pentru fiecare caracter un rand "x k y" (numerele lor in alfabet), unde
//   la criptare   y = (x + k) mod m
//   la decriptare y = (x - k) mod m
int main()
{
    string comanda, generator, cuvant, Alfabet, text;
    int sir[MAX];
    int lungimeSir = 0;
    long long f1 = 0, f2 = 0, k1 = 0;

    cin >> comanda >> generator;
    if (generator == "cuvant")
        cin >> cuvant;
    else if (generator == "sir")
    {
        cin >> lungimeSir;
        if (lungimeSir < 1 || lungimeSir > MAX)
        {
            cerr << "text_lung";
            return 1;
        }
        for (int i = 0; i < lungimeSir; i++)
            cin >> sir[i];
    }
    else if (generator == "fibonacci")
        cin >> f1 >> f2;
    else
        cin >> k1;
    cin >> Alfabet >> text;

    int m = Alfabet.length();
    int n = text.length();
    if (n > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Cheia urmatoare, mereu redusa modulo m.
    long long cheie = 0;
    long long anterior = ((f1 % m) + m) % m;  // pentru Fibonacci: K(i-1)
    long long curent = ((f2 % m) + m) % m;    // pentru Fibonacci: K(i)
    if (generator == "asincron")
        cheie = ((k1 % m) + m) % m;

    for (int i = 0; i < n; i++)
    {
        if (generator == "cuvant")
            cheie = Alfabet.find(cuvant[i % cuvant.length()]);
        else if (generator == "sir")
            cheie = ((sir[i % lungimeSir] % m) + m) % m;
        else if (generator == "fibonacci")
        {
            if (i == 0)
                cheie = anterior;
            else if (i == 1)
                cheie = curent;
            else
            {
                long long urmator = (anterior + curent) % m;
                anterior = curent;
                curent = urmator;
                cheie = curent;
            }
        }

        int x = Alfabet.find(text[i]);
        int y;
        if (comanda == "cripteaza")
            y = (x + cheie) % m;
        else
            y = ((x - cheie) % m + m) % m;
        cout << x << " " << cheie << " " << y << endl;

        // La sistemul asincron cheia urmatoare este caracterul criptat de acum.
        if (generator == "asincron")
        {
            if (comanda == "cripteaza")
                cheie = y;
            else
                cheie = x;
        }
    }
    return 0;
}
