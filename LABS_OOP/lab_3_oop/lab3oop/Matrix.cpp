#include <iostream>
#include <iomanip>
#include "Matrix.h"



namespace MXSpace
{
	unsigned Matrix::LotObj = 0;

	//---------��������������---------------
	Matrix::RowProxy::RowProxy(const Matrix* A, unsigned R)
	{
		this->R = R;
		this->A = A;
	}

	double& Matrix::RowProxy::operator[](unsigned C)
	{
		if (C >= A->col)
			throw "����� �� �������, ������ �" + A->ID;

		return A->data[R * A->col + C]; //����������� ������ �� ��-� �������
	}

	double Matrix::RowProxy::operator[](unsigned C) const
	{
		if (C >= A->col)
			throw "����� �� �������, ������ �" + A->ID;

		return A->data[R * A->col + C]; //����������� �������� �� ��-� �������
	}

	//���������� ��������������:
	Matrix::RowProxy Matrix::operator[](const unsigned R)
	{
		return RowProxy(this, R); //���������� ������ ���������������� ������
	}
	const Matrix::RowProxy Matrix::operator[](const unsigned R) const
	{
		return RowProxy(this, R); //���������� ������ ���������������� ������
	}


	//������������

	//����������� ��� ���������� �������
	Matrix::Matrix(unsigned mn, const double* data) : Matrix(mn, mn, data) {}

	//����������� ��� ��������� ������� � ��������� ��������� 
	Matrix::Matrix(unsigned m, unsigned n, const double* _data) : ID(LotObj++)
	{
		std::cout << "�������� �����������:" << ID << std::endl;
		if (m == 0 || n == 0)
		{
			this->data = nullptr;
			this->row = this->col = 0;
			return;
		}

		this->row = m;
		this->col = n;

		if (_data != nullptr)
		{
			this->data = new double[row * col];
			std::copy(data, data + row * col, this->data);
		}
		else
		{
			this->data = new double[row * col]();
		}
	}

	//����������� � ��������� �������� � ����������(��)
	Matrix::Matrix(unsigned mn, double(*func)(unsigned M, unsigned N, unsigned R, unsigned C)) :Matrix::Matrix(mn, mn, func)
	{
	}

	//����������� � ��������� �������� � ���������� (��)
	Matrix::Matrix(unsigned m, unsigned n, double (*func)(unsigned M, unsigned N, unsigned R, unsigned C)) : Matrix::Matrix(row, col)
	{
		for (unsigned int i = 0; i < row; i++)
		{
			for (unsigned int j = 0; j < col; j++)
			{
				this->data[i * col + j] = func(i, j, row, col);
			}
		}
	}

	//����������� �����������
	Matrix::Matrix(const Matrix& other) :Matrix()
	{
		int digitsInNum = (int)ceil(log10(ID + 0.5));
		std::cout << "\033[27C";
		for (int i = 0; i < digitsInNum; i++) std::cout << "\033[C";
		std::cout << "\033[A";
		std::cout << "�������� ����������� �����������:" << ID << std::endl;
		*this = other;
	}

	//����������� �����������
	Matrix::Matrix(Matrix&& m) noexcept :Matrix()
	{
		int digitsInNum = (int)ceil(log10(ID + 0.5));
		std::cout << "\033[27C";
		for (int i = 0; i < digitsInNum; i++) std::cout << "\033[C";
		std::cout << "\033[A";
		std::cout << "�������� ����������� �����������:" << ID << std::endl;
		*this = std::move(m);
	}

	//���������� 
	Matrix::~Matrix()
	{
		std::cout << "�������� ����������:" << ID << std::endl;
		if (this->data != nullptr)
		{
			delete[] this->data;
			this->data = nullptr;
		}
		LotObj--;
		ID = LotObj;
	}

	//���������� ��������� "="
	Matrix& Matrix::operator=(const Matrix& other)
	{
		if (this == &other) //�������� �� ����������������
			return *this;

		int otherArrSize = other.row * other.col;
		if (row * col != otherArrSize) //��������� �������� ���������� ������ 
		{
			if (this->data != nullptr) delete[] this->data;

			//��������� ������ ��� ����� ������
			this->data = new double[otherArrSize];
		}

		this->col = other.col;
		this->row = other.row;

		if (otherArrSize > 0) std::copy(other.data, other.data + otherArrSize, this->data);

		return *this;
	}

	//������������ �������� ������������
	Matrix& Matrix::operator=(Matrix&& m) noexcept
	{
		if (this == &m) return *this;

		if (this->data != nullptr)
		{
			delete[] this->data;
			this->data = nullptr;
			this->row = 0;
			this->col = 0;
		}

		std::swap(this->row, m.row);
		std::swap(this->col, m.col);
		std::swap(this->data, m.data);

		return *this;
	}

