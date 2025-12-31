# 문자 분류 상수
TokenInfo = -1
LETTER = 1           # 문자로 시작
DIGIT = 2            # 숫자로 시작
UNKNOWN = 99         # 알 수 없음 (연산자로 시작)

# 토큰 상수
NULL = 0             #
INT_LIT = 10         #
IDENT = 11           #
OPERATION = 12       #
MIX = 13             #

# 연산자 상수
ASSIGN_OP = 20       # =
ADD_OP = 21          # +
SUB_OP = 22          # -
MULT_OP = 23         # *
DIV_OP = 24          # /
LESS_THAN = 25       # <
LESS = 26            # <=
MORE_THAN = 27       # >
MORE = 28            # >=
EQUAL = 29           # ==
NOT_EQUAL = 30       # !=
NOT = 31             # !
SEMI_COLON = 32      # ;
LEFT_BRACE = 33      # {
RIGHT_BRACE = 34     # }
LEFT_PARENTHESES = 35   # (
RIGHT_PARENTHESES = 36  # )

# 문자 상수
SMALL_LETTER = 37
CAPITAL_LETTER = 38


# 전역 변수
charClass = 0
input_str = ""
input_str_index = 0
lexeme = ""
nextChar = ""
token = 0
nextToken = 0

# 에러 판별자
SYNTAX_ERROR = 0
declaration_error = 0

# 숫자열, 문자열
lower_string = ""
demical = ""

# 계산 결과 저장 배열
print_final = []
printdata = 0

# 임시 저장 변수
# 변수를 리스트로 저장 -> 검색 가능
# var_list = []
var_dict = {}

# 변수 및 연산자 확인 변수
cmp_detect = 0

moving_bool = False
moving_dec = 0
moving_term = 0

# 연산자 확인 첫번째
def lookup_op_1(ch):
    global nextToken, ADD_OP, SUB_OP, MULT_OP, DIV_OP, ASSIGN_OP, NOT, LESS_THAN, MORE_THAN, SEMI_COLON, OPERATION, LEFT_BRACE, RIGHT_BRACE, LEFT_PARENTHESES, RIGHT_PARENTHESES

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
    elif ch == '{':
        addChar()
        nextToken = LEFT_BRACE
    elif ch == '}':
        addChar()
        nextToken = RIGHT_BRACE
    elif ch == '(':
        addChar()
        nextToken = LEFT_PARENTHESES
    elif ch == ')':
        addChar()
        nextToken = RIGHT_PARENTHESES
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

# 문자가 소문자인지
def lookup_char(ch) :
    global nextToken

    if ch.islower() and (nextToken==SMALL_LETTER or len(lexeme)==0):
        addChar()
        nextToken = SMALL_LETTER
    else:
        addChar()
        nextToken = IDENT

    return nextToken

# 숫자인지 아닌지
def lookup_digit(ch):
    global nextToken

    if ch.isdigit() and (nextToken==INT_LIT or len(lexeme)==0):
        addChar()
        nextToken = INT_LIT
    else:
        addChar()
        nextToken = MIX

    return nextToken


# 임시버퍼에 토큰 저장
def addChar():
    global lexeme, nextChar
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
    global nextChar
    while nextChar.isspace():
        getChar()

# 토큰의 정보 저장
def lex():
    global nextToken, lexeme, nextChar, charClass, LETTER, DIGIT, UNKNOWN, NULL, TokenInfo
    lexeme = ""
    getNonBlank()

    # 문자는 다르지
    if charClass == LETTER:
        TokenInfo = LETTER
        # lookup_char(nextChar)
        # getChar()
        while nextChar != '\0' and not nextChar.isspace():
            lookup_char(nextChar)
            getChar()

    # 숫자도 같애
    elif charClass == DIGIT:
        TokenInfo = DIGIT
        # lookup_digit(nextChar)
        # getChar()
        while nextChar != '\0' and not nextChar.isspace():
            lookup_digit(nextChar)
            getChar()

    # 연산자는 같고
    elif charClass == UNKNOWN:
        TokenInfo = UNKNOWN
        lookup_op_1(nextChar)
        getChar()

        while nextChar != '\0' and not nextChar.isspace():
            lookup_op_2(nextChar)
            getChar()

    elif charClass == NULL:
        TokenInfo = NULL
        nextToken = NULL
        lexeme = "NULL"

    # print(f"next token: {nextToken}, next lexeme: {lexeme}")
    return nextToken

