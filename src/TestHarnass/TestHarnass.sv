module TestHarnass (
    input logic clk,
    input logic rst,
    output logic done,
    output logic out

);

logic [127:0] a, b;
logic [255:0] c;
logic enable;

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
        a <= 128'd194012132967336151925193938223512605765;
        b <= 128'd265378315908090481383838817922603599831;
        enable <= 1'b0;
    end else begin
        enable <= 1'b1;
    end
end

assign out = clk;


endmodule