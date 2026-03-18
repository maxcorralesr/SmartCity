#include <iostream>
#include "operations.h"
using namespace std;
int main() {
    int option;
    double a, b;
    cout << "Mini Calculadora Colaborativa\n";
    cout << "1. Sumar\n2. Restar\n3. Multiplicar\n4. Dividir\n";
    cout << "Elige una opción: ";
    cin >> option;
    cout << "Ingresa dos números: ";
    cin >> a >> b;
    switch(option) {
        case 1: cout << "Resultado: " << add(a, b); break;
        case 2: cout << "Resultado: " << subtract(a, b); break;
        case 3: cout << "Resultado: " << multiply(a, b); break;
        case 4: cout << "Resultado: " << divide(a, b); break;
        default: cout << "Opción inválida";
    }
    cout << endl;
    return 0;
}
