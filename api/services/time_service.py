
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


def converter_para_brasilia(data_hora: datetime) -> datetime:
    """Interpreta horários sem fuso como UTC e converte para Brasília."""
    if data_hora.tzinfo is None:
        data_hora = data_hora.replace(tzinfo=timezone.utc)

    return data_hora.astimezone(FUSO_BRASILIA)
