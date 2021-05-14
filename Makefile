.PHONY : all

login=xdolejsi

folder=src

TASKS=message forest race

define make_executable
chmod 775 $(folder)/$1.py;
cp src/$1.py $1;
endef

define convert_eol
dos2unix $1;
endef

define delete
rm $1;
endef

build:
	$(foreach task,$(TASKS),$(call make_executable,$(task)))
	$(foreach task,$(TASKS),$(call convert_eol,$(task)))

clear:
	$(foreach task,$(TASKS),$(call delete,$(task)))

all:
	build
