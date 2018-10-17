#include <iostream>
#include <vector>
#include <cmath>
#include <Windows.h>
#define M_MAXN 50
using namespace std;

vector<vector<double> > init_v;

//Define Matrix class
class Matrix
{
	//Matrix
public:
	explicit Matrix(int h = 1, int w = 1, vector<vector<double>> mat = init_v)
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
	void init(int h, int w, vector<vector<double>> mat) {
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
		vector<vector<double>> temp;
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
		vector<vector<double>> temp;
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
		vector<vector<double>> temp;
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
		vector<vector<double>> Temp;
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

private:
	int height;
	int width;
	vector<vector<double>> matrix;

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
		vector<vector<double>> Temp;
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

//Dataset
Matrix Dataset[12];

void init()
{
	double Sto[12][3] = {
		{3, 6, 1},
		{1, 5, -1},
		{3, 5, 1},
		{6, 5, 1},
		{2, 4, -1},
		{4, 4, 1},
		{6, 3, 1},
		{1, 2, -1},
		{2.6, 1.6, -1},
		{4, 2, 1},
		{2, 1, -1},
		{7, 1, 1} };
	//cout << "Done" << endl;
	vector<vector<double> > temp;
	temp.resize(1);
	temp[0].resize(3);
	for (int i = 0; i < 12; i++) {
		for (int j = 0; j < 3; j++) {
			temp[0][j] = Sto[i][j];
		}
		Dataset[i].init(1, 3, temp);
	}

	//cout << "Done" << endl;
}

//Perceptron
void perceptron(Matrix &w, double &b, double lr) {
	int kase = 0;
	for (int i = 0; i < 12; i++) {
		vector<vector<double> > temp_sto;
		temp_sto.resize(1);
		temp_sto[0].resize(2);
		temp_sto[0][0] = Dataset[i].getElement(0, 0);
		temp_sto[0][1] = Dataset[i].getElement(0, 1);
		Matrix temp_trans(1, 2, temp_sto);
		Matrix temp_mul = temp_trans.TransposedMat();
		Matrix result = w.multiply(temp_mul);
		double value = result.getElement(0, 0);
		double key = Dataset[i].getElement(0, 2)*(value + b);

		if (key > 0) { kase++; }
		else { break; }
	}

	if (kase == 12) {
		return;
	}
	else {
		vector<vector<double> > sto;
		sto.resize(1);
		sto[0].resize(2);
		sto[0][0] = Dataset[kase].getElement(0, 0);
		sto[0][0] = sto[0][0] * Dataset[kase].getElement(0, 2)*lr;
		sto[0][1] = Dataset[kase].getElement(0, 1);
		sto[0][1] = sto[0][1] * Dataset[kase].getElement(0, 2)*lr;
		Matrix temp(1, 2, sto);
		w = w.add(temp);
		b = b + lr * Dataset[kase].getElement(0, 2);
		perceptron(w, b, lr);
	}
}

int main() {
	init();
	vector<vector<double> > temp;
	temp.resize(1);
	temp[0].resize(2);

	temp[0][0] = 0;
	temp[0][1] = 0;

	Matrix w(1, 2, temp);
	double b = 0.0;
	double lr = 0.5;

	perceptron(w, b, lr);

	cout << w.getElement(0, 0) << " " << w.getElement(0, 1);
	cout << endl;
	cout << b << endl;

	system("pause");
	return 0;
}
