"""Configuration management for MedPredict."""
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for MedPredict."""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """Initialize configuration from YAML file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    @property
    def model_config(self) -> Dict[str, Any]:
        """Get model configuration."""
        return self.config.get('model', {})
    
    @property
    def data_config(self) -> Dict[str, Any]:
        """Get data configuration."""
        return self.config.get('data', {})
    
    @property
    def mlflow_config(self) -> Dict[str, Any]:
        """Get MLflow configuration."""
        return self.config.get('mlflow', {})
    
    @property
    def api_config(self) -> Dict[str, Any]:
        """Get API configuration."""
        return self.config.get('api', {})
