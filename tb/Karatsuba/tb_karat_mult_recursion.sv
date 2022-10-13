// This is the karat_mult_recursion_tb module for project 
// Karatsuba_multiplier_HDL
// Copyright (C) 2020 JC-S
// 
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

//-----------------------------------------------------------------------------
//
//FILE NAME     : karat_mult_recursion_tb.sv
//AUTHOR        : JC-S
//FUNCTION      : Testbench for karat_mul module
//INITIAL DATE  : 2020/06/23
//VERSION       : 1.0
//CHANGE LOG    : 1.0: initial version.
//
//-----------------------------------------------------------------------------

`timescale 1ns / 1ps

module karat_mult_recursion_tb();

parameter wI = 128;
parameter wO = 2 * wI;
parameter nSTAGE = 5;
parameter CLK_PERIOD = 10;

logic   [wI-1:0]    iX, iY;
logic   [wO-1:0]    oO_ref;
logic   [wO-1:0]    oO_rec;
assign  oO_ref = iX * iY;

logic   clk, reset;
logic   i_enable, o_finish_rec;

initial begin
    clk = 1'b1;
    reset = 1'b0;
    #CLK_PERIOD;
    reset = 1'b1;
    #CLK_PERIOD;
    reset = 1'b0;
    #CLK_PERIOD;
    forever begin
        clk = ~clk;
        #(CLK_PERIOD/2);
    end
end

initial begin
    reset = 1'b1;
    i_enable = 1'b0;
    iX = 'b0;
    iY = 'b0;
    #CLK_PERIOD;
    reset = 1'b0;
    #(CLK_PERIOD*10);
    i_enable = 1'b1;
    forever begin
        if(o_finish_rec && clk)
        begin
            assert (oO_rec == oO_ref);
            if (oO_rec == oO_ref) begin
                assert (oO_rec == oO_ref); 
                $display("PASS: oO == oO_ref");
            end
            else
            begin
                $error("ERROR: oO != oO_ref!");
                $finish;    
            end
            std::randomize(iX, iY);
        end
        #(CLK_PERIOD/2);
    end
end

karat_mult_recursion #(
    .wI         (wI),
    .nSTAGE     (nSTAGE)
)
u_karat_mult_recursion (
    .o_finish   (o_finish_rec),
    .oO         (oO_rec),
    .reset(reset),
    .clk(clk),
    .*);

endmodule

