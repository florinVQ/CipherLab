#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const int MAX_LATURA = 9;  // randurile si coloanele se scriu cu o singura cifra

// Intrare: comanda, cuvantul-cheie, alfabetul, textul
// (la decriptare textul este format din perechi de cifre).
int main()
{
    string comanda, cuvant, Alfabet, text;

    cin >> comanda >> cuvant >> Alfabet;
    getline(cin >> ws, text);

    int m = Alfabet.length();
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Numarul de coloane: radacina patrata a lui m, rotunjita in sus.
    int coloane = 1;
    while (coloane * coloane < m)
        coloane++;
    if (coloane > MAX_LATURA)
    {
        cerr << "polibius_alfabet";
        return 1;
    }

    // Patratul, citit rand cu rand: cuvantul-cheie (fara repetari), apoi restul alfabetului.
    string patrat = "";
    string sir = cuvant + Alfabet;
    for (int i = 0; i < sir.length(); i++)
        if (patrat.find(sir[i]) == string::npos)
            patrat = patrat + sir[i];

    if (comanda == "cripteaza")
    {
        for (int i = 0; i < text.length(); i++)
        {
            int p = patrat.find(text[i]);
            cout << p / coloane + 1 << p % coloane + 1 << " ";
        }
        return 0;
    }

    // Decriptare: strangem cifrele si le citim doua cate doua (rand, coloana).
    int cifre[MAX];
    int nrCifre = 0;
    for (int i = 0; i < text.length(); i++)
    {
        if (text[i] >= '1' && text[i] <= '9')
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
    {
        int p = (cifre[i] - 1) * coloane + (cifre[i + 1] - 1);
        if (cifre[i + 1] > coloane || p >= m)
        {
            cerr << "polibius_cifre";
            return 1;
        }
        cout << patrat[p];
    }
    return 0;
}
