module register_file #(
    parameter WIDTH = 32
) (
    input wire clk,
    input wire rst,
    input wire write_en,
    input wire [4:0] rs1_addr,
    input wire [4:0] rs2_addr,
    input wire [WIDTH-1:0] write_data,
    input wire [4:0] write_addr,
    output logic [WIDTH-1:0] rs1_data,
    output logic [WIDTH-1:0] rs2_data
);

    logic [WIDTH-1:0] registers [31:0];

    assign rs1_data = (rs1_addr == 0) ? 0 : registers[rs1_addr];
    assign rs2_data = (rs2_addr == 0) ? 0 : registers[rs2_addr];


    always_ff @(posedge clk) begin
        if (rst) begin
            for (int i = 0; i < 32; i = i + 1) begin
                registers[i] <= 0;
            end
        end
        else if (write_en && write_addr != 0) begin
            registers[write_addr] <= write_data;
        end
    end

endmodule