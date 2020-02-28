package com.example;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

import javax.annotation.Resource;
import javax.servlet.ServletException;
import javax.servlet.annotation.HttpConstraint;
import javax.servlet.annotation.ServletSecurity;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;

@WebServlet("/example")
@ServletSecurity(value = @HttpConstraint(rolesAllowed = {
        "Manager" }, transportGuarantee = ServletSecurity.TransportGuarantee.NONE))
public class ExampleServlet extends HttpServlet {

    @Resource(name = "jdbc/db2ds")
    DataSource ds;

    @Resource(name = "jdbc/nokrb5")
    DataSource noKrb5;

    private static final long serialVersionUID = 1L;

    @Override
    protected void doGet(HttpServletRequest request,
                        HttpServletResponse response)
                        throws ServletException, IOException {

        response.setContentType("text/html"); 
        PrintWriter pw = response.getWriter(); 
        pw.println("<h2>Example Servlet</h2>"); 
        pw.println("getAuthType: " + request.getAuthType());
        pw.println("getRemoteUser: " + request.getRemoteUser());
        pw.println("getUserPrincipal: " + request.getUserPrincipal());

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

        pw.println("<br/><br/>Attempting kerberos connection<br/>");
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

    
   }
} 