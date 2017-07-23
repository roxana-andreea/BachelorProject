package com.remotecarcontrol.homemenu;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.telephony.SmsManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.remotecarcontrol.R;
import com.remotecarcontrol.remotecarcontrol.Configuration;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

public class DashboardActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        //ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.SEND_SMS},1);
        final Activity thisActivity = this;


        int [] buttons_ids = {R.id.button_lock, R.id.button_unlock, R.id.button_start_engine, R.id.button_stop_engine,
                R.id.button_windows_up, R.id.button_windows_down, R.id.button_trunk, R.id.button_panic};
        String[] commands = {"LOCK CAR", "UNLOCK CAR", "START ENGINE", "STOP ENGINE", "UP WINDOWS", "DOWN WINDOWS", "OPEN TRUNK", "START ALARM"};

        for (int i = 0; i < buttons_ids.length; i++) {
            int id = buttons_ids[i];
            final String command = commands[i];
            Button button = (Button)findViewById(id);

            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    int permissionCheck = ContextCompat.checkSelfPermission(thisActivity,
                            Manifest.permission.SEND_SMS);
                    if (permissionCheck != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(thisActivity,
                                new String[]{Manifest.permission.SEND_SMS},
                                1);
                    } else {

                        SessionManager manager = new SessionManager(getApplicationContext());
                        String device_phone_number = manager.getString(Configuration.selected_car_phone);
                        String pincode = manager.getString(Configuration.user_pincode);

                        if (device_phone_number == null) {
                            device_phone_number = "+40746215807";
                        }
                        if (pincode == null) {
                            pincode = "1234";
                        }
                        SmsManager smsManager = SmsManager.getDefault();

                        smsManager.sendTextMessage(device_phone_number, null, command + " " + pincode, null, null);


                    }
                }
            });
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {

        /*if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            return;
        }*/
        Log.d("RequestPermission", "Permission request result");
    }

}
