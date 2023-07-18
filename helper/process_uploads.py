import os
import pandas as pd


def process_csv(file, id, info):
    dataframe = pd.read_csv(file.file)
    print(dataframe)
    path = os.path.join(os.curdir, "data", "logs", "{}.csv".format(id))
    dataframe.to_csv(path, encoding='utf-8', index=False)


async def process_xes(file, id):
    contents = await file.read()
    file_content = contents.decode('UTF-8')

    path = os.path.join(os.curdir, "data", "logs", "{}.xes".format(id))
    print(path)
    with open(path, "w+") as file:
        file.write(file_content)
        file.close()
