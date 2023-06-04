use warnings;
use strict;

open my $targetfh, '<', $ARGV[0] or die "Can't open file $!";
open my $regexfh, '<', $ARGV[1] or die "Can't open file $!";

read $targetfh, my $target, -s $targetfh;
read $regexfh, my $regex, -s $regexfh;

if($target =~ /$regex/) {
	print("True\n");
}
else {
	print("False\n");
}
