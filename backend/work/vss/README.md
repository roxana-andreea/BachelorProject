# VSS API Documentation 
## Commands
### Run program
> python3 manage.py runserver –t 0.0.0.0 –p 8080
> python3 manage.py create_tables
> python3 manage.py drop_tables
### Flask
> flask.url_for('static', filename='path/to/filename')
### SQL Alchemy
    session.add(location)
    #Commit the sample records
    session.commit()

    # Create.
    session.add(appt)
    session.commit()

    # Update.
    appt.title = 'Your Appointment'
    session.commit()

    # Delete.
    session.delete(appt)
    session.commit()

