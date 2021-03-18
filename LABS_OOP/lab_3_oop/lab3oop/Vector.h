#pragma once 
#include "Matrix.h"
#include <iostream>

namespace MXSpace
{
	class Vector : public Matrix
	{
	public:

		//������������
		Vector(unsigned size = 0, bool orient = true, const double* data = nullptr);

		//���������� ����������
		double& operator[](const unsigned size);	//��������������
		const double& operator[](const unsigned size) const;	
		Vector& operator+=(const Vector& other);	//���������� +=
		Vector& operator-=(const Vector& other);	//���������� -=
		Vector& operator*=(const Vector& other);	//���������� *=
		Vector& operator*=(const double k);			//���������� *=k
		Vector operator-() const;					//���������� - (�������)
		friend Vector operator*(const Vector& lhs, const Vector& rhs);	//���������� *
		friend Vector operator*(const Vector& lhsV, const double rhsD);	//���������� *k
		friend Vector operator*(const double lhsD, const Vector& rhsV);	//���������� k*
		friend Vector operator+(const Vector& lhs, const Vector& rhs);	//���������� + (��������)
		friend Vector operator-(const Vector& lhs, const Vector& rhs);	//���������� - (��������)

		//������
		bool get_orient() const;	//��������� ���������� �������
		void change_orient();		//��������� ���������� �������

	private:
		bool orientation;	//���� ������, �� true
	};
}