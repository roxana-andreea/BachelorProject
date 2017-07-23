package com.remotecarcontrol.remotecarcontrol;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request.Method;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.remotecarcontrol.R;
import com.remotecarcontrol.homemenu.MenuActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends Activity {

    private static final String TAG = RegisterActivity.class.getSimpleName();
    private Button btnLogin;
    private Button btnLinkToRegister;
    private EditText inputEmail;
    private EditText inputPassword;
    private ProgressDialog pDialog;
    private SessionManager session;
    private SQLiteHandler db;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        inputEmail = (EditText) findViewById(R.id.email);
        inputPassword = (EditText) findViewById(R.id.password);
        btnLogin = (Button) findViewById(R.id.btnLogin);
        btnLinkToRegister = (Button) findViewById(R.id.btnLinkToRegisterScreen);

        // Progress dialog
        pDialog = new ProgressDialog(this);
        pDialog.setCancelable(false);

        // SQLite database handler
        //db = new SQLiteHandler(getApplicationContext());

        // Session manager
        session = new SessionManager(getApplicationContext());

        // Check if user is already logged in or not
        if (session.isLoggedIn()) {
            // User is already logged in. Take him to main activity
            Log.d(TAG, "User already logged in. Take him to main activity.");
            Controller cont = Controller.getInstance();
            cont.putKeyValue(Configuration.username_key, session.getString(Configuration.username_key));
            cont.putKeyValue(Configuration.username_password, session.getString(Configuration.username_password));
            cont.putKeyValue(Configuration.selected_car_key, session.getString(Configuration.selected_car_key));

            Intent intent = new Intent(LoginActivity.this, MenuActivity.class);
            startActivity(intent);
            finish();
        }

        // Login button Click Event
        btnLogin.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                String email = inputEmail.getText().toString().trim();
                String password = inputPassword.getText().toString().trim();

                // Check for empty data in the form
                if (!email.isEmpty() && !password.isEmpty()) {
                    // login user
                    checkLogin(email, password);
                } else {
                    // Prompt user to enter credentials
                    Toast.makeText(getApplicationContext(),
                            "Please enter the credentials!", Toast.LENGTH_LONG)
                            .show();
                }
            }

        });

        // Link to Register Screen
        btnLinkToRegister.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                Intent i = new Intent(getApplicationContext(),
                        RegisterActivity.class);
                startActivity(i);
                finish();
            }
        });

    }

    /**
     * function to verify login details in mysql db
     * */
    private void checkLogin(final String login, final String password) {
        // Tag used to cancel the request
        String tag_string_req = "req_login";

        pDialog.setMessage("Logging in ...");
        showDialog();

        String loginURL = Configuration.URL_LOGIN + login;

        StringRequest strReq = new StringRequest(Method.GET,
                loginURL, new Response.Listener<String>() {

            @Override
            public void onResponse(String response) {
                Log.d(TAG, "Login Response: " + response.toString());
                hideDialog();

                try {
                    JSONObject jObj = new JSONObject(response);

                        // user successfully logged in
                        // Create login session
                        session.setLogin(true);

                        // Now store the user in SQLite

                       /* String id = jObj.getString("id");

                        JSONObject user = jObj;
                        String name = user.getString("name");
                        String login = user.getString("login");
                        String created_at = user
                                .getString("_created");

                        // Inserting row in users table
                        db.addUser(name, login, id, created_at);*/
                        String pincode = jObj.getString("pincode");

                        Controller cont = Controller.getInstance();
                        cont.putKeyValue(Configuration.username_key, login);
                        cont.putKeyValue(Configuration.username_password, password);

                        session.putString(Configuration.username_key, login);
                        session.putString(Configuration.username_password, password);
                        session.putString(Configuration.user_pincode, pincode);

                        // Launch main activity
                        Intent intent = new Intent(LoginActivity.this,
                                MenuActivity.class);
                        startActivity(intent);
                        finish();
                } catch (JSONException e) {
                    // JSON error
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(), "Json error: " + e.getMessage(), Toast.LENGTH_LONG).show();
                }

            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e(TAG, "Login Error: " + error.getMessage());

                String message = "Error code: " + error.networkResponse.statusCode;

                if (error.networkResponse.statusCode == 422) {
                    message = "User already registered.";
                } else if (error.networkResponse.statusCode == 401) {
                    message = "Username or password invalid.";
                }

                Toast.makeText(getApplicationContext(),
                        message, Toast.LENGTH_LONG).show();
                hideDialog();
            }
        }) {

            /*
            @Override
            protected Map<String, String> getParams() {
                // Posting parameters to login url
                Map<String, String> params = new HashMap<String, String>();


                params.put("login", login);
                params.put("password", password);


                return params;
            }*/

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String> headers = new HashMap<>();
                String credentials = login + ":" + password;
                String auth = "Basic "
                        + Base64.encodeToString(credentials.getBytes(), Base64.NO_WRAP);
                // headers.put("Content-Type", "application/json");
                headers.put("Authorization", auth);
                return headers;
            }

        };

        // Adding request to request queue
        strReq.setShouldCache(false);
        Controller.getInstance().addToRequestQueue(strReq, tag_string_req);
    }

    private void showDialog() {
        if (!pDialog.isShowing())
            pDialog.show();
    }

    private void hideDialog() {
        if (pDialog.isShowing())
            pDialog.dismiss();
    }
}
