from src.core.auth import (
    create_user,
    get_by_usr_and_pwd,
    create_role,
    get_role,
    add_role_to_user,
    add_permission_to_role,
    get_permission,
    create_permission,
)

from src.core.board import create_payment,create_associate,add_discipline,add_discipline_to_associate,list_all_disciplines
from passlib.hash import sha256_crypt
from src.web.helpers.auth import get_permissions
from src.core.board import list_all_associates
import random


def run():
    """Creates an admin user, the roles and permissions"""
    # create roles
    adm_role = get_role("Admin")
    if adm_role is None:
        adm_role = create_role("Admin")
    op_role = get_role("Operario")
    if op_role is None:
        op_role = create_role("Operario")
    us_role = get_role("Socio")
    if us_role is None:
        us_role = create_role("Socio")

    # link roles w/ permissions
    op_perm, adm_perm = get_permissions()
    for perm in adm_perm:
        perm_obj = get_permission(perm)
        if perm_obj is None:
            perm_obj = create_permission(perm)
        add_permission_to_role(adm_role, perm_obj)

    for perm in op_perm:
        perm_obj = get_permission(perm)
        if perm_obj is None:
            perm_obj = create_permission(perm)
        add_permission_to_role(op_role, perm_obj)

    # creates user with role admin
    if get_by_usr_and_pwd("admin", "1234") is None:
        create_user(
            {
                "name": "admin",
                "surname": "admin",
                "email": "admin@villaelisa.com",
                "username": "admin",
                "password": sha256_crypt.encrypt("1234"),
            }
        )
        add_role_to_user(get_by_usr_and_pwd("admin", "1234"), get_role("Admin"))


def populate():
    """Populates the database with some data"""
    adm_role = get_role("Admin")
    op_role = get_role("Operario")
    us_role = get_role("Socio")
    roles = [adm_role, op_role]
    names = ["Juan", "Pablo", "Maria", "Diana", "Horacio", "Pedro", "Kevin", "César"]
    last_names = [
        "Perez",
        "Gonzalez",
        "Garcia",
        "Rodriguez",
        "Lopez",
        "Martinez",
        "Hernandez",
        "Gomez",
    ]
    emails = [
        "juan@gmail.com",
        "pablo@gmail.com",
        "maria@gmail.com",
        "diana@gmail.com",
        "horacio@gmail.com",
        "pedro@gmail.com",
        "kevin@gmail.com",
        "cesar@gmail.com",
    ]
    more_emails = [f"{last_name.lower()}@gmail.com" for last_name in last_names]
    usernames = [
        "juan",
        "pablo",
        "maria",
        "diana",
        "pedro",
        "horacio",
        "kevin",
        "cesar",
    ]
    passwords = ["1234", "1234", "1234", "1234", "1234", "1234", "1234", "1234"]

    dicipline_name = [
        "Futbol",
        "Basquetbol",
        "Voleibol",
        "Gimnasia Artística",
        "Handball",
        "Tenis",
        "Taekwon-do",
        "Patín artístico",
    ]
    dicipline_category = [
        "12 a 14 años",
        "16 a 20 años",
        "16 a 20 años",
        "10 a 12 años",
        "20 a 26 años",
        "20 a 26 años",
        "14 a 18 años",
        "12 a 14 años",
    ]
    instructors = [
        "Juan",
        "Pablo",
        "Maria",
        "Diana",
        "Horacio",
        "Pedro",
        "Kevin",
        "César",
    ]
    days_and_hours = [
        "Lunes 6:00pm - 8:00pm",
        "Martes 6:00pm - 8:00pm",
        "Miercoles 6:00pm - 8:00pm",
        "Lunes 2:00pm - 4:00pm",
        "Viernes 6:00pm - 8:00pm",
        "Sabado 6:00pm - 8:00pm",
        "Martes 4:00pm - 6:00pm",
        "Jueves 4:00pm - 6:00pm",
    ]
    monthly_cost = [800.00, 700.00, 500.00, 600.00, 800.00, 700.00, 900.00, 600.00]

    dni = [
        22583743,
        46583754,
        20583743,
        42583443,
        28582754,
        30583741,
        14583743,
        23683784,
    ]
    address = [
        "Calle 1",
        "Calle 2",
        "Calle 3",
        "Calle 4",
        "Calle 5",
        "Calle 6",
        "Calle 7",
        "Calle 8",
    ]
    telephones = [
        22123456,
        22123457,
        22123458,
        22123459,
        22123460,
        22123461,
        22123462,
        22123463,
    ]
    genders = ["male", "male", "female", "other", "male", "male", "other", "male"]

    try:
        for i in range(0, 7):
            u = create_user(
                {
                    "name": names[i],
                    "surname": last_names[i],
                    "email": emails[i],
                    "username": dni[i],
                    "password": sha256_crypt.encrypt(passwords[i]),
                }
            )
            add_role_to_user(u, us_role)
            add_discipline(
                {
                    "name": dicipline_name[i],
                    "category": dicipline_category[i],
                    "instructors": instructors[i],
                    "dates": days_and_hours[i],
                    "monthly_cost": monthly_cost[i],
                    "available": True,
                }
            )
            create_associate(
                {
                    "DNI_number": dni[i],
                    "DNI_type": "DNI",
                    "name": names[i],
                    "surname": last_names[i],
                    "email": more_emails[i],
                    "gender": genders[i],
                    "address": address[i],
                    "phone_number": telephones[i],
                }
            )
    except Exception as e:
        print(e)

    u = create_user(
        {
            "name": "operador",
            "surname": "operador",
            "email": "operador@villaelisa.com",
            "username": "operador",
            "password": sha256_crypt.encrypt("1234"),
        }
    )
    add_role_to_user(u, op_role)
    associate = list_all_associates()[0]
    add_discipline_to_associate(associate, list_all_disciplines()[0])
    from src.core.board.repositories.configuration import get_cfg
    from src.web.helpers.payment_helpers import disciplines_fee_amount

    config = get_cfg()
    create_payment(
        last_installment=1,
        amount=disciplines_fee_amount(associate) + config.base_fee,
        date="2021-12-12",
        associate=associate,
    )
