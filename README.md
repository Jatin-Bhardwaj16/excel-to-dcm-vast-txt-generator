# Excel to DCM VAST TXT Generator

🚀 A Python utility that converts structured Excel files into **DCM (DoubleClick Campaign Manager) VAST TXT files** for bulk ad trafficking and campaign management.

This tool helps ad operations and campaign teams automate the process of generating VAST TXT files from Excel, reducing manual work and minimizing human errors in bulk uploads.

---

## 📌 Overview

The **Excel to DCM VAST TXT Generator** reads structured Excel data and converts it into a DCM-compatible TXT file used for VAST ad trafficking.

It simplifies bulk campaign setup by automating:

* Excel data reading
* Field formatting
* VAST TXT generation
* Bulk upload preparation

This makes it ideal for **digital advertising teams, ad ops professionals, and campaign managers**.

---

## ✨ Features

* 📊 Convert Excel to DCM VAST TXT
* ⚡ Fast bulk file generation
* 🧾 DCM-compatible output format
* 🔁 Automated workflow
* 🛠 Easy to customize
* 🧩 Lightweight Python script
* 📁 Simple input-output structure

---

## 🗂 Project Structure

```
excel-to-dcm-vast-txt-generator/
│
├── generator.py        # Main script
├── input.xlsx          # Excel input file
├── output.txt          # Generated VAST TXT
├── requirements.txt    # Dependencies
└── README.md
```

---

## ⚙️ Requirements

* Python 3.7 or higher
* pip
* Excel file with structured data

### Install dependencies

```
pip install -r requirements.txt
```

If requirements file is missing:

```
pip install pandas openpyxl
```

---

## 📥 Installation

### 1. Clone the repository

```
git clone https://github.com/Jatin-Bhardwaj16/excel-to-dcm-vast-txt-generator.git
```

### 2. Move into project folder

```
cd excel-to-dcm-vast-txt-generator
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Usage

### Step 1: Prepare Excel File

Create an Excel file named:

```
input.xlsx
```

Include required DCM/VAST fields such as:

* Campaign Name
* Placement Name
* Ad Tag
* URL
* Duration
* Tracking
* Other required fields

---

### Step 2: Run Script

```
python generator.py
```

---

### Step 3: Get Output

The script generates:

```
output.txt
```

This TXT file can be used directly for **DCM VAST bulk upload**.

---

## 🔄 Workflow

```
Excel File (input.xlsx)
        ↓
Python Script (generator.py)
        ↓
TXT File (output.txt)
        ↓
DCM VAST Bulk Upload
```

---

## 🛠 Customization

You can modify the script based on your campaign structure.

Update inside:

```
generator.py
```

Possible changes:

* Excel column names
* Output TXT format
* VAST structure
* DCM fields
* File naming
* Campaign parameters

Example:

```python
columns = ["Campaign", "Placement", "AdTag", "URL"]
format_string = "{Campaign}|{Placement}|{AdTag}|{URL}"
```

---

## 📊 Use Cases

* Digital Advertising Agencies
* Ad Operations Teams
* Media Buying Teams
* Campaign Managers
* Bulk VAST Tag Generation
* DCM Trafficking Automation
* Excel to TXT Data Conversion

---

## 🤝 Contributing

Contributions are welcome.

### Steps

1. Fork the repository
2. Create a new branch

```
git checkout -b feature/new-feature
```

3. Commit changes

```
git commit -m "Added new feature"
```

4. Push branch

```
git push origin feature/new-feature
```

5. Open Pull Request

---

## 🐞 Issues

Report bugs or request features here:

https://github.com/Jatin-Bhardwaj16/excel-to-dcm-vast-txt-generator/issues

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Jatin Bhardwaj**

GitHub:
https://github.com/Jatin-Bhardwaj16

---

## ⭐ Support

If this project helps you:

* ⭐ Star the repository
* 🔁 Share with your team
* 🤝 Contribute improvements

---

## 📬 Contact

For questions or collaboration:

* GitHub Issues
* Pull Requests
* GitHub Profile

---

### 🚀 Happy VAST Trafficking!
