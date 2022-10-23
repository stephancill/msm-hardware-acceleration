package elliptic_curve_structs;

typedef struct packed {
    logic [255:0] x;
    logic [255:0] y;
} curve_point_t;

curve_point_t inf_point = {256'h0, 256'h0};

typedef struct packed {
    logic [255:0] p;
    logic [255:0] n;
    logic [255:0] a;
    logic [255:0] b;
    curve_point_t base_point;
} secp256k1_parameters;

secp256k1_parameters params = '{p:256'd37,
                                n:256'd13,
                                a:256'd0,
                                b:256'd7,
								base_point:{256'd6,
										    256'd1}};

typedef struct packed {
    logic m;            // m = 1 for secp256k1
    logic k;            // k = 256 for secp256k1
} barrett_constants_t;

barrett_constants_t barrett_constants = '{m:1, k:256};

typedef struct packed {
    logic [255:0] r;
    logic [255:0] s;
} signature_t;

endpackage : elliptic_curve_structs
