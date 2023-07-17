import ply.lex as lex

# Tokens da linguagem
tokens = (
    'HEAD',
    'DECLARE',
    'INSTRUCTIONS',
    'END',
    'PLUS',
    'MINUS',
    'DIV',
    'MULT',
    'INT',
    'NInt',
    'ID',
    'AND',
    'OR',
    'MORE',
    'LESS',
    'EQ',
    'NEQ',
    'MOREEQ',
    'LESSEQ',
    'INPUT',
    'OUTPUT',
    'WHILE',
    'DO',
    'IF',
    'ELSE',
    'STRING'
)

# Simbolos literais
literals = ['(',')','[',']',',','=','{','}','%']

#Regras
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIV = r'\/'
t_MULT = r'\*'
t_MORE = r'\>'
t_LESS = r'\<'
t_EQ = r'\=\='
t_NEQ = r'\!\='
t_MOREEQ = r'\>\='
t_LESSEQ  = r'\<\='

def t_HEAD(t):
    r'(?i)inicio'
    return t

def t_DECLARE(t):
    r'(?i)variaveis:'
    return t

def t_INSTRUCTIONS(t):
    r'(?i)codigo:'
    return t

def t_END(t):
    r'(?i)fim'
    return t

def t_INT(t):
    r'(?i)int'
    return t

def t_INPUT(t):
    r'le'
    return t

def t_OUTPUT(t):
    r'escreve'
    return t

def t_WHILE(t):
    r'enquanto'
    return t

def t_DO(t):
    r'faz'
    return t

def t_IF(t):
    r'se'
    return t

def t_ELSE(t):
    r'casocontrario'
    return t

def t_AND(t):
    r'e'
    return t

def t_OR(t):
    r'ou'
    return t

def t_STRING(t):
    r'\"[^"]*\"'
    return t

def t_ID(t):
    r'[A-Za-z]+'
    return t

def t_NInt(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Syntax ERROR!")
    t.lexer.skip(1)

t_ignore = ' \r\n\t'

lexer = lex.lex()
