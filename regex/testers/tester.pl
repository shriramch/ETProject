use warnings;
use strict;

my $target = "ZA\n";
my $regex = "^A*\$";

if($target =~ /$regex/) {
	print("True\n");
}
else {
	print("False\n");
}
