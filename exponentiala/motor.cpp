#include <iostream>
#include <string>
using namespace std;

const int MAX = 10000;
const long long MAX_MODUL = 2000000000;  // asa z * z incape intr-un long long
const int PRIMUL_COD = 10;               // primul caracter al alfabetului are codul 10 (A = 10, B = 11, ...)

bool estePrim(long long n)
{
    if (n < 2)
        return false;
    for (long long d = 2; d * d <= n; d++)
        if (n % d == 0)
            return false;
    return true;
}

long long cmmdc(long long a, long long b)
{
    while (b != 0)
    {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

// Inversul lui e modulo n, cu algoritmul lui Euclid extins (presupune cmmdc(e, n) = 1).
long long inversModulo(long long e, long long n)
{
    long long t0 = 0, t = 1, r0 = n, r = e % n;
    while (r != 0)
    {
        long long q = r0 / r;
        long long aux = t0 - q * t;
        t0 = t;
        t = aux;
        aux = r0 - q * r;
        r0 = r;
        r = aux;
    }
    return ((t0 % n) + n) % n;
}

string inBaza2(long long c)
{
    if (c == 0)
        return "0";
    string cifre = "";
    while (c > 0)
    {
        cifre = char('0' + c % 2) + cifre;
        c /= 2;
    }
    return cifre;
}

// x^c mod n, prin ridicari la patrat repetate. Fiecare pas se scrie ca rand
// "PAS  numarul pasului  bitul ci  z dupa ridicarea la patrat  z dupa inmultirea cu x (sau -)".
long long exponentiereModulara(long long x, long long c, long long n)
{
    string biti = inBaza2(c);
    long long z = 1;
    x = x % n;
    for (int i = 0; i < biti.length(); i++)
    {
        z = z * z % n;
        cout << "PAS\t" << i + 1 << "\t" << biti[i] << "\t" << z << "\t";
        if (biti[i] == '1')
        {
            z = z * x % n;
            cout << z;
        }
        else
            cout << "-";
        cout << endl;
    }
    return z;
}

// Intrare:
//   cripteaza p e k          + alfabetul + textul (k = cate caractere intra intr-un bloc)
//   decripteaza p e          + alfabetul + numerele criptate
//   putere x c n             + o linie fara importanta (doar x^c mod n, pas cu pas)
// Iesire: randuri despartite prin tab: EXPONENT, BLOC, PAS, INVERS, REZULTAT.
int main()
{
    string comanda, Alfabet, text;
    long long p, e, k = 0;

    cin >> comanda;
    if (comanda == "putere")
    {
        long long x, c, n;
        cin >> x >> c >> n;
        if (n < 2 || n > MAX_MODUL || x < 0 || c < 0)
        {
            cerr << "exp_putere";
            return 1;
        }
        cout << "EXPONENT\t" << c << "\t" << inBaza2(c) << endl;
        long long r = exponentiereModulara(x, c, n);
        cout << "REZULTAT\t" << r << endl;
        return 0;
    }

    cin >> p >> e;
    if (comanda == "cripteaza")
        cin >> k;
    cin >> Alfabet;
    getline(cin >> ws, text);

    if (p > MAX_MODUL || !estePrim(p))
    {
        cerr << "exp_p";
        return 1;
    }
    if (e < 1 || cmmdc(e, p - 1) != 1)
    {
        cerr << "exp_e";
        return 1;
    }
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }
    long long a = inversModulo(e, p - 1);
    cout << "INVERS\t" << a << endl;

    if (comanda == "cripteaza")
    {
        if (k < 1 || k > 4)
        {
            cerr << "exp_k";
            return 1;
        }
        cout << "EXPONENT\t" << e << "\t" << inBaza2(e) << endl;
        // Fiecare bloc de k caractere devine numarul M format din codurile lor (A = 10, ...).
        for (int inceput = 0; inceput < text.length(); inceput += k)
        {
            string bloc = text.substr(inceput, k);
            long long M = 0;
            for (int i = 0; i < bloc.length(); i++)
                M = M * 100 + Alfabet.find(bloc[i]) + PRIMUL_COD;
            if (M >= p)
            {
                cerr << "exp_bloc";
                return 1;
            }
            cout << "BLOC\t" << bloc << "\t" << M << endl;
            long long Y = exponentiereModulara(M, e, p);
            cout << "Y\t" << Y << endl;
        }
        return 0;
    }

    // Decriptare: M = Y^a mod p, apoi M se imparte in coduri de cate 2 cifre, de la dreapta.
    cout << "EXPONENT\t" << a << "\t" << inBaza2(a) << endl;
    text = text + " ";
    string numar = "";
    for (int i = 0; i < text.length(); i++)
    {
        if (text[i] >= '0' && text[i] <= '9')
        {
            numar = numar + text[i];
            continue;
        }
        if (numar == "")
            continue;
        if (numar.length() > 10 || stoll(numar) >= p)
        {
            cerr << "exp_y";
            return 1;
        }
        long long Y = stoll(numar);
        numar = "";
        cout << "BLOC_Y\t" << Y << endl;
        long long M = exponentiereModulara(Y, a, p);

        string bloc = "";
        for (long long rest = M; rest > 0; rest /= 100)
        {
            int cod = rest % 100 - PRIMUL_COD;
            if (cod < 0 || cod >= Alfabet.length())
            {
                cerr << "exp_cod";
                return 1;
            }
            bloc = Alfabet[cod] + bloc;
        }
        cout << "M\t" << M << "\t" << bloc << endl;
    }
    return 0;
}
