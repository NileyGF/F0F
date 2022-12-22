package Errors;

import Tokens.*;
import Tokens.F0FToken.TokenType;

public class F0FErrors {
    public static void error(int line, String message) {
        report(line, "", message);
    }

    private static void report(int line, String where, String message) {
        System.err.println("[line " + line + "] Error" + where + ": " + message);
        //hadError = true;
    }

    public static void error(F0FToken token, String message) {
        if (token.type == TokenType.EOF) {
            report(token.line, " at end", message);
        } 
        else {
            report(token.line, " at '" + token.lex + "'", message);
        }
    }
}
