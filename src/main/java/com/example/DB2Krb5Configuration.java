package com.example;

import java.util.HashMap;
import java.util.Map;

import javax.security.auth.login.AppConfigurationEntry;
import javax.security.auth.login.Configuration;

public class DB2Krb5Configuration extends Configuration {

	@Override
	public AppConfigurationEntry[] getAppConfigurationEntry(String name) {
		System.out.println("--------- MJS Configuration ----------- : " + name);

		Map<String, String> options = new HashMap<String, String>();
		options.put("credsType","both");
		options.put("useKeyTab", "true");
		options.put("keyTab","/dne/krb5.keytab");
		options.put("principal","dbuser");
		options.put("doNotPrompt","true");
		AppConfigurationEntry[] configArray = {
			new AppConfigurationEntry("com.sun.security.auth.module.Krb5LoginModule", AppConfigurationEntry.LoginModuleControlFlag.REQUIRED,options)
		};

		if (name.equals("JaasClient") || name.equals("com.sun.security.jgss.krb5.initiate")) {
			return configArray;
		}
		return null;

	}

}