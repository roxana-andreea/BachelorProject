package com.remotecarcontrol.homemenu;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.remotecarcontrol.R;
import com.remotecarcontrol.homemenu.vss_api.VSSRequestAuth;
import com.remotecarcontrol.remotecarcontrol.Configuration;
import com.remotecarcontrol.remotecarcontrol.Controller;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Timer;
import java.util.TimerTask;

public class StatusActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_status);

        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {


                SessionManager manager = new SessionManager(getApplicationContext());
                String id_device = manager.getString(Configuration.selected_car_key);

                for (final String outer_pid : Configuration.PARAMS_ALL) {

                    Response.Listener<String> respL = new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            Log.d("StatusRefreshResponse", response);

                            try {
                                JSONObject jObj = new JSONObject(response);
                                JSONArray items = jObj.getJSONArray("_items");
                                if (items.length() > 0) {
                                    JSONObject item = items.getJSONObject(0);
                                    String pid = item.getString("pid");
                                    String value = item.getString("value");

                                    int tv_id = mapPidToTextViewId(pid);

                                    TextView textView = (TextView) findViewById(tv_id);
                                    textView.setText(value + Configuration.PARAMS_APPEND.get(pid));
                                } else {
                                    int tv_id = mapPidToTextViewId(outer_pid);

                                    TextView textView = (TextView) findViewById(tv_id);
                                    textView.setText("-");
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        private int mapPidToTextViewId(String pid) {
                            if (pid.equals(Configuration.PARAM_TEMP_PID)) {
                                return R.id.textview_temp;
                            } else if (pid.equals(Configuration.PARAM_FUEL_PID)) {
                                return R.id.textview_fuel;
                            } else if (pid.equals(Configuration.PARAM_SPEED_PID)) {
                                return R.id.textview_speed;
                            } else {
                                return R.id.textview_lock;
                            }
                        }
                    };


                    String myURL = Configuration.URL_INPUTS + "?where={\"pid\":\"" + outer_pid +
                            "\",\"id_device\":\"" + id_device + "\"}&sort=-_created&max_results=1";
                    Log.d("StatusActivityRefresh", "URL: " + myURL);

                    VSSRequestAuth strReq = new VSSRequestAuth(Request.Method.GET,
                            myURL, respL,
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            });
                    Controller.getInstance().addToRequestQueue(strReq, "StatusActivityRefresh");
                }
            }
        }, 0, 5000);
    }
}
