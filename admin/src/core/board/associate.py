from datetime import datetime
import enum
from sqlalchemy import Column, String, Integer, Enum, Boolean
from src.core.db import db
from src.core.board.base_model import BaseModel
import os


associate_disciplines = db.Table(
    "associate_disciplines",
    Column("associate_id", Integer, db.ForeignKey("associates.id"), primary_key=True),
    Column("discipline_id", Integer, db.ForeignKey("disciplines.id"), primary_key=True),
    Column("created_at", db.DateTime, default=db.func.now()),
)


class GenderOptions(enum.Enum):
    male = 1
    female = 2
    other = 3


class DNIOptions(enum.Enum):
    DNI = 1
    LE = 2
    LC = 3


class Associate(BaseModel):
    """Club associate model
    Args:
        - DNI type (select) : list with all different DNI types ex: DNI, LE, LC
        - DNI number (integer) :  Associate DNI number
        - gender (select) : Associate gender ex: M|F|Otro
        - associate number (integer): Associate number. Unique, autogenerated
        - address (text) : associate address .
        - phone number (optional) (text): Associate Phone number.
        - Entry date  (datetime): Entry-date autogenerated

    """

    __tablename__ = "associates"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    active = Column(Boolean(), default=True)
    profile_pic = Column(
        String(), default=os.path.join(os.getcwd(), "public", "profile_icon.png")
    )
    email = Column(String(50), nullable=False)
    DNI_number = Column(Integer, nullable=False)
    DNI_type = Column(Enum(DNIOptions, validate_string=True))
    gender = Column(Enum(GenderOptions, validate_string=True))
    address = Column(String())
    phone_number = Column(String, nullable=True)
    entry_date = Column(db.DateTime)
    deleted = Column(Boolean(), default=False)

    payments = db.relationship("Payment", back_populates="associate", lazy=True)
    disciplines = db.relationship(
        "Discipline", secondary="associate_disciplines", back_populates="associates"
    )

    def __init__(self, **data):
        self.DNI_number = data["DNI_number"]
        self.name = data["name"]
        self.surname = data["surname"]
        self.email = data["email"]
        self.DNI_type = data["DNI_type"]
        self.gender = data["gender"]
        self.address = data["address"]
        self.phone_number = data["phone_number"]
        self.active = True
        self.entry_date = datetime.utcnow()

    def __repr__(self):
        return f"""{self.name} {self.surname} con el dni {self.DNI_number} con el correo {self.email}"""

    def _to_dict(self):
        """Returns:
        User: The dictionary representation of the user.
        """
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "DNI_number": self.DNI_number,
            "DNI_type": str(self.DNI_type).rsplit(".", 1)[-1],
            "gender": str(self.gender).rsplit(".", 1)[-1],
            "address": self.address,
            "phone_number": self.phone_number,
        }

    def _to_dict_with_disciplines(self):
        """Returns:
        User: The dictionary representation of the user.
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "DNI_number": self.DNI_number,
            "DNI_type": str(self.DNI_type).rsplit(".", 1)[-1],
            "gender": str(self.gender).rsplit(".", 1)[-1],
            "address": self.address,
            "phone_number": self.phone_number,
            "disciplines": list(map(lambda d: d.to_dict(), self.disciplines)),
        }

    def to_dict(self, disciplines=False):
        return self._to_dict_with_disciplines() if disciplines else self._to_dict()