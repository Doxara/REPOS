//�������� ���������, ������� � ������� ������ ������ � ������� ������������ ���������� ������� ����������� ��� ������������� ������������������ �����.	-
//��� ������������� ����� � ��������� ������������ ������ ���������. +
//������ � ����� �������� �� �����.	+
//��������� ������ ������� ��� ������ ������� ����� ����� ���������� ���������, � ������� ��������� ��� �������.	+
//����� ���������� ������ � ������������� ����������� ������ ���������� ���������� ���������� ��� ������.	+
//Upd:
//�������� ���������, ������� � ������� ��������� ������ ����� �������� ���������� ���� ����� ����� ������ ������ �����.
//���� ����� �������� ���������.������������� ���� ������ �� �����.
//����� ���������� ������ � ������������� ����������� ������ ���������� ���������� ���������� ��� ������.

#include "Graph.h"
#include <iostream>
#include <limits>
#include <list>

namespace g
{
	Graph::Graph(int N) : N(N)
	{
		if (N != 0)
		{
			this->Points.resize(N);
			for (auto i = 0; i < N; i++)
			{
				this->Points[i] = new Edge;
			}
		}
			
	}

	bool Graph::isEdge(int I, int k)
	{
		for (auto iter = Points[I]->num.begin(); iter != Points[I]->num.end(); iter++)
		{
			if (*iter == k)
				return true;
		}
		return false;
	}

	bool Graph::isPointExist(int key)
	{
		if (!this->isEmpty())
		{
			if ((unsigned)key < this->Points.size())
			{
				if (this->Points[key] == nullptr)
					return false;
				else
					return true;
			}
			else
				return false;
		}
		else
			throw "���� ����";
		
	}

	bool Graph::isEmpty()
	{
		return (Points.empty());
	}

	/*USED FOR THE INITIAL FILLING OF THE GRAPH*/
	void Graph::addEdgeOrient(int I, int k, int w)		
	{
		if (I >= N)
			throw "������ ������� �� ����������";
		
			if (!this->isPointExist(I))
			{
				Edge* a = new Edge;
				a->num.push_back(k);
				a->weights.push_back(w);
				Points[I] = a;
			}
			else
			{
				Points[I]->num.push_back(k);
				Points[I]->weights.push_back(w);
			}
	}

	/*USED FOR THE ADD EDGE AFTER FILLING OF THE GRAPH*/
	void Graph::addEdgeNotOrient(int I, int k, int w)
	{
			if (this->isEmpty())
				throw "���������� �������� ������� - ���� ����";
			if (!this->isPointExist(k))
				throw "������ ������� �� ����������";
			if (!this->isPointExist(I))
				throw "������ ������� �� ����������";
		addEdgeOrient(I, k, w);
		addEdgeOrient(k, I, w);
	}


	void Graph::addExtraVertex(int k)
	{
		if ((unsigned)k >= Points.size())
		{
			Points.resize(k+1, nullptr);
			Edge* a = new Edge;
			Points[k] = a;
			N = k + 1;
		}
		else
		{
			if (!isPointExist(k))
			{
				Points[k] = new Edge;
			}
			else
				throw "�������� ������� ��� ����������";
		}
	}

	void Graph::delVertex(int k)
	{
		if (isEmpty())
			throw "���������� �������� ������� - ���� ����";
		if (!isPointExist(k))
			throw "������ ������� �� ����������";
		for (size_t i = 0; i < Points[k]->num.size(); i++)
		{
			for (auto iter = Points[Points[k]->num.front()]->num.begin(); iter != Points[Points[k]->num.front()]->num.end(); iter++)
			{
				if (*iter == k)
				{
					Points[this->Points[k]->num.front()]->num.erase(iter);
					break;
				}
			}
			Points[k]->num.pop_front();
		}
		if (k < this->N)
		{
			delete Points[k];
			Points[k] = nullptr;
		}
		else
		{
			delete this->Points[k];
			this->Points.resize(k+1);
		}
	}
	
	int Graph::getNumOfVertex()
	{
		int counter = 0;
		for (int i = 0; i < N; i++)
		{
			if (Points[i] != nullptr)
				counter++;
		}
		return counter;
	}

	int Graph::getNumofEdge()
	{
		int counter = 0;
		for (auto i = 0; i < N; i++)
		{
			if (Points[i] != nullptr)
			{
				if (!Points[i]->num.empty())
					counter = counter + Points[i]->num.size();
			}
		}
		return counter/2;
	}

