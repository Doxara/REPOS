#pragma once
#include <limits>
#include <list>
#include <vector>

using namespace std;

namespace g
{

	class Graph
	{
	private:
			
		struct Edge		
		{
			list <int> num;	//adjacency list for vertices
		};
		
		//Points==nullptr if Graph is empty
		//Points[i]==nullptr if Point not exist
		vector <Edge*> Points;	//Points in Graph

		int* Mark = nullptr; //components 
		int N = 0;	//Capasity of Graph

	public:
		Graph(int N);

		bool isEdge(int I, int k);
		bool isPointExist(int key);
		bool isEmpty();

		//Standart Functions
		void addEdgeOrient(int I, int k);
		void addEdgeNotOrient(int I, int k);
		void addExtraVertex(int k);
		void delVertex(int k);
		int getNumOfVertex();
		int getNumofEdge();

		//Get connected comp
		int getNumConnectedComp();
		void comp(int*, int);

		void print();
		~Graph();
	};
}

