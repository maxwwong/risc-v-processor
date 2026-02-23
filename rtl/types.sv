package riscv_types;
    typedef enum logic [3:0] { 
        ADD,
        SUB,
        AND,
        OR,
        XOR,
        SLL,
        SRL,
        SRA,
        SLT,
        SLTU
    } alu_op;
    
endpackage