#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <string>
#include <cstring>
#include <ctime>
#include <cstdlib>
#include <Windows.h>
#define M_MAXN 50
#define MAXN 60000+10
using namespace std;

vector<vector<double> > init_v;

//Define Matrix class
class Matrix
{
	//Matrix
public:
	explicit Matrix(int h = 1, int w = 1, vector<vector<double> > mat = init_v)
		: height(h), width(w)
	{
		if (mat.empty() == true) {
			mat.resize(1);
			mat[0].resize(1);
			mat[0][0] = 0;
			//cout << "Done" << endl;
		}
		//cout << "Done" << endl;
		matrix.resize(height);
		//cout << "Done" << endl;
		for (int i = 0; i < height; i++)
		{
			matrix[i].resize(width);
		}

		if (mat.size() != h || mat[0].size() != w)
		{
			std::cout << "INPUT ERROR!";
			std::cout << std::endl;
			system("pause");
			exit(1);
		}
		else
		{
			for (int i = 0; i < h; i++)
			{
				for (int j = 0; j < w; j++)
				{
					matrix[i][j] = mat[i][j];
				}
			}
		}
	}

	//Initialization
	void init(int h, int w, vector<vector<double> > mat) {
		height = h;
		width = w;

		matrix.resize(height);
		for (int i = 0; i < height; i++)
		{
			matrix[i].resize(width);
		}

		if (mat.size() != h || mat[0].size() != w)
		{
			std::cout << "INPUT ERROR!";
			std::cout << std::endl;
			system("pause");
			exit(1);
		}
		else
		{
			for (int i = 0; i < h; i++)
			{
				for (int j = 0; j < w; j++)
				{
					matrix[i][j] = mat[i][j];
				}
			}
		}
	}

	//Get height
	int getHeight() { return height; }

	//Get width
	int getWidth() { return width; }

	//Get element
	double getElement(int i, int j) { return matrix[i][j]; }

	//Print matirx
	void printMat()
	{
		for (int i = 0; i < height; i++)
		{
			for (int j = 0; j < width; j++)
			{
				cout << matrix[i][j];
				cout << " ";
			}
			cout << endl;
		}
		cout << endl;
	}

	//Add
	Matrix add(Matrix two)
	{
		//cout << "Done" << endl;
		vector<vector<double> > temp;
		temp.resize(height);
		for (int i = 0; i < height; i++)
		{
			temp[i].resize(width);
		}
		//temp.clear();
		static Matrix out(height, width, temp);
		//cout << "Done" << endl;

		if (height == two.height && width == two.width)
		{
			for (int i = 0; i < height; i++)
			{
				for (int j = 0; j < width; j++)
				{
					out.matrix[i][j] = matrix[i][j] + two.matrix[i][j];
				}
			}
		}
		else
		{
			cout << "ERROR" << endl;
			system("pause");
			exit(1);
		}

		return out;
	}

	//Multiply
	Matrix multiply(Matrix two)
	{
		vector<vector<double> > temp;
		temp.resize(height);
		for (int i = 0; i < height; i++)
		{
			temp[i].resize(two.getWidth());
		}
		//temp.clear();
		static Matrix out(height, two.getWidth(), temp);

		if (width == two.height)
		{
			for (int i = 0; i < height; i++)
			{
				for (int j = 0; j < two.width; j++)
				{
					int sum = 0;
					for (int k = 0; k < width; k++)
					{
						sum += matrix[i][k] * two.matrix[k][j];
					}
					out.matrix[i][j] = sum;
				}
			}
			return out;
		}
		else
		{
			cout << "ERROR" << endl;
			system("pause");
			exit(1);
		}
	}

	//Transpose matrix
	Matrix TransposedMat()
	{
		vector<vector<double> > temp;
		temp.resize(width);
		for (int i = 0; i < width; i++)
		{
			temp[i].resize(height);
		}
		//temp.clear();
		static Matrix out(width, height, temp);

		for (int i = 0; i < width; i++)
		{
			for (int j = 0; j < height; j++)
			{
				out.matrix[i][j] = matrix[j][i];
			}
		}
		return out;
	}

	//Determinant
	double Determinant()
	{
		if (height == 1 && width == 1)
		{
			return matrix[0][0];
		}

		double A[M_MAXN][M_MAXN];
		for (int i = 0; i < height; i++)
		{
			for (int j = 0; j < width; j++)
			{
				A[i][j] = matrix[i][j];
			}
		}

		double sum = determinant(A, height);
		return sum;
	}

	//Adjugate matrix
	Matrix AdjugateMatrix()
	{
		vector<vector<double> > Temp;
		Temp.resize(height);
		for (int i = 0; i < height; i++)
		{
			Temp[i].resize(width);
		}
		//Temp.clear();
		Matrix temp(height, width, Temp);

		for (int i = 0; i < temp.height; i++)
		{
			for (int j = 0; j < temp.width; j++)
			{
				temp.matrix[i][j] = AlgebraMinor(i, j);
				//cout << AlgebraMinor(i, j) << endl;
			}
		}

		static Matrix out = temp.TransposedMat();
		return out;
	}

