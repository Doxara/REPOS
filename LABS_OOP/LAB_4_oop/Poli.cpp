#include "Poli.h"
#include <cmath>
#include <algorithm>

namespace FR
{
	double Poli::operator()(int X)
	{
		double res = 0.0;
		for (unsigned i = 0; i < this->data.size(); i++)
		{
			res += data[i] * pow(X, i);
		}
		return res;
	}

	Poli& Poli::operator*=(const Poli& other)
	{
		for (unsigned i = 0; i < std::min(other.data.size(), this->data.size()); i++)
		{
			this->data[i] *= other.data[i];
		}
		return *this;
	}

	Poli& Poli::operator/=(const Poli& other)
	{
		for (unsigned i = 0; i < std::min(other.data.size(), this->data.size()); i++)
		{
			this->data[i] /= other.data[i];
		}
		return *this;
	}

	Poli& Poli::operator+=(const Poli& other)
	{
		for (unsigned i = 0; i < std::min(other.data.size(), this->data.size()); i++)
		{
			this->data[i] += other.data[i];
		}
		return *this;
	}

	Poli& Poli::operator-=(const Poli& other)
	{
		for (unsigned i = 0; i < std::min(other.data.size(), this->data.size()); i++)
		{
			this->data[i] -= other.data[i];
		}
		return *this;
	}

	Poli operator+(const Poli& lhs, const Poli& rhs)
	{
		return Poli(lhs) += rhs;
	}

	Poli operator-(const Poli& lhs, const Poli& rhs)
	{
		return Poli(lhs) -= rhs;
	}

	Poli operator*(const Poli& lhs, const Poli& rhs)
	{
		return std::move(Poli(lhs)) *= rhs;
	}

	Poli operator/(const Poli& lhs, const Poli& rhs)
	{
		return std::move(Poli(lhs)) /= rhs;
	}

	void Poli::filldata(int a, int n)
	{
		if (n > 0)
		{
			if (a == 0)
			{
				for (int i = 0; i < n; i++)
				{
					this->data.push_back(rand() % 10);
				}
			}
			else
			{
				for (int i = 0; i < n; i++)
				{
					this->data.push_back(a);
				}
			}
		}
	}
	void Poli::printdata()
	{
		for (int i = 0; i < this->data.size(); i++)
		{
			std::cout << this->data[i] << std::endl;
		}
		std::cout << std::endl;
	}
}
