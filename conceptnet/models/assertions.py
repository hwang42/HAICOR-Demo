# Copyright (c) 2020 Hecong Wang
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from .common import database


class Relation(database.Model):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True)
    relation = Column(String, unique=True, nullable=False)
    directed = Column(Boolean, nullable=False)

    assertions = relationship("Assertion", back_populates="relation")


class Dataset(database.Model):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    uri = Column(String, unique=True, nullable=False)

    assertions = relationship("Assertion", back_populates="dataset")


class License(database.Model):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True)
    uri = Column(String, unique=True, nullable=False)

    assertions = relationship("Assertion", back_populates="license")


class Assertion(database.Model):
    __tablename__ = "assertions"
    __table_args__ = (
        UniqueConstraint("relation_id", "source_id", "target_id"),
    )

    id = Column(Integer, primary_key=True)
    relation_id = Column(Integer, ForeignKey("relations.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    surface_text = Column(String)
    surface_source = Column(String)
    surface_target = Column(String)
    weight = Column(Float, nullable=False)

    relation = relationship("Relation", back_populates="assertions")
    source = relationship("Concept", back_populates="as_source_assertions",
                          foreign_keys="Assertion.source_id")
    target = relationship("Concept", back_populates="as_target_assertions",
                          foreign_keys="Assertion.target_id")
    dataset = relationship("Dataset", back_populates="assertions")
    license = relationship("License", back_populates="assertions")
    sources = relationship("Source", back_populates="assertion")


class Source(database.Model):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("assertion_id", "index", "field"),)

    id = Column(Integer, primary_key=True)
    assertion_id = Column(Integer, ForeignKey("assertions.id"), nullable=False)
    index = Column(Integer, nullable=False)
    field = Column(String, nullable=False)
    value = Column(String, nullable=False)

    assertion = relationship("Assertion", back_populates="sources")
