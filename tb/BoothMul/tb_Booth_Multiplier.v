///////////////////////////////////////////////////////////////////////////////
//
//  Copyright 2010-2012 by Michael A. Morris, dba M. A. Morris & Associates
//
//  All rights reserved. The source code contained herein is publicly released
//  under the terms and conditions of the GNU Lesser Public License. No part of
//  this source code may be reproduced or transmitted in any form or by any
//  means, electronic or mechanical, including photocopying, recording, or any
//  information storage and retrieval system in violation of the license under
//  which the source code is released.
//
//  The souce code contained herein is free; it may be redistributed and/or 
//  modified in accordance with the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either version 2.1 of
//  the GNU Lesser General Public License, or any later version.
//
//  The souce code contained herein is freely released WITHOUT ANY WARRANTY;
//  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
//  PARTICULAR PURPOSE. (Refer to the GNU Lesser General Public License for
//  more details.)
//
//  A copy of the GNU Lesser General Public License should have been received
//  along with the source code contained herein; if not, a copy can be obtained
//  by writing to:
//
//  Free Software Foundation, Inc.
//  51 Franklin Street, Fifth Floor
//  Boston, MA  02110-1301 USA
//
//  Further, no use of this source code is permitted in any form or means
//  without inclusion of this banner prominently in any derived works. 
//
//  Michael A. Morris
//  Huntsville, AL
//
///////////////////////////////////////////////////////////////////////////////

`timescale 1ns / 1ps

///////////////////////////////////////////////////////////////////////////////
// Company:         M. A. Morris & Associates
// Engineer:        Michael A. Morris
//  
// Create Date:     21:48:39 07/10/2010
// Design Name:     Booth_Multiplier
// Module Name:     C:/XProjects/ISE10.1i/F9408/tb_Booth_Multiplier.v
// Project Name:    Booth_Multiplier
// Target Devices:  Spartan-3AN
// Tool versions:   Xilinx ISE 10.1 SP3
//
// Description:
//
// Verilog Test Fixture created by ISE for module: Booth_Multiplier
//
// Dependencies: 
//
// Revision: 
//
//  0.01    10G10   MAM     File Created
//
// Additional Comments: 
//
///////////////////////////////////////////////////////////////////////////////

module tb_Booth_Multiplier;

parameter N = 7;
parameter CLK_PERIOD = 10;

//  UUT Signals

reg     Rst;
reg     Clk;

reg     Ld;
reg     [(2**N - 1):0] M;
reg     [(2**N - 1):0] R;

wire    Valid;
wire    [(2**(N+1) - 1):0] P, P_ref;
assign P_ref = M * R;


// Instantiate the Unit Under Test (UUT)

Booth_Multiplier    #(
    .pN(N)
  ) uut (
    .Rst(Rst), 
    .Clk(Clk), 
    .Ld(Ld), 
    .M(M), 
    .R(R), 
    .Valid(Valid), 
    .P(P)
  );

initial begin
    // Initialize Inputs
  Rst = 1;
  Clk = 1;
  Ld  = 0;
  M   = 0;
  R   = 0;
 

  // Wait 100 ns for global reset to finish
  #(CLK_PERIOD*10) Rst = 0;
  
  // Add stimulus here
  #CLK_PERIOD Ld = 1'b1;

  M = 128'd123;
  R = 128'd456;

  #(CLK_PERIOD*2) Ld = 1'b0;

  forever begin
    if (Valid) begin
      if (P == P_ref) begin
        $display("PASS: P == P_ref");
      end else begin
        $display("ERROR: P != P_ref");
      end
      $finish();
    end 
    #CLK_PERIOD;
  end
    
end

///////////////////////////////////////////////////////////////////////////////

always #CLK_PERIOD Clk = ~Clk;
      
///////////////////////////////////////////////////////////////////////////////

endmodule
