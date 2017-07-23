package com.remotecarcontrol.remotecarcontrol;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.support.annotation.NonNull;
import android.util.Log;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

/**
 * Maintains session data across the app using SharedPreferences.
 * We store a boolean flag isLoggedin in shared preferences to check the login status
 */

public class SessionManager {
    // LogCat tag
    private static String TAG = SessionManager.class.getSimpleName();

    // Shared Preferences
    SharedPreferences pref;

    Editor editor;
    Context _context;

    // Shared pref mode
    int PRIVATE_MODE = 0;

    // Shared preferences file name

    private static final int PREF_VERSION = 1;

    private static final String PREF_NAME = "AndroidHiveLogin" + PREF_VERSION;

    private static final String KEY_IS_LOGGEDIN = "isLoggedIn";

    private static final String KEY_CAR_LIST = "carList";

    public SessionManager(Context context) {
        this._context = context;
        pref = _context.getSharedPreferences(PREF_NAME, PRIVATE_MODE);
        editor = pref.edit();
    }

    public void setLogin(boolean isLoggedIn) {

        editor.putBoolean(KEY_IS_LOGGEDIN, isLoggedIn);


        // commit changes
        editor.commit();

        Log.d(TAG, "User login session modified!");
    }

    public Set<String> getCars() {
        Set<String> set = pref.getStringSet(KEY_CAR_LIST, new HashSet<String>());
        return new HashSet<String>(set);
    }

    public void putCars(Set<String> cars) {
        editor.putStringSet(KEY_CAR_LIST, cars);
        editor.commit();
    }

    public boolean isLoggedIn(){
        return pref.getBoolean(KEY_IS_LOGGEDIN, false);
    }

    public void putString(String key, String value) {
        editor.putString(key, value);
        editor.commit();
    }

    public String getString(String key) {
        return pref.getString(key, null);
    }

    public void clear() {
        putCars(new HashSet<String>());
        setLogin(false);
        editor.remove(Configuration.selected_car_key);
        editor.remove(Configuration.username_key);
        editor.remove(Configuration.username_password);
        editor.commit();
    }
}
