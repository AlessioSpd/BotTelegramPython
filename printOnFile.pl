#!/usr/bin/perl

$path = shift @ARGV;
$value = shift @ARGV;
open($fh, ">>", $path) if(-e $path);
print $fh "$value\n";
close $fh;