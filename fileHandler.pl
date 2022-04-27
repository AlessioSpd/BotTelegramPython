#!/usr/bin/perl

$task = shift @ARGV;
$path = './lists';

if($task eq 'create_list'){
	$list_name = shift @ARGV;

	if(-e $path){
		open($fh, ">>", $path);
		print $fh "#$list_name\n" if(-z $path);
		print $fh "#$list_name\n" unless(-z $path);
		close $fh;
	} else {
		open($fh, ">", $path) unless(-e $path);
		print $fh "#$list_name\n";
		close $fh;
	}

} elsif ($task eq 'write_file'){
	$list_name = shift @ARGV;
	$element = shift @ARGV;

	open($in, '<', $path);
	open($out, '>', "$path.temp");

	while (<$in>){   
	    print $out $_;
	    if ($_ =~ /#$list_name/) {print $out "$element\n";}
	}

	close ($in);
	close ($out);
	rename ("$path.temp", $path) || die "Unable to rename: $!";

} elsif ($task eq 'read_file'){
	$list_name = shift @ARGV;
	$flag = 0;

	open($fh, '<', $path);
	while (<$fh>) {
		if ($_ =~ /#.*/){
			if($_ =~ /#$list_name/){
				$flag = 1;
				next;
			} else {
				$flag = 0;
			}
		}
		if($flag == 1){
			print $_;
		}
	}
	close $fh;

} elsif ($task eq 'print_list'){
	open($fh, "<", $path);
	while(<$fh>){
		if($_ =~ /#(.*)/){
			print "$1\n";
		}
	}
	close $fh;

} elsif ($task eq 'modify_file'){
	$list_name = shift @ARGV;
	$element = shift @ARGV;
	$flag = 0;
	$count = 0;

	open($in, '<', $path);
	open($out, '>', "$path.temp");

	while (<$in>){
	    $flag = 1 if ($_ =~ /#$list_name/);
	    if($flag == 1 and $_ =~ /^$element$/){
	    	$count++;
	    	next;
	    }
	    print $out $_;
	}

	close ($in);
	close ($out);
	rename ("$path.temp", $path) || die "Unable to rename: $!";

	if($count == 0) {print "errore";}

} elsif ($task eq 'delete_list'){
	$list_name = shift @ARGV;
	$flag = 0;
	$count = 0;

	open($in, '<', $path);
	open($out, '>', "$path.temp");

	while (<$in>){
		if ($_ =~ /#.*/){
			if($_ =~ /#$list_name/){
				$flag = 1;
				$count++;
				next;
			} else {
				$flag = 0;
			}
		}
	    next if($flag == 1);
	    print $out $_;
	}

	close ($in);
	close ($out);
	rename ("$path.temp", $path) || die "Unable to rename: $!";
	print "errore" if($count == 0);
}