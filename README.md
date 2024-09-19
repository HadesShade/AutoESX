# AutoESX

AutoESX is a Python-based automation tool intended to manage VMware ESXi operations. It provides functionalities for importing and exporting virtual machines, managing virtual switches, and configuring port groups. New features are coming soon!

## Installation

To get started with AutoESX, you need to have Python installed on your machine. Follow these steps to install the necessary dependencies:

1. Clone the repository:
   ```bash
   git clone https://github.com/HadesShade/AutoESX.git
   cd AutoESX
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the main script, execute the following command:
```bash
python AutoESX.py -i <path/to/inventory_file>.yaml -j <path/to/job_file>.yaml
```

Make sure to provide the necessary configuration and input files as required by the script.

## Features

* **VM Import**: Import virtual machines from OVA files.
* **VM Export**: Export virtual machines to OVA files.
* **Virtual Switch Management**: Add, remove, and list virtual switches.
* **Port Group Management**: Configure and manage port groups.
* **Policy Management**: Set and get policies for virtual switches and port groups.

## Sample YAML Files

Sample YAML files are available in the `sample_yaml` directory to help you get started with the configuration.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.