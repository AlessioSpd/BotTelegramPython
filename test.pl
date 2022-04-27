#!/usr/bin/perl
my $infile = './lists';
my $outfile = "$infile.tmp";

open (my $in,  '<', $infile ) || die "Can't open $infile $!\n";
open (my $out, '>', $outfile) || die "Can't open $outfile $!\n";

while (<$in>)
{   
    print $out $_;
    if ($_ =~ /#l1/) {print $out "Simon\n";}
}

close ($in);
close ($out);
rename ($outfile, $infile) || die "Unable to rename: $!";