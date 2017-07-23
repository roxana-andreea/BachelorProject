package com.remotecarcontrol.homemenu;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.remotecarcontrol.R;
import com.remotecarcontrol.homemenu.vss_api.VSSRequestAuth;
import com.remotecarcontrol.remotecarcontrol.Configuration;
import com.remotecarcontrol.remotecarcontrol.Controller;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Timer;
import java.util.TimerTask;

public class AlertsActivity extends Activity {


    Timer alert_timer = new Timer();
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alerts);

        alert_timer.schedule(new TimerTask() {
            @Override
            public void run() {
                String[] keys_enabled = {Configuration.TEMP_LIMIT_ENABLE_KEY, Configuration.SPEED_LIMIT_ENABLE_KEY, Configuration.FUEL_LIMIT_ENABLE_KEY};
                String[] keys = {Configuration.TEMP_LIMIT_KEY, Configuration.SPEED_LIMIT_KEY, Configuration.FUEL_LIMIT_KEY};
                String[] pids = {Configuration.PARAM_TEMP_PID, Configuration.PARAM_SPEED_PID, Configuration.PARAM_FUEL_PID};
                int[] comparison_sign = {1, 1, -1};

                for (int i = 0; i < keys.length; i++) {
                    String key_enabled = keys_enabled[i], key = keys[i], pid = pids[i];
                    final int sign = comparison_sign[i];
                    final TextView tv = getTextViewByPid(pid);
                    if (isPreferenceEnabled(key_enabled)) {
                        final double limit = Double.parseDouble(getLimit(key));

                        String id_device = Controller.getInstance().getValue(Configuration.selected_car_key);
                        String myURL = Configuration.URL_INPUTS + "?where={\"pid\":\"" + pid +
                                "\",\"id_device\":\"" + id_device + "\"}&sort=-_created&max_results=1";

                        final VSSRequestAuth strReq = new VSSRequestAuth(Request.Method.GET,
                                myURL,
                                new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String response) {
                                        JSONObject jObj = null;
                                        try {
                                            jObj = new JSONObject(response);
                                            JSONArray items = jObj.getJSONArray("_items");
                                            if (items.length() > 0) {
                                                JSONObject item = items.getJSONObject(0);
                                                String pid = item.getString("pid");
                                                String value = item.getString("value");
                                                double double_value = Double.parseDouble(value);


                                                if (double_value * sign >= limit * sign) {
                                                    Log.d("AlertsActivity", String.format("Limit %f Value %f", limit, double_value));
                                                    //alerts.add(getAlertMessage(pid, limit, double_value));

                                                    tv.setText(getAlertMessage(pid, limit, double_value));
                                                    setVisibility((LinearLayout) tv.getParent(), View.VISIBLE);
                                                } else {
                                                    setVisibility((LinearLayout) tv.getParent(), View.GONE);
                                                }
                                            } else {
                                                setVisibility((LinearLayout) tv.getParent(), View.GONE);
                                            }
                                        }  catch (JSONException e) {
                                            e.printStackTrace();
                                        }
                                    }
                                },
                                new Response.ErrorListener() {
                                    @Override
                                    public void onErrorResponse(VolleyError error) {

                                    }
                                });
                        Controller.getInstance().addToRequestQueue(strReq, "AlertActivityRefresh");
                    } else {
                        setVisibility((LinearLayout) tv.getParent(), View.GONE);
                    }
                }
            }
        }, 0, 5000);
    }

    public void setVisibility(final View view, final int visibility) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                view.setVisibility(visibility);
            }
        });
    }

    private TextView getTextViewByPid(String pid) {
        if (pid.equals(Configuration.PARAM_TEMP_PID)) {
            return (TextView) findViewById(R.id.alert_temp_tv);
        } else if (pid.equals(Configuration.PARAM_SPEED_PID)) {
            return (TextView) findViewById(R.id.alert_speed_tv);
        } else {
            return (TextView) findViewById(R.id.alert_fuel_tv);
        }
    }

    public String getAlertMessage(String pid, double limit, double value) {
        if (pid.equals(Configuration.PARAM_TEMP_PID)) {
            return String.format("Temperature limit of %.0f was exceeded: %.0f", limit, value);
        } else if (pid.equals(Configuration.PARAM_SPEED_PID)) {
            return String.format("Speed limit of %.0f km/h was exceeded: %.0f km/h", limit, value);
        }
        else if (pid.equals(Configuration.PARAM_FUEL_PID)) {
            return String.format("Fuel limit of %.0f%% was exceeded: %.0f", limit, value);
        }
        return "Unknown alert pid";
    }

    public boolean isPreferenceEnabled(String key_enabled) {
        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        return preferences.getBoolean(key_enabled, false);
    }

    public String getLimit(String key) {
        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        return preferences.getString(key, "999");
    }

}