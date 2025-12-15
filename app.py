from flask import Flask, render_template, request
from netmiko import ConnectHandler
from jinja2 import Template

app = Flask(__name__)

# Simple Jinja2 template for access VLANs on SW1/SW2
VLAN_TEMPLATE = """
vlan {{ vlan_id }}
 name {{ vlan_name }}
!
{% for intf in interfaces %}
interface {{ intf }}
 description {{ site_name }} {{ vlan_name }}
 switchport mode access
 switchport access vlan {{ vlan_id }}
 spanning-tree portfast
!
{% endfor %}
"""

SWITCHES = [
    {"device_type": "cisco_ios", "host": "192.168.1.62", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "192.168.1.63", "username": "cisco", "password": "cisco"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        site_name = request.form.get("site_name")
        mgmt_subnet = request.form.get("mgmt_subnet")

        # VLAN list typed as: 10:STAFF:fa0/1,fa0/2;20:GUEST:fa0/3,fa0/4
        raw_vlan = request.form.get("vlans", "")
        vlan_items = [v for v in raw_vlan.split(";") if v.strip()]

        changes = []
        tmpl = Template(VLAN_TEMPLATE)

        for vlan_def in vlan_items:
            vlan_id, vlan_name, intfs = vlan_def.split(":")
            interfaces = [i.strip() for i in intfs.split(",") if i.strip()]
            cfg_text = tmpl.render(
                vlan_id=vlan_id.strip(),
                vlan_name=vlan_name.strip(),
                interfaces=interfaces,
                site_name=site_name.strip(),
            )
            cfg_lines = [l for l in cfg_text.splitlines() if l.strip()]
            changes.append((vlan_id, vlan_name, interfaces, cfg_lines))

        results = []
        for sw in SWITCHES:
            with ConnectHandler(**sw) as conn:
                # optional: configure a loopback with mgmt IP per site
                base_cfg = [
                    f"hostname {site_name}-{conn.host}",
                    "ip domain-name netautomation.com",
                ]
                conn.send_config_set(base_cfg)

                for vlan_id, vlan_name, interfaces, cfg_lines in changes:
                    out = conn.send_config_set(cfg_lines)
                    results.append(
                        {
                            "device": conn.host,
                            "vlan_id": vlan_id,
                            "vlan_name": vlan_name,
                            "interfaces": interfaces,
                            "output": out,
                        }
                    )

        return render_template("result.html",
                               site_name=site_name,
                               mgmt_subnet=mgmt_subnet,
                               results=results)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
