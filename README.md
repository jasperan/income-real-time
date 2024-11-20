# Real-Time Income Simulator

This is a graphical interface simulator that calculates real-time income based on a starting amount and monthly income. The simulator displays the income dynamically and features a rainbow effect when a whole extra dollar is reached.

## Features

- Real-time income calculation and display
- Beautiful gradient background
- Responsive UI design
- Rainbow effect for whole dollar increments
- Real-time graph of income over time
- Additional statistics including time elapsed, income rate, and total earned

## Requirements

- Python 3.x
- Tkinter (comes with Python)
- Additional Python packages listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jasperan/income-real-time.git
   cd income-real-time
   ```

2. **Install the required packages:**

   Make sure you have `pip` installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulator

1. **Navigate to the project directory:**

   ```bash
   cd income-real-time
   ```

2. **Run the simulator:**

   ```bash
   python income_simulator.py
   ```

## Usage

- **Starting Amount:** Enter your initial bank account balance.
- **Monthly Income:** Enter your expected monthly income.
- **Start Simulation:** Click to start the real-time income calculation.
- **Reset:** Click to reset the simulation.

## Customization

- **Styles:** Modify `style_config.py` to change the appearance of the UI.
- **Graph Settings:** Adjust `graph_utils.py` for different graph configurations.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.