# 문자 분류 상수
LETTER = 1
DIGIT = 2
UNKNOWN = 99

# 토큰 상수
NULL = 0
INT_LIT = 10
IDENT = 11
OPERATION = 12

# 연산자 상수
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LESS_THAN = 25
LESS = 26
MORE_THAN = 27
MORE = 28
EQUAL = 29
NOT_EQUAL = 30
NOT = 31
SEMI_COLON = 32

# 변수 상수
VAR_X = 33
VAR_Y = 34
VAR_Z = 35

# 전역 변수
charClass = 0
lexeme = ""
input_str = ""
nextChar = ""
lexLen = 0
token = 0
nextToken = 0
input_str_index = 0
SYNTAX_ERROR = 0
bexpr_error = 0
expr_index = 0
notdecimal = 0
dec_dect = 0
demical = ""
demical_index = 0
term_data = 0
aexpr_data = 0

# 계산 결과 저장 배열
# print_index = 0
print_final = []
print_x = []
print_y = []
print_z = []

# 임시 저장 변수
var_x = 0
var_y = 0
var_z = 0

# 변수 및 연산자 확인 변수
var_detect = 0
cmp_detect = 0

moving_bool = False
moving_dec = 0

bool_dec = 1
bool_dec_x = 1
bool_dec_y = 1
bool_dec_z = 1

# 연산자 확인 첫번째
def lookup_op_1(ch):
    global nextToken, ADD_OP, SUB_OP, MULT_OP, DIV_OP, ASSIGN_OP, NOT, LESS_THAN, MORE_THAN, SEMI_COLON, OPERATION
    if ch == '+':
        addChar()
        nextToken = ADD_OP
    elif ch == '-':
        addChar()
        nextToken = SUB_OP
    elif ch == '*':
        addChar()
        nextToken = MULT_OP
    elif ch == '/':
        addChar()
        nextToken = DIV_OP
    elif ch == '=':
        addChar()
        nextToken = ASSIGN_OP
    elif ch == '!':
        addChar()
        nextToken = NOT
    elif ch == '<':
        addChar()
        nextToken = LESS_THAN
    elif ch == '>':
        addChar()
        nextToken = MORE_THAN
    elif ch == ';':
        addChar()
        nextToken = SEMI_COLON
    else:
        addChar()
        nextToken = OPERATION
    return nextToken


# 연산자 확인 두번째 이후
def lookup_op_2(ch):
    global nextToken, ASSIGN_OP, EQUAL, NOT, NOT_EQUAL, LESS, LESS_THAN, MORE, MORE_THAN, OPERATION
    if ch == '=':
        if nextToken == ASSIGN_OP:
            addChar()
            nextToken = EQUAL
        elif nextToken == NOT:
            addChar()
            nextToken = NOT_EQUAL
        elif nextToken == LESS_THAN:
            addChar()
            nextToken = LESS
        elif nextToken == MORE_THAN:
            addChar()
            nextToken = MORE
        else:
            addChar()
            nextToken = OPERATION
    else:
        addChar()
        nextToken = OPERATION
    return nextToken

# x, y, z 구분
def lookup_var(ch):
    global nextToken, VAR_X, VAR_Y, VAR_Z

    if ch == 'x':
        addChar()
        nextToken = VAR_X
    elif ch == 'y':
        addChar()
        nextToken = VAR_Y
    elif ch == 'z':
        addChar()
        nextToken = VAR_Z
    else:
        addChar()
        nextToken = IDENT

    return nextToken

# 임시버퍼에 토큰 저장
def addChar():
    global lexLen, lexeme, nextChar
    lexeme = lexeme + nextChar

# 토큰이 될 때까지 문자 읽기
def getChar():
    global input_str_index, nextChar, charClass, input_str, LETTER, DIGIT, UNKNOWN, NULL

    if input_str_index < len(input_str):
        nextChar = input_str[input_str_index]
        input_str_index += 1
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        elif nextChar == '\0' :
            charClass = NULL
        else:
            charClass = UNKNOWN
    else:
        charClass = NULL

# 공백 무시
def getNonBlank():
    while nextChar.isspace():
        getChar()

# 토큰의 정보 저장
def lex():
    global lexLen, nextToken, lexeme, nextChar, charClass, LETTER, DIGIT, UNKNOWN, NULL
    lexeme = ""
    lexLen = 0
    getNonBlank()

    if charClass == LETTER:

        lookup_var(nextChar)
        getChar()

        while nextChar != '\0' and not nextChar.isspace():
            addChar()
            getChar()
            nextToken = IDENT

    elif charClass == DIGIT:
        addChar()
        getChar()

        nextToken = INT_LIT

    elif charClass == UNKNOWN:
        lookup_op_1(nextChar)
        getChar()

        while nextChar != '\0' and not nextChar.isspace():
            lookup_op_2(nextChar)
            getChar()

    elif charClass == NULL:
        nextToken = NULL
        lexeme = 'NULL'

    # print(f"next token: {nextToken}, next lexeme: {lexeme}")
    return nextToken

