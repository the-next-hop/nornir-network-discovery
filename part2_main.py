import json
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
templates_dir = "./templates"

def get_interface_desc(nr):
    get_interface = nr.run(
        task=netmiko_send_command,
        command_string="show interface description",
        use_textfsm=True,
        textfsm_template=f"{templates_dir}/show_int_desc.textfsm"
    )

    list_of_results = []

    for host_name, multi_result in get_interface.items():
        result = multi_result[0].result
        list_of_results.append({host_name: result})

    return(list_of_results)

def get_device_uptime_and_version(nr):
 
    get_version = nr.run(
            task=netmiko_send_command,
            command_string="show version",
            use_textfsm=True,
            textfsm_template=f"{templates_dir}/show_version.textfsm"
        )

    list_of_results = []

    for host_name, multi_result in get_version.items():
        result = multi_result[0].result
        software_image = result[0].get("software_image")
        version = result[0].get("version")
        uptime = result[0].get("uptime")
        list_of_results.append({host_name: {"version": version, "uptime": uptime, "software_image": software_image}})
    
    return(list_of_results)

def get_cdp_neighbors(nr):
    get_cdp = nr.run(
            task=netmiko_send_command,
            command_string="show cdp neighbors detail",
            use_textfsm=True,
            textfsm_template=f"{templates_dir}/show_cdp_neigbhors_detail.textfsm"
        )

    list_of_results = []

    for host_name, multi_result in get_cdp.items():
        result = multi_result[0].result
        for host in result:
            local_interface = host.get("local_interface")
            remote_interface = host.get("remote_interface")
            neighbor_hostname = host.get("neighbor_name")
            neighbor_ip = host.get("mgmt_address")
            list_of_results.append({host_name: {"local_interface": local_interface, "remote_interface": remote_interface, "neighbor_hostname": neighbor_hostname, "neighbor_ip": neighbor_ip}})

    return(list_of_results)

def get_device_info():
    print("*" * 20)
    print(json.dumps(get_interface_desc(nr), indent=2))
    print("*" * 20)
    print(json.dumps(get_device_uptime_and_version(nr), indent=2))
    print("*" * 20)
    print(json.dumps(get_cdp_neighbors(nr), indent=2))

if __name__ == "__main__":
    get_device_info()