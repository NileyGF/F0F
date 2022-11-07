package Grammar;

import java.util.List;

import Tokens.*;

public abstract class Expression {
    public interface Visitor<R> {
        R visitAssignExpression(Assign expression);
        R visitBinaryExpression(Binary expression);
        R visitCallExpression(Call expression);
        R visitGetExpression(Get expression);
        R visitGroupingExpression(Grouping expression);
        R visitLiteralExpression(Literal expression);
        R visitLogicalExpression(Logical expression);
        R visitSetExpression(Set expression);
        R visitSuperExpression(Super expression);
        R visitThisExpression(This expression);
        R visitUnaryExpression(Unary expression);
        R visitVariableExpression(Variable expression);
    }
    public static class Assign extends Expression {
        public Assign(F0FToken name, Expression value) {
            this.name = name;
            this.value = value;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitAssignExpression(this);
        }

        public final F0FToken name;
        public final Expression value;
    }
    public static class Binary extends Expression {
        public Binary(Expression left, F0FToken operator, Expression right) {
            this.left = left;
            this.operator = operator;
            this.right = right;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitBinaryExpression(this);
        }

        public final Expression left;
        public final F0FToken operator;
        public final Expression right;
    }
    public static class Call extends Expression {
        public Call(Expression callee, F0FToken paren, List<Expression> arguments) {
            this.callee = callee;
            this.paren = paren;
            this.arguments = arguments;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitCallExpression(this);
        }

        public final Expression callee;
        public final F0FToken paren;
        public final List<Expression> arguments;
    }
    public static class Get extends Expression {
        public Get(Expression object, F0FToken name) {
            this.object = object;
            this.name = name;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitGetExpression(this);
        }

        public final Expression object;
        public final F0FToken name;
    }
    public static class Grouping extends Expression {
        public Grouping(Expression expression) {
            this.expression = expression;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitGroupingExpression(this);
        }

        public final Expression expression;
    }
    public static class Literal extends Expression {
        public Literal(Object value) {
            this.value = value;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitLiteralExpression(this);
        }

        public final Object value;
    }
    public static class Logical extends Expression {
        public Logical(Expression left, F0FToken operator, Expression right) {
            this.left = left;
            this.operator = operator;
            this.right = right;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitLogicalExpression(this);
        }

        public final Expression left;
        public final F0FToken operator;
        public final Expression right;
    }
    public static class Set extends Expression {
        public Set(Expression object, F0FToken name, Expression value) {
            this.object = object;
            this.name = name;
            this.value = value;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitSetExpression(this);
        }

        public final Expression object;
        public final F0FToken name;
        public final Expression value;
    }
    public static class Super extends Expression {
        public Super(F0FToken keyword, F0FToken method) {
            this.keyword = keyword;
            this.method = method;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitSuperExpression(this);
        }

        public final F0FToken keyword;
        public final F0FToken method;
    }
    public static class This extends Expression {
        public This(F0FToken keyword) {
            this.keyword = keyword;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitThisExpression(this);
        }

        public final F0FToken keyword;
    }
    public static class Unary extends Expression {
        public Unary(F0FToken operator, Expression right) {
            this.operator = operator;
            this.right = right;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitUnaryExpression(this);
        }

        public final F0FToken operator;
        public final Expression right;
    }
    public static class Variable extends Expression {
        public Variable(F0FToken name) {
            this.name = name;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitVariableExpression(this);
        }

        public final F0FToken name;
    }

    public abstract <R> R accept(Visitor<R> visitor);
}
