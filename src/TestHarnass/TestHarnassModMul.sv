module TestHarnassModMul (
    input logic clk,
    input logic rst,
    output logic done
);

parameter p = params.p;
parameter CLK_PERIOD = 10;

logic   [P_WIDTH-1:0]    a, b;
logic  [P_WIDTH-1:0]    r_ref, r;
logic [P_WIDTH*2-1:0] ab;

MultiplierAdapter #(
    .width(128)
) u_MultiplierAdapter (
    .clk(clk),
    .reset(rst),
    .a(a),
    .b(b),
    .enable(enable),
    .ab(c),
    .done(done)
);

always_ff @(clk) begin
    if ( rst ) begin
        // Random hex number
        a = 377'h1647170e013bf53a7b050468f43383b17361703bef0431b3f0f3ddad4af519168f4af9b29e96740671f4fbb2b93eb11;
        b = 377'h144b5478f0886377ee7fe272cd4ca5a12f1e38816016588cffe3240b0776a00199763223e90b4b30d4f21c3d098f416;
  
        enable <= 1'b0;
    end else begin
        enable <= 1'b1;
    end
end

// assign out = clk;


endmodule