	//��������� ������ ������
	//���������� ������:
	std::ostream& operator<<(std::ostream& out, const Matrix& mat)
	{
		auto width = out.width();

		if (width == 0)
			width = 5;

		for (unsigned int i = 0; i < mat.row; i++)
		{
			for (unsigned int j = 0; j < mat.col; j++)
			{
				out << std::setw(width) << mat[i][j] << "\t";
			}
			out << std::endl;
		}
		out << std::endl;
		return out;
	}

	//���������� ��������� "-" (�������)
	Matrix Matrix::operator-() const
	{
		return std::move(Matrix(*this) *= -1.0);
	}

	//���������� ��������� "*"
	Matrix operator*(const Matrix& A, const Matrix& B)
	{
		return std::move(Matrix(A)) *= B;
	}

	//���������� ��������� "*k"
	Matrix operator*(const Matrix& A, const double B)
	{
		return std::move(Matrix(A)) *= B;
	}

	//���������� ��������� "k*"
	Matrix operator*(const double A, const Matrix& B)
	{
		return std::move(Matrix(B)) *= A;
	}

	//���������� ��������� "+"
	Matrix operator+(const Matrix& A, const Matrix& B)
	{
		return std::move(Matrix(A)) += B;
	}

	//���������� ��������� "-" 
	Matrix operator-(const Matrix& A, const Matrix& B)
	{
		return std::move(Matrix(A)) -= B;
	}

	//���������� ��������� "+="
	Matrix& Matrix::operator+=(const Matrix& other)
	{
		if (this->isSum(other) == false)
			throw "����c����� ����������, ������ �" + this->ID;

		for (unsigned int i = 0; i < this->row * this->col; i++)
		{
			this->data[i] += other.data[i];
		}
		return *this;
	}

	//���������� ��������� "-="
	Matrix& Matrix::operator-=(const Matrix& other)
	{
		if (this->isSum(other) == false)
			throw "����c����� ����������, ������ �" + this->ID;

		for (unsigned int i = 0; i < this->row * this->col; i++)
		{
			this->data[i] -= other.data[i];
		}
		return *this;
	}

	//���������� ��������� "*="
	Matrix& Matrix::operator*=(const Matrix& other)
	{
		if (this->isMultiply(other) == false)
			throw "����c����� ����������, ������ �" + this->ID;

		if (other.data == nullptr) return *this;

		double* resultMatrix = new double[this->row * other.col];
		for (unsigned int i = 0; i < this->row; i++)
		{
			for (unsigned int j = 0; j < other.col; j++)
			{
				resultMatrix[i * other.col + j] = 0;
				for (unsigned int k = 0; k < other.row; k++)
				{
					resultMatrix[i * other.col + j] += (this->data[i * this->col + k] * other.data[k * other.col + j]);
				}
			}
		}
		delete[] this->data;
		this->col = other.col;
		this->data = resultMatrix;

		return *this;
	}

	//���������� ��������� "*=k"
	Matrix& Matrix::operator*=(const double k)
	{
		for (unsigned int i = 0; i < this->row * this->col; i++)
		{
			this->data[i] *= k;
		}
		return *this;
	}


	//������

	unsigned Matrix::GetCount()		//������ ���-�� ��������� 
	{
		return LotObj;
	}

	unsigned int Matrix::GetRow() const	///������ ���������� ��������
	{
		return row;
	}

	unsigned int Matrix::GetCol() const	///������ ���������� �����
	{
		return col;
	}

	unsigned Matrix::GetID() const	//������ id
	{
		return ID;
	}

	double Matrix::getMax() const	//����� ������������� ��������
	{
		if (data == nullptr)
			throw "���������� ��������� ����. ����. � ������� �������, ������ �" + this->ID;

		double max = data[0];
		for (unsigned int i = 1; i < row * col; i++)
		{
			if (data[i] > max)
			{
				max = data[i];
			}
		}
		return max;
	}

	double Matrix::getMin() const	//����� ������������ ��������
	{
		if (data == nullptr)
			throw "���������� ��������� ���. ����. � ������� �������, ������ �" + this->ID;

		double min = data[0];
		for (unsigned int i = 1; i < row * col; i++)
		{
			if (data[i] < min)
			{
				min = data[i];
			}
		}
		return min;
	}

	bool Matrix::isMultiply(const Matrix& other) const	//�������� �� ����������� ���������
	{
		return (this->col == other.row);
	}

	bool Matrix::isSum(const Matrix& other) const	//�������� �� ����������� ��������
	{
		return ((this->col == other.col) && (this->row == other.row));
	}
	
}
