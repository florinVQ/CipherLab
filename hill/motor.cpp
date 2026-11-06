// Cifrul Hill cu matrice n x n (n = 2, 4, 6 sau 8) si alfabet dat de utilizator.
//   C = matrice * P   (mod m)
// m este numarul modular = numarul de caractere ale alfabetului (la alfabetul latin m = 26).
// La criptare matricea este matricea cheie K.
// La decriptare matricea este matricea modular inversa K^-1 (K * K^-1 = I mod m);
// programul NU calculeaza inversa, o introduci tu.
// Date citite de la tastatura (sau de la interfata Python):
//   cripteaza n m a11 a12 ... ann      (matricea, rand cu rand)   |   decripteaza n m a11 ... ann
//   alfabetul (toate caracterele, pe o linie)
//   textul, pe o singura linie
#include <iostream>
using namespace std;

const int MAX = 10000;

int main()
{
    string comanda, Alfabet, text;
    int n, m;
    int matrice[8][8];
    int numere[MAX + 8];  // caracterele textului, ca numere 0..m-1
    int nr = 0;

    cin >> comanda >> n >> m;
    if (n != 2 && n != 4 && n != 6 && n != 8)
    {
        cerr << "hill_dim";
        return 1;
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> matrice[i][j];
    cin.ignore(1000, '\n');
    getline(cin, Alfabet);
    getline(cin, text);

    if (m < 2 || m != Alfabet.length())
    {
        cerr << "hill_modul";
        return 1;
    }
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Numerele negative din matrice devin pozitive (modulo m).
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            matrice[i][j] = ((matrice[i][j] % m) + m) % m;

    // Pastram doar caracterele care se afla in alfabet.
    for (int i = 0; i < text.length(); i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (text[i] == Alfabet[j])
            {
                numere[nr] = j;
                nr++;
            }
        }
    }
    // Completam ultimul bloc cu ultimul caracter al alfabetului.
    while (nr % n != 0)
    {
        numere[nr] = m - 1;
        nr++;
    }

    // Fiecare bloc de n caractere se inmulteste cu matricea.
    for (int bloc = 0; bloc < nr; bloc += n)
    {
        for (int linie = 0; linie < n; linie++)
        {
            int suma = 0;
            for (int coloana = 0; coloana < n; coloana++)
                suma = suma + matrice[linie][coloana] * numere[bloc + coloana];
            cout << Alfabet[suma % m];
        }
    }
    return 0;
}
