package com.remotecarcontrol.homemenu.settings;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.preference.DialogPreference;
import android.util.AttributeSet;

import com.remotecarcontrol.remotecarcontrol.Controller;
import com.remotecarcontrol.remotecarcontrol.LoginActivity;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

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
            session.clear();
            Controller.getInstance().clear();

            /*SQLiteHandler db = new SQLiteHandler(getContext().getApplicationContext());
            db.deleteUsers();*/

            Intent intent = new Intent(getContext().getApplicationContext(), LoginActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
            getContext().getApplicationContext().startActivity(intent);
        }
    }
}
