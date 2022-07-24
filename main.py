from typing import Union, Optional, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Report(BaseModel):
    num: int
    created: int
    done: Optional[int]
    topic: str
    room: str
    responsible: str
    status: str


class CommercialPremise(BaseModel):
    area: str
    renter: str
    scope: str
    rental_amount: str
    debt: str
    profit: str
    photos: List[str]


class FreeCommercialPremise(BaseModel):
    area: str
    scope: str
    rental_amount: str
    detail: str
    photos: List[str]


@app.get("/reports/", response_model=List[Report])
def get_reports():

    return [
        Report(
            num = 12,
            created = 1657475269,
            done = None,
            topic = "На этаже не работет кондиционер",
            room = "231",
            responsible = "Иванов П.А.",
            status = "В работе"
    ),
        Report(
            num=24,
            created=1658512069,
            done=1658771269,
            topic="Не работает лифт №1",
            room="142",
            responsible="Васильев И.Н.",
            status="Выполнено"
        ),
        Report(
            num=25,
            created=1657648069,
            done=1659203269,
            topic="На этаже не работет кондиционер",
            room="412",
            responsible="Сангиев А.К.",
            status="Провалено"
        ),
        Report(
            num=12,
            created=1658684869,
            done=None,
            topic="Не работает домофон",
            room="231",
            responsible="Лехин Н.Т.",
            status="Новая"
        ),
        Report(
            num=22,
            created=1658684869,
            done=None,
            topic="Не работает кондиционер",
            room="16",
            responsible="Тереньтев С.А.",
            status="Новая"
        ),
    ]


@app.get("/commercial-premises/", response_model=List[CommercialPremise])
def get_commercial_premises():
    return [
        CommercialPremise(
            area="87.5 кв.м.",
            renter="Территория фитнеса",
            scope="Спорт",
            rental_amount="160 000 ₽",
            debt="0 ₽",
            profit="476 000 ₽",
            photos=[
                "https://sargorstroy.ru/800/600/https/www.ecopan.nsk.ru/upload/iblock/81f/Kaylasplan11.jpg",
                "https://yakutsk.ru/wp-content/uploads/2022/05/06/base_kvartus_object_341_3412399_cb59lmmmlzpiunuzogircn7pbpzmjjsmlolwaxibnyj8cuyqa6.jpeg"
            ]
        ),
        CommercialPremise(
            area="47.5 кв.м.",
            renter="Азбука вкуса",
            scope="Продукты",
            rental_amount="90 000 ₽",
            debt="0 ₽",
            profit="286 000 ₽",
            photos=[
                "https://arch-shop.ru/wp-content/uploads/2015/01/02-office-plan-800px.jpg",
                "https://www.sherland.ru/upload/medialibrary/464/464aa665c00c1fd34a2de21accf8cc36.jpg"
            ]
        )
    ]


@app.get("/commercial-premises/free/", response_model=List[FreeCommercialPremise])
def get_free_commercial_premises():
    return [
        FreeCommercialPremise(
            area="37.5 кв.м.",
            scope="Продукты",
            rental_amount="37 500 ₽",
            detail="Квадратное",
            photos=[
                "https://sargorstroy.ru/800/600/https/www.ecopan.nsk.ru/upload/iblock/81f/Kaylasplan11.jpg",
                "https://yakutsk.ru/wp-content/uploads/2022/05/06/base_kvartus_object_341_3412399_cb59lmmmlzpiunuzogircn7pbpzmjjsmlolwaxibnyj8cuyqa6.jpeg"
            ]
        ),
        FreeCommercialPremise(
            area="120 кв.м.",
            rental_amount="120 000 ₽",
            scope="СПА",
            detail="Квадратное",
            photos=[
                "https://arch-shop.ru/wp-content/uploads/2015/01/02-office-plan-800px.jpg",
                "https://www.sherland.ru/upload/medialibrary/464/464aa665c00c1fd34a2de21accf8cc36.jpg"
            ]
        )
    ]