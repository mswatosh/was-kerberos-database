package com.example;

import java.io.IOException;
import java.io.PrintWriter;
import java.security.Security;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.Resource;
import javax.security.auth.Subject;
import javax.security.auth.callback.CallbackHandler;
import javax.security.auth.login.Configuration;
import javax.security.auth.login.LoginContext;
import javax.security.auth.login.LoginException;
import javax.security.auth.login.Configuration.Parameters;
import javax.servlet.ServletException;
import javax.servlet.annotation.HttpConstraint;
import javax.servlet.annotation.ServletSecurity;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.transaction.HeuristicMixedException;
import javax.transaction.UserTransaction;


import javax.sql.DataSource;

@WebServlet("/example")
@ServletSecurity(value = @HttpConstraint(rolesAllowed = {
        "Manager" }, transportGuarantee = ServletSecurity.TransportGuarantee.NONE))
public class ExampleServlet extends HttpServlet {


    public static final String SUCCESS = "SUCCESS";
    public static final String FAILURE = "FAILURE";

    @Resource(name = "jdbc/krb5ds")
    DataSource ds;

    
    @Resource(name = "jdbc/nokrb5")
    DataSource noKrb5;
/*
    @Resource(lookup = "jdbc/db2krbkeytab")
    DataSource db2krbkeytab;

    @Resource(lookup = "jdbc/db2krbcc")
    DataSource db2krbcc;

    @Resource(lookup = "jdbc/db2nokrb")
    DataSource db2nokrb;
*/
    @Resource
    private UserTransaction tran;


    private static final long serialVersionUID = 1L;

