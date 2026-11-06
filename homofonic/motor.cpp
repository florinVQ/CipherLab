#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

char Alfabet_Latin[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

// Cate numere primeste fiecare litera A..Z (suma = 100).
int omofoane[26] = {11, 1, 5, 4, 12, 1, 1, 1, 11, 1, 1, 4, 3,
                    6, 4, 3, 1, 7, 5, 6, 6, 2, 1, 1, 1, 1};

int main()
{
    string comanda, text;
    int cheie;
    int coduri[100];         // numerele 0..99, amestecate
    int tabel[26][12];       // tabel[litera][i] = al i-lea numar al literei
    char literaDinCod[100];  // pentru decriptare: ce litera ascunde fiecare numar

    cin >> comanda >> cheie;
    if (cheie < 0 || cheie > 9999)
    {
        cerr << "homofonic_cheie";
        return 1;
    }

    // Amestecam numerele 0..99 folosind cheia ca punct de plecare.
    for (int i = 0; i < 100; i++)
        coduri[i] = i;
    unsigned int stare = cheie;
    for (int i = 99; i > 0; i--)
    {
        stare = stare * 1103515245 + 12345;
        int j = (stare / 65536) % 32768 % (i + 1);
        int aux = coduri[i];
        coduri[i] = coduri[j];
        coduri[j] = aux;
    }

    // Impartim numerele amestecate literelor.
    int urmator = 0;
    for (int litera = 0; litera < 26; litera++)
    {
        for (int i = 0; i < omofoane[litera]; i++)
        {
            tabel[litera][i] = coduri[urmator];
            literaDinCod[coduri[urmator]] = Alfabet_Latin[litera];
            urmator++;
        }
    }

    if (comanda == "cripteaza")
    {
        getline(cin >> ws, text);
        if (text.length() > MAX)
        {
            cerr << "text_lung";
            return 1;
        }
        int folosit[26] = {0};  // de cate ori am folosit deja fiecare litera
        for (int i = 0; i < text.length(); i++)
        {
            for (int litera = 0; litera < 26; litera++)
            {
                if (text[i] == Alfabet_Latin[litera])
                {
                    int numar = tabel[litera][folosit[litera] % omofoane[litera]];
                    folosit[litera]++;
                    if (numar < 10)
                        cout << "0";
                    cout << numar << " ";
                }
            }
        }
        return 0;
    }

    int numar;
    while (cin >> numar)
    {
        if (numar < 0 || numar > 99)
        {
            cerr << "homofonic_cod";
            return 1;
        }
        cout << literaDinCod[numar];
    }
    return 0;
}
