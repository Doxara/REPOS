using System;
using System.Linq;
 

namespace Metjo
{
    class Program
    {
        static void Main(string[] args)
        {
            Matrix ass = new Matrix(4,5);
            Matrix fg = new Matrix(4, 5);
            Matrix fhdfh = new Matrix(new double [,] { { 5,6 },{ 4,7 },{ 4, 1 } });
            Console.WriteLine($"want ass x fg is can {Matrix.isMyltiply(ass,fg)}");
            Matrix.Print(ass, fg, fhdfh);
        }
    }
}
