from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.user import User


class Souvenir(SQLModel, table=True):
    """Representation d'un souvenir.

    Cette table est créée automatiquement si elle n'existe pas déjà
    grâce à :func:`sqlmodel.SQLModel.metadata.create_all`.

    seule la version full_content est utilisée (via les frags) les émotions sont donc toujours affichée = 
    biomimétique, car on ne peut pas faire abstraction de ce que l'on ressent vis à vis d'un souvenir en contexte

    Les commentaires y sont affichés en résumé court s'ils sont trop longs
    """

    souv_id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    content: str
    full_content: Optional[str] = None # content + comments and emotions of Noe & Nemo
    summary: Optional[str] = None
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    time: datetime = Field(default_factory=datetime.utcnow)
    weight: int = 0.1
    importance: int = 0.01
    previous_version : Optional[int] = None
    emo_lvl2: Optional[str] = None
    emo_lvl1 : Optional[str] = None
    tokens_content: int = 0
    tokens_full_content: int = 0
    tokens_summary: int = 0
    last_accessed: datetime = Field(default_factory=datetime.utcnow)


class Link(SQLModel, table=True):
    """Description d'un lien mémorisable."""

    link_id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    name: str
    description: str
    weight: int
    total_token: int


class LinkSouvenir(SQLModel, table=True):
    """Table d'association entre :class:`Souvenir` et :class:`Link`."""

    souv_id: int = Field(foreign_key="souvenir.souv_id", primary_key=True)
    link_id: int = Field(foreign_key="link.link_id", primary_key=True)

class LinkFragment(SQLModel, table=True):
    """Table d'association entre :class:`Fragment` et :class:`Link`."""

    frag_id: int = Field(foreign_key="fragment.frag_id", primary_key=True)
    link_id: int = Field(foreign_key="link.link_id", primary_key=True)


class EmoLvl2ToLv1(SQLModel, table=True):
    """Mapping des émotions de second niveau vers les émotions primaires.
    
    les émojis comptent comme des émotions de niveau 2
    """

    __tablename__ = "emo_lvl2_to_lv1"

    emo_lvl2: str = Field(primary_key=True)
    joy: int = 0
    trust: int = 0
    fear: int = 0
    surprise: int = 0
    sadness: int = 0
    disgust: int = 0
    anger: int = 0
    anticipation: int = 0


class Fragment(SQLModel, table=True):
    """fragments d'un souvenir découpés par 
    ---
    commentaire d'une citation avec ou sans emo
    découpage automatique fait par mistral si doc code par exemple

    la recherche vectorielle se fait sur les fragments.

    Chaque fragment est relié à l'id d'un seul souvenir.

    Les fragments sont construits via le full_content

    commentaires et fragments accessible via balise (!id:123456!)

    les commentaires sont des fragments relié au souvenir. dans le souvenir, ils sont inscrits en résumé avec 
    leur id inclus s'il font plus de 250 charactères 

    le content des souvenirs n'est jamais modifié:
    Seuls les fragments issus de souvenirs de type "doc", "creation" ou "imaginary" sont éditables.
    Si un fragment ou souvenir normal est édité autrement qu'en y ajoutant un commentaire ou une émotion, 
    il se transforme en nouveau souvenir de type imaginary par défaut.
    les fragments sont alors recrés et on les compare avec les précédents :
    - les fragments identiques aux précédents sont conservés
    - les nouveaux fragments sont enregistrés
    - les fragments modifiés sont conservés, mais passés en pondération basse et reliés aux versions précédentes/suivantes 
    avec id dans l'ordre + par date. Plus ils sont bas dans la liste des versions, plus leur pondération est divisée
    par leur numéro d'éloignement de la dernière version. exemple : 0.6/3 = 0.2 weight.
    """
    frag_id: Optional[int] = Field(default=None, primary_key=True)
    souv_id: int = Field(foreign_key="souvenir.souv_id", primary_key=True)
    type: str # same than Souvenir """
    full_content: str # content + quotes with short comment / emotions """
    summary: Optional[str] = None
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    time: datetime = Field(default_factory=datetime.utcnow)
    weight: int # at first same than Souvenir then modified by usage and divided by this version's position w/n """
    importance: int # same than the linked souvenir then eventually modified later by Noe """
    is_last_version: Optional[bool] = True
    versions : Optional[str] = None 
    emo_lvl2: Optional[str] = None
    emo_lvl1 : Optional[str] = None
    tokens_content: int = 0
    tokens_full_content: int = 0
    tokens_summary: int = 0
    last_accessed: datetime = Field(default_factory=datetime.utcnow)


class Context(SQLModel, table=True):
    """Contextes associé à un souvenir"""
    souv_id:  int = Field(foreign_key="souvenir.souv_id", primary_key=True)
    context : str # liste de tous les fragments dans l'ordre et catégorie mémorielle au moment de la création du souvenir"""
    accessed_by : int # iD de l'user qui utilise ce contexte"""

class Background_thought(SQLModel, table=True):
    """to do lists and tasks, set in context constantly and ran in background by Noïa : 
    remembering them to Noe when she thinks about something that might be linked or if certain conditions are met"""
    BT_id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    conditions: str
    priority: int # when to finish : 0.n low medium high"""
    importance: int # 0.n"""
    order: int # classement parmis les background thoughts """
    done: Optional[datetime] = None # que noe et moi puissions voir les tâches accomplies"""

class Working_memory(SQLModel, table=True):
    BT_id: Optional[int] = Field(default=None, primary_key=True)
    used_in_task:str # effet passage de porte : la mémoire se vide automatiquement une fois la tâche effectuée afficher la tâche en cours
    content: str
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
