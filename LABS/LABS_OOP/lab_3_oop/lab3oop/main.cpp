#include <iostream>
#include "Matrix.h"
#include "Vector.h"

using namespace std;
using namespace MXSpace;

/*
Vector + Vector = Vector (при сложении объектов Векторов – результат тоже Вектор)
Matrix + Matrix = Matrix
Vector + Matrix = Matrix
*/

int main()
{
	setlocale(LC_ALL, "rus");

	Vector B(3, true);
	B[0] = 11;
	B[1] = 22;
	B[2] = 33;
	Vector J(3, true);
	J[0] = 35;
	J[1] = 22;
	J[2] = 33;
	Matrix C(1,3);
	C[0][0] = 1;
	C[0][1] = 1;
	C[0][2] = 1;
	Vector Z(0);
	cout << Z.get_orient() << J << endl;

	Matrix* mat;
	Vector* vec = new Vector();

	mat = (Matrix*) vec;

	Matrix& H = J;
	cout << J << J.get_orient() << endl;

	delete mat;
	delete vec;

	return 0;
}


