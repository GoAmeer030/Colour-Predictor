# Color Predictor

This project allows users to collect data from a **color prediction trading or gambling** **sites** using a scraper (`scrape.py`) and build a predictive model (`model.ipynb`) to forecast colors in a color prediction game. Additionally, a pre-trained model (`model.joblib`) is available for direct use along with a prediction script (`predict.py`).

## Getting Started

### Prerequisites

-   Python 3.x
-   Necessary Python packages (mentioned in `requirements.txt`)

### Installation

1. Clone this repository.
2. Install the required Python packages by running:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Scraper (`scrape.py`)

-   The `scrape.py` file facilitates data scraping from the gambling site.
-   It requires valid login credentials and allows modification of XPATH values for site compatibility.
-   Run the scraper using:
    ```bash
    python scrape.py
    ```
-   The collected data is saved in `data.csv`.

### Model Training (`model.ipynb`)

-   The `model.ipynb` notebook contains the code to train a predictive model using the collected data.
-   It uses `RandomForestClassifier` from `scikit-learn`.
-   Follow the instructions in the notebook to train and save the model as `model.joblib`.

### Pre-trained Model (`model.joblib`) and Prediction Script (`predict.py`)

-   The pre-trained model (`model.joblib`) can be directly downloaded from the releases section.
-   Use `predict.py` script to make predictions using the pre-trained model:
    ```bash
    python predict.py
    ```
-   Enter the value to predict when prompted.

## Important Notices and Cautions

-   **Educational Purpose Only:** This project is for educational purposes only to showcase machine learning capabilities and is not meant for actual gambling or financial investment.
-   **Accuracy Disclaimer:** The provided model has limited accuracy (color: ~45-50%, number: ~15-20%). Users are responsible for their actions when using this model for any gambling purposes.
-   **Site Policy Compliance:** Using this tool may violate the gambling site's policies and result in a permanent ban.
-   **Financial Caution:** The developer takes no responsibility for financial losses or consequences resulting from the use of this project.

## Disclaimer

This project and its components are meant for educational purposes only. Users are advised to comply with all laws and regulations applicable in their respective regions.

For detailed instructions and code explanations, refer to individual files in the repository.
