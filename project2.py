# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name: Amane Chibana and Harry Wang                                        #
# Pledge: I pledge my honor that I have abided by the Stevens Honor System. # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def translate(instruction):  # We are using split up instruction line for parameter.
    opcode = 0b000000000000000000000000 # 24 bit machine code
    operation = instruction[0]

    if operation == "add":
        opcode += 0b1 << 0 #RegWrite
        opcode += 0b0 << 4 #5th opcode number is add/subtract
        opcode += 0b1 << 5 #6th opcode number is print
    elif operation == "sub":
        opcode += 0b1 << 0 #RegWrite
        opcode += 0b1 << 4 #5th opcode number is add/subtract
        opcode += 0b1 << 5 #6th opcode number is print
    elif operation == "load":
        opcode += 0b1 << 0 #RegWrite
        opcode += 0b1 << 2 #3rd opcode number is memread
    elif operation == "store":
        opcode += 0b1 << 3 #4th opcode number is memwrite

    source1 = instruction[2] #register 1

    if operation == "add" or operation == "sub":
        opcode += int(source1[1]) << 20 # the number of register will be where r1 should be in machine code which is the 21st bit 
    else:
        if source1[0] == "r":
            opcode += int(source1[1]) << 12
        else: 
            opcode += 0b1 << 1 # imm
            opcode += int(source1) << 12
            
    if operation == "add" or operation == "sub": # There is no source 2 if its load or store.
        source2 = instruction[3] #register 2

        if source2[0] == "r": # if its an register, then place the register number where it should be which is the 13th bit
            opcode += int(source2[1]) << 12
        else: # if its an imm, then...
            opcode += 0b1 << 1
            opcode += int(source2) << 12
    
    dst_reg = instruction[1]     

    if operation == "store": # If its store, use register 2 as "dst_reg"
        opcode += int(dst_reg[1]) << 20
    else:
        opcode += int(dst_reg[1]) << 22  # Not store, so just put dst_reg where it belongs, the last two bits.

    result = hex(opcode)[2:]

    while(len(result) < 6):
        result = "0" + result

    return result # final translated opcode

if __name__ == "__main__":
    
    instruction_file = open("project2.txt", 'r') # project2.txt is the file with instructions 
    instructions = open("instructionfile", 'w') # instructionfile is the instruction image file
    data_file = open("datafile", 'w') # datafile is the memory image file

    instructions.write("v3.0 hex words addressed\n")  
    data_file.write("v3.0 hex words addressed\n") 

    address_line = 0x00  # to write address for project2.txt
    address_line2 = 0x00 # to write address for datafile
    instructions.write((hex(address_line))[2:] + "0: ")
    data_file.write((hex(address_line2))[2:] + "0: ") 

    counter = 0 
    counter2 = 0

    for line in instruction_file: # every line in the instruction 

        instruction = line.split() # line in project2.txt is now a list 

        if(line == "" or line == "\n" or instruction[0] == "#"): # if its a comment or empty list or we reach end the end of a line...
            continue 

        if(instruction[0] == ".data"): # data segment 
            for data in instruction[1:]: # starting from the first address...
                data_file.write(data[2:] + " ") 
                counter2 += 1
                if counter2 == 8:
                    counter2 = 0
                    data_file.write("\n")
                    address_line2 += 0x08
                    if address_line2 > 0xf8:
                        break
                    if len(str(hex(address_line2)[2:])) == 1:
                        data_file.write("0" + hex(address_line2)[2:] + ": ")
                    else:
                        data_file.write(hex(address_line2)[2:] + ": ")
        else:

            instructions.write(translate(instruction) + " ") 
            counter += 1
            if counter == 8: # if there are eight hexadecimal on a line.. start a new line 
                counter = 0 # reset the counter 
                instructions.write("\n") 
                address_line += 0x08 # changing for next line
                if address_line > 0xf8: # reach the end of the image file
                    break   
                if len(str(hex(address_line)[2:])) == 1:
                    instructions.write("0" + hex(address_line)[2:] + ": ")
                else:
                    instructions.write(hex(address_line)[2:] + ": ")
        
    instruction_file.close() 
    instructions.close()
    data_file.close() 


    





    




