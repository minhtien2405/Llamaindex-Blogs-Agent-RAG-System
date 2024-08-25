#!/bin/bash

# Run the data crawler
python3 data_crawler.py

# Run the setup data script
python3 setup_data.py

# Run the Chainlit application
chainlit run app.py
