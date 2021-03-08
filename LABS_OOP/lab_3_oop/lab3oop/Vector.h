#pragma once 
#include "Matrix.h"

namespace MXSpace
{
	class Vector : public Matrix
	{
	public:
		
		Vector(unsigned size = 0, bool orient = true, const double* data = nullptr);
		double& operator[](const unsigned size);
		Vector& operator+=(const Vector& other);
		bool get_orient() const;
		void change_orient();
	private:
		bool orientation;	//Если строка, то true
		
	};
}