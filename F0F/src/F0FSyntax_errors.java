public class F0FSyntax_errors {
    static void error(int line, String message) 
    {
        report(line, "", message);
    }
    private static void report(int line, String where, String message) 
    {
        System.err.println(
        "[line " + line + "] Error" + where + ": " + message);
        //hadError = true;
    }
}
