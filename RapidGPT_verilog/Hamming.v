/* Design a Hamming window in verilog */
module hamming_window_rom(
    input wire [3:0] address, // 4-bit address for 16 coefficients
    output reg [7:0] coefficient // 8-bit window coefficient
);

// Pre-calculated Hamming Window coefficients for N=16 (example values)
// Replace these with the actual calculated coefficients for your window size
reg [7:0] coefficients[15:0] = {
    8'hFF, // coefficient for n=0
    8'hF7, // coefficient for n=1
    8'hE1, // coefficient for n=2
    8'hC7, // coefficient for n=3
    8'hA5, // coefficient for n=4
    8'h7F, // coefficient for n=5
    8'h57, // coefficient for n=6
    8'h30, // coefficient for n=7
    8'h0F, // coefficient for n=8
    8'hF1, // coefficient for n=9
    8'hD7, // coefficient for n=10
    8'hC1, // coefficient for n=11
    8'hB0, // coefficient for n=12
    8'hA3, // coefficient for n=13
    8'h9A, // coefficient for n=14
    8'h96  // coefficient for n=15
};

always @(address) begin
    coefficient = coefficients[address]; // Output the coefficient based on the address
end

endmodule