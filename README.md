# Roboracer Autodrive UI

A Python-based user interface for controlling and configuring parameters in autonomous F1/10 Cars.

## Features

- Wall following parameter configuration
- Interactive parameter adjustment interface

## Project Structure

- `wall_follow_params_set.py`: Control Wall Follow Parametes - Data Saved as JSON
- `wall_follow_params_set_interface.py`: Simple Interface for relatively simpler applications - data saved as CSV

## Technologies

- Python (100%)
- ROS (Robot Operating System) integration

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/roboracer-autodrive-ui.git
```

2. Navigate to the project directory:

```bash
cd roboracer-autodrive-ui
```

3. Install required dependencies:

Note: Preferable to be Run in a python virtual env
```bash
pip install --upgrade gradio
```

4. Run the application:
```bash
python wall_follow_params_set.py
```

## Usage

- Use the UI to adjust wall following parameters.
- Changes are saved in a JSON file for `wall_follow_params_set.py` and a CSV file for `wall_follow_params_set_interface.py`.
- Ensure that ROS is running if you're using the ROS integration features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.