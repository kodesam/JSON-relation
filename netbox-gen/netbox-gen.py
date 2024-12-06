import yaml
from jinja2 import Environment, FileSystemLoader

# Load the YAML data
with open('server_hardware_data.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('server_hardware_template.j2')

# Render the template with data
output = template.render(data=data)

# Save the rendered output
with open('netbox_output.yaml', 'w') as output_file:
    output_file.write(output)

print("NetBox YAML output has been generated and saved as 'netbox_output.yaml'.")
