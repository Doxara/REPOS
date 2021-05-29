#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

void matrixInFile(ofstream& File, int matOrder, double** A, double* B = nullptr)
{
    File << fixed;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            File << std::setprecision(7) << A[i][j] << "\t";
        }
        if (B != nullptr) File << "|\t" << B[i];
        File << "\n";
    }
    File << resetiosflags(ios_base::floatfield);
}

void matrixsInFile(ofstream& File, int matOrder, double** matA, double** matB)
{
    File << fixed;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            File << std::setprecision(7) << matA[i][j] << "\t";
        }
        File << "|\t";
        for (int j = 0; j < matOrder; j++)
        {
            File << std::setprecision(7) << matB[i][j] << "\t";
        }
        File << "\n";
    }
    File << resetiosflags(ios_base::floatfield);
}

void gauss_slau(double* B, double** A, int matOrder)
{
    //Создадим копии матрицы и вектора:
    double* tempB = new double[matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        tempB[i] = B[i];
    }

    double** tempA = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        tempA[i] = new double[matOrder];
    }
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            tempA[i][j] = A[i][j];
        }
    }

    //Прямой ход:
    ofstream File("gaussSlauOutput.txt");
    File << "Исходная матрица:\n";
    matrixInFile(File, matOrder, tempA, tempB);

    //Нормализуем 1ю строку:
    if (tempA[0][0] == 0.0)
    {
        throw "Нулевой элемент. Требуется перестановка строк.";
    }
    for (int i = 1; i < matOrder; i++)
    {
        tempA[0][i] /= tempA[0][0];
    }
    tempB[0] /= tempA[0][0];
    tempA[0][0] = 1;

    File << "\nA(1):\n";
    matrixInFile(File, matOrder, tempA, tempB);
    for (int i = 1; i < matOrder; i++)//перебираем строки начиная со 2й
    {
        for (int j = i; j < matOrder; j++)//перебираем строки с текущей и ниже
        {
            double buf = tempA[j][i - 1];
            for (int q = 0; q < matOrder; q++)//перебираем все элементы обрабатываемой строки
            {
                /*вычитаем эл-ты "отброшенной строки",
                домноженные на элемент обрабатываемой строки,
                который находится под самым левым элементом "отброшенной" строки*/
                tempA[j][q] -= tempA[i - 1][q] * buf;
            }
            tempB[j] -= tempB[i - 1] * buf; //вычитаем у вектора тоже самое
        }

        //Нормализуем обрабатываемую строку:
        if (tempA[i][i] == 0.0)
        {
            throw "Нулевой элемент. Требуется перестановка строк.";
        }
        for (int j = 0; j < i; j++)
        {
            tempA[i][j] /= tempA[i][i];
        }
        for (int j = i + 1; j < matOrder; j++)
        {
            tempA[i][j] /= tempA[i][i];
        }
        tempB[i] /= tempA[i][i];
        tempA[i][i] = 1;

        File << "\nA(" << i + 1 << "):\n";
        matrixInFile(File, matOrder, tempA, tempB);
    }

    //Обратный ход:
    double* tempRoots = new double[matOrder];
    for (int i = matOrder - 1; i >= 0; i--)
    {
        double root = tempB[i];
        for (int j = i + 1; j < matOrder; j++)
        {
            root -= tempA[i][j] * tempRoots[j];
        }
        tempRoots[i] = root;
    }

    //Невязка:
    double* discrepancy = new double[matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        double sum = 0;
        for (int j = 0; j < matOrder; j++)
        {
            sum += A[i][j] * tempRoots[j];
        }

        discrepancy[i] = B[i] - sum;
    }
    //Норма вектора невязки:
    double discrepancyNorm = 0;
    for (int i = 0; i < matOrder; i++)
    {
        discrepancyNorm += discrepancy[i] * discrepancy[i];
    }
    discrepancyNorm = sqrt(discrepancyNorm);

    //Вывод в файл:
    File << "\n";
    for (int i = 0; i < matOrder; i++)
    {
        File << tempRoots[i] << " ";
    }
    File << "\n";

    for (int i = 0; i < matOrder; i++)
    {
        File << discrepancy[i] << " ";
    }
    File << "\n";
    File << discrepancyNorm;

    //Закрытие файла и очищение памяти
    File.close();
    delete[] discrepancy;
    delete[] tempRoots;
    delete[] tempB;
    for (int i = 0; i < matOrder; i++)
    {
        delete[] tempA[i];
    }
    delete[] tempA;
}

