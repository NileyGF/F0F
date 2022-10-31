package Tokens;
public class F0FToken 
{
    protected String lex;
    protected TokenType type;
    protected Object literal;
    protected int line;
    protected int column; //where the lexeme begins in the line
    protected int length;
    
    public F0FToken(TokenType type, String lexeme, Object literal, int line, int column, int length) 
    {
        this.type = type;
        this.lex = lexeme;
        this.literal = literal;
        this.line = line;
        this.column = column;
        this.length = length;
    }

    public String getLexeme(){ return lex; }
    public String toString() {
        return type + " " + lex + " line: " + line + " column : " + column + " length: " + length; 
    }


    public enum TokenType {
        //single character tokens
        opar, cpar, obracket/*[*/, cbracket/*]*/, obrace/*{*/, cbrace/*}*/, 
        comma, dot, semicolon, minus, plus, star, slash, percent, caret /* ^ */, 
        quoat, double_quoat,
    
        //comparisson
        equal, equal_equal, excl, excl_equal,
        greater, greater_equal, less, less_equal,
        
        //literals
        INT, FLOAT, DOUBLE, VOID, BOOL, STRING, MFUN, POINT ,/* DERIV, */
        // Floor, Ceil, Round, Random
    
        //keywords
        True, False, Null, And, Or, Def, Return, While, For, If, Else, Print,

        Identifier, Integer, Decimal,
    
        EOF
    }
    
}
