#include "Vector.h"

namespace MXSpace
{
	Vector::Vector(unsigned size, bool orient, const double* data) : Matrix(1, size, data)
	{
		if (!orient)
		{
			std::swap(this->row, this->col);
		}
		this->orientation = orient;
	}

	bool Vector::get_orient() const
	{
		return orientation;
	}

	void Vector::change_orient()
	{
			std::swap(this->row, this->col);
			orientation = !orientation;
	}

	double& Vector::operator[](const unsigned R)
	{
			return this->data[R];
	}

	Vector& Vector::operator+=(const Vector& other)
	{
		Matrix::operator += (other);
		return *this;
	}

}