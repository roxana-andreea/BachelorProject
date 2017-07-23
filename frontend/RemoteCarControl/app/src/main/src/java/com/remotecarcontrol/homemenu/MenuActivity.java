package com.remotecarcontrol.homemenu;

import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.ViewConfiguration;
import android.widget.TabHost;
import android.widget.TabHost.TabSpec;

import com.remotecarcontrol.R;

import java.lang.reflect.Field;

public class MenuActivity extends TabActivity {


    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);


        TabHost tabHost = getTabHost();

        // Tab for Dashboard
        TabSpec dashboardspec = tabHost.newTabSpec("Dashboard");
        // setting Title and Icon for the Tab
        dashboardspec.setIndicator(null, getResources().getDrawable(R.drawable.icon_dashboard_tab));
        Intent dashboardIntent = new Intent(this, DashboardActivity.class);
        dashboardspec.setContent(dashboardIntent);

        // Tab for Alerts
        TabSpec alertsspec = tabHost.newTabSpec("Alerts");
        alertsspec.setIndicator(null, getResources().getDrawable(R.drawable.icon_alerts));
        Intent alertsIntent = new Intent(this, AlertsActivity.class);
        alertsspec.setContent(alertsIntent);

        // Comment

        // Tab for GPS
        TabSpec gpsspec = tabHost.newTabSpec("GPS");
        gpsspec.setIndicator(null, getResources().getDrawable(R.drawable.icon_gps));
        Intent gpsIntent = new Intent(this, GPSActivity.class);
        gpsspec.setContent(gpsIntent);

        // Tab for Settings
        TabSpec settingsspec = tabHost.newTabSpec("Settings");
        settingsspec.setIndicator(null, getResources().getDrawable(R.drawable.icon_settings));
        Intent settingsIntent = new Intent(this, SettingsActivity.class);
        settingsspec.setContent(settingsIntent);

        // Tab for Status
        TabSpec statusspec = tabHost.newTabSpec("Status");
        statusspec.setIndicator(null, getResources().getDrawable(R.drawable.icon_status));
        Intent statusIntent = new Intent(this, StatusActivity.class);
        statusspec.setContent(statusIntent);


        // Adding all TabSpec to TabHost
        tabHost.addTab(dashboardspec);
        tabHost.addTab(gpsspec);
        tabHost.addTab(alertsspec);
        tabHost.addTab(statusspec);
        tabHost.addTab(settingsspec);


        try {
            ViewConfiguration config = ViewConfiguration.get(this);
            Field menuKeyField = ViewConfiguration.class.getDeclaredField("sHasPermanentMenuKey");
            if (menuKeyField != null) {
                menuKeyField.setAccessible(true);
                menuKeyField.setBoolean(config, false);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}


    

