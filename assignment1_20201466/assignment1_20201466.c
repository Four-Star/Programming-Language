#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

/* 전역 변수 선언 */
int charClass;
char lexeme[100];
char input_str[2048];
char nextChar;
int lexLen;
int token;
int nextToken;
int input_str_index;
int SYNTAX_ERROR;
int bexpr_error;
int expr_index;
int notdecimal;
int dec_dect;
char demical[100];
int demical_index;
int term_data;
int aexpr_data;

/* 계산 후 저장할 배열 */
int print_index;
int print_final[100];

/* 계산 결과 저장할 배열 */
int print_x[100];           // 1번
int print_y[100];           // 2번
int print_z[100];           // 3번

bool print_x_bool[100];     // 4번
bool print_y_bool[100];     // 5번
bool print_z_bool[100];     // 6번

/* 임시 저장공간 */
int var_x;
int var_y;
int var_z;

/* 변수(x, y, z)와 연산자 확인 변수 */
int var_detect;
int cmp_detect;

bool moving_bool;
int moving_dec;

int bool_dec;

int bool_dec_x;
int bool_dec_y;
int bool_dec_z;

/* 함수 */
/* 문자열 추출 함수 */
int lookup_op_1(char ch);
int lookup_op_2(char ch);
int lookup_var(char ch);
void addChar();
void getChar();
void getNonBlank();
int lex();

/* 파싱 함수 */
void program();
void statement();
void expr();
void bexpr();
void relop();
void aexpr();
void term();
void factor();
void number();
void dec();
void var();

/* 에러 함수 */
void error();



/* Character */
#define LETTER 1
#define DIGIT 2
#define UNKNOWN 99

/*
 * 토큰
 * ' +, -, *, /, =, !, <, >, ; '
 */
#define NULL_A 0
#define INT_LIT 10
#define IDENT 11
#define OPERATION 12

/* 연산자 */
#define ASSIGN_OP 20
#define ADD_OP 21
#define SUB_OP 22
#define MULT_OP 23
#define DIV_OP 24
#define LESS_THAN 25
#define LESS 26
#define MORE_THAN 27
#define MORE 28
#define EQUAL 29
#define NOT_EQUAL 30
#define NOT 31
#define SEMI_COLON 32

/* 변수 */
#define VAR_X 33
#define VAR_Y 34
#define VAR_Z 35


int main() {
    while (1) {
        SYNTAX_ERROR = 0;
        bexpr_error = 0;
        input_str_index = 0;
        var_x=0; var_y=0; var_z=0;
        print_index = 0;
        bool_dec = 1;
        bool_dec_x = 1; bool_dec_y = 1; bool_dec_z = 1;
        memset(input_str, '\0', sizeof(input_str));
        printf(">> ");
        fgets(input_str, 2048, stdin);

        if (strcmp(input_str, "terminate\n") == 0) {
            exit(0);
        }

        getChar();

        /*
         * RD 파싱 시작
         */
        program();

        /*
         *  출력
         */
        printf(">> ");
        if (SYNTAX_ERROR == 0) {
            int length_print = print_index;
            for (int i=0; i<print_index; i++) {
                switch (print_final[i]) {
                    // INT 형 x 출력
                    case 1 :
                        printf("%d ", print_x[i]);
                        break;

                    // int 형 y 출력
                    case 2 :
                        printf("%d ", print_y[i]);
                        break;

                    // int 형 z 출력
                    case 3 :
                        printf("%d ", print_z[i]);
                        break;

                    // bool 형 x 출력
                    case 4 :
                        if (print_x_bool[i] == 0) {
                            printf("FALSE ");
                        }
                        else {
                            printf("TRUE ");
                        }
                        break;

                    // bool 형 y 출력
                    case 5 :
                        if (print_y_bool[i] == 0) {
                            printf("FALSE ");
                        }
                        else {
                            printf("TRUE ");
                        }
                        break;

                    // bool 형 z 출력
                    case 6 :
                        if (print_z_bool[i] == 0) {
                            printf("FALSE ");
                        }
                        else {
                            printf("TRUE ");
                        }
                        break;

                    default :
                        break;
                }
            }
            printf("\n");
        }
        else {
            printf("syntax error!!\n");
        }
    }
    return 0;
}

/*
 *  연산자가 처음 올 때 어떤 연산자인지 확인하여 정보를 저장하는 함수
 */