	//Calculate distance
	//Euclidean distance
	double L2Distance(Matrix two) {
		if (two.height != height) { cout << "ERROR" << endl; return 0; }
		if (two.width != width) { cout << "ERROR" << endl; return 0; }

		double sum = 0.0;
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				double dif = matrix[i][j] - two.matrix[i][j];
				dif = (dif > 0) ? dif : 0.0 - dif;
				dif = pow(dif, 2.0);
				sum += dif;
			}
		}
		sum = pow(sum, 0.5);

		return sum;
	}

private:
	int height;
	int width;
	vector<vector<double> > matrix;

	//Determinant
	double determinant(double a[][M_MAXN], int dimension)
	{
		double sum = 0;
		double m_copy[M_MAXN][M_MAXN];
		memset(m_copy, 0, sizeof(m_copy));
		copy_m(a, m_copy, dimension);
		if (dimension == 2)
		{
			double result = a[0][0] * a[1][1] - a[0][1] * a[1][0];
			return result;
		}
		for (int i = 0; i < dimension; i++)
		{
			if (a[i][dimension - 1] - 0 < 0.000001)
				continue;
			spread(a, i, dimension);
			double tmp = a[i][dimension - 1] * determinant(a, dimension - 1);
			int sign = (i + 1 + dimension) % 2 == 0 ? 1 : (-1);
			sum += (double)sign * tmp;
			copy_m(m_copy, a, dimension);
		}
		return sum;
	}

	void spread(double a[][M_MAXN], int row, int dimension)
	{
		if (row == dimension - 1)
			return;
		for (int i = row; i < dimension - 1; i++)
			for (int j = 0; j < dimension - 1; j++)
				a[i][j] = a[i + 1][j];
	}

	void copy_m(double src[][M_MAXN], double dst[][M_MAXN], int dimension)
	{
		for (int i = 0; i < dimension; i++)
			for (int j = 0; j < dimension; j++)
				dst[i][j] = src[i][j];
	}

	//Adjugate matrix
	double AlgebraMinor(int i, int j)
	{
		vector<vector<double> > Temp;
		Temp.resize(height - 1);
		for (int i = 0; i < height - 1; i++)
		{
			Temp[i].resize(width - 1);
		}
		//Temp.clear();
		Matrix temp(height - 1, width - 1, Temp);

		int kase_1 = 0, kase_2 = 0;
		for (int x = 0; x < height; x++)
		{
			kase_2 = 0;
			if (x != i)
			{
				for (int y = 0; y < width; y++)
				{
					if (y != j)
					{
						temp.matrix[kase_1][kase_2] = matrix[x][y];
						//cout << matrix[x][y] << endl;
						kase_2++;
					}
				}
				kase_1++;
			}
		}

		//cout << temp.Determinant() << endl;
		double out = temp.Determinant() * pow(-1.0, i + j);
		return out;
	}
};

//Random function
int* random(int a, int b, int num) {
	static int* out;
	out = (int*)malloc(num * sizeof(int));
	static int* Num;
	Num = (int*)malloc(num * sizeof(int));
	/*srand((unsigned)time(NULL));
	for (int i = 0; i < num; i++) {
	out[i] = rand() % (b - a) + a;
	}
	return out;*/
	vector<int> tempfornum;
	for (int i = 0; i < num; ++i) {
		tempfornum.push_back(i);
	}
	random_shuffle(tempfornum.begin(), tempfornum.end());
	for (int i = 0; i < num; i++) {
		Num[i] = tempfornum[i];
	}

	vector<int> temp;
	for (int i = a; i < b; ++i) {
		temp.push_back(i);
	}
	random_shuffle(temp.begin(), temp.end());
	for (int i = 0; i < num; i++) {
		int tem = Num[i];
		out[i] = temp[tem];
	}
	return out;
}

//Quick sort
struct value_knn {
	double distance;
	int num;
};
typedef value_knn value_knn;

//Partition
//r need to reduce 1
int partition(vector<value_knn> &arr, int p, int r) {
	double x = arr[r].distance;
	int i = p - 1;
	for (int j = p; j <= r - 1; j++) {
		if (arr[j].distance <= x) {
			i += 1;
			swap(arr[i], arr[j]);
		}
	}
	swap(arr[i + 1], arr[r]);
	return i + 1;
}
//recursion
void QuickSort(vector<value_knn> &arr, int p, int r) {
	if (p < r) {
		int q = partition(arr, p, r);
		QuickSort(arr, p, q - 1);
		QuickSort(arr, q + 1, r);
	}
}

//Get dataset
int cn = 0;

struct Data {
	int label;
	Matrix data;
};
typedef Data Data;
Data dataset[MAXN];

