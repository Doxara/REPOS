#include <iostream>
#include "Fract.h"
#include "Poli.h"

using namespace FR;
using namespace std;

int main()
{
   
    Fract a(5, 1);
    Fract b(-8, -5);
    Poli z, g;
    z.filldata(0, 15);
    g.filldata(3, 13);
    z.printdata();
    g.printdata();
    g -= z;
    
    g.printdata();
    
    return 0;
}

