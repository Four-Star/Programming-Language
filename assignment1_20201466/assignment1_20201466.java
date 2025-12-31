package RD;

import java.util.Arrays;
import java.util.Scanner;

public class assignment1_20201466 {
    // 전역 변수 선언
    static int charClass;
    static char[] lexeme = new char[120];
    static char[] input_str = new char[2048];
    static char nextChar;
    static int lexLen;
    static int token;
    static int nextToken;
    static int input_str_index;
    static int SYNTAX_ERROR;
    static int bexpr_error;
    static int expr_index;
    static int notdecimal;
    static int dec_dect;
    static char[] demical = new char[120];
    static int demical_index;
    static int term_data;
    static int aexpr_data;

    // 계산 후 저장할 배열
    static int print_index;
    static int[] print_final = new int[120];

    // 계산 결과 저장할 배열
    static int[] print_x = new int[120];           // 1번
    static int[] print_y = new int[120];           // 2번
    static int[] print_z = new int[120];           // 3번

    static boolean[] print_x_bool = new boolean[120];     // 4번
    static boolean[] print_y_bool = new boolean[120];     // 5번
    static boolean[] print_z_bool = new boolean[120];     // 6번

    // 임시 저장공간
    static int var_x;
    static int var_y;
    static int var_z;

    // 변수(x, y, z)와 연산자 확인 변수
    static int var_detect;
    static int cmp_detect;

    static boolean moving_bool;
    static int moving_dec;

    static int bool_dec;

    static int bool_dec_x;
    static int bool_dec_y;
    static int bool_dec_z;

    // 매크로 지정
    public class TokenConstants {
        public static final int LETTER = 1;
        public static final int DIGIT = 2;
        public static final int UNKNOWN = 99;

        // 토큰
        // ' +, -, *, /, =, !, <, >, ; '
        public static final int NULL = 0;
        public static final int INT_LIT = 10;
        public static final int IDENT = 11;
        public static final int OPERATION = 12;

        // 연산자
        public static final int ASSIGN_OP = 20;
        public static final int ADD_OP = 21;
        public static final int SUB_OP = 22;
        public static final int MULT_OP = 23;
        public static final int DIV_OP = 24;
        public static final int LESS_THAN = 25;
        public static final int LESS = 26;
        public static final int MORE_THAN = 27;
        public static final int MORE = 28;
        public static final int EQUAL = 29;
        public static final int NOT_EQUAL = 30;
        public static final int NOT = 31;
        public static final int SEMI_COLON = 32;

        // 변수
        public static final int VAR_X = 33;
        public static final int VAR_Y = 34;
        public static final int VAR_Z = 35;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            SYNTAX_ERROR = 0;
            bexpr_error = 0;
            input_str_index = 0;
            var_x = 0;
            var_y = 0;
            var_z = 0;
            print_index = 0;
            bool_dec = 1;
            bool_dec_x = 1;
            bool_dec_y = 1;
            bool_dec_z = 1;
            nextToken = -1;
            Arrays.fill(input_str, '\0');

            System.out.print(">> ");
            String input = scanner.nextLine();
            input += '\0';
            input_str = input.toCharArray();

            if (input.equals("terminate\0")) {
                System.exit(0);
            }

            getChar();

            /*
             * RD 파싱 시작
             */
            program();