int lookup_op_1(char ch) {
    switch (ch) {
        case '+' :
            addChar();
            nextToken = ADD_OP;
            break;

        case '-' :
            addChar();
            nextToken = SUB_OP;
            break;

        case '*' :
            addChar();
            nextToken = MULT_OP;
            break;

        case '/' :
            addChar();
            nextToken = DIV_OP;
            break;

        case '=' :
            addChar();
            nextToken = ASSIGN_OP;
            break;

        case '!' :
            addChar();
            nextToken = NOT;
            break;

        case '<' :
            addChar();
            nextToken = LESS_THAN;
            break;

        case '>' :
            addChar();
            nextToken = MORE_THAN;
            break;

        case ';' :
            addChar();
            nextToken = SEMI_COLON;
            break;

        default :
            addChar();
            nextToken = OPERATION;
            break;
    }
    return nextToken;
}

/*
 *   연산자가 2개 이상 연속으로 올 때 자신이 쓰는
 */
int lookup_op_2(char ch) {
    switch (ch) {
        case '=' :
            // '=='
            if (nextToken == ASSIGN_OP) {
                addChar();
                nextToken = EQUAL;
            }

            // '!='
            else if (nextToken == NOT) {
                addChar();
                nextToken = NOT_EQUAL;
            }

            // '<='
            else if (nextToken == LESS_THAN) {
                addChar();
                nextToken = LESS;
            }

            // '>='
            else if (nextToken == MORE_THAN) {
                addChar();
                nextToken = MORE;
            }

            // 기타 등등
            else {
                addChar();
                nextToken = OPERATION;
            }
            break;

            // 기타 등등
        default :
            addChar();
            nextToken = OPERATION;
            break;
    }
    return nextToken;
}

/*
 * <var> 결과 값을 확인 하려는 함수
 */
int lookup_var(char ch) {
    switch (ch) {
        case 'x' :
            addChar();
            nextToken = VAR_X;
            break;

        case 'y' :
            addChar();
            nextToken = VAR_Y;
            break;

        case 'z' :
            addChar();
            nextToken = VAR_Z;
            break;

        default :
            addChar();
            nextToken = IDENT;
            break;
    }

    return nextToken;
}

/*
 *  분리한 토큰을 배열에 저장하는 함수
 */
void addChar() {
    if (lexLen <= 98) {
        lexeme[lexLen++] = nextChar;
        lexeme[lexLen] = 0;
    }
    else {
        printf("error");
    }
}

/*
 *   판단할 문자가 문자인지, 숫자인지, 연산자인지 판단하는 함수
 */
void getChar() {
    if ((nextChar = input_str[input_str_index++]) != '\0') {
        if (isalpha(nextChar)) {
            charClass = LETTER;
        }
        else if (isdigit(nextChar)) {
            charClass = DIGIT;
        }
        else { charClass = UNKNOWN; }
    }
    else {
        charClass = NULL_A;
    }
}

/*
 *   공백 키를 건너 띄어주는 함수
 */
void getNonBlank() {
    while (isspace(nextChar)) {
        getChar();
    }
}

/*
 *   분리한 토큰의 정보를 저장해주는 함수
 */
int lex() {
    lexLen = 0;
    getNonBlank();

    switch (charClass) {
        case LETTER :
            lookup_var(nextChar);
            getChar();

            while (!isspace(nextChar)) {
                addChar();
                getChar();
                nextToken = IDENT;
            }

            break;

        case DIGIT :
            addChar();
            getChar();

            nextToken = INT_LIT;
            break;

        case UNKNOWN :
            lookup_op_1(nextChar);
            getChar();

            while (!isspace(nextChar)) {
                lookup_op_2(nextChar);
                getChar();
            }

            break;

        case NULL_A :
            nextToken = NULL_A;
            lexeme[0] = 'N';
            lexeme[1] = 'U';
            lexeme[2] = 'L';
            lexeme[3] = 'L';
            lexeme[4] = 0;
            break;
    }
//    printf("next token : %d, next lexeme : %s\n", nextToken, lexeme);
    return nextToken;
}

/*
 *  <program> -> {<statement>}
 */
void program() {
    lex();

    while (nextToken != NULL_A && SYNTAX_ERROR == 0) {
        statement();
    }
}

/*
 *  <statement> -> <var> = <expr> ; | print <var> ;
 */
