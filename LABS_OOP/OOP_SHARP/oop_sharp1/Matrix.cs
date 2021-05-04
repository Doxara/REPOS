using System;
using System.Collections.Generic;
using System.Text;

namespace Metjo
{
    class Matrix
    {
        private int rows, cols;
        private double[,] data;
        private Guid ID;
        private static uint LotObj = 0;
        public Matrix(int _rows ,int _cols) 
        {
            this.ID = Guid.NewGuid();
            LotObj++;
            Console.WriteLine($"Create obj ID {this.ID}, num obj in program is {LotObj}");
            if (_rows != 0 && _cols != 0)
                data = new double[_rows, _cols];
            
            if (_rows >= 0 && cols >= 0)
            {
                rows = _rows;
                cols = _cols;
            }
        }
        public Matrix(Matrix A)
        {
            this.ID = Guid.NewGuid();
            this.rows = A.rows;
            this.cols = A.cols;
            this.data = A.data;
        }
        public Matrix(in double[,] arr) 
        {
            this.ID = Guid.NewGuid();
            if (arr != null)
            {
                rows = arr.GetLength(0);
                cols = arr.GetLength(1);
                data = arr;
            }
        }
        public Matrix(int mn) : this(mn, mn) { }

        public int Cols
        {
            get { return cols; }
        }
        public int Rows
        {
            get { return rows; }
        }
        public Guid id
        {
            get { return ID; }
        }
        //public static bool operator >(Counter c1, Counter c2)
        //{
        //    return c1.Value > c2.Value;
        //}
        public static bool isMyltiply(in Matrix A,in Matrix B)
        {
            return A.rows == B.cols || A.cols == B.rows;
        }
        public static bool isSum(in Matrix A,in Matrix B)
        { return A.rows == B.rows && A.cols == B.cols; }
        public void Print()
        {
            Console.WriteLine($"ID:{ID}\tRows:{rows}\tCols{cols}");
            if (data != null)
            {
                for (int i = 0; i < data.GetLength(0); i++)
                {
                    for (int j = 0; j < data.GetLength(1); j++)
                    {
                        Console.Write("{0,3}", data[i, j]);
                    }
                    Console.WriteLine();
                }
            }
        }
        public static void Print(params Matrix[] matrices)
        {
            for (int i = 0; i < matrices.Length; i++)
                matrices[i].Print();
        }
        ~Matrix() 
        {
            Console.WriteLine($"Obj {this.ID} was destroyed");
            LotObj--;
        }
    }
}
