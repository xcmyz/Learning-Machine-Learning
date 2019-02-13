#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <ctime>
#define MAXN 2000
using namespace std;

class NeuralNetwork
{
public:
	NeuralNetwork(int num_of_layer, \
		vector<int> layer_num, double lr);
	~NeuralNetwork();

	void initial();
	void forward_for_train(vector<double> train_data, vector<double> d);
	int forward_for_test(vector<double> test_data);
	void backward(int batch);

	//Test
	void print_w();
	void print_v();
	void print_grad();
	void print_e();

private:
	int number_of_layer;
	vector<int> each_layer_num;
	vector<double> b;
	vector<vector<vector<double> > > w;
	vector<vector<double> > x;
	vector<vector<double> > value;
	vector<vector<double> > grad;
	vector<double> e;

	double learning_rate;
	double activation_function(double x);
	double step_length(int batch);
};

void NeuralNetwork::initial() {
	for (int k = 0; k < number_of_layer; k++) {
		for (int l = 0; l < each_layer_num[k]; l++) {
			for (int m = 0; m < each_layer_num[k + 1]; m++) {
				double t = rand() % 100 / (double)1001;
				w[k][l][m] = t;
			}
		}
	}

	for (int n = 0; n < number_of_layer; n++) {
		double t = rand() % 100 / (double)1001;
		b[n] = t;
	}
}

NeuralNetwork::NeuralNetwork(int num_of_layer, vector<int> layer_num, double lr)
	:number_of_layer(num_of_layer), each_layer_num(layer_num), learning_rate(lr)
{
	cout << "The initialization of w begins..." << endl;
	//number_of_layer = each_layer_num.length() - 1
	w.resize(number_of_layer);
	for (int i = 0; i < number_of_layer; i++) {
		w[i].resize(each_layer_num[i]);
		for (int j = 0; j < each_layer_num[i]; j++) {
			w[i][j].resize(each_layer_num[i + 1]);
		}
	}
	cout << "The initialization of w has done." << endl;

	cout << "The initialization of value, grad, x, e and etc begins..." << endl;
	//The first dimension is output value
	e.clear();
	e.resize(each_layer_num[number_of_layer]);

	b.resize(number_of_layer);

	grad.resize(number_of_layer);
	for (int x = 0; x < number_of_layer; x++) {
		grad[x].resize(each_layer_num[x + 1]);
	}

	value.resize(number_of_layer);
	for (int y = 0; y < number_of_layer; y++) {
		value[y].resize(each_layer_num[y + 1]);
	}

	x.resize(number_of_layer + 1);
	for (int z = 0; z < number_of_layer + 1; z++) {
		x[z].resize(each_layer_num[z]);
	}
	cout << "The initialization of value, grad, x, e and etc has done." << endl;

	cout << "Assigning an initial value..." << endl;
	initial();
	cout << "Assigned an initial value..." << endl;
}

NeuralNetwork::~NeuralNetwork()
{
	//Default
}

void NeuralNetwork::forward_for_train(vector<double> train_data, \
	vector<double> d) {
	for (int i = 0; i < each_layer_num[0]; i++) {
		x[0][i] = train_data[i];
	}

	//Layer depended
	for (int cnt = 0; cnt < number_of_layer; cnt++) {
		//Add
		for (int i = 0; i < each_layer_num[cnt + 1]; i++) {
			double temp_value = 0.0;
			for (int j = 0; j < each_layer_num[cnt]; j++) {
				temp_value = temp_value + w[cnt][j][i] * x[cnt][j];
			}
			value[cnt][i] = temp_value;
		}

		//Activate
		for (int y = 0; y < each_layer_num[cnt + 1]; y++) {
			double value_for_process = 0;
			value_for_process = value[cnt][y] + b[cnt];
			value[cnt][y] = value[cnt][y] + b[cnt];
			x[cnt + 1][y] = activation_function(value_for_process);
		}
	}

	//Count e
	for (int i = 0; i < each_layer_num[number_of_layer]; i++) {
		double temp_e = d[i] - x[number_of_layer][i];
		e[i] = temp_e;
	}
}

