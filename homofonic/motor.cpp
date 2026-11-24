#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const int MAX_CARACTERE = 90;
const int MAX_PE_CARACTER = 12;
const int MAX_CODURI = MAX_CARACTERE * MAX_PE_CARACTER;

// Intrare: comanda, cheia (0-9999), cate omofoane are fiecare caracter
// (intai cate numere urmeaza, apoi numerele), alfabetul, textul
// (la decriptare textul este format din numere).
int main()
{
    string comanda, Alfabet, text;
    int cheie, m;
    int omofoane[MAX_CARACTERE];
    int coduri[MAX_CODURI];                      // numerele 0 .. total-1, amestecate
    int tabel[MAX_CARACTERE][MAX_PE_CARACTER];   // tabel[caracter][i] = al i-lea numar al caracterului
    int caracterDinCod[MAX_CODURI];              // la decriptare: ce caracter ascunde fiecare numar

    cin >> comanda >> cheie >> m;
    if (cheie < 0 || cheie > 9999)
    {
        cerr << "homofonic_cheie";
        return 1;
    }
    int total = 0;
    for (int i = 0; i < m; i++)
    {
        cin >> omofoane[i];
        total += omofoane[i];
    }
    cin >> Alfabet;
    getline(cin >> ws, text);
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Toate numerele se scriu cu acelasi numar de cifre (cel putin 2).
    int cifre = 2;
    for (int limita = 100; limita < total; limita *= 10)
        cifre++;

    // Amestecam numerele 0 .. total-1 folosind cheia ca punct de plecare.
    for (int i = 0; i < total; i++)
        coduri[i] = i;
    unsigned int stare = cheie;
    for (int i = total - 1; i > 0; i--)
    {
        stare = stare * 1103515245 + 12345;
        int j = (stare / 65536) % 32768 % (i + 1);
        int aux = coduri[i];
        coduri[i] = coduri[j];
        coduri[j] = aux;
    }

    // Impartim numerele amestecate caracterelor.
    int urmator = 0;
    for (int c = 0; c < m; c++)
    {
        for (int i = 0; i < omofoane[c]; i++)
        {
            tabel[c][i] = coduri[urmator];
            caracterDinCod[coduri[urmator]] = c;
            urmator++;
        }
    }

    if (comanda == "cripteaza")
    {
        int folosit[MAX_CARACTERE] = {0};  // de cate ori am folosit deja fiecare caracter
        for (int i = 0; i < text.length(); i++)
        {
            int c = Alfabet.find(text[i]);
            int numar = tabel[c][folosit[c] % omofoane[c]];
            folosit[c]++;
            string scris = to_string(numar);
            while (scris.length() < cifre)
                scris = "0" + scris;
            cout << scris << " ";
        }
        return 0;
    }

    // Decriptare: citim numerele unul cate unul din text.
    string numar = "";
    text = text + " ";
    for (int i = 0; i < text.length(); i++)
    {
        if (text[i] >= '0' && text[i] <= '9')
        {
            numar = numar + text[i];
            continue;
        }
        if (numar == "")
            continue;
        if (numar.length() > 6 || stoi(numar) >= total)
        {
            cerr << "homofonic_cod";
            return 1;
        }
        cout << Alfabet[caracterDinCod[stoi(numar)]];
        numar = "";
    }
    return 0;
}
