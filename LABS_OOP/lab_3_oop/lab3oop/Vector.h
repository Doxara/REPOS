#pragma once 
#include "Matrix.h"
#include <string>
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
		Vector& operator+=(const Vector& other);	//���������� +=
		Vector& operator-=(const Vector& other);	//���������� -=
		Vector& operator*=(const Vector& other);	//���������� *=
		Vector& operator*=(const double k);			//���������� *=k
		Vector operator-() const;					//���������� - (�������)
		friend Vector operator*(const Vector& lhs, const Vector& rhs);	//���������� *
		friend Vector operator*(const Vector& leftV, const double rightD);	//���������� *k
		friend Vector operator*(const double leftD, const Vector& rightV);	//���������� k*
		friend Vector operator+(const Vector& lhs, const Vector& rhs);	//���������� + (��������)
		friend Vector operator-(const Vector& lhs, const Vector& rhs);	//���������� - (��������)

		//������
		bool get_orient() const;	//��������� ���������� �������
		void change_orient();		//��������� ���������� �������
	private:
		bool orientation;	//���� ������, �� true
		
	};
}