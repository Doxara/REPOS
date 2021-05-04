#include "Fract.h"
#include <iostream>

namespace fr
{
	Fract::Fract(int a, int b) : A(a),B(b)
	{
		if (b == 0)
			throw "������ ������ �� ����";
		if (b < 0)
		{
			b = -b;
			a = -a;
		}
		this->A = a;
		this->B = b;
	}

	Fract::Fract(const Fract& other) : Fract()
	{
		*this = other;
	}

	Fract::Fract(Fract&& m) noexcept :Fract()
	{
		*this = std::move(m);
	}

	Fract& Fract::operator*=(const Fract& other)
	{
		this->A *= other.A;
		this->B *= other.B;
		reduction();
		return *this;
	}

	Fract& Fract::operator/=(const Fract& other)
	{
		this->A *= other.B;
		this->B *= other.A;
		reduction();
		return *this;
	}

	Fract& Fract::operator+=(const Fract& other)
	{
		this->A *= other.B;
		this->A += other.A * this->B;
		this->B *= other.B;
		reduction();
		return *this;
	}

	Fract& Fract::operator-=(const Fract& other)
	{
		this->A *= other.B;
		this->A -= other.A * this->B;
		this->B *= other.B;
		reduction();
		return *this;
	}

	Fract operator+(const Fract& lhs, const Fract& rhs)
	{
		return Fract(lhs) += rhs;
	}

	Fract operator-(const Fract& lhs, const Fract& rhs)
	{
		return Fract(lhs) -= rhs;
	}

	Fract operator*(const Fract& lhs, const Fract& rhs)
	{
		return std::move(Fract(lhs)) *= rhs;
	}

	Fract operator/(const Fract& lhs, const Fract& rhs)
	{
		return std::move(Fract(lhs)) /= rhs;
	}

	Fract& Fract::operator=(const Fract& other)
	{
		if (this == &other) 
			return *this;
		this->A = other.A;
		this->B = other.B;
		return *this;
	}

	Fract& Fract::operator=(Fract&& m) noexcept
	{
		if (this == &m) return *this;

		std::swap(this->A, m.A);
		std::swap(this->B, m.B);
		return *this;
	}

	std::ostream& operator<<(std::ostream& out, const Fract& fr)
	{
		out << fr.A << "/" << fr.B << std::endl;
		return out;
	}

	int Fract::NOD (int g, int h)
	{
		if (g == 0 || h == 0)
			return 1;

		g = abs(g);
		h = abs(h);
		
		while (g != h)
		{
			if (g > h)
				g -= h;
			else
				h -= g;
		}
		return g;
	}

	void Fract::reduction() 
	{
		int nod = NOD(this->A, this->B);
		this->A /= nod;
		this->B /= nod;
	}

	int Fract::DeComp()
	{
		int a = this->A / this->B;
		this->A = this->A % this->B;
		return a;
	}
}
