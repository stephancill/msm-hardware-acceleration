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

import elliptic_curve_structs::*;

module tb_Booth_Multiplier();

parameter p = params.p;
parameter CLK_PERIOD = 10;

logic   [P_WIDTH-1:0]    a, b;
logic  [P_WIDTH-1:0]    r_ref, r;
logic [P_WIDTH*2-1:0] ab, ab_ref;
assign ab_ref = a * b;

logic   clk, reset, i_enable, done;

initial begin
    clk = 1'b1;
    #CLK_PERIOD;
    forever begin
        clk = ~clk;
        #(CLK_PERIOD/2);
    end
end

initial begin
  i_enable = 1'b0;
  #(CLK_PERIOD*5);
  a = 377'h1647170e013bf53a7b050468f43383b17361703bef0431b3f0f3ddad4af519168f4af9b29e96740671f4fbb2b93eb11;
  b = 377'h144b5478f0886377ee7fe272cd4ca5a12f1e38816016588cffe3240b0776a00199763223e90b4b30d4f21c3d098f416;
  
  #CLK_PERIOD;
  reset = 1'b1;
  #CLK_PERIOD;
  reset = 1'b0;
  i_enable = 1'b1;

 forever begin
   if (done) begin
       if (ab == ab_ref) begin
           $display("PASS: r == r_re");
            
       end else
       begin
           $display("ERROR: r != r_re");
       end
       $finish();
   end 
   #CLK_PERIOD;
 end
end

BoothWrapper #(
    .width         (P_WIDTH)
  ) u_booth_multiplier (
    .a(a),
    .b(b),
    .ab(ab),
    .clk(clk),
    .reset(reset),
    .done(done)
    );

endmodule
