#pragma once
#include <vector>
#include <iostream>

namespace fr
{
	class Poli
	{
		std::vector <double> data;		//i=0 x^0, i=1 x^1..., i=n x^n
	public:
		Poli(int n = 0, std::vector <double> dat = { 0 });
		Poli(const Poli& other);
		Poli(Poli&& m) noexcept;

		double operator()(int X);
		Poli& operator+=(const Poli& other);
		Poli& operator-=(const Poli& other);
		Poli& operator*=(const Poli& other);
		friend Poli operator+(const Poli& lhs, const Poli& rhs);
		friend Poli operator-(const Poli& lhs, const Poli& rhs);
		friend Poli operator*(const Poli& lhs, const Poli& rhs);
		friend Poli operator/(const Poli& lhs, const Poli& rhs);
		Poli& operator = (const Poli& other);
		Poli& operator = (Poli&& m) noexcept;

		std::pair <Poli, Poli> sub(const Poli& right);
		Poli NOD(const Poli& A, const Poli& B);
		void delnum();
		void filldata(int a = 0, int n = 1);
		void printdata();
	};
}
