`default_nettype none

module counter (
    input wire clk,
    input wire rst_n,
    input wire load_en,
    input wire [7:0] load_val,
    input wire oe,
    output wire[7:0] output_val
);

    reg [7:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 8'b0;
        end else if(load_en) begin
            count <= load_val;
        end else begin
            count <= count + 1;
        end
    end

    assign output_val = oe ? count : 8'bz;

endmodule