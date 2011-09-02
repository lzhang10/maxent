#setup objects
dvi_objs := manual.dvi

objs = $(dvi_objs)

#available commands
all: $(objs)

list:
	@echo '$$(dvi_objs) =' $(dvi_objs)
	@echo '$$(tex_objs) =' $(tex_objs)
	@echo '$$(objs) =' $(objs)

force: ;

ps: $(objs)
	#latex $(basename $(dvi_objs)).tex
	dvips $(dvi_objs)

pdf: $(objs)
	latex $(basename $(dvi_objs)).tex
	dvipdf $(dvi_objs)

html: $(objs)
	latex2html -local_icons -bottom_navigation $(basename $(dvi_objs)).tex

#rules for different file type
$(tex_objs):%.tex:%.ctx
	cct $<

$(dvi_objs):%.dvi:%.tex
	latex $<
	bibtex $(basename $(dvi_objs))
