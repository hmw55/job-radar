from dataclasses import dataclass

from app.sources.greenhouse import GreenhouseSource


@dataclass(frozen=True)
class GreenhouseBoardConfig:
    board_token: str
    company_name: str


GREENHOUSE_BOARDS = [
    GreenhouseBoardConfig(board_token="airbnb", company_name="Airbnb"),
    GreenhouseBoardConfig(board_token="stripe", company_name="Stripe"),
]


def build_greenhouse_sources() -> list[GreenhouseSource]:
    return [
        GreenhouseSource(
            board_token=board.board_token,
            company_name=board.company_name,
        )
        for board in GREENHOUSE_BOARDS
    ]