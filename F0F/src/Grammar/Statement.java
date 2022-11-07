package Grammar;

import java.util.List;

import Tokens.*;

public abstract class Statement {
    public interface Visitor<R> {
        R visitBlockStatement(Block statement);
        R visitClassStatement(Class statement);
        R visitExpressionStatement(Expression statement);
        R visitFunctionStatement(Function statement);
        R visitIfStatement(If statement);
        R visitPrintStatement(Print statement);
        R visitReturnStatement(Return statement);
        R visitVarStatement(Var statement);
        R visitWhileStatement(While statement);
    }
    public static class Block extends Statement {
        public Block(List<Statement> statements) {
            this.statements = statements;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitBlockStatement(this);
        }

        public final List<Statement> statements;
    }
    public static class Class extends Statement {
        public Class(F0FToken name, Expression superclass, List<Statement.Function> methods) {
            this.name = name;
            this.superclass = superclass;
            this.methods = methods;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitClassStatement(this);
        }

        public final F0FToken name;
        public final Expression superclass;
        public final List<Statement.Function> methods;
    }
    public static class Expression extends Statement {
        public Expression(Expression expression) {
            this.expression = expression;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitExpressionStatement(this);
        }

        public final Expression expression;
    }
    public static class Function extends Statement {
        public Function(F0FToken name, List<F0FToken> parameters, List<Statement> body) {
            this.name = name;
            this.parameters = parameters;
            this.body = body;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitFunctionStatement(this);
        }

        public final F0FToken name;
        public final List<F0FToken> parameters;
        public final List<Statement> body;
    }
    public static class If extends Statement {
        public If(Expression condition, Statement thenBranch, Statement elseBranch) {
            this.condition = condition;
            this.thenBranch = thenBranch;
            this.elseBranch = elseBranch;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitIfStatement(this);
        }

        public final Expression condition;
        public final Statement thenBranch;
        public final Statement elseBranch;
    }
    public static class Print extends Statement {
        public Print(Expression expression) {
            this.expression = expression;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitPrintStatement(this);
        }

        public final Expression expression;
    }
    public static class Return extends Statement {
        public Return(F0FToken keyword, Expression value) {
            this.keyword = keyword;
            this.value = value;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitReturnStatement(this);
        }

        public final F0FToken keyword;
        public final Expression value;
    }
    public static class Var extends Statement {
        public Var(F0FToken name, Expression initializer) {
            this.name = name;
            this.initializer = initializer;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitVarStatement(this);
        }

        public final F0FToken name;
        public final Expression initializer;
    }
    public static class While extends Statement {
        public While(Expression condition, Statement body) {
            this.condition = condition;
            this.body = body;
        }

        public <R> R accept(Visitor<R> visitor) {
            return visitor.visitWhileStatement(this);
        }

        public final Expression condition;
        public final Statement body;
    }

    public abstract <R> R accept(Visitor<R> visitor);
}
