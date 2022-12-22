package Parser;

import Tokens.*;
import Tokens.F0FToken.TokenType;
import Grammar.*;
import java.util.List;
import Errors.*;

public class F0FParser {
    private final List<F0FToken> tokens;
    private int current = 0;
    private final Traverse t;

    private static class ParseError extends RuntimeException {}

    public F0FParser(List<F0FToken> tokens){
        this.tokens = tokens;
        t = new Traverse();
    }


    public Expression parse() {
        try {
            return expression();
        } 
        catch (ParseError error) {
            return null;
        }
    }


    private Expression expression(){
        //expression -> equality
        return equality();
    }

    private Expression equality(){
        //equality -> comparison ((!=|==)comparison)*
        //Associates: Left
        Expression expression = comparison();

        while(t.match(TokenType.excl_equal, TokenType.equal_equal)){
            F0FToken operator = t.previous();
            Expression right = comparison();
            expression = new Expression.Binary(expression, operator, right);//I suppose this evaluates
        }
        return expression;
    }

    private Expression comparison(){
        //comparison -> term ((>|>=|<|<=)term)*
        //Associates: Left
        Expression expression = term();

        while(t.match(TokenType.greater, TokenType.greater_equal, TokenType.less, TokenType.less_equal)){
            F0FToken operator = t.previous();
            Expression right = term();
            expression = new Expression.Binary(expression, operator, right);//I suppose this evaluates
        }
        return expression;
    }

    private Expression term(){
        //term -> factor((-|+)factor)*
        //Associates: Left
        Expression expression = factor();

        while(t.match(TokenType.minus, TokenType.plus)){
            F0FToken operator = t.previous();
            Expression right = factor();
            expression = new Expression.Binary(expression, operator, right);//I suppose this evaluates
        }
        return expression;
    }

    private Expression factor(){
        //factor -> unary ((/|*)unary)*
        //Associates: Left
        Expression expression = unary();

        while(t.match(TokenType.slash, TokenType.star)){
            F0FToken operator = t.previous();
            Expression right = unary();
            expression = new Expression.Binary(expression, operator, right);//I suppose this evaluates
        }
        return expression;
    }

    private Expression unary(){
        //unary -> (!|-)unary | primary
        //Associates: Right
        if(t.match(TokenType.excl,TokenType.minus)){
            F0FToken operator = t.previous();
            Expression right = unary();
            return new Expression.Unary(operator, right);
        }
        return primary();
    }

    private Expression primary(){
        //primary -> NUMBER|STRING|true|false|null|(expression)
        
        if(t.match(TokenType.False)) return new Expression.Literal(false);
        if(t.match(TokenType.True)) return new Expression.Literal(true);
        if(t.match(TokenType.Null)) return new Expression.Literal(null);
        if(t.match(TokenType.STRING,TokenType.INT,TokenType.DOUBLE,TokenType.VOID,TokenType.BOOL,TokenType.MFUN,TokenType.POINT)) 
            return new Expression.Literal(t.previous().literal);
        if(t.match(TokenType.opar)){
            Expression expression = expression();
            t.consume(TokenType.cpar, "Expect ')' after expression");
            return new Expression.Grouping(expression);
        }
        throw t.error(t.peek(), "Expect expression.");
    }

    class Traverse{
        public Traverse(){}

        public boolean match(TokenType type) {
            if (check(type)) {
                advance();
                return true;
            }    
            return false;
        }

        public boolean match(TokenType... types) {
            for (TokenType type : types) {
                if (check(type)) {
                    advance();
                    return true;
                }
            }    
            return false;
        }
    
        public F0FToken consume(TokenType type, String message) {
            if (check(type)) return advance();
            
            throw error(peek(), message);
        }
    
        public boolean check(TokenType tokenType) {
            if (isAtEnd()) return false;
            return peek().type == tokenType;
        }
    
        public F0FToken advance() {
            if (!isAtEnd()) current++;
            return previous();
        }
    
        public boolean isAtEnd() {
            return peek().type == TokenType.EOF;
        }
    
        public F0FToken peek() {
            return tokens.get(current);
        }

        public F0FToken previous() {
            return tokens.get(current - 1);
        }
        private ParseError error(F0FToken token, String message) {
            F0FErrors.error(token, message);
            return new ParseError();
        }

        //panic mode synchronization.
        private void synchronize() {
            advance();
    
            while (!isAtEnd()) {
                if (previous().type == TokenType.semicolon) 
                    return;
                
                switch (peek().type) 
                {
                    //case CLASS:
                    case Def:
                    case INT:
                    case DOUBLE:
                    case BOOL:
                    case STRING:
                    case VOID:
                    case MFUN:
                    // case POINT:
                    // case DERIV:
                    case For:
                    case If:
                    // case Else:
                    case While:
                    case Print:
                    case Return:
                    return;
                    default: break;
                }
    
                advance();
            }
        }
    } 
 }