double gauss_det(double** A, int matOrder)
{
    //Создадим копию матрицы:
    double** tempA = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        tempA[i] = new double[matOrder];
    }
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            tempA[i][j] = A[i][j];
        }
    }

    ofstream File("gaussDetOutput.txt");
    File << "A(1):\n";
    matrixInFile(File, matOrder, tempA);

    for (int i = 1; i < matOrder; i++)//перебираем строки начиная со 2й
    {
        for (int j = i; j < matOrder; j++)//перебираем строки с текущей и ниже
        {
            double buf = tempA[j][i - 1] / tempA[i - 1][i - 1];
            for (int q = 0; q < matOrder; q++)//перебираем все элементы обрабатываемой строки
            {
                tempA[j][q] -= tempA[i - 1][q] * buf;
            }
        }
        File << "\nA(" << i + 1 << "):\n";
        matrixInFile(File, matOrder, tempA);
    }

    double det = tempA[0][0];
    for (int i = 1; i < matOrder; i++)
    {
        det *= tempA[i][i];
    }

    //Вывод в файл:
    File << "\n" << det;


    //Закрытие файла и очищение памяти:
    File.close();
    for (int i = 0; i < matOrder; i++)
    {
        delete[] tempA[i];
    }
    delete[] tempA;

    return det;
}

void gauss_inverse(double** A, int matOrder)
{
    //Создадим копию матрицы:
    double** tempA = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        tempA[i] = new double[matOrder];
    }
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            tempA[i][j] = A[i][j];
        }
    }
    //Создадим единичную матрицу: 
    double** identityM = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        identityM[i] = new double[matOrder] {0};
    }
    for (int i = 0; i < matOrder; i++)
    {
        identityM[i][i] = 1;
    }
    //Создадим обратную матрицу: 
    double** inverseM = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        inverseM[i] = new double[matOrder];
    }


    //Прямой ход:
    ofstream File("gaussInverseOutput.txt");
    File << "Исходные матрицы:\n";
    matrixsInFile(File, matOrder, tempA, identityM);

    //Нормализуем 1ю строку:
    if (tempA[0][0] == 0.0)
    {
        throw "Нулевой элемент. Требуется перестановка строк.";
    }
    for (int i = 1; i < matOrder; i++)
    {
        tempA[0][i] /= tempA[0][0];
    }
    for (int i = 0; i < matOrder; i++)
    {
        identityM[0][i] /= tempA[0][0];
    }
    tempA[0][0] = 1;

    File << "\nA(1)|E(1):\n";
    matrixsInFile(File, matOrder, tempA, identityM);
    for (int i = 1; i < matOrder; i++)//перебираем строки начиная со 2й
    {
        for (int j = i; j < matOrder; j++)//перебираем строки с текущей и ниже
        {
            double buf = tempA[j][i - 1];
            for (int q = 0; q < matOrder; q++)//перебираем все элементы обрабатываемой строки
            {
                /*вычитаем эл-ты "отброшенной строки",
                домноженные на элемент обрабатываемой строки,
                который находится под самым левым элементом "отброшенной" строки*/
                tempA[j][q] -= tempA[i - 1][q] * buf;
            }
            for (int z = 0; z < matOrder; z++)
            {
                identityM[j][z] -= identityM[i - 1][z] * buf; //вычитаем у векторОВ тоже самое
            }
        }

        //Нормализуем обрабатываемую строку:
        if (tempA[i][i] == 0.0)
        {
            throw "Нулевой элемент. Требуется перестановка строк.";
        }
        for (int j = 0; j < i; j++)
        {
            tempA[i][j] /= tempA[i][i];
        }
        for (int j = i + 1; j < matOrder; j++)
        {
            tempA[i][j] /= tempA[i][i];
        }
        for (int z = 0; z < matOrder; z++)
        {
            identityM[i][z] /= tempA[i][i];
        }
        tempA[i][i] = 1;

        File << "\nA(" << i + 1 << ")|E(" << i + 1 << "):\n";
        matrixsInFile(File, matOrder, tempA, identityM);
    }

    //Обратный ход:
    for (int k = 0; k < matOrder; k++)
    {
        for (int i = matOrder - 1; i >= 0; i--)
        {
            double root = identityM[i][k];
            for (int j = i + 1; j < matOrder; j++)
            {
                root -= tempA[i][j] * inverseM[j][k];
            }
            inverseM[i][k] = root;
        }
    }

    File << "\n\nОбратная матрица:\n";
    matrixInFile(File, matOrder, inverseM);

    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            tempA[i][j] = 0;
            for (int k = 0; k < matOrder; k++)
                tempA[i][j] += A[i][k] * inverseM[k][j];
        }
    }
    for (int i = 0; i < matOrder; i++)
    {
        tempA[i][i] -= 1.0;
    }

    File << "\nМатрица невязки:\n";
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            File << std::setw(14) << tempA[i][j] << "\t";
        }
        File << "\n";
    }

    double discrepancyNorm = 0;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            discrepancyNorm += tempA[i][j] * tempA[i][j];
        }
    }
    discrepancyNorm = sqrt(discrepancyNorm);

    File << "\nНорма невязки:\n";
    File << discrepancyNorm;

    for (int i = 0; i < matOrder; i++)
    {
        delete[] tempA[i];
        delete[] identityM[i];
        delete[] inverseM[i];
    }
    delete[] tempA;
    delete[] identityM;
    delete[] inverseM;
}

