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
@ServletSecurity(value = @HttpConstraint(rolesAllowed = { "Manager"},
  transportGuarantee = ServletSecurity.TransportGuarantee.NONE))
public class ExampleServlet extends HttpServlet { 

    @Resource(name = "jdbc/db2ds")
    DataSource ds;

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
        //pw.println("getUserPrincipal().getName(): " + request.getUserPrincipal() == null ? "User Principal is null" : request.getUserPrincipal().getName());

        try (Connection con = ds.getConnection(); Statement stmt = con.createStatement();) {
            stmt.execute("CREATE TABLE MYTABLE (ID SMALLINT NOT NULL PRIMARY KEY, STRVAL NVARCHAR(40))");
            stmt.close();
            pw.println("Create Table Successful\n");
        } catch (SQLException e) {
            e.printStackTrace(pw);
        }

    
   }
} 