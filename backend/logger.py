from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install
import logging
from datetime import datetime
from pathlib import Path


install(show_locals=True, width=120, word_wrap=True)

custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "debug": "bold green",
    "timestamp": "bold blue",
})


class RichLogger:
    def __init__(self, name: str = "app"):
        self.name = name
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.log_filename = self.log_dir / f"app_{datetime.now().strftime('%Y-%m-%d')}.log"
        self.console = Console(theme=custom_theme)
        
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        rich_handler = RichHandler(
            console=self.console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_path=True,
            enable_link_path=True,
            markup=True,
            log_time_format="[timestamp]%Y-%m-%d %H:%M:%S[/]"
        )

        file_handler = logging.FileHandler(self.log_filename, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        logger.addHandler(rich_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

        return logger

    def _format_message(self, message: str, level: str) -> str:
        return f"[{level}]{message}[/{level}]"

    def debug(self, message: str) -> None:
        formatted = self._format_message(message, "debug")
        self.logger.debug(formatted)

    def info(self, message: str) -> None:
        formatted = self._format_message(message, "info")
        self.logger.info(formatted)

    def warning(self, message: str) -> None:
        formatted = self._format_message(message, "warning")
        self.logger.warning(formatted)

    def error(self, message: str) -> None:
        formatted = self._format_message(message, "error")
        self.logger.error(formatted)

    def critical(self, message: str) -> None:
        formatted = self._format_message(message, "critical")
        self.console.print("\n[bold red]"+"!"*50+"[/]")
        self.logger.critical(formatted)
        self.console.print("[bold red]"+"!"*50+"\n[/]")

    def exception(self, message: str) -> None:
        self.console.print("\n[bold red]"+"!"*50+"[/]")
        self.logger.exception(f"[error]{message}[/]")
        self.console.print("[bold red]"+"!"*50+"\n[/]")

    def success(self, message: str) -> None:
        """Custom success message with green checkmark"""
        self.console.print(f"[bold green]✓[/] {message}")


default_logger = RichLogger()