            /*
             *  출력
             */
            System.out.print(">> ");
            if (SYNTAX_ERROR == 0) {
                int length_print = print_index;
                for (int i = 0; i < print_index; i++) {
                    switch (print_final[i]) {
                        // INT 형 x 출력
                        case 1:
                            System.out.print(print_x[i] + " ");
                            break;

                        // int 형 y 출력
                        case 2:
                            System.out.print(print_y[i] + " ");
                            break;

                        // int 형 z 출력
                        case 3:
                            System.out.print(print_z[i] + " ");
                            break;

                        // bool 형 x 출력
                        case 4:
                            if (!print_x_bool[i]) {
                                System.out.print("FALSE ");
                            } else {
                                System.out.print("TRUE ");
                            }
                            break;

                        // bool 형 y 출력
                        case 5:
                            if (!print_y_bool[i]) {
                                System.out.print("FALSE ");
                            } else {
                                System.out.print("TRUE ");
                            }
                            break;

                        // bool 형 z 출력
                        case 6:
                            if (!print_z_bool[i]) {
                                System.out.print("FALSE ");
                            } else {
                                System.out.print("TRUE ");
                            }
                            break;

                        default:
                            break;
                    }
                }
                System.out.println();
            } else {
                System.out.println("syntax error!!");
            }
        }
    }

    // 문자열 추출 함수 첫번째
    static int lookup_op_1(char ch) {
        switch (ch) {
            case '+' :
                addChar();
                nextToken = TokenConstants.ADD_OP;
                break;

            case '-' :
                addChar();
                nextToken = TokenConstants.SUB_OP;
                break;

            case '*' :
                addChar();
                nextToken = TokenConstants.MULT_OP;
                break;

            case '/' :
                addChar();
                nextToken = TokenConstants.DIV_OP;
                break;

            case '=' :
                addChar();
                nextToken = TokenConstants.ASSIGN_OP;
                break;

            case '!' :
                addChar();
                nextToken = TokenConstants.NOT;
                break;

            case '<' :
                addChar();
                nextToken = TokenConstants.LESS_THAN;
                break;

            case '>' :
                addChar();
                nextToken = TokenConstants.MORE_THAN;
                break;

            case ';' :
                addChar();
                nextToken = TokenConstants.SEMI_COLON;
                break;

            default :
                addChar();
                nextToken = TokenConstants.OPERATION;
                break;
        }
        return nextToken;
    }

    // 문자열 추출 함수 두번째 이상
    static int lookup_op_2(char ch) {
        switch (ch) {
            case '=' :
                // '=='
                if (nextToken == TokenConstants.ASSIGN_OP) {
                    addChar();
                    nextToken = TokenConstants.EQUAL;
                }

                // '!='
                else if (nextToken == TokenConstants.NOT) {
                    addChar();
                    nextToken = TokenConstants.NOT_EQUAL;
                }

                // '<='
                else if (nextToken == TokenConstants.LESS_THAN) {
                    addChar();
                    nextToken = TokenConstants.LESS;
                }

                // '>='
                else if (nextToken == TokenConstants.MORE_THAN) {
                    addChar();
                    nextToken = TokenConstants.MORE;
                }

                // 기타 등등
                else {
                    addChar();
                    nextToken = TokenConstants.OPERATION;
                }
                break;

            // 기타 등등
            default :
                addChar();
                nextToken = TokenConstants.OPERATION;
                break;
        }
        return nextToken;
    }


    // x, y, z 구분 함수
    static int lookup_var(char ch) {
        switch (ch) {
            case 'x' :
                addChar();
                nextToken = TokenConstants.VAR_X;
                break;

            case 'y' :
                addChar();
                nextToken = TokenConstants.VAR_Y;
                break;

            case 'z' :
                addChar();
                nextToken = TokenConstants.VAR_Z;
                break;

            default :
                addChar();
                nextToken = TokenConstants.IDENT;
                break;
        }

        return nextToken;
    }


    // 임시 버퍼에 토큰을 저장
    static void addChar() {
        if (lexLen <= 98) {
            lexeme[lexLen++] = nextChar;
            lexeme[lexLen] = '\0';
        }
        else {
            System.out.println("error");
        }
    }

    // 토큰으로 나눌 때까지 한글자 씩 읽기
    static void getChar() {
        if ((nextChar = input_str[input_str_index++]) != '\0') {
            if (Character.isLetter(nextChar)) {
                charClass = TokenConstants.LETTER;
            }
            else if (Character.isDigit(nextChar)) {
                charClass = TokenConstants.DIGIT;
            }
            else {
                charClass = TokenConstants.UNKNOWN;
            }
        }
        else {
            charClass = TokenConstants.NULL;
        }
    }

    // 공백 빼기
    static void getNonBlank() {
        while (Character.isWhitespace(nextChar)) {
            getChar();
        }
    }

    // 토큰에 대한 정보를 저장
    static int lex() {
        lexLen = 0;
        Arrays.fill(lexeme, '\0');
        getNonBlank();

        switch (charClass) {
            case TokenConstants.LETTER:
                lookup_var(nextChar);
                getChar();

                while (nextChar!='\0' && !Character.isWhitespace(nextChar)) {
                    addChar();
                    getChar();
                    nextToken = TokenConstants.IDENT;
                }

                break;

            case TokenConstants.DIGIT:
                addChar();
                getChar();

                nextToken = TokenConstants.INT_LIT;
                break;

            case TokenConstants.UNKNOWN:
                lookup_op_1(nextChar);
                getChar();

                while (nextChar!='\0' && !Character.isWhitespace(nextChar)) {
                    lookup_op_2(nextChar);
                    getChar();
                }

                break;

            case TokenConstants.NULL:
                nextToken = TokenConstants.NULL;
                lexeme[0] = 'N';
                lexeme[1] = 'U';
                lexeme[2] = 'L';
                lexeme[3] = 'L';
                lexeme[4] = '\0';
                break;
        }
//        String str = new String(lexeme).replaceAll("\0", "");
//        System.out.printf("next token : %d, next lexeme : %s\n", nextToken, str);
        return nextToken;
    }



    // 파싱 함수
    /*
     *  <program> -> {<statement>}
     */
    static void program() {
        lex();

        while (nextToken != TokenConstants.NULL && SYNTAX_ERROR == 0) {
            statement();
        }
    }


    /*
     *  <statement> -> <var> = <expr> ; | print <var> ;
     */
    static void statement() {
        String str = new String(lexeme).replaceAll("\0", "");
        if (SYNTAX_ERROR == 0) {
            // <var> = <expr> ;
            if (!"print".equals(str)) {
                var();

                if (SYNTAX_ERROR == 0) {
                    if (nextToken != TokenConstants.ASSIGN_OP) {
                        error();
                    } else {
                        expr_index = input_str_index;
                        lex();
                        expr();
                    }
                }

                if (SYNTAX_ERROR == 0) {
                    if (nextToken != TokenConstants.SEMI_COLON) {
                        error();
                    } else {
                        lex();
                    }
                }

                // <expr> 의 결과 값을 저장
                if (SYNTAX_ERROR == 0) {
                    // 결과 값이 bool 형일 때
                    if (bool_dec == 0) {
                        switch (var_detect) {
                            case TokenConstants.VAR_X:
                                bool_dec_x = 0;
                                var_x = moving_bool ? 1 : 0;
                                break;

                            case TokenConstants.VAR_Y:
                                bool_dec_y = 0;
                                var_y = moving_bool ? 1 : 0;
                                break;

                            case TokenConstants.VAR_Z:
                                bool_dec_z = 0;
                                var_z = moving_bool ? 1 : 0;
                                break;

                            default:
                                break;
                        }
                    }
                    // 결과 값이 int 형일 때
                    else if (bool_dec == 1) {
                        switch (var_detect) {
                            case TokenConstants.VAR_X:
                                bool_dec_x = 1;
                                var_x = moving_dec;
                                break;

                            case TokenConstants.VAR_Y:
                                bool_dec_y = 1;
                                var_y = moving_dec;
                                break;

                            case TokenConstants.VAR_Z:
                                bool_dec_z = 1;
                                var_z = moving_dec;
                                break;

                            default:
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
                    if (nextToken != TokenConstants.SEMI_COLON) {
                        error();
                    } else {
                        lex();
                    }
                }

                if (SYNTAX_ERROR == 0) {
                    // x, y, z 구별
                    switch (var_detect) {
                        case TokenConstants.VAR_X:
                            // x 가 bool 형 일 때
                            if (bool_dec_x == 0) {
                                print_x_bool[print_index] = var_x != 0;
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

                        case TokenConstants.VAR_Y:
                            // y 가 bool형 일 때
                            if (bool_dec_y == 0) {
                                print_y_bool[print_index] = var_y != 0;
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

                        case TokenConstants.VAR_Z:
                            // z 가 bool형 일 때
                            if (bool_dec_z == 0) {
                                print_z_bool[print_index] = var_z != 0;
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

                        default:
                            break;
                    }
                }
            }
        }
    }


    /*
     *  <expr> -> <bexpr> | <aexpr>
     */
    static void expr() {
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
    static void bexpr() {
        int front=0, back=0;
        if (SYNTAX_ERROR == 0) {
            number();
            if (demical[0] != '\0') {
                String str_front = new String(demical).replaceAll("\0", "");
                front = Integer.parseInt(str_front);
            }
            else {
                error();
            }


            if (SYNTAX_ERROR == 0) {
                relop();
            }

            if (SYNTAX_ERROR == 0) {
                number();
            }

            // 숫자를 변환하고 연산자의 판별을 통해 계산 (bool 형)
            if (SYNTAX_ERROR == 0) {
                if (demical[0] != '\0') {
                    String str_back = new String(demical).replaceAll("\0", "");
                    back = Integer.parseInt(str_back);
                }
                else {
                    error();
                }

                boolean bool_bexpr = false;

                switch (cmp_detect) {
                    case TokenConstants.EQUAL:
                        bool_bexpr = (front == back);
                        break;

                    case TokenConstants.NOT_EQUAL:
                        bool_bexpr = (front != back);
                        break;

                    case TokenConstants.MORE:
                        bool_bexpr = (front >= back);
                        break;

                    case TokenConstants.MORE_THAN:
                        bool_bexpr = (front > back);
                        break;

                    case TokenConstants.LESS:
                        bool_bexpr = (front <= back);
                        break;

                    case TokenConstants.LESS_THAN:
                        bool_bexpr = (front < back);
                        break;

                    default:
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
    static void relop() {
        if (SYNTAX_ERROR == 0) {
            switch (nextToken) {
                case TokenConstants.EQUAL:
                    cmp_detect = TokenConstants.EQUAL;
                    break;

                case TokenConstants.NOT_EQUAL:
                    cmp_detect = TokenConstants.NOT_EQUAL;
                    break;

                case TokenConstants.MORE:
                    cmp_detect = TokenConstants.MORE;
                    break;

                case TokenConstants.MORE_THAN:
                    cmp_detect = TokenConstants.MORE_THAN;
                    break;

                case TokenConstants.LESS:
                    cmp_detect = TokenConstants.LESS;
                    break;

                case TokenConstants.LESS_THAN:
                    cmp_detect = TokenConstants.LESS_THAN;
                    break;

                default:
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
    static void aexpr() {
        int front = 0, back = 0, operand = 0;
        if (SYNTAX_ERROR == 0) {
            term();
            front = term_data;

            // 에러가 나지 않았거나 +, - 가 오면 반복
            while ((nextToken == TokenConstants.ADD_OP || nextToken == TokenConstants.SUB_OP) && SYNTAX_ERROR == 0) {
                if (nextToken == TokenConstants.ADD_OP) {
                    operand = TokenConstants.ADD_OP;
                } else if (nextToken == TokenConstants.SUB_OP) {
                    operand = TokenConstants.SUB_OP;
                }
                lex();
                term();

                // 계산
                back = term_data;
                if (operand == TokenConstants.ADD_OP) {
                    front = front + back;
                } else if (operand == TokenConstants.SUB_OP) {
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
    static void term() {
        int front = 0, back = 0, operand = 0;
        if (SYNTAX_ERROR == 0) {
            factor();
            if (demical[0] != '\0') {
                String str_front = new String(demical).replaceAll("\0", "");
                front = Integer.parseInt(str_front);
            }
            else {
                error();
            }

            // 에러가 나지 않았거나 *, / 가 오면 반복
            while ((nextToken == TokenConstants.MULT_OP || nextToken == TokenConstants.DIV_OP) && SYNTAX_ERROR == 0) {
                if (nextToken == TokenConstants.MULT_OP) {
                    operand = TokenConstants.MULT_OP;
                } else if (nextToken == TokenConstants.DIV_OP) {
                    operand = TokenConstants.DIV_OP;
                }
                lex();
                factor();

                // 계산
                if (demical[0] != '\0') {
                    String str_back = new String(demical).replaceAll("\0", "");
                    back = Integer.parseInt(str_back);
                }
                else {
                    error();
                }
                if (operand == TokenConstants.MULT_OP) {
                    front = front * back;
                } else if (operand == TokenConstants.DIV_OP) {
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
    static void factor() {
        if (SYNTAX_ERROR == 0) {
            number();
        }
    }

    /*
     *  <number> -> <dec>{<dec>}
     */
    static void number() {
        dec_dect = 0;
        Arrays.fill(demical, '\0');
        if (SYNTAX_ERROR == 0) {
            dec();
            dec_dect++;

            // 정수이거나 에러가 나지 않았을 때
            while (notdecimal == 0 && SYNTAX_ERROR == 0) {
                dec();
            }
            notdecimal = 0;
            demical_index = 0;
        }
    }


    /*
     * <dec> -> 0|1|2|3|4|5|6|7|8|9
     */
    static void dec() {
        if (SYNTAX_ERROR == 0) {
            if (nextToken == TokenConstants.INT_LIT) {
                demical[demical_index++] = lexeme[0];
                lex();
            }
            // 첫번째 <dec> 에 정수가 아니면 에러
            else if (dec_dect == 0) {
                error();
                bexpr_error = -1;
            }
            // 이후의 <dec>은 지금 판별하진 ㅇ낳음
            else {
                notdecimal = -1;
            }
        }
    }

    /*
     *  <var> -> x | y | z
     */
    static void var() {
        if (SYNTAX_ERROR == 0) {
            if (nextToken == TokenConstants.VAR_X || nextToken == TokenConstants.VAR_Y || nextToken == TokenConstants.VAR_Z) {
                if (nextToken == TokenConstants.VAR_X) {
                    var_detect = TokenConstants.VAR_X;
                } else if (nextToken == TokenConstants.VAR_Y) {
                    var_detect = TokenConstants.VAR_Y;
                } else if (nextToken == TokenConstants.VAR_Z) {
                    var_detect = TokenConstants.VAR_Z;
                }
                lex();
            } else {
                error();
            }
        }
    }


    // 에러 함수
    static void error() {
        SYNTAX_ERROR = -1;
    }

}
