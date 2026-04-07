import csv
import json
import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
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

def get_interface_desc(nr):
    
    try:
        get_interface = nr.run(
            task=netmiko_send_command,
            command_string="show interface description",
            use_textfsm=True,
            textfsm_template=f"{templates_dir}/show_int_desc.textfsm"
        )

        headers = ["device_name", "interface", "status", "protocol", "description"]
            
        with open(f"{output_dir}/get_interface_desc.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for host_name, multi_result in get_interface.items():
                result = multi_result[0].result
                print(f"[{current_time}] Processing interface descriptions for device: {host_name}")

                for entry in result:
                    row = {
                        "device_name": host_name,
                        "interface": entry.get("interface"),
                        "status": entry.get("status"),
                        "protocol": entry.get("protocol"),
                        "description": entry.get("description")
                    }
                    writer.writerow(row)

    except Exception as e:
        print(f"[{current_time}] Error occurred while getting interface descriptions: {e}")

def get_device_uptime_and_version(nr):
 
    try:
        get_version = nr.run(
                task=netmiko_send_command,
                command_string="show version",
                use_textfsm=True,
                textfsm_template=f"{templates_dir}/show_version.textfsm"
            )
        
        if not get_version:
            print(f"[{current_time}] No version data retrieved for devices.")
            return

        headers = ["device_name", "software_image", "version", "uptime"]
            
        with open(f"{output_dir}/get_device_uptime_and_version.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for host_name, multi_result in get_version.items():
                print(f"[{current_time}] Processing version and uptime information for device: {host_name}")
                result = multi_result[0].result

                for entry in result:
                    row = {
                        "device_name": host_name,
                        "software_image": entry.get("software_image"),
                        "version": entry.get("version"),
                        "uptime": entry.get("uptime"),
                    }
                    writer.writerow(row)

    except Exception as e:
        print(f"[{current_time}] Error occurred while getting device uptime and version: {e}")
            

def get_cdp_neighbors(nr):
    try:
        get_cdp = nr.run(
                task=netmiko_send_command,
                command_string="show cdp neighbors detail",
                use_textfsm=True,
                textfsm_template=f"{templates_dir}/show_cdp_neigbhors_detail.textfsm"
            )
        if not get_cdp:
            print(f"[{current_time}] No CDP neighbor data retrieved for devices.")
            return

        headers = ["device_name", "local_interface", "remote_interface", "neighbor_hostname", "neighbor_ip"]
            
        with open(f"{output_dir}/get_cdp_neighbors.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for host_name, multi_result in get_cdp.items():
                print(f"[{current_time}] Processing CDP neighbor data for device: {host_name}")
                result = multi_result[0].result

                for entry in result:
                    row = {
                        "device_name": host_name,
                        "local_interface": entry.get("local_interface"),
                        "remote_interface": entry.get("remote_interface"),
                        "neighbor_hostname": entry.get("neighbor_name"),
                        "neighbor_ip": entry.get("mgmt_address")
                    }
                    writer.writerow(row)

    except Exception as e:
        print(f"[{current_time}]Error occurred while getting CDP neighbors: {e}")   

def save_config_to_file(nr):

    try:
        get_config = nr.run(
                task=netmiko_send_command,
                command_string="show running-config",
                enable=True
            )
        
        if not get_config:
            print(f"[{current_time}] No configuration data retrieved for devices.")
            return

        for host_name, multi_result in get_config.items():
            print(f"[{current_time}] Saving running configuration for device: {host_name}")
            result = multi_result[0].result
            with open(f"{config_dir}/{host_name}_{current_time}_running_config.txt", "w") as f:
                f.write(result)

    except Exception as e:
        print(f"[{current_time}] Error occurred while saving device configurations: {e}")    

def get_all():
    for task in [get_interface_desc, get_device_uptime_and_version, get_cdp_neighbors, save_config_to_file]:
        try:
            if task(nr) is not None:
                print(f"[{current_time}] Data for task {task.__name__} has been started successfully.")

            print(f"[{current_time}] Completed task: {task.__name__}")

        except Exception as e:
            print(f"[{current_time}] Error occurred while executing task {task.__name__}: {e}")

if __name__ == "__main__":
    get_all()
    