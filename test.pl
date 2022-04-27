#!/usr/bin/perl

$path = shift @ARGV;
$value = shift @ARGV;
print $value;
# open($fh, ">>", $path) if(-e $path);
# print $fh $value;
# close $fh;