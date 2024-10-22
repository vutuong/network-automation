import streamlit as st
from streamlit_ace import st_ace
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml
from tabulate import tabulate
from lxml import etree

# Title of the Streamlit app
st.title("Input your tableview")

# Set the language mode for syntax highlighting (e.g., python, json, yaml, etc.)
language_mode = "yaml"  # You can change this to other languages like 'json', 'yaml', 'html', etc.

# Set the default text for the editor
default_tableview = """
---
juniper_ldp_detailTable:
  args:
    detail: true
  item: //ldp-neighbor-information/ldp-neighbor
  key: interface-name
  rpc: get-ldp-neighbor-information
  view: _juniper_ldp_detail_view
_juniper_ldp_detail_view:
  fields:
    ldp_neighbor_address: ldp-neighbor-address
    interface_name: interface-name
    ldp_label_space_id: ldp-label-space-id
    ldp_remaining_time: ldp-remaining-time
"""

# Display a VS Code-like text area for input using st_ace (Ace Editor)
tableview_input = st_ace(
    value=default_tableview,
    language=language_mode,
    theme="monokai",  # You can change themes: monokai, github, solarized_dark, etc.
    height=400,  # Adjust the height of the editor
    auto_update=True  # Enable auto-update as you type
)

# # Display the extracted text/code
# st.subheader("Extracted Text:")
# st.code(tableview_input, language=language_mode)


# Title of the Streamlit app
st.title("Input your xml data")

# Set the language mode for syntax highlighting (e.g., python, json, yaml, etc.)
language_mode = "xml"  # You can change this to other languages like 'json', 'yaml', 'html', etc.

# Set the default text for the editor
default_xml = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/20.4R0/junos">
    <output>
        logical-system: default
    </output>
    <ldp-neighbor-information xmlns="http://xml.juniper.net/junos/20.4R0/junos-routing">
        <ldp-neighbor>
            <ldp-neighbor-address>172.20.82.1</ldp-neighbor-address>
            <interface-name>lo0.0</interface-name>
            <ldp-label-space-id>0.0.0.0:0</ldp-label-space-id>
            <ldp-remaining-time>0</ldp-remaining-time>
        </ldp-neighbor>
    </ldp-neighbor-information>
    <cli>
        <banner></banner>
    </cli>                              
</rpc-reply>
"""

# Display a VS Code-like text area for input using st_ace (Ace Editor)
xml_input = st_ace(
    value=default_xml,
    language=language_mode,
    theme="monokai",  # You can change themes: monokai, github, solarized_dark, etc.
    height=400,  # Adjust the height of the editor
    auto_update=True  # Enable auto-update as you type
)

# # Display the extracted text/code
# st.subheader("Extracted Text:")
# st.code(xml_input, language=language_mode)

def display_ldp_details_table(ldp_view_file, xml_file):
    """
    Function to display LDP details in a table format with dynamic table extraction.
    
    Parameters:
    ldp_view_file (str): Path to the YAML file defining the TableView.
    xml_file (str): Path to the XML file containing the LDP data.
    """
    # Load the YAML TableView definition
    with open(ldp_view_file, 'r') as TableView:
        tableview_namespace = yaml.safe_load(TableView)
    
    # Extract the table name (the first key in the YAML file)
    table_name = list(tableview_namespace.keys())[0]
    
    # Load the Table and View using FactoryLoader
    factory_namespace = FactoryLoader().load(tableview_namespace)
    # defined_tablelist = {}
    # defined_tablelist.update(factory_namespace)
    
    # Print the dynamically extracted table name (Optional)
    print(f"Extracted table name: {table_name}")
    
    # Load the table data using the extracted tableview definition
    data = factory_namespace[table_name](path=xml_file)
    data.get()
    
    # Prepare the data for tabular display
    table_data = []
    for i in data:
        row = [
            i.ldp_neighbor_address,
            i.interface_name,
            i.ldp_label_space_id,
            i.ldp_remaining_time
        ]
        table_data.append(row)
    
    # Define the headers for the table
    headers = ["LDP Neighbor Address", "Interface Name", "LDP Label Space ID", "LDP Remaining Time"]
    
    # Print the data as a formatted table using tabulate
    # print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    # Create a formatted table using tabulate
    table_str = tabulate(table_data, headers=headers, tablefmt="pretty")
    
    return table_str


# Function to get user input and write it to a file
def write_input_to_file(file_path,user_input):
    
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the input to the file
        file.write(user_input)
    
    print(f"Your input has been written to {file_path}")

# print(tableview_input)
write_input_to_file("tableview.yml",tableview_input)
# print(xml_input)
write_input_to_file("input_data.xml",xml_input)
# Button to process the input data
if st.button("Display LDP Details Table"):
    if tableview_input and xml_input:
        # Call the function to display LDP details in table format
        display_ldp_details_table("tableview.yml", "input_data.xml")
        table_output = display_ldp_details_table("tableview.yml", "input_data.xml")
        # Display the table in Streamlit
        st.subheader("LDP Details Table:")
        st.text(table_output)  # or use st.markdown(table_output) if you want markdown formatting
    else:
        st.error("Both YAML TableView and XML content are required.")

#streamlit run app.py
