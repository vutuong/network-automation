#Install python3 lib

pip install --upgrade pip setuptools

pip install junos-eznc

pip install prettytable

pip install tabulate

pip install streamlit

pip install streamlit-code-editor

pip install streamlit-ace

#Run the app

streamlit run app_extract_tableview_offline.py

#Run with docker
docker build -t tableview_xml_extract .
docker run -d -p 8501:8501 tableview_xml_extract
