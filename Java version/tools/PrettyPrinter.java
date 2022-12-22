package tools;

import Grammar.*;
import Grammar.Expression.Assign;
import Grammar.Expression.Binary;
import Grammar.Expression.Call;
import Grammar.Expression.Get;
import Grammar.Expression.Grouping;
import Grammar.Expression.Literal;
import Grammar.Expression.Logical;
import Grammar.Expression.Set;
import Grammar.Expression.Super;
import Grammar.Expression.This;
import Grammar.Expression.Unary;
import Grammar.Expression.Variable;

public class PrettyPrinter implements Expression.Visitor<String>{

    public String print(Expression expression) {
        return expression.accept(this);
    }

    @Override
    public String visitBinaryExpression(Binary expression) {
        return parenthesize(expression.operator.lex, expression.left, expression.right);
    }
    @Override
    public String visitGroupingExpression(Grouping expression) {
        return parenthesize("group", expression.expression);
    }
    @Override
    public String visitLiteralExpression(Literal expression) {
        if(expression.value == null)
            return "null";
        return expression.value.toString();
    }
    @Override
    public String visitUnaryExpression(Unary expression) {
        return parenthesize(expression.operator.lex, expression.right);
    }
    private String parenthesize(String name, Expression ... expressions){
        StringBuilder builder = new StringBuilder();
        builder.append("(").append(name);
        for(Expression expression : expressions){
            builder.append(" ");
            builder.append(expression.accept(this));
        }
        builder.append(")");
        return builder.toString();
    }
    @Override
    public String visitAssignExpression(Assign expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitCallExpression(Call expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitGetExpression(Get expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitLogicalExpression(Logical expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitSetExpression(Set expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitSuperExpression(Super expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitThisExpression(This expression) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public String visitVariableExpression(Variable expression) {
        // TODO Auto-generated method stub
        return null;
    }
    
}
