# Clínica Estética – Sistema Especialista

This project is part of the [PosWeb-SistemasEspecialistas](https://github.com/MelquesPaiva/PosWeb-SistemasEspecialistas) repository and focuses on a specialized system for aesthetic clinics. It leverages expert systems to assist in managing patient interactions, processing prescriptions, and training a chatbot for client communication.

## 📁 Project Structure

```
clinica-estetica/
├── chat.py
├── process_prescriptions.py
├── service.py
├── train_robot.py
├── requirements.txt
└── ...
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MelquesPaiva/PosWeb-SistemasEspecialistas.git
cd PosWeb-SistemasEspecialistas/clinica-estetica
```

### 2. Set Up a Python Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Ensure all required packages are installed:

```bash
pip install -r requirements.txt
```

## 🛠️ Running the Application

### Start the Service

The `service.py` script initializes the main service of the expert system.

```bash
python3 service.py
```

### Launch the Chatbot

The `chat.py` script starts the chatbot interface for client interactions.

```bash
python3 chat.py
```

## 🤖 Additional Functionalities

### Train the Chatbot

Before using the chatbot, train it with the necessary data:

```bash
python3 train_robot.py
```

### Process Prescriptions

To process and manage client prescriptions:

```bash
python3 process_prescriptions.py
```

## 📌 Notes

- Always activate the virtual environment before running any scripts to ensure the correct dependencies are used.
- Ensure that the `requirements.txt` file is up-to-date with all necessary packages.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.