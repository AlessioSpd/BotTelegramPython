#!/usr/bin/perl

$path = shift @ARGV;
open($fh, "<", $path) if(-e $path);
while(<$fh>){
	print $_;
}
close $fh;