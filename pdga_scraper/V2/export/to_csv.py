import pandas as pd
from pathlib import Path
from dataclasses import fields

def csv_writer(datasets):

    output_dir = Path("pdga_scraper/V2/TestOutputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    for field in fields(datasets):
        name = field.name
        data = getattr(datasets, name)

        df = pd.DataFrame.from_dict(data, orient="index")
        df.to_csv(output_dir / f"{name}.csv")