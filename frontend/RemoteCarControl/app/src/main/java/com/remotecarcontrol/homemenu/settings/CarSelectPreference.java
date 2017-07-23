package com.remotecarcontrol.homemenu.settings;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.CountDownTimer;
import android.preference.ListPreference;
import android.preference.Preference;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.remotecarcontrol.R;
import com.remotecarcontrol.homemenu.vss_api.VSSRequestAuth;
import com.remotecarcontrol.remotecarcontrol.Configuration;
import com.remotecarcontrol.remotecarcontrol.Controller;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class CarSelectPreference extends ListPreference {

    ListPreference select_preference;

    public CarSelectPreference(Context context, AttributeSet attrs) {
        super(context, attrs);

        select_preference = this;

    }

    @Override
    protected void onPrepareDialogBuilder(AlertDialog.Builder builder) {
        SessionManager manager = new SessionManager(getContext().getApplicationContext());
        Set<String> car_hashes = manager.getCars();

        ArrayList<String> car_names = new ArrayList<String>();
        ArrayList<String> car_ids = new ArrayList<String>();

        for (String car_hash : car_hashes) {
            String[] car_split = car_hash.split("\\+");
            car_ids.add(car_split[0] + "+" + car_split[2]);
            car_names.add(car_split[1]);
        }

        CharSequence[] cars_s_ids = car_ids.toArray(new CharSequence[car_ids.size()]);
        CharSequence[] cars_s_names = car_names.toArray(new CharSequence[car_names.size()]);
        select_preference.setEntries(cars_s_names);
        select_preference.setEntryValues(cars_s_ids);



        super.onPrepareDialogBuilder(builder);    //To change body of overridden methods use File | Settings | File Templates.

        //builder.setPositiveButton("Add Car", new AddNewCarListener());

        Log.d("CarSelectPreference", "DialogBuilderCalled " + car_hashes + " " + car_hashes.size());
        setOnPreferenceChangeListener(new OnPreferenceChangeListener() {
            @Override
            public boolean onPreferenceChange(Preference preference, Object o) {
                //Log.d("CAR_PREF", preference.getKey() + "--" + preference.get);

                //Log.d("CAR_PREF", o.toString());
                String[] strs = o.toString().split("\\+");
                String car_id = strs[0], car_phone = strs[1];

                SessionManager manager = new SessionManager(getContext().getApplicationContext());
                manager.putString(Configuration.selected_car_key, car_id);
                manager.putString(Configuration.selected_car_phone, car_phone);

                Controller cont = Controller.getInstance();
                cont.putKeyValue(Configuration.selected_car_key, car_id);

                return true;
            }
        });


    }



    /* Obsolete */
    class AddNewCarListener implements DialogInterface.OnClickListener {
        ProgressBar progressBar;
        AlertDialog dialog;

        @Override
        public void onClick(DialogInterface dialogInterface, int i) {
            AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
            builder.setTitle("Add Car");

            LayoutInflater inflater = LayoutInflater.from(getContext());
            View new_view = inflater.inflate(R.layout.dialog_new_car, null);
            builder.setView(new_view);
            progressBar = (ProgressBar) new_view.findViewById(R.id.progressBar);

            builder.setNegativeButton("Cancel", null);
            builder.setPositiveButton("OK", null);

            dialog = builder.create();

            dialog.show();
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(new VerifyCarCredentialsListener());

        }


        class VerifyCarCredentialsListener implements View.OnClickListener {

            @Override
            public void onClick(View view) {
                progressBar.setVisibility(View.VISIBLE);

                String car_id = ((EditText) dialog.findViewById(R.id.car_id_edittext)).getText().toString();

                String myURL = Configuration.URL_DEVICE + car_id;

                VSSRequestAuth strReq = new VSSRequestAuth(Request.Method.GET,
                        myURL, new Response.Listener<String>() {

                    @Override
                    public void onResponse(String response) {
                        Log.d("AddCarResponse", response);

                        /*boolean ok = true;
                        try {
                            JSONObject jObj = new JSONObject(response);
                            if (!jObj.has("id")) {
                                ok = false;
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        if (ok) {*/
                            Toast.makeText(getContext().getApplicationContext(), "Car Added", Toast.LENGTH_SHORT).show();

                            EditText car_id_et = (EditText) dialog.findViewById(R.id.car_id_edittext);
                            EditText car_name_et = (EditText) dialog.findViewById(R.id.car_name_edittext);

                            String car_hash = car_id_et.getText().toString() + "+" + car_name_et.getText().toString();

                            SessionManager manager = new SessionManager(getContext().getApplicationContext());
                            Set<String> set = manager.getCars();

                            set.add(car_hash);
                            manager.putCars(set);

                            if (Controller.getInstance().getValue(Configuration.selected_car_key) == null) {
                                Controller.getInstance().putKeyValue(Configuration.selected_car_key, car_id_et.getText().toString());
                            }
                            if (manager.getString(Configuration.selected_car_key) == null) {
                                manager.putString(Configuration.selected_car_key, car_id_et.getText().toString());
                            }

                            dialog.dismiss();
                        /*} else {
                            Toast.makeText(getContext().getApplicationContext(), "Invalid Car Id", Toast.LENGTH_SHORT).show();
                        }*/
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        progressBar.setVisibility(View.GONE);
                        Toast.makeText(getContext().getApplicationContext(), "Invalid Car ID.", Toast.LENGTH_SHORT).show();
                    }
                });
                Controller.getInstance().addToRequestQueue(strReq, "check_device");


                /*new CountDownTimer(1500, 1500) {

                    @Override
                    public void onTick(long l) {


                    }

                    @Override
                    public void onFinish() {

                        Toast.makeText(getContext().getApplicationContext(), "Car Added", Toast.LENGTH_SHORT).show();

                        EditText car_id_et = (EditText) dialog.findViewById(R.id.car_id_edittext);
                        EditText car_name_et = (EditText) dialog.findViewById(R.id.car_name_edittext);

                        String car_hash = car_id_et.getText().toString() + "+" + car_name_et.getText().toString();

                        SessionManager manager = new SessionManager(getContext().getApplicationContext());
                        Set<String> set = manager.getCars();

                        set.add(car_hash);
                        manager.putCars(set);

                        dialog.dismiss();

                    }
                }.start();
                */
            }
        }
    }
}
