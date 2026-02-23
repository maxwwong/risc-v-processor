import riscv_types::*;

module alu #(
    parameter WIDTH = 32
) (
    input wire [WIDTH-1:0] a,
    input wire [WIDTH-1:0] b,
    input alu_op op,
    output logic [WIDTH-1:0] result 
);

always_comb begin
    case (op)
        ADD: result = a + b;
        SUB: result = a - b;
        AND: result = a & b;
        OR: result = a | b;
        XOR: result = a ^ b;
        SLL: result = a << b[4:0];
        SRA: result = $signed(a) >>> b[4:0];
        SRL: result = a >> b[4:0];
        SLT: result = $signed(a) < $signed(b) ? 32'b1 : 32'b0;
        SLTU: result = (a < b) ? 32'b1 : 32'b0;
        default: result = 32'b0;
    endcase
end

endmodule