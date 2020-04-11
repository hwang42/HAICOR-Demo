# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .common import database


class Language(database.Model):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String)

    concepts = relationship("Concept", back_populates="language")


class PartOfSpeech(database.Model):
    __tablename__ = "part_of_speeches"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String)

    concepts = relationship("Concept", back_populates="part_of_speech")


class Concept(database.Model):
    __tablename__ = "concepts"
    __table_args__ = (UniqueConstraint("lang", "text", "speech", "suffix"),)

    id = Column(Integer, primary_key=True)
    lang = Column(Integer, ForeignKey("languages.id"), nullable=False)
    text = Column(String, nullable=False)
    speech = Column(Integer, ForeignKey("part_of_speeches.id"))
    suffix = Column(String)

    language = relationship("Language", back_populates="concepts")
    part_of_speech = relationship("PartOfSpeech", back_populates="concepts")
    as_source_assertions = relationship("Assertion", back_populates="source",
                                        foreign_keys="Assertion.source_id")
    as_target_assertions = relationship("Assertion", back_populates="target",
                                        foreign_keys="Assertion.target_id")
