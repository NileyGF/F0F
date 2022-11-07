package tools;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;

public class GenerateAST {
    public static void main(String[] args) throws IOException {
        String outputDir = "src/Grammar";

        defineAst(outputDir, "Expression", Arrays.asList(
            "Assign   : F0FToken name, Expression value",
            "Binary   : Expression left, F0FToken operator, Expression right",
            "Call     : Expression callee, F0FToken paren, List<Expression> arguments",
            "Get      : Expression object, F0FToken name",
            "Grouping : Expression expression",
            "Literal  : Object value",
            "Logical  : Expression left, F0FToken operator, Expression right",
            "Set      : Expression object, F0FToken name, Expression value",
            "Super    : F0FToken keyword, F0FToken method",
            "This     : F0FToken keyword",
            "Unary    : F0FToken operator, Expression right",
            "Variable : F0FToken name"
        )); 
        defineAst(outputDir, "Statement", Arrays.asList(
            "Block      : List<Statement> statements",
            "Class      : F0FToken name, Expression superclass, List<Statement.Function> methods",
            "Expression : Expression expression",
            "Function   : F0FToken name, List<F0FToken> parameters, List<Statement> body",
            "If         : Expression condition, Statement thenBranch, Statement elseBranch",
            "Print      : Expression expression",
            "Return     : F0FToken keyword, Expression value",
            "Var        : F0FToken name, Expression initializer",
            "While      : Expression condition, Statement body"
        ));
    }
    private static void defineAst(String outputDir, String baseName, List<String> types) throws IOException {
        String path = outputDir + "/" + baseName + ".java";
        PrintWriter writer = new PrintWriter(path, "UTF-8");

        writer.println("package Grammar;");
        writer.println("");
        writer.println("import java.util.List;");
        writer.println("");
        writer.println("import Tokens.*;");
        writer.println("");
        writer.println("public abstract class " + baseName + " {");

        defineVisitor(writer, baseName, types);

        // The AST classes.
        for (String type : types) {
            String className = type.split(":")[0].trim();
            String fields = type.split(":")[1].trim();
            defineType(writer, baseName, className, fields);
        }

        // The base accept() method.
        writer.println("");
        writer.println("    public abstract <R> R accept(Visitor<R> visitor);");

        writer.println("}");
        writer.close();
    }

    private static void defineVisitor(PrintWriter writer, String baseName, List<String> types) {
        writer.println("    public interface Visitor<R> {");

        for (String type : types) {
            String typeName = type.split(":")[0].trim();
            writer.println("        R visit" + typeName + baseName + "(" + typeName + " " + baseName.toLowerCase() + ");");
        }

        writer.println("    }");
    }

    private static void defineType(PrintWriter writer, String baseName, String className, String fieldList) {
        writer.println("    public static class " + className + " extends " + baseName + " {");

        // Constructor.
        writer.println("        public " + className + "(" + fieldList + ") {");

        // Store parameters in fields.
        String[] fields = fieldList.split(", ");
        for (String field : fields) {
            String name = field.split(" ")[1];
            writer.println("            this." + name + " = " + name + ";");
        }

        writer.println("        }");

        // Visitor pattern.
        writer.println();
        writer.println("        public <R> R accept(Visitor<R> visitor) {");
        writer.println("            return visitor.visit" + className + baseName + "(this);");
        writer.println("        }");

        // Fields.
        writer.println();
        for (String field : fields) {
            writer.println("        public final " + field + ";");
        }

        writer.println("    }");
    }
}
