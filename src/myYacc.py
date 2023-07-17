from myLex import tokens
import ply.yacc as yacc

# Regras da grmática
def p_Programa(p):
   "programa : HEAD DECLARE Dec INSTRUCTIONS Code END"
   p[0] = p[3] + "START\n" + p[5] + "STOP"

def p_Dec(p):
   "Dec : Var Dec"
   p[0] = p[1] + p[2]

def p_Dec_Var(p):
   "Dec : Var"
   p[0] = p[1]

def p_Var(p):
   "Var : INT ID '=' NInt"
   p.parser.table[p[2]] = parser.id
   parser.id += 1
   p[0] = "PUSHI " + str(p[4]) + "\n"

def p_Var_ID(p):
   "Var : INT ID"
   p.parser.table[p[2]] = parser.id
   parser.id += 1
   p[0] = "PUSHI 0\n"

def p_Var_ArrayEmpty(p):
   "Var : INT ID '[' NInt ']'"
   p.parser.arrTable[p[2]] = (parser.id,parser.id + int(p[4]))
   p.parser.id += p[4]
   p[0] = "PUSHN " + str(p[4]) + "\n"

def p_Var_Array(p):
   "Var : INT ID '=' '[' Values ']'"
   p.parser.arrTable[p[2]] = (parser.id,parser.id + p[5].count("\n") - 1)
   p.parser.id += p[5].count("\n") - 1
   p[0] = p[5]

def p_Values(p):
   "Values : NInt ',' Values"
   p[0] = "PUSHI " + str(p[1]) + "\n" + p[3]

def p_Values_NInt(p):
   "Values : NInt"
   p[0] = "PUSHI " + str(p[1]) + "\n"

def p_Code(p):
   """Code : Inst Code"""
   p[0] = p[1] + p[2]

def p_Code_Inst(p):
   "Code : Inst"
   p[0] = p[1]

def p_Code_Empty(p):
   "Code : "
   p[0] = ""

def p_Inst(p):
   """Inst : Atrib
           | Cycle
           | Cond
           | Write"""
   p[0] = p[1]

def p_Atrib_Read(p):
   "Atrib : Read"
   p[0] = p[1]

def p_Atrib_Exp(p):
   "Atrib : ID '=' Exp"
   p[0] = p[3] + "STOREG " + str(parser.table[p[1]]) + "\n"

def p_Atrib_IDArr(p):
   "Atrib : ID '=' ID '[' Fator ']'"
   p[0] = "PUSHGP\n"
   p[0] += "PUSHI " + str(parser.arrTable[p[3]][0]) + "\n" + p[5] + "ADD\nLOADN\n"
   p[0] += "STOREG " + str(parser.table[p[1]]) + "\n"

def p_Atrib_Arr(p):
   "Atrib : ID '[' Fator ']' '=' Fator"
   p[0] = "PUSHGP\n"
   p[0] += "PUSHI " + str(parser.arrTable[p[1]][0]) + "\n" + p[3] + "ADD\n"
   p[0] += p[6] + "STOREN\n"

def p_Exp_Termo(p):
   "Exp : Termo"
   p[0] = p[1]

def p_Exp(p):
   """Exp : Exp opL Termo
          | Exp opA Termo"""
   p[0] = p[1] + p[3] + p[2]

def p_Termo_Fator(p):
   "Termo : Fator"
   p[0] = p[1]

def p_Termo_opM(p):
   "Termo : Termo opM Fator"
   p[0] = p[1] + p[3] + p[2]

def p_Fator_ID(p):
   "Fator : ID"
   p[0] = "PUSHG " + str(parser.table[p[1]]) + "\n"

def p_Fator_NInt(p):
   "Fator : NInt"
   p[0] = "PUSHI " + str(p[1]) + "\n"

def p_Fator_Exp(p):
   "Fator : '(' Exp ')'"
   p[0] = p[2]

def p_Cond(p):
   "Cond : IF '(' Exp ')' '{' Code '}' ELSE '{' Code '}'"
   n = parser.condCounter
   parser.condCounter += 1
   p[0] = p[3] + "JZ I" + str(n) + "\n"
   p[0] += p[6] + "JUMP EI" + str(n) + "\nI" + str(n) + ": nop\n"
   p[0] += p[10] + "EI" + str(n) + ": nop\n" 

def p_Cycle_While(p):
   "Cycle : WHILE '(' Exp ')' DO '{' Code '}'"
   n = parser.cycleCounter
   parser.cycleCounter += 1
   p[0] = "W" + str(n) + ": nop\n"
   p[0] += p[3] + "JZ EW" + str(n) + "\n"
   p[0] += p[7] + "JUMP W" + str(n) + "\nEW" + str(n) + ": nop\n"
   
def p_Read(p):
   "Read : ID '=' INPUT '(' ')'"
   p[0] = "READ\nATOI\nSTOREG " + str(parser.table[p[1]]) + "\n"

def p_Write_String(p):
   "Write : OUTPUT '(' STRING ')'"
   p[0] = "PUSHS " + p[3] + "\n" + "WRITES\n"

def p_Write_Var(p):
   "Write : OUTPUT '(' Fator ')'"
   p[0] = p[3] + "STRI\n" + "WRITES\n"

def p_WriteArr(p):
   "Write : OUTPUT '(' ID '[' Fator ']' ')'"
   p[0] = "PUSHGP\n"
   p[0] += "PUSHI " + str(parser.arrTable[p[3]][0]) + "\n" + p[5] + "ADD\n"
   p[0] += "LOADN\n" + "STRI\n" + "WRITES\n"

def p_opA_PLUS(p):
   "opA : PLUS"
   p[0] = "ADD\n"

def p_opA_MINUS(p):
   "opA : MINUS"
   p[0] = "SUB\n"

def p_opM_MULT(p):
   "opM : MULT"
   p[0] = "MUL\n"

def p_opM_DIV(p):
   "opM : DIV"
   p[0] = "DIV\n"

def p_opM_MOD(p):
   "opM : '%'"
   p[0] = "MOD \n"

def p_opL_MORE(p):
   "opL : MORE"
   p[0] = "SUP\n"

def p_opL_LESS(p):
   "opL : LESS"
   p[0] = "INF\n"

def p_opL_MOREEQ(p):
   "opL : MOREEQ"
   p[0] = "SUPEQ\n"

def p_opL_LESSEQ(p):
   "opL : LESSEQ"
   p[0] = "INFEQ\n"

def p_opL_EQ(p):
   "opL : EQ"
   p[0] = "EQUAL\n"

def p_opL_NEQ(p):
   "opL : NEQ"
   p[0] = "EQUAL\nNOT\n"

def p_opL_AND(p):
   "opL : AND"
   p[0] = "MUL\n"

def p_opL_OR(p):
   "opL : OR"
   p[0] = "OR\n"

def p_error(p):
   parser.success = False
   print("Syntax error!")
   exit()


# Inicializar o parser e as suas variáveis
parser = yacc.yacc()
parser.table = {}
parser.arrTable = {}
parser.id = parser.cycleCounter = parser.condCounter = 0

# Esperar o input com o nome do fixeiro
fileName = input("Insira o nome do ficheiro: ")
file = open("tests/" + fileName + ".txt","r")
text = file.read()
parser.success = True
p = parser.parse(text)
# Criar um ficheiro de output com o código máquina
file = open("outputs/" + fileName + "out.txt",'w')
file.write(p)
