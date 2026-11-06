#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

char Alfabet_Latin[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int main()
{
    string comanda, text;
    int k = 0;
    int pozitii[MAX];

    cin >> comanda;
    if (comanda != "atac")
        cin >> k;
    getline(cin >> ws, text);

    int n = text.length();
    if (n > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Pozitia fiecarei litere din text in alfabet (-1 daca nu este litera).
    for (int i = 0; i < n; i++)
    {
        pozitii[i] = -1;
        for (int j = 0; j < 26; j++)
            if (text[i] == Alfabet_Latin[j])
                pozitii[i] = j;
    }

    if (comanda == "atac")
    {
        // Toate cele 26 de chei posibile.
        for (int cheie = 0; cheie < 26; cheie++)
        {
            cout << "k=" << cheie << "\t";
            for (int i = 0; i < n; i++)
            {
                if (pozitii[i] == -1)
                    cout << text[i];
                else
                    cout << Alfabet_Latin[(pozitii[i] - cheie + 26) % 26];
            }
            cout << endl;
        }
        return 0;
    }

    if (comanda == "decripteaza")
        k = -k;
    k = ((k % 26) + 26) % 26;

    for (int i = 0; i < n; i++)
    {
        if (pozitii[i] == -1)
            cout << text[i];
        else
            cout << Alfabet_Latin[(pozitii[i] + k) % 26];
    }
    return 0;
}