int NeuralNetwork::forward_for_test(vector<double> test_data) {
	for (int i = 0; i < each_layer_num[0]; i++) {
		x[0][i] = test_data[i];
	}

	for (int i = 0; i < each_layer_num[0]; i++) {
		x[0][i] = test_data[i];
	}

	//Layer depended
	for (int cnt = 0; cnt < number_of_layer; cnt++) {
		//Add
		for (int i = 0; i < each_layer_num[cnt + 1]; i++) {
			double temp_value = 0.0;
			for (int j = 0; j < each_layer_num[cnt]; j++) {
				temp_value = temp_value + w[cnt][j][i] * x[cnt][j];
			}
			value[cnt][i] = temp_value;
		}

		//Activate
		for (int y = 0; y < each_layer_num[cnt + 1]; y++) {
			double value_for_process = 0;
			value_for_process = value[cnt][y] + b[cnt];
			value[cnt][y] = value[cnt][y] + b[cnt];
			x[cnt + 1][y] = activation_function(value_for_process);
		}
	}


	int out = 0;
	double max_value = x[number_of_layer][0];
	for (int tt = 0; tt < each_layer_num[number_of_layer]; tt++) {
		if (max_value < x[number_of_layer][tt]) {
			max_value = x[number_of_layer][tt];
			out = tt;
		}
	}

	return out;
}

void NeuralNetwork::backward(int batch) {
	//Count grad
	//Calculate the first 
	for (int i = 0; i < each_layer_num[number_of_layer]; i++) {
		grad[number_of_layer - 1][i] = e[i] * \
			x[number_of_layer][i] * (1 - x[number_of_layer][i]);
	}
	//Recursion
	for (int xx = number_of_layer - 1 - 1; xx >= 0; xx--) {
		for (int i = 0; i < each_layer_num[xx + 1]; i++) {
			double temp_value = 0.0;
			for (int m = 0; m < each_layer_num[xx + 1 + 1]; m++) {
				temp_value += w[xx + 1][i][m] * grad[xx + 1][m];
			}
			grad[xx][i] = x[xx + 1][i] * (1 - x[xx + 1][i]);
			grad[xx][i] = grad[xx][i] * temp_value;
		}
	}

	//Update
	for (int k = 0; k < number_of_layer; k++) {
		for (int l = 0; l < each_layer_num[k]; l++) {
			for (int m = 0; m < each_layer_num[k + 1]; m++) {
				w[k][l][m] = w[k][l][m] + \
					step_length(batch)*grad[k][m] * x[k][l];
			}
		}
	}

	for (int n = 0; n < number_of_layer; n++) {
		double temp_sum_grad = 0;
		for (int o = 0; o < each_layer_num[n + 1]; o++) {
			temp_sum_grad = temp_sum_grad + \
				grad[n][o];
		}
		double t_v = (temp_sum_grad / each_layer_num[n + 1])*step_length(batch);
		b[n] = b[n] + t_v;
	}
}

double NeuralNetwork::activation_function(double x)
{
	//Sigmoid
	double t1 = exp(-x);
	double t2 = t1 + 1.0;
	double t3 = 1.0 / t2;
	return t3;
}

double NeuralNetwork::step_length(int batch) {
	double out = 0.0;
	out = learning_rate / (1.0 + (double)batch / 100000.0);

	return out;
}

void NeuralNetwork::print_w() {
	for (int i = 0; i < number_of_layer; i++) {
		for (int j = 0; j < each_layer_num[i]; j++) {
			for (int k = 0; k < each_layer_num[i + 1]; k++) {
				cout << w[i][j][k] << " ";
			}
			cout << endl;
		}
		cout << endl;
	}
}

void NeuralNetwork::print_v() {
	for (int i = 0; i < number_of_layer; i++) {
		for (int j = 0; j < each_layer_num[i + 1]; j++) {
			cout << value[i][j] << " ";
		}
		cout << endl;
	}
	cout << endl;
}

void NeuralNetwork::print_grad() {
	for (int i = 0; i < number_of_layer; i++) {
		for (int j = 0; j < each_layer_num[i + 1]; j++) {
			cout << grad[i][j] << " ";
		}
		cout << endl;
	}
}

void NeuralNetwork::print_e() {
	for (int i = 0; i < each_layer_num[number_of_layer]; i++) {
		cout << e[i] << " ";
	}
	cout << endl;
}
