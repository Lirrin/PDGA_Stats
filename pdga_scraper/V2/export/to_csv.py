import pandas as pd
from pathlib import Path

def csv_writer(datasets): #for troubleshooting

    output_dir = Path("TestOutputs")
    output_dir.mkdir(exist_ok=True)
    for name, data in datasets.items():
        df = pd.DataFrame.from_dict(data, orient="index")
        df.to_csv(f"TestOutputs/{name}.csv")