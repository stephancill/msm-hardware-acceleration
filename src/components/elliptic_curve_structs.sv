package elliptic_curve_structs;

parameter P_WIDTH = 377;

typedef struct packed {
  logic [P_WIDTH-1:0] x;
  logic [P_WIDTH-1:0] y;
} curve_point_t;

curve_point_t inf_point = '{0, 0};

typedef struct packed {
  logic [P_WIDTH-1:0] p;
  logic [P_WIDTH-1:0] n;
  logic [P_WIDTH-1:0] a;
  logic [P_WIDTH-1:0] b;
  curve_point_t base_point;
} curve_parameters_t;

// - Small parameters
// curve_parameters_t params = '{
//   p: 37,
//   n: P_WIDTH,
//   a: 0,
//   b: 7,
// 	base_point:'{6, 1}
// };

// BLS12-377
curve_parameters_t params = '{
  p: 377'h01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001,
  n: P_WIDTH,
  a: 377'd0,
  b: 377'd1,
	base_point:'{
    x: 377'h008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef, 
    y: 377'h01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6
  }
};

typedef struct packed {
    logic m;            // m = 1 for secp256k1
    logic k;            // k = 256 for secp256k1
} barrett_constants_t;

barrett_constants_t barrett_constants = '{m: 1, k: 256};

typedef struct packed {
  logic [255:0] r;
  logic [255:0] s;
} signature_t;

endpackage : elliptic_curve_structs
