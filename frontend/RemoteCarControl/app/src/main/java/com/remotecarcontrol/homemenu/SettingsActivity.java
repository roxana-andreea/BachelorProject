package com.remotecarcontrol.homemenu;

import android.app.Activity;
import android.os.Bundle;
import android.preference.PreferenceActivity;
import android.preference.PreferenceFragment;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.remotecarcontrol.R;
import com.remotecarcontrol.homemenu.vss_api.VSSRequestAuth;
import com.remotecarcontrol.remotecarcontrol.Controller;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashSet;

public class SettingsActivity extends PreferenceActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getFragmentManager().beginTransaction().replace(android.R.id.content, new MyPreferenceFragment()).commit();

        /*
        Spinner car_spinner = (Spinner) findViewById(R.id.spinner);

        String[] car_options = {"...", "Add new car"};

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                R.layout.spinner_item, car_options);


        car_spinner.setAdapter(adapter);*/

        String myURL = "http://vss.lupu.online:8080/devices/";

        VSSRequestAuth strReq = new VSSRequestAuth(Request.Method.GET,
                myURL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        HashSet<String> cars = new HashSet<>();
                        try {
                            JSONObject obj = new JSONObject(response);
                            JSONArray items = obj.getJSONArray("_items");
                            for (int i = 0; i < items.length(); i++) {
                                JSONObject item = items.getJSONObject(i);
                                cars.add(item.getString("id") + "+" + item.getString("name") +
                                        "+" + item.getString("phone"));
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        SessionManager manager = new SessionManager(getApplicationContext());
                        manager.putCars(cars);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                });
        Controller.getInstance().addToRequestQueue(strReq, "DeviceRefresh");

    }



    public static class MyPreferenceFragment extends PreferenceFragment
    {
        @Override
        public void onCreate(final Bundle savedInstanceState)
        {
            super.onCreate(savedInstanceState);
            addPreferencesFromResource(R.xml.preferences);


        }
    }

}
