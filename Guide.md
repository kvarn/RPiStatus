RPiStatus Guide
===============

This guide will help you to install a good way to edit and run python and show you how to visualize your python code in a web browser.

My code that you can download from github show things like the up time, temperature, memory, storage status and current network usage. I will try with this step by step instructions guide you and help you understand the basics.

I will assume that you run Rasbian (http://www.raspbian.org), having a network running on your RaspberryPi. I will not explain adafruit WebIDE or Flask in details but you can always read more in the provided links. I will just give you a jump start to it.

1. As always start with make an update
sudo apt-get update

2. Install Adafruit WebIDE (can be skipped if you prefer other way of edit python/code)
Install Adafruit WebIDE by following the guide at http://learn.adafruit.com/webide/overview

3. To show a webpage and get information to it using Python I use Flask. (I have tried web2py but I found it to slow for RaspberryPi)
sudo apt-get install python-pip  
sudo pip install Flask
More information about Flask http://flask.pocoo.org/ and dont forget to look at their quick start guide http://flask.pocoo.org/docs/quickstart

4. We will start creating the basic structure
4.1. Go to adafruit WebIDE http://raspberrypi.local
4.2. Create a folder "Status"
4.3. Create a file "status.py"

5. Some basic code
5.1 Open "status.py"
5.2 Type in the following code

<code>
from flask import Flask<br>

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":
      app.debug = True
      app.run('0.0.0.0')
</code>

5.3. Run and use your web browser and go to http://raspberrypi.local:5000
5.4. You should now see "hello world" in the web browser.
What we have done is to start Flask and make it return "hello world" using Python.

6. Show a web page instead of just text
6.1. Create a folder named "templates" in the "Status" folder (where you have the python file "status.py")
6.2. Create a new file named "status.html"
6.3. Add the following code to "status.html"
<code>
<html>
<head><title>RaspberryPi Status</title></head>
<body>
     Hello World
</body>
</html>
</code>
6.4. Go back to "status.py", change the first row to: 
from flask import Flask, render_template
We have now added support to render html-templates!
6.5. Now change row 7 so it will return our html-template instead:
return render_template("status.html");
6.6. Now if you refresh your web browser window it should say "Hello World" instead! 
(If Flask couldent restart your app you just go down to the terminal and press Ctrl+C and press Run again)

7. Show information from Python on a web page
7.1. We want to show information from our Python script and a good way to do that is to use AJAX and jQuery.
Add the following code after </head> and before <body> in "status.html" (found in templates folder):
<code>
<script type=text/javascript
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type=text/javascript>
  var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
</script>
<script type=text/javascript>
      $.getJSON($SCRIPT_ROOT + '/_get_hello_world', {
        }, function(data) {
          $('#mySpan').text(data.text);
      });
</script>
</code>
7.2. To show what we fetch replace the text "Hello World" in the body to the following code:
<code>
<span id="mySpan"></span>
</code>
7.3. Go back to "status.py" and we will create a route "_get_hello_world" that the web page will fetch information from.
To do that just add the following lines after the existing @app.route:
<code>
@app_route("/_get_hello_world")
def get_hello_world():
     return jsonify(text="Python say: Hello world")
</code>
7.4 We now use JSON to send back our result to the web page so we alson need to import jsonify.
Add jsonify to the first row so it should now be: from flask import Flask, render_template, jsonify
7.5 Now refresh your web browser and it should now say "Python say: Hello World"!
Note how we in the web page request data.text and in python returns json text, we create the JSON variable in python and then use it in the web page.

8. Show the CPU temperature for your Raspberry Pi
8.1. To be able to show the temperature we need to have a Python route to call.
Go to "status.py" and change your "_get_hello_world" to the following:
<code>
@app.route('/_get_temperature')
def get_temperature():
      temperature_c = str(get_temperature())
      return jsonify(temperature=temperature_c)
</code>
8.2. To get the temperature add the following function:
<code>
def get_temperature():
    "Returns the temperature in degrees C"
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
        return float(s.split('=')[1][:-3])
    except:
        return 0
</code>
8.3. We have now started to use subprocess so we need to import it.
After the first import on row 1 add the following on row 2:
import subprocess
8.4. To make a call to our new route and function go to "status.html" and change "_get_hello_world" to the following:
<code>
      $.getJSON($SCRIPT_ROOT + '/_get_temperature', {
        }, function(data) {
          $('#mySpan').text(data.temperature);
      });
</code>
8.5. Refresh the page in the web browser and you should now see the CPU temperature on your Raspberry Pi
We now have the platform to add whatever we want to the page that we can make from python on the Raspberry Pi. We can change things using buttons, light up some LEDs and so on! 

9. The last steps... 
9.1. I dont like to refresh a page to get new data so why dont we let some javascript do it for us? 
Add the following line to create a timer so the text will be updated every 3 second:
<code>
setInterval(function() { updateTimer(); }, 3000);
</code>
Now we need to create a function "updateTimer" and add our code there to get the temperature.
So just add the following before the existing code for getting the temperature:
<code>
function updateTimer() {
</code>
and add the following after the code:
<code>
}
</code>
9.2. To prevent the information to get cached I use Javascript
Inside of our function "updateTimer" we take the current time and add it to our call in python, your script section should look like:
<code>
<script type=text/javascript>
  setInterval(function() { updateTimer(); }, 3000);

  function updateTimer()
  {
      var d=new Date();
      unique = "?"+d.valueOf(); 
 
      $.getJSON($SCRIPT_ROOT + '/_get_temperature'+unique, {
        }, function(data) {
          $('#mySpan').text(data.temperature);
      });
  }
</script>
</code>
9.3. Refresh the web browser and you can now see the temperature getting updated every 3 second. You can also see the fetch in the terminal window in Adafruit WebIDE, note that the end of the request now have for example "?1380400784580" so it will be unique.

10. Now you know how to set up a environment how to code Python in a good editor and how to view your python operations in a web browser. If you want to add more information visit the following link
http://cagewebdev.com/index.php/raspberry-pi-showing-some-system-info-with-a-python-script/

You can download my code at github https://github.com/kvarn/piStatus where I have added more system information and separated the web code from the system info code. 

