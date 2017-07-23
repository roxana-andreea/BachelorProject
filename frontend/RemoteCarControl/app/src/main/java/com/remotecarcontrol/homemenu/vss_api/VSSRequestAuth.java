package com.remotecarcontrol.homemenu.vss_api;

import android.util.Base64;

import com.android.volley.AuthFailureError;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;
import com.remotecarcontrol.remotecarcontrol.Configuration;
import com.remotecarcontrol.remotecarcontrol.Controller;

import java.util.HashMap;
import java.util.Map;

public class VSSRequestAuth extends StringRequest {

    public VSSRequestAuth(int method, String url, Response.Listener<String> listener,
                         Response.ErrorListener errorListener) {
        super(method, url, listener, errorListener);
        setShouldCache(false);
    }

    public Map<String, String> getHeaders() throws AuthFailureError {
        Map<String, String> headers = new HashMap<>();
        Controller cont = Controller.getInstance();
        String credentials = cont.getValue(Configuration.username_key) + ":" + cont.getValue(Configuration.username_password);
        String auth = "Basic "
                + Base64.encodeToString(credentials.getBytes(), Base64.NO_WRAP);
        // headers.put("Content-Type", "application/json");
        headers.put("Authorization", auth);
        return headers;
    }

}
