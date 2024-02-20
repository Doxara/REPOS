#include <iostream>
#pragma once

namespace MXSpace
{
	class Matrix
	{
	private:
		class RowProxy
		{
		public:
			RowProxy(const Matrix* A, unsigned R);
			double& operator[]	(unsigned C);
			double	operator[]	(unsigned C) const;
		private:
			unsigned R;
			const Matrix* A;
		};

	public:
		//������������
		Matrix(unsigned mn = 0, const double* data = nullptr);
		Matrix(unsigned m, unsigned n, const double* data = nullptr);
		Matrix(unsigned mn, double (*func)(unsigned M, unsigned N, unsigned R, unsigned C));
		Matrix(unsigned m, unsigned n, double (*func)(unsigned M, unsigned N, unsigned R, unsigned C));
		Matrix(const Matrix& other);
		Matrix(Matrix&& m) noexcept;
		~Matrix();

		//���������� ����������
		RowProxy operator[](const unsigned R);
		const RowProxy operator[](const unsigned R) const;
		//���������� ��������� ������������
		Matrix& operator = (const Matrix& other);
		//������������ �������� ������������
		Matrix& operator=(Matrix&& m) noexcept;
		//���������� ������
		friend std::ostream& operator<< (std::ostream& out, const Matrix& mat);
		//���������� - (�������)
		Matrix operator-() const;
		//���������� *
		friend Matrix operator*(const Matrix& leftM, const Matrix& rightM);
		//���������� *k
		friend Matrix operator*(const Matrix& leftM, const double rightD);
		//���������� k*
		friend Matrix operator*(const double leftD, const Matrix& rightM);
		//���������� + (��������)
		friend Matrix operator+(const Matrix& leftM, const Matrix& rightM);
		//���������� - (��������)
		friend Matrix operator-(const Matrix& leftM, const Matrix& rightM);
		//���������� +=
		Matrix& operator+=(const Matrix& other);
		//���������� -=
		Matrix& operator-=(const Matrix& other);
		//���������� *=
		Matrix& operator*=(const Matrix& other);
		//���������� *=k
		Matrix& operator*=(const double k);

		//������
		unsigned int GetRow() const;
		unsigned int GetCol() const;
		static unsigned GetCount();
		unsigned GetID() const;
		double getMax() const;
		double getMin() const;

		//�������� �� ����������� ���������
		bool isMultiply(const Matrix& other) const;
		//�������� �� ����������� ��������/���������
		bool isSum(const Matrix& other) const;

	protected:
		double* data;	//������ � ������� �������	
		unsigned row;
		unsigned col;

	private:
		unsigned ID;
		static unsigned LotObj;
	};
	///������� �������

}