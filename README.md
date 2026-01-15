# Server
For auto-reload: `python -m brijsim.server`
Without auto-reload: `uv run serve`

# Scrap

Nodes: 0 is the reference node. Other nodes are increasing integers.

Resistor:       Rname N+ N- Value
Capacitor:      Cname N+ N- Value
Inductor:       Lname N+ N- Value
Voltage source: Vname N+ N- DCValue
Current source: Iname N+ N- DCValue

# Todo

[ ] In the electrical simulation, simply stamp components as they're added. Don't bother trying to look up interconnections later.
