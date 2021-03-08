#include <iostream>
#include "Matrix.h"
#include "Vector.h"

using namespace std;
using namespace MXSpace;


int main()
{
	setlocale(LC_ALL, "rus");
	/*Matrix A;
	Matrix X(1);
	Matrix Z(2, 3);
	Matrix CAL(1, 3, s);*/
	Matrix A(3,3);
	A[0][0] = 1;
	A[0][1] = 2;
	A[0][2] = 3;
	A[1][0] = 4;
	A[1][1] = 5;
	A[1][2] = 6;
	A[2][0] = 7;
	A[2][1] = 8;
	A[2][2] = 9;
	Vector J(3);
	J[1] = 22;
	Matrix C(3,1);
	C[0][0] = 1;
	C[1][0] = 1;
	C[2][0] = 1;

	cout << "Matrix A = " << A << "Matrix C = " << C << "Vector J = " << J << endl;
	

	cout << "A * C = " << J * A << endl;
	return 0;
}


