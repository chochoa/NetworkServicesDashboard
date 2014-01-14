#!/usr/SD/perl/bin/perl -w
use strict;

use LWP::UserAgent;
use JSON;
use Data::Dumper;

use constant PROTOCOL => 'https';
use constant PORT     => '443';
use constant API_PATH => '/webacs/api/v1';
use constant USERNAME => 'admin';
use constant PASSWORD => '********';

foreach my $hostname qw( pir-aer1-1-a.cisco.com pir-blr1-1-a.cisco.com pir-rtp5-1-a.cisco.com pir-rch2-1-a.cisco.com pir-mtv1-1-a.cisco.com ) {
   
   my $base_url = PROTOCOL.'://'.$hostname.':'.PORT.API_PATH;

   print "\n$hostname...\n\n";

   my $url = $base_url.'/data/AccessPoints/.json?.full=true&.maxResults=1000';

   my $firstResult = 0;

   while ( $firstResult % 1000 == 0 ) {
       my $ua = LWP::UserAgent->new();
       my $req = HTTP::Request->new( GET => "$url&.firstResult=$firstResult" );
       $req->authorization_basic( USERNAME, PASSWORD );
       my $res = $ua->request( $req ); 

       if (! $res->is_success) {
           die $res->status_line;
       }

       my $json = $res->content;
       my $obj = jsonToObj( $json );

       $firstResult += scalar(@{$obj->{queryResponse}{entity}});
   }

   print "Access Points: $firstResult\n";

   $url = $base_url.'/data/WlanControllers/.json?.full=true&.maxResults=1000';

   $firstResult = 0;

   while ( $firstResult % 1000 == 0 ) {
       my $ua = LWP::UserAgent->new();
       my $req = HTTP::Request->new( GET => "$url&.firstResult=$firstResult" );
       $req->authorization_basic( USERNAME, PASSWORD );
       my $res = $ua->request( $req ); 

       if (! $res->is_success) {
           die $res->status_line;
       }

       my $json = $res->content;
       my $obj = jsonToObj( $json );

       $firstResult += scalar(@{$obj->{queryResponse}{entity}});
   }
   print "Wireless LAN Controllers: $firstResult\n";
}