addi x1, x0, 42
addi x2, x0, 16
addi x3, x0, 8
addi x7, x0, 1
srl x3, x3, x7
sw x1, 0(x0)
sw x2, 0(x3)
lw x2, 0(x0)
lw x1, 0(x3)
addi x4, x0, 0
addi x4, x4, 4
beq x4, x3, -4
sub x1, x1, x3
xor x5, x1, x4
sll x6, x1, x7