void statement() {
    if (SYNTAX_ERROR == 0) {
        // <var> = <expr> ;
        if (strcmp(lexeme, "print") != 0) {
            var();

            if (SYNTAX_ERROR == 0) {
                if (nextToken != ASSIGN_OP) {
                    error();
                }
                else {
                    expr_index = input_str_index;
                    lex();
                    expr();
                }
            }

            if (SYNTAX_ERROR == 0) {
                if (nextToken != SEMI_COLON) {
                    error();
                }
                else {
                    lex();
                }
            }

            // <expr> 의 결과 값을 저장
            if (SYNTAX_ERROR == 0) {
                // 결과 값이 bool 형일 때
                if (bool_dec == 0) {
                    switch (var_detect) {
                        case VAR_X :
                            bool_dec_x = 0;
                            var_x = moving_bool;
                            break;

                        case VAR_Y :
                            bool_dec_y = 0;
                            var_y = moving_bool;
                            break;

                        case VAR_Z :
                            bool_dec_z = 0;
                            var_z = moving_bool;
                            break;

                        default :
                            break;
                    }
                }
                // 결과 값이 int 형일 때
                else if (bool_dec == 1){
                    switch (var_detect) {
                        case VAR_X :
                            bool_dec_x = 1;
                            var_x = moving_dec;
                            break;

                        case VAR_Y :
                            bool_dec_y = 1;
                            var_y = moving_dec;
                            break;

                        case VAR_Z :
                            bool_dec_z = 1;
                            var_z = moving_dec;
                            break;

                        default :
                            break;
                    }
                }
            }
        }
        // print <var> ;
        else {
            lex();
            var();

            if (SYNTAX_ERROR == 0) {
                if (nextToken != SEMI_COLON) {
                    error();
                }
                else {
                    lex();
                }
            }

            if (SYNTAX_ERROR == 0) {
                // x, y, z 구별
                switch (var_detect) {
                    case VAR_X :
                        // x 가 bool 형 일 때
                        if (bool_dec_x == 0) {
                            print_x_bool[print_index] = var_x;
                            print_final[print_index++] = 4;
                            print_final[print_index] = 0;
                        }
                        // x 가 int 형일 때
                        else if (bool_dec_x == 1) {
                            print_x[print_index] = var_x;
                            print_final[print_index++] = 1;
                            print_final[print_index] = 0;
                        }
                        break;

                    case VAR_Y :
                        // y 가 bool형 일 때
                        if (bool_dec_y == 0) {
                            print_y_bool[print_index] = var_y;
                            print_final[print_index++] = 5;
                            print_final[print_index] = 0;
                        }
                        // y 가 int 형 일 때
                        else if (bool_dec_y == 1) {
                            print_y[print_index] = var_y;
                            print_final[print_index++] = 2;
                            print_final[print_index] = 0;
                        }
                        break;

                    case VAR_Z :
                        // z 가 bool형 일 때
                        if (bool_dec_z == 0) {
                            print_z_bool[print_index] = var_z;
                            print_final[print_index++] = 6;
                            print_final[print_index] = 0;
                        }
                        // z 가 int 형일 때
                        else if (bool_dec_z == 1) {
                            print_z[print_index] = var_z;
                            print_final[print_index++] = 3;
                            print_final[print_index] = 0;
                        }
                        break;

                    default :
                        break;
                }
            }
        }
    }
}

/*
 *  <expr> -> <bexpr> | <aexpr>
 */
void expr() {
    if (SYNTAX_ERROR == 0) {
        bexpr_error = 0;

        // 먼저 실행
        bexpr();

        // <bexpr> 이 오류가 날 시 <aexpr> 실행
        if (bexpr_error == -1) {
            SYNTAX_ERROR = 0;
            bexpr_error = 0;
            input_str_index = expr_index;
            getChar();
            lex();
            aexpr();
        }
    }
}

/*
 *  <bexpr> -> <number> <relop> <number>
 */
void bexpr() {
    if (SYNTAX_ERROR == 0) {
        number();
        int front = atoi(demical);
        demical[0] = 0;

        if (SYNTAX_ERROR == 0) {
            relop();
        }

        if (SYNTAX_ERROR == 0) {
            number();
        }

        // 숫자를 변환하고 연산자의 판별을 통해 계산 (bool 형)
        if (SYNTAX_ERROR == 0) {
            int back = atoi(demical);
            demical[0] = 0;

            int bool_bexpr;

            switch (cmp_detect) {
                case EQUAL :
                    bool_bexpr = (front == back);
                    break;

                case NOT_EQUAL :
                    bool_bexpr = (front != back);
                    break;

                case MORE :
                    bool_bexpr = (front >= back);
                    break;

                case MORE_THAN :
                    bool_bexpr = (front > back);
                    break;

                case LESS :
                    bool_bexpr = (front <= back);
                    break;

                case LESS_THAN :
                    bool_bexpr = (front < back);
                    break;

                default :
                    break;
            }
            // 전역 변수에 저장
            moving_bool = bool_bexpr;
            bool_dec = 0;
        }
   }
}

