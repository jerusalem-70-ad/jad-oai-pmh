import datetime
import os
import shutil
import requests
from acdh_tei_pyutils.tei import TeiReader

import jinja2

# initial set up
template_folder = os.path.join("oai-pmh", "templates")
templateLoader = jinja2.FileSystemLoader(searchpath=template_folder)
templateEnv = jinja2.Environment(loader=templateLoader)
project_data = {
    "project_title": "Medieval Reception of the Roman Conquest of Jerusalem",
    "base_url": "https://jerusalem-70-ad.github.io/jad-astro"
}
oai_folder = os.path.join("html", "oai-pmh")
shutil.rmtree(oai_folder, ignore_errors=True)
os.makedirs(oai_folder, exist_ok=True)

print("serializing Identify.xml")
template = templateEnv.get_template("Identify.j2")
output_path = os.path.join(oai_folder, "Identify.xml")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(
        template.render(
            {
                "project_data": project_data,
                "current_date_time": datetime.datetime.now(datetime.UTC).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
            }
        )
    )
done_doc = TeiReader(output_path)
done_doc.tree_to_file(output_path)
print(f"saving {output_path}")

print("serializing ListRecords.xml")
data = requests.get("https://raw.githubusercontent.com/jerusalem-70-ad/jad-baserow-dump/refs/heads/main/json_dumps/works.json").json()  # noqa: E501
template = templateEnv.get_template("ListRecords.j2")
output_path = os.path.join(oai_folder, "ListRecords.xml")
object_list = []
for key, value in data.items():
    item = {
        "id": f"tei/works/{value['jad_id']}.xml",
        "title": f"{value['name']}",
        "datestamp": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"),
    }
    object_list.append(item)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(
        template.render(
            {
                "project_data": project_data,
                "object_list": object_list,
                "current_date_time": datetime.datetime.now(datetime.UTC).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
            }
        )
    )
done_doc = TeiReader(output_path)
done_doc.tree_to_file(output_path)
print(f"saving {output_path}")

print("serializing ListIdentifiers.xml")
template = templateEnv.get_template("ListIdentifiers.j2")
output_path = os.path.join(oai_folder, "ListIdentifiers.xml")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(
        template.render(
            {
                "project_data": project_data,
                "object_list": object_list,
                "current_date_time": datetime.datetime.now(datetime.UTC).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
            }
        )
    )
done_doc = TeiReader(output_path)
done_doc.tree_to_file(output_path)
print(f"saving {output_path}")

index_html_path = os.path.join("oai-pmh", "index.html")
shutil.copy(index_html_path, oai_folder)