# <program> -> {<statement>}
def program():
    lex()

    while nextToken != NULL and SYNTAX_ERROR == 0:
        statement()

# <statement> -> <var> = <expr> ; | print <var> ;
def statement():
    global SYNTAX_ERROR, lexeme, nextToken, input_str_index, expr_index, bool_dec, bool_dec_x, bool_dec_y, bool_dec_z, var_detect, var_x, var_y, var_z, VAR_X, VAR_Y, VAR_Z
    global print_x, print_y, print_z, print_x_bool, print_y_bool, print_z_bool, print_index, print_final, moving_bool, moving_dec
    if SYNTAX_ERROR == 0:
        # <var> = <expr> ;
        if lexeme != "print":
            var()

            if SYNTAX_ERROR == 0:
                if nextToken != ASSIGN_OP:
                    error()
                else:
                    expr_index = input_str_index
                    lex()
                    expr()

            if SYNTAX_ERROR == 0:
                if nextToken != SEMI_COLON:
                    error()
                else:
                    lex()

            # <expr> 의 결과 값을 저장
            if SYNTAX_ERROR == 0:
                # 결과 값이 bool 형일 때
                if bool_dec == 0:
                    if var_detect == VAR_X:
                        bool_dec_x = 0
                        var_x = moving_bool
                    elif var_detect == VAR_Y:
                        bool_dec_y = 0
                        var_y = moving_bool
                    elif var_detect == VAR_Z:
                        bool_dec_z = 0
                        var_z = moving_bool
                # 결과 값이 int 형일 때
                elif bool_dec == 1:
                    if var_detect == VAR_X:
                        bool_dec_x = 1
                        var_x = moving_dec
                    elif var_detect == VAR_Y:
                        bool_dec_y = 1
                        var_y = moving_dec
                    elif var_detect == VAR_Z:
                        bool_dec_z = 1
                        var_z = moving_dec
        # print <var> ;
        else:
            lex()
            var()

            if SYNTAX_ERROR == 0:
                if nextToken != SEMI_COLON:
                    error()
                else:
                    lex()

            if SYNTAX_ERROR == 0:
                # x, y, z 구별
                if var_detect == VAR_X:
                    print_x.append(var_x)
                    print_final.append(1)

                elif var_detect == VAR_Y:
                    print_y.append(var_y)
                    print_final.append(2)

                elif var_detect == VAR_Z :
                    print_z.append(var_z)
                    print_final.append(3)

# <expr> -> <bexpr> | <aexpr>
def expr():
    global SYNTAX_ERROR, bexpr_error, expr_index, input_str_index

    if SYNTAX_ERROR == 0:
        bexpr_error = 0

        # 먼저 실행
        bexpr()

        # <bexpr> 이 오류가 날 시 <aexpr> 실행
        if bexpr_error == -1:
            SYNTAX_ERROR = 0
            bexpr_error = 0
            input_str_index = expr_index
            getChar()
            lex()
            aexpr()

# <bexpr> -> <number> <relop> <number>
def bexpr():
    global SYNTAX_ERROR, demical, cmp_detect, moving_bool, bool_dec

    if SYNTAX_ERROR == 0:
        number()
        if (len(demical)==0)  :
            error()
        else :
            front = int(demical)

        if SYNTAX_ERROR == 0:
            relop()

        if SYNTAX_ERROR == 0:
            number()

        # 숫자를 변환하고 연산자의 판별을 통해 계산 (bool 형)
        if SYNTAX_ERROR == 0:
            if (len(demical) == 0):
                error()
            else :
                back = int(demical)

            bool_bexpr = 0

            if cmp_detect == EQUAL:
                bool_bexpr = (front == back)
            elif cmp_detect == NOT_EQUAL:
                bool_bexpr = (front != back)
            elif cmp_detect == MORE:
                bool_bexpr = (front >= back)
            elif cmp_detect == MORE_THAN:
                bool_bexpr = (front > back)
            elif cmp_detect == LESS:
                bool_bexpr = (front <= back)
            elif cmp_detect == LESS_THAN:
                bool_bexpr = (front < back)

            # 전역 변수에 저장
            moving_bool = bool_bexpr
            bool_dec = 0

# <relop> -> == | != | < | > | <= | >=
def relop():
    global SYNTAX_ERROR, nextToken, cmp_detect, bexpr_error

    if SYNTAX_ERROR == 0:
        if nextToken == EQUAL:
            cmp_detect = EQUAL
        elif nextToken == NOT_EQUAL:
            cmp_detect = NOT_EQUAL
        elif nextToken == MORE:
            cmp_detect = MORE
        elif nextToken == MORE_THAN:
            cmp_detect = MORE_THAN
        elif nextToken == LESS:
            cmp_detect = LESS
        elif nextToken == LESS_THAN:
            cmp_detect = LESS_THAN
        else:
            error()
            bexpr_error = -1

        if SYNTAX_ERROR == 0:
            lex()

