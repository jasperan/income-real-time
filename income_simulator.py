from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from decimal import Decimal
import time
from datetime import datetime
import threading
import json
import os

class IncomeSimulator:
    def __init__(self):
        self.console = Console()
        self.running = False
        self.last_whole = 0
        self.start_time = None
        self.current_amount = Decimal('0.00')
        
        # Load or create default configuration
        self.load_config()
        self.income_per_second = self.monthly_income / Decimal('30.44') / Decimal('24') / Decimal('60') / Decimal('60')
        
    def load_config(self):
        config_file = 'config.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                self.starting_amount = Decimal(config['starting_amount'])
                self.monthly_income = Decimal(config['monthly_income'])
                self.current_amount = Decimal(config.get('current_amount', self.starting_amount))
            else:
                # Default values
                self.starting_amount = Decimal('1000.00')
                self.monthly_income = Decimal('5000.00')
                self.current_amount = self.starting_amount
                # Save default config
                self.save_config()
        except (json.JSONDecodeError, KeyError):
            self.starting_amount = Decimal('1000.00')
            self.monthly_income = Decimal('5000.00')
            self.current_amount = self.starting_amount
            self.save_config()
    
    def save_config(self):
        config = {
            'starting_amount': str(self.starting_amount),
            'monthly_income': str(self.monthly_income),
            'current_amount': str(self.current_amount)
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
    def create_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", size=10),
            Layout(name="progress", size=6),
            Layout(name="footer", size=3)
        )
        return layout
    
    def generate_progress(self) -> Progress:
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            expand=True
        )
        
        # Calculate progress to next cent (0.01)
        current_cents = int(self.current_amount * 100)
        progress_to_next_cent = (self.current_amount * 100) - Decimal(current_cents)
        seconds_to_cent = float(Decimal('0.01') / self.income_per_second)
        progress.add_task(
            "Progress to next cent",
            total=1.0,
            completed=float(progress_to_next_cent),
            time_remaining=seconds_to_cent if progress_to_next_cent < 1.0 else 0
        )
        
        # Calculate progress to next 10 cents (0.10)
        current_ten_cents = int(self.current_amount * 10)
        progress_to_next_ten_cents = (self.current_amount * 10) - Decimal(current_ten_cents)
        seconds_to_ten_cents = float(Decimal('0.10') / self.income_per_second)
        progress.add_task(
            "Progress to next 10 cents",
            total=1.0,
            completed=float(progress_to_next_ten_cents),
            time_remaining=seconds_to_ten_cents if progress_to_next_ten_cents < 1.0 else 0
        )
        
        # Calculate progress to next euro
        current_whole = int(self.current_amount)
        progress_to_next = self.current_amount - Decimal(current_whole)
        seconds_to_euro = float(Decimal('1.0') / self.income_per_second)
        progress.add_task(
            "Progress to next euro",
            total=1.0,
            completed=float(progress_to_next),
            time_remaining=seconds_to_euro if progress_to_next < 1.0 else 0
        )
        
        return progress
    
    def generate_table(self) -> Table:
        table = Table(show_header=False, box=None, padding=0)
        table.add_column("Label", style="cyan")
        table.add_column("Value", style="green")
        
        # Add statistics
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            hourly_rate = self.income_per_second * 3600
            total_earned = self.current_amount - self.starting_amount
            
            table.add_row("Time Elapsed:", str(elapsed).split('.')[0])
            table.add_row("Income Rate:", f"€{hourly_rate:.2f}/hr")
            table.add_row("Total Earned:", f"€{total_earned:.2f}")
        
        return table
    
    def generate_content(self) -> Panel:
        amount_text = Text(f"€{self.current_amount:.2f}", style="bold white", justify="center")
        if int(self.current_amount) > self.last_whole:
            amount_text.style = "bold rainbow"
            self.last_whole = int(self.current_amount)
            
        stats_table = self.generate_table()
        progress = self.generate_progress()
        
        layout = self.create_layout()
        layout["header"].update(Panel("Real-Time Income Simulator", style="bold blue"))
        layout["main"].update(Panel(amount_text))
        layout["progress"].update(Panel(progress))
        layout["footer"].update(Panel(stats_table))
        
        return layout
    
    def run_simulation(self):
        self.start_time = datetime.now()
        
        with Live(self.generate_content(), refresh_per_second=10) as live:
            while self.running:
                self.current_amount += self.income_per_second / Decimal('10')
                live.update(self.generate_content())
                time.sleep(0.1)
    
    def start(self):
        self.console.clear()
        
        # Show current configuration
        self.console.print(f"[cyan]Current configuration:[/cyan]")
        self.console.print(f"Starting amount: €{self.starting_amount}")
        self.console.print(f"Monthly income: €{self.monthly_income}")
        self.console.print("\n[yellow]Press Enter to continue with these values, or type 'new' to enter new values:[/yellow]")
        
        choice = input().strip().lower()
        if choice == 'new':
            try:
                self.console.print("[cyan]Enter starting amount (€):[/cyan]")
                self.starting_amount = Decimal(input())
                self.console.print("[cyan]Enter monthly income (€):[/cyan]")
                self.monthly_income = Decimal(input())
                
                self.income_per_second = self.monthly_income / Decimal('30.44') / Decimal('24') / Decimal('60') / Decimal('60')
                self.save_config()  # Save new configuration
            except ValueError:
                self.console.print("[red]Please enter valid numbers[/red]")
                return
        
        self.current_amount = self.starting_amount
        self.console.clear()
        self.console.print("[green]Press Ctrl+C to stop the simulation[/green]")
        time.sleep(1)
        
        try:
            self.running = True
            self.run_simulation()
        except KeyboardInterrupt:
            self.running = False
            self.console.print("\n[yellow]Simulation stopped[/yellow]")
            self.save_config()  # Save the current amount when stopping

if __name__ == "__main__":
    simulator = IncomeSimulator()
    simulator.start() 