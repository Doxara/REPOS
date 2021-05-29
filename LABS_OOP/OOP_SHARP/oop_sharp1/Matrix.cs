using System;
using System.Text;

namespace Metjo
{
    class Matrix
    {
        private int rows;
        private int cols;
        public int Rows
        {
            get => rows;
            protected set => rows = value;
        }
        public int Cols
        {
            get { return cols; }
            protected set { cols = value; }
        }
        protected double[,] data;
        public Guid ID { get; private set; }    //ID matrix
        
        private static uint lotObj = 0;
        public static uint LotObj => lotObj;

        public Matrix()
        {
            rows = cols = 0;
            data = null;
        }
        public Matrix(int _Rows, int _Cols) //constructor with parameters
        {
            ID = Guid.NewGuid();
            lotObj++;
            Console.WriteLine($"Create obj ID {ID}, num obj in program is {LotObj}");

            // Проверка на < 0

            if (_Rows != 0 && _Cols != 0)
            {
                data = new double[_Rows, _Cols];
            }

            if (_Rows >= 0 && Cols >= 0)
            {
                Rows = _Rows;
                Cols = _Cols;
            }
        }

        

        public Matrix(Matrix A) //copy constructor
        {
            ID = Guid.NewGuid();
            Rows = A.Rows;
            Cols = A.Cols;
            data = A.data;
        }
        public Matrix(double[,] arr) //construct with double arr input
        {
            ID = Guid.NewGuid();
            if (arr != null)
            {
                Rows = arr.GetLength(0);
                Cols = arr.GetLength(1);
                data = arr;
            }
        }
        public Matrix(int mn) : this(mn, mn) { }    //Quad matrix constructor 

        public virtual double this[int i, int j]    //Indexer for accessing matrix elements
        {
            set { data[i, j] = value; }
            get { return data[i, j]; }
        }

        public static Matrix operator +(in Matrix a, in Matrix b)
        {
            
            if (IsSum(a, b))
            {
                Matrix res = new Matrix(a.Rows, a.Cols);
                for (int i = 0; i < a.data.GetLength(0); i++)
                {
                    for (int j = 0; j < a.data.GetLength(1); j++)
                    {
                        res[i, j] = a[i, j] + b[i, j];
                    }
                }
                return res;
            }
            else
            {
                throw new ArgumentException($"Невозможно сложить матрицы");
            }
        }
        public static Matrix operator -(in Matrix a, in Matrix b)
        {
            if (IsSum(a, b))
            {
                return a + (b * -1);
            }
            else
            {
                throw new ArgumentException($"Невозможно вычесть матрицы");
            }
        }
        public static Matrix operator *(in Matrix a, in Matrix b)
        {
            if (IsMyltiply(a, b))
            {
                Matrix res = new Matrix(a.Rows, b.Cols);
                for (int i = 0; i < res.data.GetLength(0); i++)
                {
                    for (int j = 0; j < res.data.GetLength(1); j++)
                    {
                        for (int k = 0; k < b.data.GetLength(0); k++)
                        {
                            res[i, j] += a[i, k] * b[k, j];
                        }
                    }
                }
                return res;
            }
            else
            {
                throw new ArgumentException($"Невозможно умножить матрицы");
            }
        }
        public static Matrix operator *(Matrix a, double k)
        {
            if (!a.isEmpty())
            {
                Matrix res = new Matrix(a);
                for (int i = 0; i < res.data.GetLength(0); i++)
                {
                    for (int j = 0; j < res.data.GetLength(1); j++)
                    {
                        res[i, j] *= k;
                    }
                }
                return res;
            }
            else
            {
                throw new ArgumentException("Невозможно умножить матрицу на k - матрица пуста");
            }
        }
        public override string ToString()   //Matrix to string with formatted string
        {
            var res = new StringBuilder();
            res.AppendLine();
            for (int i = 0; i < Rows; i++)
            {
                for (int j = 0; j < Cols; j++)
                {
                    res.AppendFormat("{0,4}", data[i, j]);
                }
                res.AppendLine();
            }
            return res.ToString();
        }
        public static bool IsMyltiply(in Matrix A, in Matrix B) => A.Cols == B.Rows;
        public static bool IsSum(in Matrix A, in Matrix B)
        { return A.Rows == B.Rows && A.Cols == B.Cols; }

        public bool isEmpty()
        { return data == null; }
        public double Min() //Find min element in Matrix
        {
            if (data == null)
                throw new ArgumentNullException();
            double res = double.MaxValue;

            // IEnumarable
            foreach (var d in data)
            {
                if (d < res) res = d;
            }
            
            return res;
        }
        public double Max() //Find max element in Matrix
        {
            if (data == null)
                throw new ArgumentNullException();
            double res = data[0, 0];
            for (int i = 0; i < data.GetLength(0); i++)
            {
                for (int j = 0; j < data.GetLength(1); j++)
                {
                    if (res < data[i, j])
                    {
                        res = data[i, j];
                    }
                }
            }
            return res;
        }

        public void Print()     //Method print Matrix to screen
        {
            Console.WriteLine($"ID:{ID}\tRows:{Rows}\tCols{Cols}");
            if (data != null)
            {
                Console.WriteLine(ToString());
            }
        }

        public static void Print(params Matrix[] matrices)  //Print array of Matrix objects
        {
            for (int i = 0; i < matrices.Length; i++)
            {
                matrices[i].Print();
            }
        }
        ~Matrix()   //Диструктор Distructor (С функцией печати на экран данных о матрице)
        {
            Console.WriteLine($"Obj {ID} was destroyed");
            lotObj--;
        }
    }
}
