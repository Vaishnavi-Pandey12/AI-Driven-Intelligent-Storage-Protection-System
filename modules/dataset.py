import numpy as np
import pandas as pd

rows = 8000

data = pd.DataFrame({
    "disk_usage_percent": np.random.randint(10,100,rows),
    "temperature": np.random.randint(25,70,rows),
    "read_error_rate": np.random.randint(0,50,rows),
    "write_error_rate": np.random.randint(0,50,rows),
    "reallocated_sector_count": np.random.randint(0,200,rows),
    "pending_sector_count": np.random.randint(0,200,rows),
    "power_on_hours": np.random.randint(100,50000,rows)
})

data["label"] = (
    (data["read_error_rate"] +
     data["write_error_rate"] +
     data["pending_sector_count"]) > 120
).astype(int)

data.to_csv("storage_health_dataset.csv", index=False)
