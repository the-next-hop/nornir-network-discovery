from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
templates_dir = "./templates"


get_interface = nr.run(
    task=netmiko_send_command, 
    command_string="show interface description",
    use_textfsm=True,
    textfsm_template=f"{templates_dir}/show_int_desc.textfsm"

)

print_result(get_interface)
