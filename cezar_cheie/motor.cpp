#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

char Alfabet_Latin[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int main()
{
    string comanda, cuvant, text, lista, unul, cuvantComplet;
    char AlfabetNou[26];
    int k = 0;

    cin >> comanda >> cuvant;
    if (comanda != "atac")
        cin >> k;
    getline(cin >> ws, text);

    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Pentru atac, "cuvant" este lista de cuvinte banuite separate prin virgula.
    // Pentru criptare/decriptare lista are un singur cuvant: cheia.
    lista = cuvant + ",";
    k = ((k % 26) + 26) % 26;

    unul = "";
    for (int c = 0; c < lista.length(); c++)
    {
        if (lista[c] != ',')
        {
            unul = unul + lista[c];
            continue;
        }
        if (unul == "" && comanda == "atac")
            continue;

        // Alfabetul nou: literele cuvantului (fara repetari), apoi restul alfabetului.
        int nr = 0;
        cuvantComplet = unul + "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        for (int i = 0; i < cuvantComplet.length(); i++)
        {
            bool esteLitera = cuvantComplet[i] >= 'A' && cuvantComplet[i] <= 'Z';
            bool existaDeja = false;
            for (int j = 0; j < nr; j++)
                if (AlfabetNou[j] == cuvantComplet[i])
                    existaDeja = true;
            if (esteLitera && !existaDeja)
            {
                AlfabetNou[nr] = cuvantComplet[i];
                nr++;
            }
        }

        // La atac incercam toate cele 26 de deplasari; altfel doar k.
        int de_la = k, pana_la = k;
        if (comanda == "atac")
        {
            de_la = 0;
            pana_la = 25;
        }
        for (int cheie = de_la; cheie <= pana_la; cheie++)
        {
            if (comanda == "atac")
                cout << "cuvant=" << unul << ", k=" << cheie << "\t";
            for (int i = 0; i < text.length(); i++)
            {
                int p = -1;  // pozitia literei in alfabet, -1 daca nu este litera
                if (comanda == "cripteaza")
                {
                    for (int j = 0; j < 26; j++)
                        if (Alfabet_Latin[j] == text[i])
                            p = j;
                    if (p == -1)
                        cout << text[i];
                    else
                        cout << AlfabetNou[(p + cheie) % 26];
                }
                else
                {
                    for (int j = 0; j < 26; j++)
                        if (AlfabetNou[j] == text[i])
                            p = j;
                    if (p == -1)
                        cout << text[i];
                    else
                        cout << Alfabet_Latin[(p - cheie + 26) % 26];
                }
            }
            if (comanda == "atac")
                cout << endl;
        }
        unul = "";
    }
    return 0;
}
