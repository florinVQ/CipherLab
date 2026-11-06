#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

char Alfabet_Latin[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int main()
{
    string comanda, text;
    int a = 0, b = 0;
    int pozitii[MAX];

    cin >> comanda;
    if (comanda != "atac")
        cin >> a >> b;
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
        // Toate perechile (a, b) cu a prim cu 26: 12 * 26 = 312 chei.
        for (a = 1; a < 26; a++)
        {
            int inversA = 0;  // numarul x pentru care (a * x) mod 26 = 1
            for (int x = 1; x < 26; x++)
                if ((a * x) % 26 == 1)
                    inversA = x;
            if (inversA == 0)
                continue;
            for (b = 0; b < 26; b++)
            {
                cout << "a=" << a << ", b=" << b << "\t";
                for (int i = 0; i < n; i++)
                {
                    if (pozitii[i] == -1)
                        cout << text[i];
                    else
                        cout << Alfabet_Latin[(inversA * (pozitii[i] - b + 26)) % 26];
                }
                cout << endl;
            }
        }
        return 0;
    }

    a = ((a % 26) + 26) % 26;
    b = ((b % 26) + 26) % 26;
    int inversA = 0;  // numarul x pentru care (a * x) mod 26 = 1
    for (int x = 1; x < 26; x++)
        if ((a * x) % 26 == 1)
            inversA = x;
    if (inversA == 0)
    {
        cerr << "afin_a";
        return 1;
    }

    for (int i = 0; i < n; i++)
    {
        if (pozitii[i] == -1)
            cout << text[i];
        else if (comanda == "cripteaza")
            cout << Alfabet_Latin[(a * pozitii[i] + b) % 26];
        else
            cout << Alfabet_Latin[(inversA * (pozitii[i] - b + 26)) % 26];
    }
    return 0;
}