/*
 *  <relop> -> == | != | < | > | <= | >=
 */
void relop() {
    if (SYNTAX_ERROR == 0) {
        switch (nextToken) {
            case EQUAL :
                cmp_detect = EQUAL;
                break;

            case NOT_EQUAL :
                cmp_detect = NOT_EQUAL;
                break;

            case MORE :
                cmp_detect = MORE;
                break;

            case MORE_THAN :
                cmp_detect = MORE_THAN;
                break;

            case LESS :
                cmp_detect = LESS;
                break;

            case LESS_THAN :
                cmp_detect = LESS_THAN;
                break;

            default :
                error();
                bexpr_error = -1;
                // lex();
                break;
        }
        if (SYNTAX_ERROR == 0) {
            lex();
        }
    }
}

/*
 *  <aexpr> -> <term> {(+ | -) <term>}
 */
void aexpr() {
    int front=0, back=0, operand=0;
    if (SYNTAX_ERROR == 0) {
        term();
        front = term_data;

        // 에러가 나지 않았거나 +, - 가 오면 반복
        while ((nextToken == ADD_OP || nextToken == SUB_OP) && SYNTAX_ERROR==0) {
            if (nextToken == ADD_OP) {
                operand = ADD_OP;
            }
            else if (nextToken == SUB_OP) {
                operand = SUB_OP;
            }
            lex();
            term();

            // 계산
            back = term_data;
            if (operand == ADD_OP) {
                front = front + back;
            }
            else if (operand == SUB_OP) {
                front = front - back;
            }
        }
    }
    if (SYNTAX_ERROR == 0) {
        bool_dec = 1;
        moving_dec = front;
    }
}

/*
 *  <term> -> <factor> {(* | /) <factor>
 */
void term() {
    int front=0, back=0, operand;
    if (SYNTAX_ERROR == 0) {
        factor();
        front = atoi(demical);

        // 에러가 나지 않았거나 *, / 가 오면 반복
        while ((nextToken == MULT_OP || nextToken == DIV_OP) && SYNTAX_ERROR==0) {
            if (nextToken == MULT_OP) {
                operand = MULT_OP;
            }
            else if (nextToken == DIV_OP) {
                operand = DIV_OP;
            }
            lex();
            factor();

            // 계산
            back = atoi(demical);
            if (operand == MULT_OP) {
                front = front * back;
            }
            else if (operand == DIV_OP) {
                front = front / back;
            }
        }
    }
    if (SYNTAX_ERROR == 0) {
        term_data = front;
    }
}

/*
 *  <factor> -> <number>
 */
void factor() {
    if (SYNTAX_ERROR == 0) {
        number();
    }
}

/*
 *  <number> -> <dec>{<dec>}
 */
void number() {
    dec_dect = 0;
    memset(demical, '\0', sizeof(demical));
    if (SYNTAX_ERROR == 0) {
        dec();
        dec_dect++;

        // 정수이거나 에러가 나지 않았을 때
        while (notdecimal==0 && SYNTAX_ERROR == 0) {
            dec();
        }
        notdecimal = 0;
        demical_index = 0;
    }
}

/*
 * <dec> -> 0|1|2|3|4|5|6|7|8|9
 */
void dec() {
    if (SYNTAX_ERROR == 0) {
        if (nextToken == INT_LIT) {
            demical[demical_index++] = lexeme[0];
            lex();
        }
        // 첫번째 <dec> 에 정수가 아니면 에러
        else if (dec_dect == 0) {
            error();
            bexpr_error = -1;
        }
        // 이후의 <dec>은 지금 판별하진 않음
        else {
            notdecimal = -1;
        }
    }
}

/*
 *  <var> -> x | y | z
 */
void var() {
    if (SYNTAX_ERROR == 0) {
        if (nextToken == VAR_X || nextToken == VAR_Y || nextToken == VAR_Z) {
            if (nextToken == VAR_X) {
                var_detect = VAR_X;
            }
            else if (nextToken == VAR_Y) {
                var_detect = VAR_Y;
            }
            else if (nextToken == VAR_Z) {
                var_detect = VAR_Z;
            }
            lex();
        }
        else {
            error();
        }
    }
}

void error() {
    SYNTAX_ERROR = -1;
}