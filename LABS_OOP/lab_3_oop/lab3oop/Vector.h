#pragma once 
#include "Matrix.h"
#include <string>
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
		Vector& operator+=(const Vector& other);	//Перегрузка +=
		Vector& operator-=(const Vector& other);	//Перегрузка -=
		Vector& operator*=(const Vector& other);	//Перегрузка *=
		Vector& operator*=(const double k);			//Перегрузка *=k
		Vector operator-() const;					//Перегрузка - (унарный)
		friend Vector operator*(const Vector& lhs, const Vector& rhs);	//Перегрузка *
		friend Vector operator*(const Vector& leftV, const double rightD);	//Перегрузка *k
		friend Vector operator*(const double leftD, const Vector& rightV);	//Перегрузка k*
		friend Vector operator+(const Vector& lhs, const Vector& rhs);	//Перегрузка + (бинарный)
		friend Vector operator-(const Vector& lhs, const Vector& rhs);	//Перегрузка - (бинарный)

		//Методы
		bool get_orient() const;	//Получение ориентации вектора
		void change_orient();		//Изменение ориентации вектора
	private:
		bool orientation;	//Если строка, то true
		
	};
}