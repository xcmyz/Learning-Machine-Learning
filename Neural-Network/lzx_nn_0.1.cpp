#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
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
				w[k][l][m] = 0.01;
			}
		}
	}

	for (int n = 0; n < number_of_layer; n++) {
		b[n] = 0.01;
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
				//cout << w[cnt][j][i] * x[cnt][j] << endl;
			}
			value[cnt][i] = temp_value;
			//cout << value[cnt][i] << endl;
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
		//cout << each_layer_num[number_of_layer] << endl;
		//cout << d[i] << endl;
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
				//cout << w[cnt][j][i] * x[cnt][j] << endl;
			}
			value[cnt][i] = temp_value;
			//cout << value[cnt][i] << endl;
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

	//cout << out << endl;
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


//Load dataset
vector<string> Load_File(string filename, int num) {
	cout << "Loading files..." << endl;
	int cnt = 0;
	static vector<string> out_string;
	out_string.clear();

	char *str;
	str = (char*)filename.data();
	ifstream in(str);

	while (true) {
		string line;
		getline(in, line);
		out_string.push_back(line);

		cnt++;
		if (cnt == num) {
			break;
		}
	}

	cout << "Loaded files." << endl;
	return out_string;
}

vector<int*> return_data(vector<string> in, int arr_size) {
	cout << "Processing data files..." << endl;

	static vector<int*> out_arr;
	out_arr.clear();
	out_arr.resize(arr_size);
	int cnt = 0;

	for (int i = 0; i < arr_size; i++) {
		vector<char> temp_arr;
		int st = 0;
		out_arr[i] = new int[MAXN];
		for (int c = 4; c < in[i].size(); c++) {
			if (in[i][c] != ' ') {
				temp_arr.push_back(in[i][c]);
			}
			if (in[i][c] == ' ') {
				int num = 0;
				for (int y = 0; y < temp_arr.size(); y++) {
					int t = temp_arr.size() - y - 1;
					num += (temp_arr[y] - 48)*(int)pow(10.0, (double)t);

				}
				out_arr[cnt][st++] = num;
				temp_arr.clear();
			}
		}

		cnt++;
	}

	if (out_arr.size() == arr_size)
		cout << "Processed data files." << endl;
	return out_arr;
}

vector<int> return_label(vector<string> in, int arr_size) {
	cout << "Processing label files..." << endl;
	static vector<int> out_arr;
	out_arr.clear();
	int cnt = 0;

	for (int i = 0; i < arr_size; i++) {
		out_arr.push_back(in[i][0] - 48);
		cnt++;
	}

	if (out_arr.size() == arr_size)
		cout << "Processed label files." << endl;
	return out_arr;
}

int main() {
	string train_file_name;
	string test_file_name;

	train_file_name = "C:/Users/28012/Desktop/Machine Learning/";
	train_file_name += "Neural Networks/MLP for MNIST/Data_train_images.txt";
	test_file_name = "C:/Users/28012/Desktop/Machine Learning/";
	test_file_name += "Neural Networks/MLP for MNIST/Data_test_images.txt";

	vector<string> train_data(Load_File(train_file_name, 60000));
	vector<string> test_data(Load_File(test_file_name, 10000));

	//Get data
	vector<int*> train_data_im(return_data(train_data, 60000));
	vector<int> train_label(return_label(train_data, 60000));

	vector<int*> test_data_im(return_data(test_data, 10000));
	vector<int> test_label(return_label(test_data, 10000));

	//Define a neural network
	cout << "Start training..." << endl;
	double start_time = clock();
	vector<int> nn_size;
	nn_size.push_back(28 * 28);
	nn_size.push_back(300);
	nn_size.push_back(10);
	NeuralNetwork lzx_first_nn(2, nn_size, 0.03);

	//Train
	for (int cnt = 0; cnt < 100; cnt++) {
		if ((cnt + 1) % 10 == 0) {
			double once_time = clock();
			double take_time = (once_time - start_time) / CLOCKS_PER_SEC;
			cout << "Have trained " << (cnt + 1) * 1000;
			cout << " times." << endl;
			cout << take_time;
			cout << "s has been used." << endl;
		}
		vector<double> in_nn;
		for (int i = 0; i < 28 * 28; i++) {
			double in_value;
			double v = train_data_im[cnt][i] + 1;
			in_value = v / 256.0;
			//in_value = v*10;
			in_nn.push_back(in_value);
		}

		vector<double> in_nn_d;
		in_nn_d.resize(10);
		for (int y = 0; y < in_nn_d.size(); y++) {
			in_nn_d[y] = 0.0;
		}
		in_nn_d[train_label[cnt]] = 1.0;

		cout << endl;
		bool ifoutput = true;
		for (int s = 0; s < 300; s++) {
			lzx_first_nn.forward_for_train(in_nn, in_nn_d);
			if (ifoutput) {
				lzx_first_nn.print_e();
				ifoutput = false;
			}
			lzx_first_nn.backward((s + 1)*(cnt + 1));
		}
		lzx_first_nn.forward_for_train(in_nn, in_nn_d);
		lzx_first_nn.print_e();
		cout << endl;
	}

	//Test
	int right_num = 0;
	for (int cnt = 0; cnt < test_data_im.size(); cnt++) {
		if ((cnt + 1) % 2000 == 0) {
			cout << (cnt + 1) << " pictures have been tested." << endl;
		}
		vector<double> in_nn;
		for (int i = 0; i < 28 * 28; i++) {
			double in_value;
			double t_v = test_data_im[cnt][i] + 1.0;
			in_value = (t_v) / 256.0;
			//in_value = t_v;
			in_nn.push_back(in_value);
		}

		/*for (int y = 0; y < 28; y++) {
			for (int b = 0; b < 28; b++) {
				cout << in_nn[y * 28 + b] << " ";
			}
			cout << endl;
		}
		cout << test_label[cnt] << endl;*/

		int  result = lzx_first_nn.forward_for_test(in_nn);
		if (result == test_label[cnt]) {
			right_num++;
		}
	}

	double end_time = clock();
	double whole_time = (end_time - start_time) / CLOCKS_PER_SEC;
	cout << "The whole time used is ";
	cout << whole_time << "s.";
	cout << endl;

	double accuracy = (double)right_num / (double)test_data_im.size();
	cout << "The accuracy of lzx_first_nn is ";
	cout << accuracy << ".";
	cout << endl;

	system("pause");
	return 0;
}
