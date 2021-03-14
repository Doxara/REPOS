#include "Vector.h"
#include <string>
#include <iostream>

using namespace std; 

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
			swap(this->row, this->col);
			orientation = !orientation;
	}

	//��������������
	double& Vector::operator[](const unsigned R)
	{
			return this->data[R];
	}

	//���������� +=
	Vector& Vector::operator+=(const Vector& other)
	{
		Matrix::operator += (other);
		return *this;
	}
	//���������� -=
	Vector& Vector::operator-=(const Vector& other)
	{
		this->Matrix::operator-=(other);
		return *this;
	}

	//���������� *=
	Vector& Vector::operator*=(const Vector& other)
	{
		this->Matrix::operator*=(other);
		return *this;
	}
	//���������� *=k
	Vector& Vector::operator*=(const double k)
	{
		this->Matrix::operator*=(k);
		return *this;
	}
	//���������� - (�������)
	Vector Vector::operator-() const
	{
		return std::move(Vector(*this) *= -1.0);
	}

	//���������� *
	Vector operator*(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) *= rhs;
	}

	//���������� *k
	Vector operator*(const Vector& leftV, const double rightD)
	{
		return Vector(leftV) *= rightD;
	}
	//���������� k*
	Vector operator*(const double leftD, const Vector& rightV)
	{
		return Vector(rightV) *= leftD;
	}
	//���������� + (��������)
	Vector operator+(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) += rhs;
	}
	//���������� - (��������)
	Vector operator-(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) -= rhs;
	}
}