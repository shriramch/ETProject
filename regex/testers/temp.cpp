#include <iostream>
#include <boost/regex.hpp>
#include <string>

using namespace std;
using namespace boost;

int main(int argc, char* argv[])
{
	string target = "ZA";
	regex reg("^A*$");

	if(regex_search(target, reg) == true)
		cout << "True\n";
	else
		cout << "False\n";

	return 0;
}
