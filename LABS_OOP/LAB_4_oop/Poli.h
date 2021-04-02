#pragma once
#include <vector>
#include <iostream>

namespace FR
{
	class Poli
	{
		std::vector <double> data;
	public:
		double operator()(int X);
		Poli& operator+=(const Poli& other);
		Poli& operator-=(const Poli& other);
		Poli& operator*=(const Poli& other);
		Poli& operator/=(const Poli& other);
		friend Poli operator+(const Poli& lhs, const Poli& rhs);
		friend Poli operator-(const Poli& lhs, const Poli& rhs);
		friend Poli operator*(const Poli& lhs, const Poli& rhs);
		friend Poli operator/(const Poli& lhs, const Poli& rhs);

		void filldata(int a = 0, int n = 1);
		void printdata();
	};
}
