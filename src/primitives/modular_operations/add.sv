import elliptic_curve_structs::*;

module add
	(input logic [P_WIDTH-1:0] a, b,
	 input logic op,
	output logic [P_WIDTH-1:0] sum);

logic [P_WIDTH:0] temp1, temp2;
	// op = 1, a-b mod p
	// op = 0, a+b mod p

always_comb
begin
	if(op) begin
			temp1 = a-b;
			temp2 = (a-b) + params.p;
			if(temp1[P_WIDTH])
				sum = temp2[P_WIDTH-1:0];
			else
				sum = temp1[P_WIDTH-1:0];
	end
	else begin
		temp1 = a + b;
		temp2 = (a + b) - params.p;
		if(temp1 >= params.p)
			sum = temp2[P_WIDTH-1:0];
		else
			sum = temp1[P_WIDTH-1:0];
	end
end
endmodule