# <program> -> {<declaration>} {<statemnet>}
# 여기서 declaration에서 statement로 이동할 판별자를 만들어줘야 할 듯
def program():
    global declaration_error, nextToken, SYNTAX_ERROR
    declaration_error = 0
    SYNTAX_ERROR = 0

    lex()

    while nextToken!=NULL and SYNTAX_ERROR==0 and declaration_error==0:
        # program_index = input_str_index
        declaration()

    while nextToken!=NULL and SYNTAX_ERROR==0:
        statement()

# <declaration> -> <type> <var> ;
# 변수 리스트에 추가
def declaration():
    global declaration_error, var_dict, SYNTAX_ERROR
    # 여기서는 아직 에러 판단을 하지 않아
    # 왜? declaration이 하나도 안올 수 있으니까
    declaration_error = 0

    type()

    if declaration_error==0:
        var()

        # 변수 등록
        var_dict[lower_string] = 0
        # print(var_dict)

    if declaration_error==0 and SYNTAX_ERROR==0:
        if nextToken == SEMI_COLON:
            lex()
        else :
            error()

# <statement> → <var> = <aexpr> ; | print <bexpr> ; | print <aexpr> ; | do ‘ { ’ {<statement>} ‘ } ’ while ( <bexpr> ) ;
# 문자를 하나씩 받는데 print하고 do를 어떻게 구분할 것인가
# 그래서 <var> = <aexpr> ; 이거를 맨 처음에 둔거같은데?
def statement():
    global nextToken, ASSIGN_OP, SYNTAX_ERROR, input_str_index, printdata, moving_bool, moving_dec
    # <var> = <aexpr> ;
    if SYNTAX_ERROR==0 :
        if lexeme=="print" :
            lex()

            if nextToken==LESS_THAN or nextToken==MORE_THAN or nextToken==LESS or nextToken==MORE or nextToken==EQUAL or nextToken==NOT_EQUAL :
                bexpr()
                printdata = moving_bool
            else :
                aexpr()
                printdata = moving_dec

            if SYNTAX_ERROR==0:
                if nextToken==SEMI_COLON:
                    lex()
                else :
                    error()

            if SYNTAX_ERROR==0:
                print_final.append(printdata)


        elif lexeme=="do" :
            while SYNTAX_ERROR==0:
                loop_dir = False
                expr_index = input_str_index

                lex()

                if SYNTAX_ERROR==0:
                    if nextToken==LEFT_BRACE:
                        lex()
                    else :
                        error()

                while nextToken!=RIGHT_BRACE and nextToken!=NULL and SYNTAX_ERROR==0:
                    statement()

                if SYNTAX_ERROR==0:
                    if nextToken==RIGHT_BRACE :
                        lex()
                    else :
                        error()

                if SYNTAX_ERROR==0:
                    if lexeme=="while" :
                        lex()
                    else :
                        error()

                if SYNTAX_ERROR==0:
                    if nextToken==LEFT_PARENTHESES:
                        lex()
                    else :
                        error()

                if SYNTAX_ERROR==0:
                    bexpr()
                    loop_dir = moving_bool

                if SYNTAX_ERROR==0:
                    if nextToken==RIGHT_PARENTHESES:
                        lex()
                    else :
                        error()

                if SYNTAX_ERROR==0:
                    if nextToken==SEMI_COLON:
                        lex()
                    else :
                        error()

                if SYNTAX_ERROR==0:
                    if loop_dir == True:
                        input_str_index = expr_index
                    else :
                        break

        else :
            variation = ""
            var()

            # 변수가 선언되었었는지 확인
            if SYNTAX_ERROR == 0:
                if lower_string in var_dict:
                    variation = lower_string
                else:
                    error()

            if SYNTAX_ERROR==0:
                if nextToken==ASSIGN_OP:
                    lex()
                else :
                    error()

            if SYNTAX_ERROR==0:
                aexpr()

            if SYNTAX_ERROR==0:
                var_dict[variation] = moving_dec

            if SYNTAX_ERROR==0:
                if nextToken==SEMI_COLON:
                    lex()
                else :
                    error()

