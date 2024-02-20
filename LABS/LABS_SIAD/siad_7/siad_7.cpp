#include <iostream>
#include <string>
#include <fstream>
#include "Graph.h"
#include <vector>

using namespace std;
using namespace g;


int main()
{
    setlocale(LC_ALL, "rus");
    string name = "input.txt";
    fstream File(name);
    int N, iter = 1;
    string str;
    vector <int> v;
    auto ptr = str.c_str();
    char* endptr = nullptr;

    File >> N;
    Graph a(N);
    File.get();
    while (!File.eof() && iter != N)
    {
        for (int i = 0; i < N; i++)
        {
            getline(File, str);
            ptr = str.c_str();
            while (ptr != str.c_str() + str.size()) {
                auto value = strtol(ptr, &endptr, 10);
                if (ptr == endptr) {
                    ptr++;
                }
                else {
                    ptr = endptr;
                    v.push_back(value);
                }
            }
            if (v.size() > (size_t)1)
            {
                a.addEdgeNotOrient(v[0], v[1], v[2]);
            }
            if (!v.empty())
                v.clear();
            iter++;
        }
    }
    
    a.print();
    
    a.showShortestPathAll ();
    
    

    

    
    return 0;
}