# Disruptions and Transfers Network

This repository contains the code and data for analyzing disruptions and transfers in a network. The project includes data collection, preprocessing, network creation, and visualization using Neo4j and PyVis.

## Project Structure

The project is organized into two main directories: `Disruptions Network` and `Transfers Network`. Each directory includes data files, code for processing the data, and scripts for importing and visualizing the data using Neo4j.

### 1. Disruptions Network

This directory contains all files related to the temporal network of train disruptions

- **Data/**
  - `disruptions.csv` - Raw data file containing disruption events.
  - `disruptions.pkl` - Pickle file for efficient data loading.

- **Visualizations/**
  - `Disruptions - Neo4j Property Graph.html` - HTML file showing visualizations of the disruptions network using Neo4j and PyVis.

- **Disruptions - Neo4j Data Import.py**
  - Python script for importing disruptions data into a Neo4j database.

- **Disruptions - Neo4j Visualizer.py**
  - Python script for creating visualizations of the disruptions network using Neo4j.

- **Disruptions - Notebook.ipynb**
  - Jupyter Notebook for web scraping, preprocessing the data, defining the temporal network, and calculating summary statistics and metrics.

- **Disruptions - Streamlit App.py**
  - Streamlit application for interactive visualization of the disruptions network.

- **Disruptions - Streamlit NS Logo.png**
  - Logo used in the Streamlit app.

### 2. Transfers Network

This directory contains all files related the temporal network of transfers in the Premier League.

- **Data/**
  - `transfers.csv` - Raw data file containing transfer events.
  - `transfers.pkl` - Pickle file for efficient data loading.
  - `transfer.pkl` - Pickle file for efficient data loading.

- **Visualizations/**
  - `Transfers - Neo4j Property Graph.html` - HTML file showing visualizations of the transfers network using Neo4j and PyVis.

- **Transfers - Neo4j Data Import.py**
  - Python script for importing transfers data into a Neo4j database.

- **Transfers - Neo4j Visualizer.py**
  - Python script for creating visualizations of the transfers network using Neo4j.

- **Transfers - Notebook.ipynb**
  - Jupyter Notebook for web scraping, preprocessing the data, defining the temporal network, and calculating summary statistics and metrics.

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Streamlit
- Neo4j
- PyVis

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IrisToetenel/BEP-Temporal-Networks-Iris
   cd BEP-Temporal-Networks-Iris

### DATA FOR THE DISRUPTIONS NETWORK
The base data for the temporal network of train disruptions has been obtained from: https://www.rijdendetreinen.nl/storingen/archief

The station names and coordinates of stations of The Netherlands have been obtained through API retrieval from: https://apiportal.ns.nl/


### DATA FOR THE TRANSFERS NETWORK
The base data for the temporal network of Premier League Transfers has been obtained from: https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1 
