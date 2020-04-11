# Copyright (c) 2020 Hecong Wang
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

CONCEPTNET_TARGET = demo/data/conceptnet-assertions-5.7.0.csv.gz
CONCEPTNET_SOURCE = 'https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz'

DATABASE_TARGET = demo/data/database.sqlite
DATABASE_SOURCE = demo/database.py
DATABASE_DEPEND = demo/app.py demo/models/*.py demo/data/*.csv

.PHONY: all clean

all: $(DATABASE_TARGET)

clean:
	rm -f $(CONCEPTNET_TARGET) $(DATABASE_TARGET)

$(CONCEPTNET_TARGET):
	wget --quiet --timestamping --show-progress --directory-prefix $(@D) \
	$(CONCEPTNET_SOURCE)

$(DATABASE_TARGET): $(CONCEPTNET_TARGET) $(DATABASE_SOURCE) $(DATABASE_DEPEND)
	python $(DATABASE_SOURCE) $(CONCEPTNET_TARGET) $(@D)
