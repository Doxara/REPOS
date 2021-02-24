#include "Vector.h"

namespace MXSpace
{
	Vector::Vector(int size) : Matrix(1, size)
	{
		for (int i = 0; i < size; i++)
		{
			this->data[i] = 0;
		}
	}
}