# <aexpr> -> <term> {(+ | -) <term>}
def aexpr():
    global SYNTAX_ERROR, nextToken, term_data, bool_dec, moving_dec, ADD_OP, SUB_OP

    front = 0
    back = 0
    operand = 0

    if SYNTAX_ERROR == 0:
        term()
        front = term_data

        # 에러가 나지 않았거나 +, - 가 오면 반복
        while (nextToken == ADD_OP or nextToken == SUB_OP) and SYNTAX_ERROR == 0:
            if nextToken == ADD_OP:
                operand = ADD_OP
            elif nextToken == SUB_OP:
                operand = SUB_OP
            lex()
            term()

            # 계산
            back = term_data
            if operand == ADD_OP:
                front = front + back
            elif operand == SUB_OP:
                front = front - back

    if SYNTAX_ERROR == 0:
        bool_dec = 1
        moving_dec = front

# <term> -> <factor> {(* | /) <factor>
def term():
    global SYNTAX_ERROR, nextToken, demical, term_data, MULT_OP, DIV_OP

    front = 0
    back = 0
    operand = 0

    if SYNTAX_ERROR == 0:
        factor()
        if (len(demical)==0)  :
            error()
        else :
            front = int(demical)

        # 에러가 나지 않았거나 *, / 가 오면 반복
        while (nextToken == MULT_OP or nextToken == DIV_OP) and SYNTAX_ERROR == 0:
            if nextToken == MULT_OP:
                operand = MULT_OP
            elif nextToken == DIV_OP:
                operand = DIV_OP
            lex()
            factor()

            # 계산
            if (len(demical) == 0):
                error()
            else:
                back = int(demical)
            if operand == MULT_OP:
                front = front * back
            elif operand == DIV_OP:
                front = front // back

    if SYNTAX_ERROR == 0:
        term_data = front

# <factor> -> <number>
def factor():
    global SYNTAX_ERROR

    if SYNTAX_ERROR == 0:
        number()

# <number> -> <dec>{<dec>}
def number():
    global dec_dect, demical, SYNTAX_ERROR, notdecimal, demical_index

    dec_dect = 0
    demical = ""

    if SYNTAX_ERROR == 0:
        dec()
        dec_dect += 1

        while notdecimal == 0 and SYNTAX_ERROR == 0:
            dec()

        notdecimal = 0
        demical_index = 0

# <dec> -> 0|1|2|3|4|5|6|7|8|9
def dec():
    global SYNTAX_ERROR, nextToken, lexeme, demical, demical_index, dec_dect, bexpr_error, notdecimal

    if SYNTAX_ERROR == 0:
        if nextToken == INT_LIT:
            demical = demical + lexeme[0]
            demical_index += 1
            lex()
        elif dec_dect == 0:
            error()
            bexpr_error = -1
        else:
            notdecimal = -1

# <var> -> x | y | z
def var():
    global SYNTAX_ERROR, nextToken, var_detect, VAR_X, VAR_Y, VAR_Z

    if SYNTAX_ERROR == 0:
        if nextToken in [VAR_X, VAR_Y, VAR_Z]:
            if nextToken == VAR_X:
                var_detect = VAR_X
            elif nextToken == VAR_Y:
                var_detect = VAR_Y
            else:
                var_detect = VAR_Z
            lex()
        else:
            error()


def error():
    global SYNTAX_ERROR
    SYNTAX_ERROR = -1



if __name__ == "__main__":
    while True:
        # 초기화
        SYNTAX_ERROR = 0
        bexpr_error = 0
        input_str_index = 0
        var_x = 0
        var_y = 0
        var_z = 0
        print_index = 0
        bool_dec = 1
        bool_dec_x = 1
        bool_dec_y = 1
        bool_dec_z = 1
        input_str = ""
        print_x = []
        print_y = []
        print_z = []
        print_final = []

        # 사용자 입력 받기
        print(">> ", end="")
        input_str = input()

        if input_str.strip() == "terminate":
            break

        input_str = input_str + '\0'
        getChar()

        # RD 파싱 시작
        program()

        # 출력
        print(">> ", end="")
        if SYNTAX_ERROR == 0:
            print_x_index = 0
            print_y_index = 0
            print_z_index = 0

            for i in range(len(print_final)):
                if print_final[i] == 1:
                    print(print_x[print_x_index], end=" ")
                    print_x_index += 1
                elif print_final[i] == 2:
                    print(print_y[print_y_index], end=" ")
                    print_y_index += 1
                elif print_final[i] == 3:
                    print(print_z[print_z_index], end=" ")
                    print_z_index += 1
            print()
        else:
            print("syntax error!!")
