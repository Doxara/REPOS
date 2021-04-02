#pragma once
#include <iostream>

namespace FR
{
	class Fract
	{
	public:
		Fract(int a = 0, int b = 1);

		Fract& operator+=(const Fract& other);
		Fract& operator-=(const Fract& other);
		Fract& operator*=(const Fract& other);
		Fract& operator/=(const Fract& other);
		friend Fract operator+(const Fract& lhs, const Fract& rhs);
		friend Fract operator-(const Fract& lhs, const Fract& rhs);
		friend Fract operator*(const Fract& lhs, const Fract& rhs);
		friend Fract operator/(const Fract& lhs, const Fract& rhs);
		friend std::ostream& operator<< (std::ostream& out, const Fract& fr);

		
	protected:
		int A, B;
		int NOD(int g, int h);
		void reduction();
		int DeComp();
	};
}