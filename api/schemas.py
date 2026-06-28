from pydantic import BaseModel

class ControlCommand(BaseModel):
    power: bool
    target_temperature: float
    timer_minutes: int  # Tempo para o ar-condicionado desligar
    reset_filter: bool  # Redefinir tempo após limpeza do filtro
    
class Telemetry(BaseModel):
    current_temperature: float
    current_humidity: float
    motion_detected: bool
    filter_hours_used: float
