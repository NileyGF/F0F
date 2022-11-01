//import java.io.BufferedReader;
import java.io.IOException;
//import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import Lexer.*;
//import Parser.*;
import Tokens.*;

public class F0F {
    //private static final Interpreter interpreter = new Interpreter();
    static boolean hadError = false;
    static boolean hadRuntimeError = false;
    public static void main(String[] args) throws Exception 
    {
        // if (args.length > 1) 
        // {
        //     System.out.println("Usage: jlox [script]");
        //     System.exit(64);
        // } 
        // else if (args.length == 1) 
        // {   runFile(args[0]);   } 
        // else 
        // {   runPrompt();    }
        runFile("F0F/1st_test");
        //run("");
    }

    private static void runFile(String path) throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(path));
        run(new String(bytes, Charset.defaultCharset()));

        // Indicate an error in the exit code.
        if (hadError) System.exit(65);
        if (hadRuntimeError) System.exit(70);
    }
    private static void run(String source) {
        F0FLexer lexer = new F0FLexer(source);
        List<F0FToken> tokens = lexer.scanTokens();
        // Parser parser = new Parser(tokens);
        // List<Stmt> statements = parser.parse();

        // Stop if there was a syntax error.
        //if (hadError) return;

        // Resolver resolver = new Resolver(interpreter);
        // resolver.resolve(statements);

        // Stop if there was a resolution error.
        //if (hadError) return;

        //interpreter.interpret(statements); 

        for(int i = 0; i < tokens.size(); i++){
            System.out.println(tokens.get(i));
        }    
    }
}