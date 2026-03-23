# DASS Assignment 2
**Author:** Prashant Vinod (Roll No: 2024101116)  
**Git Repository:** [https://github.com/Wolverine-07/DASS-Assignment-2](https://github.com/Wolverine-07/DASS-Assignment-2)  
**OneDrive Link:** [https://iiithydstudents-my.sharepoint.com/:u:/g/personal/prashant_vinod_students_iiit_ac_in/IQDtzvuhlMKRRr93CO_2V2NVATi5oxnYigMOWLnihdIWrMY?e=jp35dn](https://iiithydstudents-my.sharepoint.com/:u:/g/personal/prashant_vinod_students_iiit_ac_in/IQDtzvuhlMKRRr93CO_2V2NVATi5oxnYigMOWLnihdIWrMY?e=jp35dn)

This repository contains the completion of Phase 1 (White Box Testing), Phase 2 (Integration Testing), and Phase 3 (Black Box API Testing) for DASS Assignment 2.

## Project Structure
```text
2024101116/
├── whitebox/               # Phase 1: MoneyPoly code and White Box Tests
├── integration/            # Phase 2: StreetRace Manager code and Integration Tests
├── blackbox/               # Phase 3: QuickCart API Black Box Tests & Bug Reports
├── requirements.txt        # Shared python dependencies
└── README.md               # This file
```

## Setup Instructions
1. Navigate to the project directory:
   ```bash
   cd 2024101116
   ```
2. Set up the Python virtual environment and install dependencies:
   ```bash
   python3 -m venv ../venv
   source ../venv/bin/activate
   pip install -r requirements.txt
   ```

## How to Run the Code

### Phase 1: MoneyPoly (White Box)
To run the interactive CLI for the MoneyPoly game:
```bash
python3 whitebox/code/main.py
```

### Phase 2: StreetRace Manager (Integration)
The StreetRace manager relies predominantly on its modular back-end architecture which is thoroughly orchestrated and simulated via the integration test suite. See "How to Run Tests" below.

### Phase 3: QuickCart API (Black Box)
Ensure the QuickCart API is running via Docker before testing:
```bash
docker run -d -p 8080:8080 --name quickcart_server quickcart
```
(Note: You must have loaded the provided `quickcart_image_x86.tar` or `quickcart_image.tar` natively).

---

## How to Run Tests

All tests are written using `pytest`. Ensure the virtual environment is activated (`source ../venv/bin/activate`).

**1. Run White Box Tests & Pylint (Phase 1)**
Run the white box `pytest` suite:
```bash
pytest whitebox/tests/ -v
```
Run `pylint` on the MoneyPoly codebase to verify code quality:
```bash
pylint whitebox/code/
```

**2. Run Integration Tests (Phase 2)**
Run the StreetRace Manager integration test suite:
```bash
pytest integration/tests/ -v
```

**3. Run Black Box Tests (Phase 3)**
The QuickCart API must be running via Docker before executing the black box tests.
First, load the Docker image and start the container:
```bash
docker load -i ../quickcart_image_x86.tar  # Use quickcart_image.tar if on ARM/macOS
docker run -d -p 8080:8080 --name quickcart_server quickcart
```
Then, run the black box test suite (which targets `http://localhost:8080/api/v1`):
```bash
pytest blackbox/tests/ -v
```

**4. Run All Tests**
```bash
pytest -v
```
