using System;

namespace Metjo
{
    class Vector : Matrix
    {
        public Vector() : base(){}
        public Vector(int size, bool isHorizontal = true) : base(1,size)
        {
            if (!isHorizontal)
            {
                ChangeOrient();
            }            
        }
        public Vector(in Vector other)
        {
            Cols = other.Cols;
            Rows = other.Rows;
        }
        public Vector(double[] array, bool isHorizontal = true)
        {
            if (array != null)
            {
                if (isHorizontal)
                {
                    data = new double[array.Length, 1];
                }
                else
                {
                    data = new double[1, array.Length];
                }

                for (int i = 0; i < array.Length; i++)
                {
                    if (isHorizontal)
                    {
                        data[1, i] = array[i];
                    }
                    else
                    {
                        data[i, 1] = array[i];
                    }
                }
            }
        }

        public override double this[int i, int j]    
        {
            set { throw new NotSupportedException("Невозможно использовать такой индексатор для этого класса");}
            get { throw new NotSupportedException("Невозможно использовать такой индексатор для этого класса");}
        }
        public double this[int i]    
        {
            set 
            {
                if (IsHorizontal())
                    data[0, i] = value;
                else
                    data[i, 0] = value;
            }
            get 
            {
                if (IsHorizontal())
                    return data[0, i];
                else
                    return data[i, 0];
            }
        }
        public bool IsHorizontal()
        {
            return Rows == 1;
        }
        public void ChangeOrient()
        {
            var tr = Rows;
            Rows = Cols;
            Cols = tr;
            double[,] temp = new double[data.GetLength(1), data.GetLength(0)];
            for (int i = 0; i < data.GetLength(0); i++)
            {
                for (int j = 0; j < data.GetLength(1); j++)
                {
                    temp[j, i] = data[i, j];
                }
            }
            data = temp;
            //for (int i = 0; i < data.GetLength(0); i++)
            //{
            //    for (int j = 0; j < data.GetLength(1); j++)
            //    {
            //        data[i, j] = temp[j, i];
            //    }
            //}
        }
        
        public static Vector operator +(in Vector a,in Matrix b)
        {
            if (IsSum(a, b))
            {
                Vector temp = new Vector(a.Rows*a.Cols);
                for (int i = 0; i < a.Cols*a.Rows; i++)
                {
                    if (a.IsHorizontal())
                        temp[i] = a[i] + b[0, i];
                    else
                        temp[i] = a[i] + b[i, 0];
                }
                return temp;
            }
            else
                throw new ArgumentException("Невозможно сложить вектор и матрицу");

        }
        public static Vector operator -(in Vector a, in Matrix b)
        {
            if (IsSum(a, b))
            {
                return a+(b*-1);
            }
            else
                throw new ArgumentException("Невозможно вычесть вектор и матрицу");
        }

    }
}