    @Override
    protected void doGet(HttpServletRequest request,
                        HttpServletResponse response)
                        throws ServletException, IOException {
        response.setContentType("text/html"); 
        PrintWriter pw = response.getWriter(); 

        //  <jaasLoginContextEntry id="JaasClient" name="JaasClient" loginModuleRef="krb5LoginModule" />
        //<!-- OpenJ9 loginModule config -->
        //<jaasLoginModule id="krb5LoginModule" className="com.sun.security.auth.module.Krb5LoginModule" controlFlag="REQUIRED" libraryRef="loginLib">
        //<options credsType="both" useKeyTab="true" keyTab="/etc/krb5.keytab" principal="dbuser" doNotPrompt="true"/>
        //</jaasLoginModule>
        /*try {
            LoginContext jaasClient = new LoginContext("JaasClient",null,null,DB2Krb5Configuration.getConfiguration());
            
        } catch (LoginException e) {
            pw.println("<h2>Login Exception</h2>");
        }

        Security.setProperty("login.configuration.provider", "com.example.DB2Krb5Configuration");
        DB2Krb5Configuration config = new DB2Krb5Configuration();
        Configuration.setConfiguration(config);
*/

        pw.println("<h2>Example Servlet</h2>"); 
        pw.println("getAuthType: " + request.getAuthType());
        pw.println("getRemoteUser: " + request.getRemoteUser());
        pw.println("getUserPrincipal: " + request.getUserPrincipal());
/*
        pw.println("<br/>Attempting non-kerberos connection<br/>");

        try (Connection con = noKrb5.getConnection(); Statement stmt = con.createStatement();) {
            try {
                stmt.execute("DROP TABLE krb5test");
            } catch (SQLException x) {
                if (!("42704".equals(x.getSQLState()) || "S0005".equals(x.getSQLState())))
                    throw x;
            }
            stmt.execute("CREATE TABLE krb5test (ID SMALLINT NOT NULL PRIMARY KEY, STRVAL NVARCHAR(40))");
            stmt.close();
            pw.println("<br/>Create Table Successful<br/>");
        } catch (SQLException e) {
            pw.println("<br/>No Kerberos Datasource failed:<br/>");
            e.printStackTrace(pw);
        }

        
*/
        /*
        try {
            Connection con2 = ds.getConnection();
            Connection con3 = ds.getConnection();
            Connection con4 = ds.getConnection();
            Thread.sleep(10_000);
        } catch (Exception e) {
            e.printStackTrace(pw);
        }
*/

        pw.println("<br/><br/>Attempting kerberos connection<br/>");
        //try (Connection con = ds.getConnection(); Statement stmt = con.createStatement();) {
        try (Connection con = ds.getConnection(); Statement stmt = con.createStatement();) {
            try {
                stmt.execute("DROP TABLE krb5test");
            } catch (SQLException x) {
                if (!"42704".equals(x.getSQLState()))
                    throw x;
            }
            stmt.execute("CREATE TABLE krb5test (ID SMALLINT NOT NULL PRIMARY KEY, STRVAL NVARCHAR(40))");
            stmt.close();
            pw.println("<br/>Create Table Successful<br/>");
        } catch (SQLException e) {
            e.printStackTrace(pw);
        }

        pw.println("<br/><br/>Attempting XA Recovery <br/>");

        try {
            StringBufferWrapper output = new StringBufferWrapper();

            clearTable(ds);
            Connection[] cons = new Connection[3];
            tran.begin();
            try {
                // Use unsharable connections, so that they all get their own XA resources
                cons[0] = ds.getConnection();
                cons[1] = ds.getConnection();
                cons[2] = ds.getConnection();

                String dbProductName = cons[0].getMetaData().getDatabaseProductName().toUpperCase();
                output.appendNewLine("Product Name is " + dbProductName);

                // Verify isolation-level="TRANSACTION_READ_COMMITTED" from ibm-web-ext.xml
                int isolation = cons[0].getTransactionIsolation();
                if (isolation != Connection.TRANSACTION_READ_COMMITTED)
                    throw new Exception("The isolation-level of the resource-ref is not honored, instead: " + isolation);

                PreparedStatement pstmt;
                pstmt = cons[0].prepareStatement("insert into cities values (?, ?, ?)");
                pstmt.setString(1, "Edina");
                pstmt.setInt(2, 47941);
                pstmt.setString(3, "Hennepin");
                pstmt.executeUpdate();
                pstmt.close();

                pstmt = cons[1].prepareStatement("insert into cities values (?, ?, ?)");
                pstmt.setString(1, "St. Louis Park");
                pstmt.setInt(2, 45250);
                pstmt.setString(3, "Hennepin");
                pstmt.executeUpdate();
                pstmt.close();

                pstmt = cons[2].prepareStatement("insert into cities values (?, ?, ?)");
                pstmt.setString(1, "Moorhead");
                pstmt.setInt(2, 38065);
                pstmt.setString(3, "Clay");
                pstmt.executeUpdate();
                pstmt.close();

                output.appendNewLine("Intentionally causing in-doubt transaction");
                TestXAResource.assignSuccessLimit(1, cons);
                try {
                    tran.commit();
                    throw new Exception("Commit should not have succeeded because the test infrastructure is supposed to cause an in-doubt transaction.");
                } catch (HeuristicMixedException x) {
                    TestXAResource.removeSuccessLimit(cons);
                    output.appendNewLine("Caught expected HeuristicMixedException: " + x.getMessage());
                }
            } catch (Throwable x) {
                TestXAResource.removeSuccessLimit(cons);
                try {
                    tran.rollback();
                } catch (Throwable t) {
                }
                throw x;
            } finally {
                for (Connection con : cons)
                    if (con != null)
                        try {
                            con.close();
                        } catch (Throwable x) {
                        }
            }

            // At this point, the transaction is in-doubt.
            // We won't be able to access the data until the transaction manager recovers
            // the transaction and resolves it.
            //
            // A connection configured with TRANSACTION_SERIALIZABLE is necessary in
            // order to allow the recovery to kick in before using the connection.

            output.appendNewLine("attempting to access data (only possible after recovery)");
            Connection con = ds.getConnection();

            int isolation = con.getTransactionIsolation();
            if (isolation != Connection.TRANSACTION_SERIALIZABLE)
                throw new Exception("The isolation-level of the resource-ref is not honored, instead: " + isolation);
            try {
                ResultSet result;
                PreparedStatement pstmt = con.prepareStatement("select name, population, county from cities where name = ?");

                /*
                * Poll for results once a second for 5 seconds.
                * Most databases will have XA recovery done by this point
                *
                */
                List<String> cities = new ArrayList<>();
                for (int count = 0; cities.size() < 3 && count < 5; Thread.sleep(1000)) {
                    if (!cities.contains("Edina")) {
                        pstmt.setString(1, "Edina");
                        result = pstmt.executeQuery();
                        if (result.next())
                            cities.add(0, "Edina");
                    }

                    if (!cities.contains("St. Louis Park")) {
                        pstmt.setString(1, "St. Louis Park");
                        result = pstmt.executeQuery();
                        if (result.next())
                            cities.add(1, "St. Louis Park");
                    }

                    if (!cities.contains("Moorhead")) {
                        pstmt.setString(1, "Moorhead");
                        result = pstmt.executeQuery();
                        if (result.next())
                            cities.add(2, "Moorhead");
                    }
                    count++;
                    output.appendNewLine("Attempt " + count + " to retrieve recovered XA data. Current status: " + cities);
                }

                if (cities.size() < 3)
                    throw new Exception("Missing entry in database. Results: " + cities);
                else
                    output.appendNewLine(SUCCESS);
            } finally {
                con.close();
            }

            pw.print(output.buffer.toString());
        } catch (Exception e) {
            
            pw.println(e.getMessage());
            e.printStackTrace(pw);
        }

    
   }

   /**
     * clears table of all data to ensure fresh start for this test.
     *
     * @param datasource the data source to clear the table for
     */
    public void clearTable(DataSource datasource) throws Exception {
        try (Connection con = datasource.getConnection(); Statement stmt = con.createStatement()) {
            try {
                stmt.executeUpdate("DROP TABLE cities");

            } catch (SQLException x) {
                if (!"42704".equals(x.getSQLState()))
                    throw x;
            }
            stmt.execute("create table cities (name varchar(50) not null primary key, population int, county varchar(30))");
        }

        // End the current LTC and get a new one, so that test methods start from the correct place
        tran.begin();
        tran.commit();
    }

    //Nested class to wrap a string buffer to append with a line separator for readability of output
    public class StringBufferWrapper {
        private StringBuffer buffer;

        public StringBufferWrapper() {
            buffer = new StringBuffer();
        }

        public void appendNewLine(String str) {
            buffer.append(str + System.lineSeparator());
        }

        public void append(String str) {
            buffer.append(str);
        }

        @Override
        public String toString() {
            return buffer.toString();
        }
    }
} 