#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;

string patrat;       // caracterele dreptunghiului, citite rand cu rand
int randuri, coloane;

// Daca o pereche are doua caractere la fel, intre ele se pune caracterul de completare.
// Daca dublura este chiar caracterul de completare, se foloseste urmatorul din alfabet.
char completarePentru(char c, char completare, string Alfabet)
{
    if (c != completare)
        return completare;
    return Alfabet[(Alfabet.find(completare) + 1) % Alfabet.length()];
}

// Transforma perechea (a, b). pas = 1 la criptare, pas = -1 la decriptare.
string transformaPerechea(char a, char b, int pas)
{
    int pa = patrat.find(a), pb = patrat.find(b);
    int ra = pa / coloane, ca = pa % coloane;
    int rb = pb / coloane, cb = pb % coloane;

    if (ra == rb)  // pe acelasi rand: caracterul din dreapta (stanga la decriptare)
    {
        ca = (ca + pas + coloane) % coloane;
        cb = (cb + pas + coloane) % coloane;
    }
    else if (ca == cb)  // pe aceeasi coloana: caracterul de dedesubt (deasupra la decriptare)
    {
        ra = (ra + pas + randuri) % randuri;
        rb = (rb + pas + randuri) % randuri;
    }
    else  // dreptunghi: fiecare ia coloana celuilalt
    {
        int aux = ca;
        ca = cb;
        cb = aux;
    }
    string rezultat = "";
    rezultat = rezultat + patrat[ra * coloane + ca] + patrat[rb * coloane + cb];
    return rezultat;
}

// Intrare: comanda, cuvantul-cheie, caracterul de completare, alfabetul, textul.
int main()
{
    string comanda, cuvant, completare, Alfabet, text;

    cin >> comanda >> cuvant >> completare >> Alfabet >> text;
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }

    // Dreptunghiul: cel mai mare numar de randuri r <= radical din m care il imparte pe m.
    int m = Alfabet.length();
    randuri = 0;
    for (int r = 2; r * r <= m; r++)
        if (m % r == 0)
            randuri = r;
    if (randuri == 0)
    {
        cerr << "playfair_alfabet";
        return 1;
    }
    coloane = m / randuri;

    // Cuvantul-cheie (fara repetari), apoi restul alfabetului.
    patrat = "";
    string sir = cuvant + Alfabet;
    for (int i = 0; i < sir.length(); i++)
        if (patrat.find(sir[i]) == string::npos)
            patrat = patrat + sir[i];

    char c = completare[0];
    int pas = 1;
    if (comanda == "decripteaza")
        pas = -1;

    int i = 0;
    while (i < text.length())
    {
        char a = text[i];
        char b;
        if (comanda == "cripteaza" && (i + 1 == text.length() || text[i + 1] == a))
        {
            b = completarePentru(a, c, Alfabet);  // dublura sau ultimul caracter ramas singur
            i += 1;
        }
        else if (i + 1 == text.length())
        {
            cerr << "playfair_impar";
            return 1;
        }
        else
        {
            b = text[i + 1];
            i += 2;
        }
        cout << transformaPerechea(a, b, pas);
    }
    return 0;
}
