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
		//Конструкторы
		Matrix(unsigned mn = 0, const double* data = nullptr);
		Matrix(unsigned m, unsigned n, const double* data = nullptr);
		Matrix(unsigned mn, double (*func)(unsigned M, unsigned N, unsigned R, unsigned C));
		Matrix(unsigned m, unsigned n, double (*func)(unsigned M, unsigned N, unsigned R, unsigned C));
		Matrix(const Matrix& other);
		Matrix(Matrix&& m) noexcept;
		~Matrix();

		//Перегрузки операторов
		RowProxy operator[](const unsigned R);
		const RowProxy operator[](const unsigned R) const;
		//Перегрузка оператора присваивания
		Matrix& operator = (const Matrix& other);
		//перемещающий оператор присваивания
		Matrix& operator=(Matrix&& m) noexcept;
		//Перегрузка вывода
		friend std::ostream& operator<< (std::ostream& out, const Matrix& mat);
		//Перегрузка - (унарный)
		Matrix operator-() const;
		//Перегрузка *
		friend Matrix operator*(const Matrix& leftM, const Matrix& rightM);
		//Перегрузка *k
		friend Matrix operator*(const Matrix& leftM, const double rightD);
		//Перегрузка k*
		friend Matrix operator*(const double leftD, const Matrix& rightM);
		//Перегрузка + (бинарный)
		friend Matrix operator+(const Matrix& leftM, const Matrix& rightM);
		//Перегрузка - (бинарный)
		friend Matrix operator-(const Matrix& leftM, const Matrix& rightM);
		//Перегрузка +=
		Matrix& operator+=(const Matrix& other);
		//Перегрузка -=
		Matrix& operator-=(const Matrix& other);
		//Перегрузка *=
		Matrix& operator*=(const Matrix& other);
		//Перегрузка *=k
		Matrix& operator*=(const double k);

		//Гетеры
		unsigned int GetRow() const;
		unsigned int GetCol() const;
		static unsigned GetCount();
		unsigned GetID() const;
		double getMax() const;
		double getMin() const;

		//Проверка на возможность умножения
		bool isMultiply(const Matrix& other) const;
		//Проверка на возможность сложения/вычитания
		bool isSum(const Matrix& other) const;

	protected:
		double* data;	//Массив с данными матрицы	
		unsigned row;
		unsigned col;

	private:
		unsigned ID;
		static unsigned LotObj;
	};
	///Внешние функции

}