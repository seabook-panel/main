from flask import Blueprint, after_this_request, render_template, request
import config
import function
from function.power import PowerEvent

from auth import auth
app = Blueprint('power', __name__)
appearance = config.get_config("appearance")


@app.route('/reboot')
@auth
def reboot():
    @after_this_request
    def reboot_run(response):
        function.power.power_control(PowerEvent.REBOOT)
        print("IP地址为"+request.remote_addr+"的管理员重启了服务器。")
        return response
    return render_template('power/reboot.html')

@app.route('/shutdown')
@auth
def shutdown():
    @after_this_request
    def shutdown_run(response):
        function.power.power_control(PowerEvent.SHUTDOWN)
        print("IP地址为"+request.remote_addr+"的管理员关闭了服务器。")
        return response
    return render_template('power/shutdown.html',appearance=appearance)
