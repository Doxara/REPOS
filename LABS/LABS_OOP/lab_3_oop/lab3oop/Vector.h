#pragma once 
#include "Matrix.h"
#include <iostream>

namespace MXSpace
{
	class Vector : public Matrix
	{
	public:

		//Конструкторы
		Vector(unsigned size = 0, bool orient = true, const double* data = nullptr);

		//Перегрузка операторов
		double& operator[](const unsigned size);	//Индексирование
		const double& operator[](const unsigned size) const;	
		Vector& operator+=(const Vector& other);	//Перегрузка +=
		Vector& operator-=(const Vector& other);	//Перегрузка -=
		Vector& operator*=(const Vector& other);	//Перегрузка *=
		Vector& operator*=(const double k);			//Перегрузка *=k
		Vector operator-() const;					//Перегрузка - (унарный)
		friend Vector operator*(const Vector& lhs, const Vector& rhs);	//Перегрузка *
		friend Vector operator*(const Vector& lhsV, const double rhsD);	//Перегрузка *k
		friend Vector operator*(const double lhsD, const Vector& rhsV);	//Перегрузка k*
		friend Vector operator+(const Vector& lhs, const Vector& rhs);	//Перегрузка + (бинарный)
		friend Vector operator-(const Vector& lhs, const Vector& rhs);	//Перегрузка - (бинарный)

		//Методы
		bool get_orient() const;	//Получение ориентации вектора
		void change_orient();		//Изменение ориентации вектора

	private:
		bool orientation;	//Если строка, то true
	};
}