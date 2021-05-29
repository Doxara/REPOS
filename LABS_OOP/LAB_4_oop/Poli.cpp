#include "Poli.h"
#include <cmath>
#include <algorithm>


using namespace std;

namespace fr
{
	Poli::Poli(int n, std::vector<double> dat)
	{
		if (!dat.empty())
			this->data = dat;
		if(n!=0)
			this->data.resize(n);
	}

	Poli::Poli(const Poli& other) : Poli()
	{
		*this = other;
	}

	Poli::Poli(Poli&& m) noexcept :Poli()
	{
		*this = std::move(m);
	}

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

	Poli& Poli::operator=(const Poli& other)
	{
		if (this == &other) //Проверка на самоприсваивание
			return *this;

		auto otherSize = other.data.size();
		if (otherSize > 0 && otherSize>=data.size()) 
			std::copy(other.data.begin(), other.data.end(), this->data.begin());

		return *this;
	}

	//Перемещающий оператор присваивания
	Poli& Poli::operator=(Poli&& m) noexcept
	{
		if (this == &m) 
			return *this;
		if (!this->data.empty()) 
			this->data.clear();
		std::swap(this->data, m.data);
		return *this;
	}




	bool Equal(double x, double y)
	{
		return fabs(x - y) < (double)1e-9;
	}

	pair <Poli, Poli> Poli::sub(const Poli& right)
	{
		int n = (int)this->data.size();
		int m = (int)right.data.size();
		if (n == m == 0)
			throw - 1; 
		if (n < m)
			throw -1;

		Poli Q(n - m + 1);
		Poli A(*this);
		for (int i = n; i >= m; i--)
		{
			Q.data[i - m] = A.data[i] / right.data[m];
			for (int j = m; j >= 0; j--)
				A.data[i - m + j] -= right.data[j] * Q.data[i - m];
		}
		A.data.resize(m);
		while (A.data.size() > 1 && Equal(A.data.back(), 0))
			A.data.pop_back();
		return make_pair(Q,A);
	}

	//Poli operator/(const Poli& left, const Poli& right)
	//{
	//	/*pair <Poli, Poli> res;
	//	res.first = 
	//	return res.first;*/
	//}
		/*
	Poli Poli::NOD(const Poli& A, const Poli& B)
	{
		return A;
	}
	*/
	void Poli::filldata(int a, int n)
	{
		if (n > 0)
		{
			if (a == 0)
			{
				for (int i = 0; i < n; i++)
				{
					this->data.push_back((rand() % 10));
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

	void Poli::delnum()
	{
		int idx = this->data.size() - 1;
		bool lastIsNul = true;
		while (lastIsNul && idx > 0)
		{
			if (lastIsNul = this->data[idx] == 0)
			{
				this->data.pop_back();
				idx--;
			}
		}
	}



	void Poli::printdata()
	{
		for (auto i = 0; i < this->data.size(); i++)
		{
			
				std::cout << this->data[i] << "  ";
		}
		std::cout << std::endl;
	}


}
