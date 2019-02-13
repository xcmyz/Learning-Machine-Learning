#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <ctime>
#include <Windows.h>
#define MAXN 2000
using namespace std;

vector<string> Load_File(string filename, int num) {
	cout << "Loading files..." << endl;
	//clock_t t1 = clock();
	/*char* buffer;
	buffer = new char[MAXN];*/
	int cnt = 0;
	static vector<string> out_string;
	out_string.clear();

	/*fstream datafile;
	datafile.open(filename.c_str(), ios::in);
	int nt = 0;*/

	char *str;
	str = (char*)filename.data();
	ifstream in(str);

	while (true) {
		string line;
		/*char* buffer;
		buffer = new char[MAXN];*/
		getline(in, line);
		//cout << buffer << endl;
		out_string.push_back(line);
		//cout << out_string[cnt].size() << endl;

		/*nt++;
		if (nt == 65) {
			cout << buffer << endl;
		}*/
		cnt++;
		if (cnt == num) {
			break;
		}
		if (cnt % 100 == 0) {
			//cout << cnt << "wejhweihdiweh" << endl;
			//cout << cnt << endl;
		}
		//delete[]buffer;
	}
	//clock_t t2 = clock();
	//double t = (t2 - t1) / CLOCKS_PER_SEC;

	//cout << "Done, has take ";
	//printf("%.2f", t);
	//cout << " ." << endl;
	cout << "Done." << endl;
	//datafile.close();
	return out_string;
}

vector<int*> return_data(vector<string> in, int arr_size) {
	cout << "Processing files..." << endl;
	//cout << in[1] << endl;
	static vector<int*> out_arr;
	out_arr.clear();
	out_arr.resize(arr_size);
	int cnt = 0;

	for (int i = 0; i < arr_size; i++) {
		//cout << in[i].size() << endl;
		vector<char> temp_arr;
		int st = 0;
		out_arr[i] = new int[MAXN];
		for (int c = 4; c < in[i].size(); c++) {
			//cout << "bsjdgqkkhqwkhqkhq" << endl;
			if (in[i][c] != ' ') {
				temp_arr.push_back(in[i][c]);
			}
			if (in[i][c] == ' ') {
				int num = 0;
				for (int y = 0; y < temp_arr.size(); y++) {
					//cout << "bsjdgqkkhqwkhqkhq" << endl;
					int t = temp_arr.size() - y - 1;
					num += (temp_arr[y] - 48)*(int)pow(10.0, (double)t);

				}
				//cout << num << endl;
				//cout << "bsjdgqkkhqwkhqkhq" << endl;
				out_arr[cnt][st++] = num;
				temp_arr.clear();
				//cout << "bsjdgqkkhqwkhqkhq" << endl;
			}
		}

		cnt++;
		if (cnt % 100 == 0) {
			//cout << cnt << endl;
		}
	}

	if (out_arr.size() == arr_size)
		//cout << "Equal" << endl;
		cout << "Done." << endl;
	return out_arr;
}

vector<int> return_label(vector<string> in, int arr_size) {
	cout << "Processing files..." << endl;
	static vector<int> out_arr;
	out_arr.clear();
	int cnt = 0;

	for (int i = 0; i < arr_size; i++) {
		//cout << in[i][0] - 48 << endl;
		out_arr.push_back(in[i][0] - 48);
		//cout << out_arr[i] << endl;

		cnt++;
		if (cnt % 100 == 0) {
			//cout << cnt << endl;
		}
	}

	if (out_arr.size() == arr_size)
		//cout << "Equal" << endl;
		cout << "Done." << endl;
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
	//cout << "hguvgdkhwdigviwuhuh" << endl;

	vector<int*> train_data_im(return_data(train_data, 60000));
	vector<int> train_label(return_label(train_data, 60000));

	vector<int*> test_data_im(return_data(test_data, 10000));
	vector<int> test_label(return_label(test_data, 10000));

	/*cout << "ggkgkgkhkhljlj" << endl;
	for (int i = 0; i < 28; i++) {
		for (int j = 0; j < 28; j++) {
			int y = train_data_im[666][i * 28 + j];
			if (y < 10) {
				cout << "00" << y << " ";
			}
			else if (y >= 10 && y < 100) {
				cout << "0" << y << " ";
			}
			else {
				cout << train_data_im[7][i * 28 + j] << " ";
			}
		}
		cout << endl;
	}
	cout << train_data_im[666] << endl;
	cout << "hhohhh" << endl;*/

	//test
	int test = 66;
	FILE* Temp;
	Temp = fopen("test.txt", "wb+");
	fclose(Temp);

	ofstream location_out;
	location_out.open("test.txt", std::ios::out | std::ios::app);
	//location_out << train_data_im[6];
	for (int i = 0; i < 28; i++) {
		for (int j = 0; j < 28; j++) {
			int y = train_data_im[test][i * 28 + j];
			if (y < 10) {
				location_out << "00" << y << " ";
			}
			else if (y >= 10 && y < 100) {
				location_out << "0" << y << " ";
			}
			else {
				location_out << y << " ";
			}
			/*if (y > 100) {
				location_out << "0";
			}
			else {
				location_out << "1";
			}*/
		}
		location_out << endl;
	}
	location_out.close();
	cout << train_label[test] << endl;

	system("pause");
	return 0;
}
