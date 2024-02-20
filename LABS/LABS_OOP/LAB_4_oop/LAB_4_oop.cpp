#include <iostream>
#include "Fract.h"
#include "Poli.h"

using namespace fr;
using namespace std;

int main()
{
    vector <double> arr = { 0,0,0,0,0 };
    Poli A(arr.size(), arr);
    A.printdata();
    A.delnum();
    A.printdata();
    //Fract a(5, 1);
    //Fract b(-8, -5);
    //vector <double> anonim = { 2, 6};
    //
 

    //Poli z((int)anonim.size(),anonim);
    //Poli g(15);
    //g.filldata();
    //z.printdata();

    //vector <double> c;
    //c.push_back(12);
    //c.push_back(1);
    //c.push_back(4);
    //
    //pair <Poli, Poli> res;
    //res = g.sub(z);
    //Poli h((int)c.size(),c);
    //h.printdata();
    ////Poli res = h / z;

    //res.first.printdata();
    //res.second.printdata();
    /*int mas[20][19];
    for (int i = 0, j = 0; i < 20 && j < 19; i++,j++)
    {
        cout << (mas[i][j] = i * j) << endl;
         
    }*/
    return 0;
}

