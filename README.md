# CITS5506-IoT

Repository for the CITS5506-IoT Project

## Flask webserver

**The below commands are now all for the root directory not the webapp directory.**

Using flask as the webserver which is python web server. To install required packages open terminal in the root directory and run `pip install -r requirements.txt`, preferably in a python virtual environment if possible. Start the server by running `flask run` in the root directory.

The video streaming works, however if you change any files when running the server and the server reloads openCV will cause the server to crash. You can work around this by commenting out the `return Response(...` lines in webapp/**init**.py or by removing the line `FLASK_ENV=development` from .flaskenv.

## Audio

The two scripts are used for audio recording and streaming from a USB microphone.
Not sure how to stream the audio/voice thru internet yet

## sound_effect

It contains scripts to make a sound when the button (doorbell) is pressed using either a buzzer or speaker.

The speaker version works better than the buzzer.

The 2 scripts with camera in the name are combining sound with the already existed camera functons. However, not tested with the camera yet.

Later, other sound effect/ voice message to be added for open/lock the door and box.