void iter_slau(double* B, double** A, int matOrder)
{
    //Проверим диагональные элементы исходной матрицы на нули:
    for (int i = 0; i < matOrder; i++)
    {
        if (A[i][i] == 0) throw "На диагонали исходной матрицы присутствует ноль.";
    }

    //Сравним диагональные элементы исходной матрицы с суммой остальных элементов строки:
    for (int i = 0; i < matOrder; i++)
    {
        double sum = 0;
        for (int j = 0; j < matOrder; j++)
        {
            if (i != j) sum += fabs(A[i][j]);
        }
        if (fabs(A[i][i]) <= sum) throw "Диагональный эл-т исходной матрицы меньше суммы остальных эл-тов строки";
    }

    //Создадим матрицу альфа и вектор бета:
    double** alfa = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        alfa[i] = new double[matOrder];
    }
    double* beta = new double[matOrder];

    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            if (i == j) alfa[i][j] = 0.0;
            else alfa[i][j] = -A[i][j] / A[i][i];
        }
    }
    for (int i = 0; i < matOrder; i++)
    {
        beta[i] = B[i] / A[i][i];
    }

    double* lastX = new double[matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        lastX[i] = beta[i];
    }
    double* curentX = new double[matOrder];

    double eps = 0.00001;
    double normAlfa = 0;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            normAlfa += alfa[i][j] * alfa[i][j];
        }
    }
    normAlfa = sqrt(normAlfa);
    double breaker = eps * (1 - normAlfa) / normAlfa;

    while (true)
    {
        for (int i = 0; i < matOrder; i++)
        {
            curentX[i] = 0;
            for (int j = 0; j < matOrder; j++)
            {
                curentX[i] += alfa[i][j] * lastX[j];
            }
            curentX[i] += beta[i];
        }
        double norm = 0;
        for (int i = 0; i < matOrder; i++)
        {
            norm += (curentX[i] - lastX[i]) * (curentX[i] - lastX[i]);
        }
        norm = sqrt(norm);

        if (norm < breaker)break;
        for (int i = 0; i < matOrder; i++)
        {
            lastX[i] = curentX[i];
        }
    }

    ofstream File("iterSlauOutput.txt");
    File << "Alfa|Beta:\n";
    matrixInFile(File, matOrder, alfa, beta);

    File << "\n\n";
    for (int i = 0; i < matOrder; i++)
    {
        File << curentX[i] << "\t";
    }

    //Невязка:
    double* discrepancy = new double[matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        double sum = 0;
        for (int j = 0; j < matOrder; j++)
        {
            sum += A[i][j] * curentX[j];
        }

        discrepancy[i] = B[i] - sum;
    }
    //Норма вектора невязки:
    double discrepancyNorm = 0;
    for (int i = 0; i < matOrder; i++)
    {
        discrepancyNorm += discrepancy[i] * discrepancy[i];
    }
    discrepancyNorm = sqrt(discrepancyNorm);

    File << "\n";
    for (int i = 0; i < matOrder; i++)
    {
        File << discrepancy[i] << "\t";
    }
    File << "\n";
    File << discrepancyNorm;

    //Закрываем файл и очищаем память:
    File.close();
    for (int i = 0; i < matOrder; i++)
    {
        delete[] alfa[i];
    }
    delete[] alfa;
    delete[] beta;
    delete[] lastX;
    delete[] curentX;
    delete[] discrepancy;
}