	int Graph::getWeight(int I, int k)
	{
		if (isPointExist(I) && isPointExist(k))
		{
			if (isEdge(I, k))
			{
				if (!Points[I]->weights.empty())
				{
					int count = 0;
					for (auto nums : Points[I]->num)
					{
						count++;
						if (nums == k)
						{
							auto ptr = Points[I]->weights.begin();
							if (Points[I]->weights.size() > 1)
							{
								for (int i = 0; i < count-1; i++)
								{
									ptr++;
								}
							}
							return *ptr;
						}

					}
				}
			}
			else
				throw "������ ������� �� ����� �����";
		}
		else
			throw "������ ������ �� ����������";
	}

	int Graph::getNumConnectedComp()
	{
		if (isEmpty())
			throw "���������� ����� ��������� ��������� - ���� ����";

		int C = 0;
		if (Mark != nullptr)
			delete[]Mark;

			Mark = new int [N]{ 0 };
		for (auto i = 0; i < N; i++)
		{
			if (isPointExist(i))
			{
				if (Mark[i] == 0)
				{
					C++;
					comp(&C, i);
				}
			}
		}
		return C;
	}


	/// This function return double [][] Array - Mat Path for each vertex
	void Graph::showShortestPathAll()
	{
		double** MatDist = new double* [N];
		double** MatPath = new double* [N]; //������� ���������� ����� ����� ���������
		for (int i = 0; i < N; i++)
		{
			MatDist[i] = new double[N] {INFINITY};
			MatPath[i] = new double[N] {0};
		}
		for (int i = 0; i < N; i++)
		{
			for (int j = 0; j < N; j++)
			{
				MatPath[i][j] = INFINITY;
			}
		}
		for (int i = 0; i < N; i++)
		{
			MatDist[i][i] = 0;
			for (int j = 0; j < N; j++)
			{
				if (isEdge(i, j))
				{
					MatDist[i][j] = (double)getWeight(i, j);
				}
				else
					MatDist[i][j] = INFINITY;
				MatPath[i][j] = j;
				
			}
		}

		for (int k = 0; k < N; k++)
		{
			for (int i = 0; i < N; i++)
			{
				for (int j = 0; j < N; j++)
				{
					if ((MatDist[i][k] != INFINITY) && (MatDist[k][j] != INFINITY))
					{
						if (MatDist[i][j] > (MatDist[i][k] + MatDist[k][j]))
						{
							MatDist[i][j] = MatDist[i][k] + MatDist[k][j];
							MatPath[i][j] = MatPath[i][k];
						}
					}
				}
			}
		}
		cout << "\n  ���������� ���� �� ���� ������\n";
		for (int i = 0; i < N; i++)
		{
			for (int j = 0; j < N; j++)
			{
				if (i != j)
				{
					cout << "  (" << i << "->" << j << "): ";
					if (MatDist[i][j] != INFINITY)
					{
						int k = i;
						cout << "< " << i;
						while (k != j)
						{
							k = MatPath[k][j];
							cout << " " << k;
						}
						cout << " >" << " ���������:" << MatDist[i][j] << endl;
					}
					else
						cout << "��� ����\n";
				}
			}
		}
		for (int i = 0; i < N; i++)
		{
			delete[] MatDist[i];
			delete[] MatPath[i];
		}
		delete[] MatDist;
		delete[] MatPath;
	}

	void Graph::comp(int * C, int v)
	{
		Mark[v] = *C;
		for (auto j = 0; j < N; j++)
		{
			if (isEdge(v, j))
			{
				if (Mark[j] == 0)
					comp(C, j);
			}
		}
	}

	void Graph::print()
	{
		cout << endl << "  ����:\n  N:" << N << "\n  ���������� ����:" << getNumofEdge() << "\n  ���������� ������:" << getNumOfVertex() << endl;
		
		int C = getNumConnectedComp();
		for (auto i = 0; i < N; i++)
		{
			
			if (isPointExist(i)) {
				cout << "  [" << i << "] ";
				if (Points[i] != nullptr)
				{
					if (!Points[i]->num.empty())
					{
						copy(Points[i]->num.begin(), Points[i]->num.end(), ostream_iterator<int>(cout, " "));
					}
					cout << "\n  ����:";
					if (!Points[i]->weights.empty())
					{
						copy(Points[i]->weights.begin(), Points[i]->weights.end(), ostream_iterator<int>(cout, " "));
					}
				}
				else
					cout << "NULL";
			}
			else
				cout << "NULL";
			cout << endl;
		}
		for (int i = 1; i <= C; i++)
		{
			cout << "  ���������� ��������� " << i << ":";
			for (int j = 0;j < N; j++)
			{
				if (Mark[j] == i)
					cout << j << " ";
			}
			cout << endl;
		}

	}

	Graph::~Graph()		//Dist
	{
		for (auto i = 0; i < this->N ; i++)
			delete this->Points[i];
		Points.clear();
		delete[]Mark;
	}
}