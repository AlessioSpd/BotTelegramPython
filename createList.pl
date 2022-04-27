#!/usr/bin/perl

$name_of_file = shift @ARGV;

$folder_of_file = "./files";
mkdir $folder_of_file unless (-d $folder_of_file);

$new_file_path = $folder_of_file."/".$name_of_file;
open($fh, ">", $new_file_path) unless(-e $new_file_path);
print $fh "ciao\n";
print $fh "ciao2\n";
close $fh;