void iter_inverse(double** A, int matOrder)
{
    //Проверим диагональные элементы исходной матрицы на нули:
    for (int i = 0; i < matOrder; i++)
    {
        if (A[i][i] == 0) throw "На диагонали исходной матрицы присутствует ноль.";
    }

    //Сравним диагональные элементы исходной матрицы с суммой остальных элементов строки:
    for (int i = 0; i < matOrder; i++)
    {
        double sum = 0;
        for (int j = 0; j < matOrder; j++)
        {
            if (i != j) sum += fabs(A[i][j]);
        }
        if (fabs(A[i][i]) <= sum) throw "Диагональный эл-т исходной матрицы меньше суммы остальных эл-тов строки";
    }

    //Создадим единичную матрицу: 
    double** identityM = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        identityM[i] = new double[matOrder] {0};
    }
    for (int i = 0; i < matOrder; i++)
    {
        identityM[i][i] = 1;
    }
    //Создадим обратную матрицу: 
    double** inverseM = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        inverseM[i] = new double[matOrder];
    }

    //Создадим матрицу alfa:
    double** alfa = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        alfa[i] = new double[matOrder];
    }
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            if (i == j) alfa[i][j] = 0.0;
            else alfa[i][j] = -A[i][j] / A[i][i];
        }
    }

    //Создадим матрицу beta:
    double** beta = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        beta[i] = new double[matOrder];
    }

    for (int j = 0; j < matOrder; j++)
    {
        for (int i = 0; i < matOrder; i++)
        {
            beta[i][j] = identityM[i][j] / A[i][i];
        }
    }

    double eps = 0.00001;
    double normAlfa = 0;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            normAlfa += alfa[i][j] * alfa[i][j];
        }
    }
    normAlfa = sqrt(normAlfa);
    double breaker = eps * (1 - normAlfa) / normAlfa;



    double* lastX = new double[matOrder];
    for (int p = 0; p < matOrder; p++)
    {
        for (int i = 0; i < matOrder; i++)
        {
            lastX[i] = beta[i][p];
        }

        while (true)
        {
            for (int i = 0; i < matOrder; i++)
            {
                inverseM[i][p] = 0;
                for (int j = 0; j < matOrder; j++)
                {
                    inverseM[i][p] += alfa[i][j] * lastX[j];
                }
                inverseM[i][p] += beta[i][p];
            }
            double norm = 0;
            for (int i = 0; i < matOrder; i++)
            {
                norm += (inverseM[i][p] - lastX[i]) * (inverseM[i][p] - lastX[i]);
            }
            norm = sqrt(norm);

            if (norm < breaker)break;
            for (int i = 0; i < matOrder; i++)
            {
                lastX[i] = inverseM[i][p];
            }
        }
    }

    ofstream File("iterInverseOutput.txt");
    File << "Alfa|Beta:\n";
    matrixsInFile(File, matOrder, alfa, beta);

    File << "\n\nОбратная матрица:\n";
    matrixInFile(File, matOrder, inverseM);

    //Запишем невязку в единичную матрицу:
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            identityM[i][j] = 0;
            for (int k = 0; k < matOrder; k++)
                identityM[i][j] += A[i][k] * inverseM[k][j];
        }
    }
    for (int i = 0; i < matOrder; i++)
    {
        identityM[i][i] -= 1.0;
    }

    File << "\nМатрица невязки:\n";
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            File << std::setw(14) << identityM[i][j] << "\t";
        }
        File << "\n";
    }

    double discrepancyNorm = 0;
    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            discrepancyNorm += identityM[i][j] * identityM[i][j];
        }
    }
    discrepancyNorm = sqrt(discrepancyNorm);

    File << "\nНорма невязки:\n";
    File << discrepancyNorm;

    //Закрываем файл и очищаем память:
    File.close();

    for (int i = 0; i < matOrder; i++)
    {
        delete[] identityM[i];
        delete[] inverseM[i];
        delete[] alfa[i];
        delete[] beta[i];
    }
    delete[] identityM;
    delete[] inverseM;
    delete[] alfa;
    delete[] beta;
    delete[] lastX;
}


int main()
{
    int typeOfProblem, matOrder; //тип задачи, порядок матрицы

    ifstream File("input.txt");
    File >> typeOfProblem;
    File >> matOrder;

    double* B = new double[matOrder];
    double** A = new double* [matOrder];
    for (int i = 0; i < matOrder; i++)
    {
        A[i] = new double[matOrder];
    }

    for (int i = 0; i < matOrder; i++)
    {
        for (int j = 0; j < matOrder; j++)
        {
            File >> A[i][j];
        }
        File >> B[i];
    }
    File.close();


    switch (typeOfProblem)
    {
    case 1:
        gauss_slau(B, A, matOrder);
        break;
    case 2:
        gauss_det(A, matOrder);
        break;
    case 3:
        gauss_inverse(A, matOrder);
        break;
    case 4:
        iter_slau(B, A, matOrder);
        break;
    case 5:
        iter_inverse(A, matOrder);
        break;
    default:
        cout << "Во входном файле неверно указан номер метода.";
        break;
    }

    delete[] B;
    for (int i = 0; i < matOrder; i++)
    {
        delete[] A[i];
    }
    delete[] A;

    return 0;
}
