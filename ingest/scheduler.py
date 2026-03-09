import time
import weather_fetcher
import aqi_fetcher
import tomtom_fetcher
import merge_datasets

INTERVAL = 3600  # seconds (300 = 5 minutes)

while True:
    print("Starting data ingestion cycle...")

    try:
        weather_fetcher.main()
        aqi_fetcher.main()
        tomtom_fetcher.main()
        merge_datasets.main()

        print("Ingestion cycle completed")

    except Exception as e:
        print("Error in pipeline:", e)

    print(f"Waiting {INTERVAL} seconds...\n")
    time.sleep(INTERVAL)
