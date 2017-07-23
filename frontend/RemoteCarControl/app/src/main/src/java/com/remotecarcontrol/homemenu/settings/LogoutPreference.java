package com.remotecarcontrol.homemenu.settings;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Application;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.preference.DialogPreference;
import android.preference.ListPreference;
import android.preference.Preference;
import android.util.AttributeSet;

import com.remotecarcontrol.remotecarcontrol.LoginActivity;
import com.remotecarcontrol.remotecarcontrol.MainActivity;
import com.remotecarcontrol.remotecarcontrol.SQLiteHandler;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

import java.util.HashSet;

public class LogoutPreference extends DialogPreference {

    public LogoutPreference(Context context, AttributeSet attrs) {
        super(context, attrs);

    }


    @Override
    protected void onPrepareDialogBuilder(AlertDialog.Builder builder) {
        super.onPrepareDialogBuilder(builder);    //To change body of overridden methods use File | Settings | File Templates.
        builder.setTitle("Are you sure you want to logout?");
        builder.setPositiveButton("Logout", new LogoutClickListener());
        builder.setNegativeButton("Cancel", null);
    }

    class LogoutClickListener implements DialogInterface.OnClickListener {

        @Override
        public void onClick(DialogInterface dialogInterface, int i) {
            SessionManager session = new SessionManager(getContext().getApplicationContext());
            session.putCars(new HashSet<String>());
            session.setLogin(false);

            SQLiteHandler db = new SQLiteHandler(getContext().getApplicationContext());
            db.deleteUsers();

            Intent intent = new Intent(getContext().getApplicationContext(), LoginActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
            getContext().getApplicationContext().startActivity(intent);
        }
    }
}
