import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from datetime import datetime

nr = InitNornir(config_file="config.yaml")
templates_dir = "./templates"
output_dir = "./output"
config_dir = "./config"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)  
os.makedirs(templates_dir, exist_ok=True)

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def send_commands_from_list(nr):
    
    name_servers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
    commands = [f"ip name-server {ip}" for ip in name_servers]
    
    try:
        send_commands = nr.run(
            task=netmiko_send_config,
            config_commands=commands
        )

        print_result(send_commands)

    except Exception as e:
        print(f"[{current_time}] Error occurred while attemping to add the name-servers: {e}")

def send_config_from_file(nr):
    
    try:
        send_config = nr.run(
            task=netmiko_send_config,
            config_file=f"{templates_dir}/ntp.txt"
        )

        print_result(send_config)

    except Exception as e:
        print(f"[{current_time}] Error occurred while attemping to add the config from file: {e}")

def send_config_from_template(task):
    try:
        rendered_config = task.run(
            task=template_file,
            template="snmp.j2",
            path=templates_dir,
            **task.host
        )
        
        task.run(
            task=netmiko_send_config,
            config_commands=rendered_config.result.splitlines()
        )
        
    except Exception as e:
        print(f"[{current_time}] Error occurred while attemping to add the config from template: {e}")

if __name__ == "__main__":
    # send_commands_from_list(nr)
    # send_config_from_file(nr)
    # send_config_from_template(nr)
    render_config = nr.run(task=send_config_from_template)
    print_result(render_config)

    