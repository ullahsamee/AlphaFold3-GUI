# AFusion: AlphaFold 3 GUI

**AFusion** is a user-friendly graphical interface designed to simplify the process of generating input JSON files and running AlphaFold 3 predictions. It streamlines the setup and execution of AlphaFold 3, making it accessible to users who prefer a GUI over command-line interactions.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Launching AFusion](#launching-afusion)
  - [Using the GUI](#using-the-gui)
- [Screenshots](#screenshots)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Intuitive Interface**: Easily configure job settings, sequences, and execution parameters through a clean and modern GUI.
- **Entity Management**: Add multiple entities (Protein, RNA, DNA, Ligand) with support for modifications, MSA options, and templates.
- **Dynamic JSON Generation**: Automatically generates the required JSON input file for AlphaFold 3 based on user inputs.
- **Integrated Execution**: Run AlphaFold 3 directly from the GUI with customizable Docker execution settings.
- **Visual Feedback**: Provides command output within the interface for monitoring and debugging.

## Prerequisites

Before using AFusion, ensure that you have the following:

1. **AlphaFold 3 Installed**: AFusion requires AlphaFold 3 to be installed and set up on your system. Follow the installation instructions provided in the [AlphaFold 3 GitHub Repository](https://github.com/google-deepmind/alphafold3) to deploy AlphaFold 3.

2. **Docker Installed**: Docker is required to run AlphaFold 3. Install Docker from the [official website](https://www.docker.com/get-started).

3. **Python 3.10 or Higher**: AFusion is built with Python and requires Python 3.10 or higher.

4. **Streamlit Library**: Install Streamlit to run the GUI application.

   ```bash
   pip install streamlit
   ```

5. **Other Dependencies**: Ensure the following Python libraries are installed:

   ```bash
   pip install numpy pandas pillow
   ```

6. **AFusion Source Code**: Clone or download the AFusion source code from this repository.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/afusion.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd afusion
   ```

3. **Install Python Dependencies**

   Install the required Python packages if you haven't already.

   ```bash
   pip install Streamlit
   ```

   *(Note: Create a `requirements.txt` file in the project directory with the necessary packages.)*

4. **Place the Logo Image**

   Ensure that the `logo_afusion.png` image is placed in the project directory. This image is used as the logo in the application.

## Usage

### Launching AFusion

1. **Start the Streamlit App**

   From the project directory, run:

   ```bash
   streamlit run app.py --server.fileWatcherType=none
   ```

2. **Access the Application**

   - The application will launch, and Streamlit will provide a local URL (e.g., `http://localhost:8501`).
   - Open the provided URL in your web browser to access AFusion.

### Using the GUI

#### 1. Welcome Page

- **Logo and Introduction**: You'll see the AFusion logo and a brief description.
- **Navigation Sidebar**: Use the sidebar on the left to navigate to different sections of the app.

#### 2. Job Settings

- **Job Name**: Enter a descriptive name for your job.
- **Model Seeds**: Provide integer seeds separated by commas (e.g., `1,2,3`).

#### 3. Sequences

- **Number of Entities**: Select how many entities you want to add (Proteins, RNA, DNA, Ligand).
- **Entity Details**: For each entity:
  - **Entity Type**: Select the type (Protein, RNA, DNA, Ligand).
  - **Entity ID**: Provide an identifier for the entity.
  - **Sequence Input**: Enter the sequence information.
  - **Modifications**: Optionally add modifications with their types and positions.
  - **MSA Options**: Choose MSA generation options and provide MSA data if applicable.
  - **Templates**: Optionally add template data with mmCIF content and indices.

#### 4. Bonded Atom Pairs (Optional)

- **Add Bonds**: Check the box to add bonded atom pairs.
- **Define Bonds**: For each bond, provide details for the first and second atoms, including entity IDs, residue IDs, and atom names.

#### 5. User Provided CCD (Optional)

- **User CCD Input**: Paste or enter custom CCD data in mmCIF format.

#### 6. Generated JSON

- **Review JSON Content**: The application generates the JSON input file based on your entries. You can review it here.

#### 7. AlphaFold 3 Execution Settings
Find more in [here](https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md)

- **Paths Configuration**:
  - **AF Input Path**: Specify the path to the AlphaFold input directory (e.g., `/home/user/af_input`).
  - **AF Output Path**: Specify the path to the output directory (e.g., `/home/user/af_output`).
  - **Model Parameters Directory**: Provide the path to the model parameters directory.
  - **Databases Directory**: Provide the path to the databases directory.

- **Execution Options**:
  - **Run Data Pipeline**: Choose whether to run the data pipeline (CPU-intensive).
  - **Run Inference**: Choose whether to run inference (requires GPU).

#### 8. Run AlphaFold 3

- **Save JSON File**: Click the "Save JSON File" button to save the generated JSON to the specified input path.
- **Run AlphaFold 3 Now**: Click the "Run AlphaFold 3 Now ▶️" button to execute the AlphaFold 3 prediction using the Docker command.
  - **Docker Command**: The exact Docker command used is displayed for your reference.
  - **Command Output**: Execution output is displayed within the app for monitoring.

## Screenshots

<img width="931" alt="screenshot" src="https://github.com/user-attachments/assets/e3739384-6fe8-4d0b-aa72-a8e56e5ee9f7">

## License

This project is licensed under the GPL3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **AlphaFold 3**: This GUI is designed to work with [AlphaFold 3](https://github.com/google-deepmind/alphafold3) by DeepMind.
- **Streamlit**: AFusion is built using [Streamlit](https://streamlit.io/), an open-source app framework for machine learning and data science teams.
- **Contributors**: Waiting for more!

---

If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

Happy Folding! 🧬