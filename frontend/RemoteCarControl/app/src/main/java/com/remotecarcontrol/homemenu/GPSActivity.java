package com.remotecarcontrol.homemenu;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.google.android.gms.maps.*;
import com.google.android.gms.maps.model.*;

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

public class GPSActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private Timer gpsTimer;
    LatLng current_position = new LatLng(44.423913, 26.157956);
    private boolean shouldMoveCamera = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.gps_map);
        mapFragment.getMapAsync(this);


    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */

    public void addMarkerAtCurrentPosition(boolean moveCamera) {
        mMap.clear();
        mMap.addMarker(new MarkerOptions().position(current_position).title("Your car").icon(
                BitmapDescriptorFactory.fromResource(R.drawable.selected_settings)
        ).flat(true));
        if (moveCamera) {
            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(current_position, 18.0f));
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        Log.d("GPSActivity", "Map Ready");
        mMap = googleMap;
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.e("GPSActivity", "Insufficient map permissions");
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        mMap.setMyLocationEnabled(true);
        mMap.getUiSettings().setZoomControlsEnabled(true);
        mMap.getUiSettings().setCompassEnabled(true);



        //addMarkerAtCurrentPosition();


        Button car_pos = (Button) findViewById(R.id.googlemaps_car_location);

        car_pos.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(current_position, 18.0f));
            }
        });

        gpsTimer = new Timer();
        gpsTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                //Log.d("TimerTask", "execute");
                SessionManager manager = new SessionManager(getApplicationContext());
                String id_device = manager.getString(Configuration.selected_car_key);
                String gps_pid = 99 + "";
                if (id_device == null || id_device.isEmpty()) {
                    return;
                }
                String myURL = Configuration.URL_INPUTS + "?where={\"pid\":\"" + gps_pid +
                        "\",\"id_device\":\"" + id_device + "\"}&sort=-_created&max_results=1";

                VSSRequestAuth strReq = new VSSRequestAuth(Request.Method.GET,
                        myURL,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                //Log.d("NewPosition", response);

                                JSONObject jObj = null;
                                try {
                                    jObj = new JSONObject(response);
                                    JSONArray items = jObj.getJSONArray("_items");
                                    if (items.length() > 0) {
                                        JSONObject item = items.getJSONObject(0);
                                        String pid = item.getString("pid");
                                        String value = item.getString("value");
                                        String latm = value.split(",")[0];
                                        String longm = value.split(",")[2];

                                        double latDeg = Double.parseDouble(latm.substring(0, 2));
                                        double latMin = Double.parseDouble(latm.substring(2));

                                        double longDeg = Double.parseDouble(longm.substring(0, 3));
                                        double longMin = Double.parseDouble(longm.substring(3));

                                        current_position = new LatLng(latDeg + latMin / 60, longDeg + longMin / 60);
                                        addMarkerAtCurrentPosition(shouldMoveCamera);
                                        shouldMoveCamera = false;

                                    } else {
                                        mMap.clear();
                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }


                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {

                            }
                });
                Controller.getInstance().addToRequestQueue(strReq, "GPSActivityRefresh");
            }
        }, 0, 10000);


    }
}