void init(string file) {
	ifstream infile;
	infile.open(file.data());

	string s;
	int k = 0;
	while (getline(infile, s)) {
		vector<int> temp_arr;
		for (int i = 4; i < s.size();) {
			if (s[i] != ' ') {
				vector<int> temp_for_count;
				while (s[i] != ' ') {
					int ch = s[i] - 48;
					temp_for_count.push_back(ch);
					i++;
				}
				int sum = 0;
				for (int x = 0; x < temp_for_count.size(); x++) {
					int cnt = temp_for_count.size() - x;
					sum += temp_for_count[x] * (int)pow(10, cnt - 1);
				}
				temp_arr.push_back(sum);
			}
			i++;
		}

		int h = 28, w = 28;
		vector<vector<double> > temp_sto;
		temp_sto.resize(28);
		for (int g = 0; g < 28; g++) { temp_sto[g].resize(28); }
		for (int q = 0; q < 28; q++) {
			for (int w = 0; w < 28; w++) {
				temp_sto[q][w] = temp_arr[q * 28 + w];
			}
		}
		dataset[cn].data.init(h, w, temp_sto);
		dataset[cn].label = s[0] - 48;
		cn++;
		/*
		//test
		cout << temp_arr.size() << endl;
		for (int b = 0; b < temp_arr.size(); b++) {
		cout << temp_arr[b];
		if((b+1)%28 == 0)
		cout << endl;
		}
		cout << dataset[0].label << endl;
		dataset[0].data.printMat();
		k = 1;
		if (k == 1) break;
		*/
		k++;
		if (k % 2000 == 0) {
			printf("Done ");
			cout << k << endl;
		}

		if (k == 60000)
			break;
	}
	infile.close();
	//cout << cn << endl;
}

//k-nearest neighbor
void KNN() {
	double acc;
	int right_num = 0;
	int wrong_num = 0;
	int K = 6;
	vector<double> times;
	init("Data_train_images.txt");

	ifstream file;
	string file_name = "Data_test_images.txt";
	file.open(file_name.data());

	string s;
	int k = 0;
	while (getline(file, s)) {
		clock_t start;
		start = clock();
		vector<int> temp_arr;
		for (int i = 4; i < s.size();) {
			if (s[i] != ' ') {
				vector<int> temp_for_count;
				while (s[i] != ' ') {
					int ch = s[i] - 48;
					temp_for_count.push_back(ch);
					i++;
				}
				int sum = 0;
				for (int x = 0; x < temp_for_count.size(); x++) {
					int cnt = temp_for_count.size() - x;
					sum += temp_for_count[x] * (int)pow(10, cnt - 1);
				}
				temp_arr.push_back(sum);
			}
			i++;
		}

		int h = 28, w = 28;
		vector<vector<double> > temp_sto;
		temp_sto.resize(28);
		for (int g = 0; g < 28; g++) { temp_sto[g].resize(28); }
		for (int q = 0; q < 28; q++) {
			for (int w = 0; w < 28; w++) {
				temp_sto[q][w] = temp_arr[q * 28 + w];
			}
		}

		//test
		Matrix test(h, w, temp_sto);
		vector<value_knn> dis;
		int* Arr = random(0, 60000, 10000);
		for (int p = 0; p < 10000; p++) {
			value_knn t;
			t.num = Arr[p];
			t.distance = dataset[t.num].data.L2Distance(test);
			//cout << t.distance << endl;
			dis.push_back(t);
		}
		//cout << dis.size() << endl;
		QuickSort(dis, 0, dis.size() - 1);

		//Majority voting rule
		int arr[10];
		//memset(arr, -1, sizeof(int));
		for (int i = 0; i < 10; i++) {
			arr[i] = 0;
		}
		//cout << endl;
		for (int o = 0; o < K; o++) {
			int temp_num;
			temp_num = dis[o].num;
			int temp_label = dataset[temp_num].label;
			arr[temp_label]++;
		}
		/*for (int i = 0; i < 10; i++) {
		cout << arr[i];
		}
		cout << endl;*/
		int label = 0;
		int max = arr[0];
		for (int i = 0; i < 10; i++) {
			if (max < arr[i]) {
				max = arr[i];
				label = i;
			}
		}
		//cout << s[0] << endl;
		if (label == (s[0] - 48))
			right_num++;
		else
			wrong_num++;

		clock_t end;
		end = clock();
		double ti;
		ti = (double)(end - start) / CLOCKS_PER_SEC;
		times.push_back(ti);

		k++;
		if (k % 10 == 0) {
			cout << "have tested ";
			cout << k << " pictures";
			cout << endl;
		}

		if (k == 1001) { break; }
	}

	cout << endl;
	double time_sum = 0.0;
	for (int e = 0; e < times.size(); e++) {
		time_sum += times[e];
	}
	double average = time_sum / times.size();
	cout << "Average time use is ";
	cout << average << "." << endl;
	//cout << right_num << endl;
	acc = (double)right_num / (double)k;
	acc = acc * 100.0;
	cout << "Accuracy rating is ";
	cout << acc << "%." << endl;

	file.close();
}

int main() {
	KNN();
	cout << endl;
	system("pause");
	return 0;
}
