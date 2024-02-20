#include "Vector.h"
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
	double& Vector::operator[](const unsigned size)
	{
		if (size >= this->col * this->row)
			throw "����� �� �������, ������ �" + this->GetID();
		return this->data[size];
	}

	const double& Vector::operator[](const unsigned size) const
	{
		if (size >= this->col * this->row)
			throw "����� �� �������, ������ �" + this->GetID();
		return this->data[size];
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
		if ((other.col == other.row) && (other.row < 1))
			throw "��������� �������� � ���������� ��� �������";
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
	Vector operator*(const Vector& lhsV, const double rhsD)
	{
		return Vector(lhsV) *= rhsD;
	}

	//���������� k*
	Vector operator*(const double lhsD, const Vector& rhsV)
	{
		return Vector(rhsV) *= lhsD;
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