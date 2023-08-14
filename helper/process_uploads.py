import os
import pandas as pd


def process_csv(file, id, path = "logs"):
    dataframe = pd.read_csv(file.file)
    path = os.path.join(os.curdir, "data", path, "{}.csv".format(id))
    dataframe.to_csv(path, encoding='utf-8', index=False)


async def process_xes(file, id, path = "logs"):
    contents = await file.read()
    file_content = contents.decode('UTF-8')

    path = os.path.join(os.curdir, "data", path, "{}.xes".format(id))
    with open(path, "w+") as file:
        file.write(file_content)
        file.close()
