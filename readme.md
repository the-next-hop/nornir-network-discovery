# nornir-network-discovery

Companion code for the **Nornir Network Discovery** series on [The Next Hop](https://the-next-hop.co.uk).

A practical, no-fluff series that takes you from querying your first network device with Nornir, all the way to pushing config using lists, files and Jinja2 templates.

---

## Series

| Part | Article | Script |
|------|---------|--------|
| 1 | [Getting Started — Your First Nornir Script](https://the-next-hop.co.uk/part-1-from-zero-to-querying-network-devices/) | `part1_main.py` |
| 2 | [Parsing Real Data with TextFSM](https://the-next-hop.co.uk/part-2-parsing-real-data-with-textfsm/) | `part2_main.py` |
| 3 | [From Parsed Data to Reports and Backups with Nornir](https://the-next-hop.co.uk/part-3-from-parsed-data-to-reports-and-backups-with-nornir/) | `part3_main.py` |
| 4 | [Pushing Config with Nornir](https://the-next-hop.co.uk/part-4-pushing-config-with-nornir-three-ways-to-make-changes/) | `part4_main.py` |

---

## Lab Environment

- **Platform:** GNS3
- **Devices:** Cisco 7200 (IOS 15.2)
- **Hostnames:** Odin, Thor, Loki
- **Protocol:** SSH

---

## Requirements

```bash
python3 -m venv venv && source venv/bin/activate  # Mac/Linux
python -m venv venv && venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## Project Structure

```
nornir-network-discovery/
├── config/
├── inventory/
│   ├── hosts.yaml
│   ├── groups.yaml
│   └── defaults.yaml
├── output/
├── templates/
│   ├── show_int_desc.textfsm
│   ├── show_version.textfsm
│   ├── show_cdp_neighbors_detail.textfsm
│   ├── ntp.txt
│   └── snmp.j2
├── .gitignore
├── config.yaml
├── requirements.txt
├── part1_main.py
├── part2_main.py
├── part3_main.py
└── part4_main.py
```

---

## Inventory Setup

Before running any script, update the inventory files with your own device details.

`inventory/hosts.yaml` — define your devices:
```yaml
odin:
  hostname: 192.168.1.21
  groups:
    - cisco_ios
  data:
    snmp:
      - location: "Your site location"
        community: "your_community_string"
```

`inventory/groups.yaml` — define platform per group:
```yaml
cisco_ios:
  platform: cisco_ios
```

`inventory/defaults.yaml` — set your credentials:
```yaml
username: your_username
password: your_password
```

---

## Usage

Each script is self-contained and can be run independently:

```bash
python part1_main.py
python part2_main.py
python part3_main.py
python part4_main.py
```

---

## Disclaimer

This repo is built for lab and learning purposes. Do not use against production devices without understanding what each script does first.
