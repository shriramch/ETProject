#include <fstream>
#include <iostream>
#include <boost/regex.hpp>
#include <string>

using namespace std;
using namespace boost;

int main(int argc, char* argv[])
{
	ifstream target_in(argv[1]);
	ifstream reg_in(argv[2]);
	ostringstream tstr, rstr;
	
	tstr << target_in.rdbuf();
	string target(tstr.str());
	target_in.close();
	
	rstr << reg_in.rdbuf();
	regex reg(rstr.str());
	reg_in.close();

	if(regex_search(target, reg) == true)
		cout << "True\n";
	else
		cout << "False\n";

	return 0;
}