# <bexpr> → <relop> <aexpr> <aexpr>
def bexpr():
    global SYNTAX_ERROR, cmp_detect, moving_bool, moving_dec
    moving_bool = False

    relop()

    if SYNTAX_ERROR==0:
        aexpr()
        if SYNTAX_ERROR==0:
            front = moving_dec

    if SYNTAX_ERROR==0:
        aexpr()
        if SYNTAX_ERROR==0:
            back = moving_dec

    if SYNTAX_ERROR==0:
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

        moving_bool = bool_bexpr


# <relop> → == | != | < | > | <= | >=
def relop():
    global SYNTAX_ERROR, nextToken, cmp_detect

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

    if SYNTAX_ERROR == 0:
        lex()

# <aexpr> → <term> {( + | - | * | / ) <term>}
def aexpr():
    global SYNTAX_ERROR, nextToken, moving_term, moving_dec, ADD_OP, SUB_OP, MULT_OP, DIV_OP

    front = 0
    back = 0
    operand = 0
    moving_dec = 0

    if SYNTAX_ERROR==0:
        term()
        front = moving_term

        while ((nextToken==ADD_OP or nextToken==SUB_OP or nextToken==MULT_OP or nextToken==DIV_OP) and  SYNTAX_ERROR==0):
            if nextToken == ADD_OP:
                operand = ADD_OP
            elif nextToken == SUB_OP:
                operand = SUB_OP
            elif nextToken == MULT_OP:
                operand = MULT_OP
            elif nextToken == DIV_OP:
                operand = DIV_OP
            lex()
            term()

            if SYNTAX_ERROR==0:
                # 계산
                back = moving_term
                if operand == ADD_OP:
                    front = front + back
                elif operand == SUB_OP:
                    front = front - back
                elif operand == MULT_OP:
                    front = front * back
                elif operand == DIV_OP:
                    front = int(front / back)

    if SYNTAX_ERROR==0:
        moving_dec = front

# <term> → <number> | <var> | ( <aexpr> )
def term():
    global SYNTAX_ERROR, var_dict, moving_term
    # number
    if TokenInfo==DIGIT :
        number()
        if SYNTAX_ERROR==0:
            moving_term = demical

    # var
    elif TokenInfo==LETTER :
        var()
        if SYNTAX_ERROR==0:
            # print(lower_string)
            # print(var_dict)
            if lower_string in var_dict:
                moving_term = var_dict[lower_string]
            else :
                error()

    # ( aexpr )
    elif TokenInfo==UNKNOWN :
        if nextToken==LEFT_PARENTHESES:
            lex()
        else :
            error()

        if SYNTAX_ERROR==0:
            aexpr()
            if SYNTAX_ERROR==0:
                moving_term = moving_dec

        if SYNTAX_ERROR==0:
            if nextToken==RIGHT_PARENTHESES:
                lex()
            else :
                error()
    # error
    else :
        error()


# <type> → int
# declartion int가 아니면 바뀐다.
# 문자를 하나씩만 받아서 함수를 호출 해야해
# <var> 로 받으면 안되나?
def type():
    global declaration_error, lexeme

    # int 인지 아닌지 확인
    if lexeme == "int":
        lex()
    else :
        declaration_error = -1


# <number> → <dec>{<dec>}
# <dec> → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
def number():
    global demical, SYNTAX_ERROR
    if SYNTAX_ERROR == 0:
        if nextToken == INT_LIT:
            demical = int(lexeme)
            lex()
        else:
            error()

# <var> → <alphabet>{<alphabet>}
# <alphabet> → a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
def var():
    global lower_string, SYNTAX_ERROR

    if SYNTAX_ERROR == 0:
        if nextToken == SMALL_LETTER :
            lower_string = lexeme
            lex()
        else :
            error()

def error():
    global SYNTAX_ERROR
    SYNTAX_ERROR = -1


if __name__ == "__main__":
    while True:
        # 초기화
        SYNTAX_ERROR = 0
        input_str = ''
        input_str_index = 0
        print_final = []
        var_dict = {}
        moving_bool = False
        moving_dec = 0
        moving_term = 0
        cmp_detect = 0


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
        if SYNTAX_ERROR == 0:
            if len(print_final) > 0:
                for i in print_final:
                    print(i, end=" ")
                print()
        else:
            print("Syntax Error!!")