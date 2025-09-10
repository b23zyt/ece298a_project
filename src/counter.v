`default_nettype none

module counter (
    input wire clk,
    input wire rst_n,
    input wire load_en,
    input wire oe,
    input wire [7:0] load_val,
    output wire[7:0] count_val,
    output wire[7:0] count_oe
);

    reg [7:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'b0;
        else if(load_en)
            count <= load_val;
        else
            count <= count + 1;
    end

    assign count_val = count;
    assign count_oe = {8{oe}}; //8 bit output 

endmodule