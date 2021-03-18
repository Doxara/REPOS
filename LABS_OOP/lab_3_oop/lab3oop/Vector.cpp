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

	//Индексирование
	double& Vector::operator[](const unsigned size)
	{
		if (size >= this->col * this->row)
			throw "Выход за границы, объект №" + this->GetID();
		return this->data[size];
	}

	const double& Vector::operator[](const unsigned size) const
	{
		if (size >= this->col * this->row)
			throw "Выход за границы, объект №" + this->GetID();
		return this->data[size];
	}

	//Перегрузка +=
	Vector& Vector::operator+=(const Vector& other)
	{
		Matrix::operator += (other);
		return *this;
	}
	//Перегрузка -=
	Vector& Vector::operator-=(const Vector& other)
	{
		this->Matrix::operator-=(other);
		return *this;
	}

	//Перегрузка *=
	Vector& Vector::operator*=(const Vector& other)
	{
		if ((other.col == other.row) && (other.row < 1))
			throw "Умножение векторов в результате даёт матрицу";
		this->Matrix::operator*=(other);
		return *this;
	}

	//Перегрузка *=k
	Vector& Vector::operator*=(const double k)
	{
		this->Matrix::operator*=(k);
		return *this;
	}

	//Перегрузка - (унарный)
	Vector Vector::operator-() const
	{
		return std::move(Vector(*this) *= -1.0);
	}

	//Перегрузка *
	Vector operator*(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) *= rhs;
	}

	//Перегрузка *k
	Vector operator*(const Vector& lhsV, const double rhsD)
	{
		return Vector(lhsV) *= rhsD;
	}

	//Перегрузка k*
	Vector operator*(const double lhsD, const Vector& rhsV)
	{
		return Vector(rhsV) *= lhsD;
	}

	//Перегрузка + (бинарный)
	Vector operator+(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) += rhs;
	}

	//Перегрузка - (бинарный)
	Vector operator-(const Vector& lhs, const Vector& rhs)
	{
		return Vector(lhs) -= rhs;
	}
}