import sysinfo
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
      return render_template('status.html')
      

@app.route('/_get_up_time')
def get_up_time():
      up_time = str(sysinfo.get_up_stats()[0])
      return jsonify(uptime=up_time)

@app.route('/_get_memory')
def get_ram():
      free_ram = str(sysinfo.get_ram()[1])
      total_ram = str(sysinfo.get_ram()[0])
      return jsonify(free=free_ram, total=total_ram)

@app.route('/_get_hdd')
def get_hdd():
      free_hdd = str(sysinfo.disk_usage("/")[0])
      total_hdd = str(sysinfo.disk_usage("/")[1])
      return jsonify(free=free_hdd, total=total_hdd)
      
@app.route('/_get_temperature')
def get_temperature():
      temperature_c = str(sysinfo.get_temperature())
      return jsonify(temperature=temperature_c)

@app.route('/_get_cpu_speed')
def get_cpu_speed():
      speed = str(sysinfo.get_cpu_speed())
      return jsonify(cpu_speed=speed)
      
@app.route('/_get_curr_networkspeed')
def get_curr_networkspeed():
      network_speed = sysinfo.get_network_speed();
      n_sending = str(network_speed[0])
      n_reciving =  str(network_speed[1])
      return jsonify(sending=n_sending, reciving=n_reciving)     

if __name__ == "__main__":
      #app.debug = True
      app.run('0.0.0.0')
      
