package com.remotecarcontrol.remotecarcontrol;

import java.util.HashMap;
import java.util.Map;

/**
 * Login and register urls.
 */
public class Configuration {
    // Server user login url
    public static String URL_LOGIN = "http://vss.lupu.online:8080/users/";

    // Server user register url
    public static String URL_REGISTER = "http://vss.lupu.online:8080/users/";
    public static String URL_DEVICE = "http://vss.lupu.online:8080/devices/";
    public static String URL_INPUTS = "http://vss.lupu.online:8080/inputs/";

    public static String username_key = "username";
    public static String username_password = "password";
    public static String selected_car_key = "selected_car";
    public static String selected_car_phone = "selected_car_phone";
    public static String user_pincode = "user_pincode";


    public static String PARAM_TEMP_PID = "0105";
    public static String PARAM_SPEED_PID = "010D";
    public static String PARAM_FUEL_PID = "33";
    public static String PARAM_LOCK_PID = "44";

    public static String[] PARAMS_ALL = {PARAM_TEMP_PID, PARAM_SPEED_PID, PARAM_FUEL_PID, PARAM_LOCK_PID};

    public static Map<String, String> PARAMS_APPEND;

    static {
        PARAMS_APPEND = new HashMap<String, String>() {{
            put(PARAM_TEMP_PID, " C");
            put(PARAM_SPEED_PID, " km/h");
            put(PARAM_FUEL_PID, "%");
            put(PARAM_LOCK_PID, "");
        }};
    }

    public static String TEMP_LIMIT_KEY = "temp_limit";
    public static String TEMP_LIMIT_ENABLE_KEY="temp_limit_enabled";
    public static String SPEED_LIMIT_KEY = "speed_limit";
    public static String SPEED_LIMIT_ENABLE_KEY="speed_limit_enabled";
    public static String FUEL_LIMIT_KEY = "fuel_limit";
    public static String FUEL_LIMIT_ENABLE_KEY="FUEL_limit_enabled";

};
