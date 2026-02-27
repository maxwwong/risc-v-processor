module pc #(
    parameter MEM_WIDTH = 32
) (
    input wire clk,
    input wire rst,
    input wire jump_en,
    input wire [MEM_WIDTH-1:0] new_addr,
    output logic [MEM_WIDTH-1:0] pc_out
);
    logic [MEM_WIDTH-1:0] pc_local;

    assign pc_out = pc_local;

    always_ff @(posedge clk) begin
        if (rst) begin
            pc_local <= 0;
        end else begin
            if (jump_en) begin
                pc_local <= new_addr;
            end else begin
                pc_local <= pc_local + 4;
            end
        end
    end

endmodule