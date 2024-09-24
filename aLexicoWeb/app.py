from flask import Flask, render_template, request
import re

app = Flask(__name__)

def lex_analysis(code):
    tokens = []
    errors = []
    lines = code.splitlines()

    # Define patrones básicos para los tokens
    patterns = {
        'FOR': r'\bfor\b',
        'INT': r'\bint\b',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'NUMBER': r'\d+',
        'OPERATOR': r'[=<>+();{}]',
        'PRINT': r'System\.out\.println',
        'STRING': r'\".*?\"',
        'WHITESPACE': r'\s+'
    }

    # Combina patrones en una expresión regular
    master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns.items())
    
    # Procesa cada línea
    for line_number, line in enumerate(lines, start=1):
        # Verifica si hay caracteres no reconocidos en la línea
        invalid_characters = re.findall(r'[^a-zA-Z0-9_=\s<>,;{}()." ]', line)
        if invalid_characters:
            errors.append((line_number, f'Error léxico: Caracter(es) no reconocido(s) {", ".join(invalid_characters)}'))

        for match in re.finditer(master_pattern, line):
            kind = match.lastgroup
            value = match.group()
            if kind != 'WHITESPACE':  # Ignora espacios en blanco
                tokens.append((line_number, value, kind))

    return tokens, errors

def syntax_analysis(tokens):
    errors = []
    # Ejemplo básico de análisis sintáctico (reconocimiento de for loop)
    if tokens:
        for i in range(len(tokens)):
            if tokens[i][2] == 'FOR':
                if i + 5 < len(tokens):
                    if tokens[i + 1][2] == 'IDENTIFIER' and tokens[i + 2][2] == 'OPERATOR' and \
                       tokens[i + 3][2] == 'NUMBER' and tokens[i + 4][2] == 'OPERATOR' and \
                       tokens[i + 5][2] == 'NUMBER':
                        continue
                    else:
                        errors.append((tokens[i][0], 'Error sintáctico: Se esperaba una estructura de bucle for válida.'))
    return errors

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    lexical_errors = []
    syntax_errors = []
    
    if request.method == 'POST':
        code = request.form['code']
        tokens, lexical_errors = lex_analysis(code)
        syntax_errors = syntax_analysis(tokens)

    return render_template('index.html', tokens=tokens, lexical_errors=lexical_errors, syntax_errors=syntax_errors)

if __name__ == '__main__':
    app.run(debug=True)
