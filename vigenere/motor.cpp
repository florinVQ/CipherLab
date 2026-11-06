#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

char Alfabet_Latin[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int main()
{
    string comanda, cuvant, text;
    int cheie[MAX];
    int lungimeCheie = 0;

    cin >> comanda >> cuvant;
    getline(cin >> ws, text);

    if (text.length() > MAX || cuvant.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Deplasarile date de literele cuvantului-cheie.
    for (int i = 0; i < cuvant.length(); i++)
    {
        for (int l = 0; l < 26; l++)
        {
            if (cuvant[i] == Alfabet_Latin[l])
            {
                cheie[lungimeCheie] = l;
                lungimeCheie++;
            }
        }
    }
    if (lungimeCheie == 0)
    {
        cerr << "cheie_litere";
        return 1;
    }

    int j = 0;  // pozitia in cheie; spatiile nu consuma litere din cheie
    for (int i = 0; i < text.length(); i++)
    {
        int p = -1;  // pozitia literei in alfabet, -1 daca nu este litera
        for (int l = 0; l < 26; l++)
            if (text[i] == Alfabet_Latin[l])
                p = l;
        if (p == -1)
        {
            cout << text[i];
            continue;
        }
        if (comanda == "cripteaza")
            cout << Alfabet_Latin[(p + cheie[j]) % 26];
        else
            cout << Alfabet_Latin[(p - cheie[j] + 26) % 26];
        j = (j + 1) % lungimeCheie;
    }
    return 0;
}
