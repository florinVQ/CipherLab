#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const int MAX_CUVINTE = 100;

// Alfabetul nou: caracterele cuvantului (fara repetari), apoi restul alfabetului.
string alfabetCuCuvant(string cuvant, string Alfabet)
{
    string nou = "";
    string sir = cuvant + Alfabet;
    for (int i = 0; i < sir.length(); i++)
        if (nou.find(sir[i]) == string::npos)
            nou = nou + sir[i];
    return nou;
}

string cripteaza(string text, string Alfabet, string AlfabetNou, int k)
{
    int m = Alfabet.length();
    string rezultat = "";
    for (int i = 0; i < text.length(); i++)
    {
        int p = Alfabet.find(text[i]);
        rezultat = rezultat + AlfabetNou[(p + k) % m];
    }
    return rezultat;
}

string decripteaza(string text, string Alfabet, string AlfabetNou, int k)
{
    int m = Alfabet.length();
    string rezultat = "";
    for (int i = 0; i < text.length(); i++)
    {
        int p = AlfabetNou.find(text[i]);
        rezultat = rezultat + Alfabet[(p - k + m) % m];
    }
    return rezultat;
}

// Intrare la criptare/decriptare: comanda, cuvantul-cheie, k, alfabetul, textul.
// Intrare la atac: comanda, numarul de cuvinte banuite, cuvintele, alfabetul, textul.
int main()
{
    string comanda, Alfabet, text;
    string cuvinte[MAX_CUVINTE];
    int nrCuvinte = 1, k = 0;

    cin >> comanda;
    if (comanda == "atac")
    {
        cin >> nrCuvinte;
        if (nrCuvinte > MAX_CUVINTE)
            nrCuvinte = MAX_CUVINTE;
        for (int i = 0; i < nrCuvinte; i++)
            cin >> cuvinte[i];
    }
    else
        cin >> cuvinte[0] >> k;
    cin >> Alfabet >> text;

    int m = Alfabet.length();
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }
    k = ((k % m) + m) % m;

    if (comanda == "cripteaza")
        cout << cripteaza(text, Alfabet, alfabetCuCuvant(cuvinte[0], Alfabet), k);
    else if (comanda == "decripteaza")
        cout << decripteaza(text, Alfabet, alfabetCuCuvant(cuvinte[0], Alfabet), k);
    else
    {
        // Fiecare cuvant banuit, cu toate cele m deplasari: cuvant, k, textul obtinut.
        for (int c = 0; c < nrCuvinte; c++)
        {
            string AlfabetNou = alfabetCuCuvant(cuvinte[c], Alfabet);
            for (int cheie = 0; cheie < m; cheie++)
                cout << cuvinte[c] << "\t" << cheie << "\t"
                     << decripteaza(text, Alfabet, AlfabetNou, cheie) << endl;
        }
    }
    return 0;
}
