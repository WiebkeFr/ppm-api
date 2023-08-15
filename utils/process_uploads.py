import os
import pandas as pd

from utils.run_events import start_shell_script
from utils.subscriptions import add_subscription


def process_csv(file, id, path="logs"):
    dataframe = pd.read_csv(file.file)
    path = os.path.join(os.curdir, "data", path, "{}.csv".format(id))
    dataframe.to_csv(path, encoding='utf-8', index=False)


async def process_xes(file, id, path="logs"):
    contents = await file.read()
    file_content = contents.decode('UTF-8')

    path = os.path.join(os.curdir, "data", path, "{}.xes".format(id))
    with open(path, "w+") as file:
        file.write(file_content)
        file.close()


async def process_xml(file, id):
    print("process file")
    contents = await file.read()
    file_content = contents.decode('UTF-8')
    updated_xml = add_subscription(file_content, id)

    path = os.path.join(os.curdir, "data", "cpee", "{}.xml".format(id))
    with open(path, 'w') as file:
        file.write(updated_xml)
        file.close()
    start_shell_script(path)
