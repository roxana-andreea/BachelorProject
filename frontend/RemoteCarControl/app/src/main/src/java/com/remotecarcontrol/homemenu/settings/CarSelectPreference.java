package java.com.remotecarcontrol.homemenu.settings;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.CountDownTimer;
import android.preference.ListPreference;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.remotecarcontrol.R;
import com.remotecarcontrol.remotecarcontrol.SessionManager;

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
        Set<String> cars = manager.getCars();
        CharSequence[] cars_s = cars.toArray(new CharSequence[cars.size()]);
        select_preference.setEntries(cars_s);
        select_preference.setEntryValues(cars_s);

        super.onPrepareDialogBuilder(builder);    //To change body of overridden methods use File | Settings | File Templates.

        builder.setPositiveButton("Add Car", new AddNewCarListener());

        Log.d("CarSelectPreference", "DialogBuilderCalled " + cars_s + " " + cars_s.length);
    }


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
                // TODO launch server request in order to verify credentials.

                new CountDownTimer(1500, 1500) {

                    @Override
                    public void onTick(long l) {


                    }

                    @Override
                    public void onFinish() {

                        Toast.makeText(getContext().getApplicationContext(), "Car Added", Toast.LENGTH_SHORT).show();

                        TextView car_id_tv = (TextView) dialog.findViewById(R.id.car_id_textview);

                        SessionManager manager = new SessionManager(getContext().getApplicationContext());
                        Set<String> set = manager.getCars();

                        set.add(car_id_tv.getText().toString());
                        manager.putCars(set);

                        dialog.dismiss();

                    }
                }.start();
            }
        }
    }
}
