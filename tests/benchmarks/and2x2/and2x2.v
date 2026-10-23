/////////////////////////////////////////
//  Functionality: Two 2-input AND 
//  Author:        Xifan Tang
////////////////////////////////////////
`timescale 1ns / 1ps

module and2x2(
  a,
  b,
  c);

input wire [1:0] a;
input wire [1:0] b;
output wire [1:0] c;

 and2 INST0 (
  .a(a[0]),
  .b(b[0]),
  .c(c[0]),
 );

 and2 INST1 (
  .a(a[1]),
  .b(b[1]),
  .c(c[1]),
 );

endmodule
