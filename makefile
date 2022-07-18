
NAME = main
PDF = $(NAME).pdf
MAIN = $(NAME).tex
BBL = $(NAME).bbl
AUX = $(NAME).aux
TEX := $(wildcard tex/*.tex)
BIB = bib/bibliography.bib

all: $(PDF)

$(PDF): $(TEX) $(MAIN) $(BBL) 
	pdflatex $(MAIN)
	pdflatex $(MAIN)

.PHONY: bib
bib: $(BBL)

$(BBL): $(BIB) | $(AUX)
	pdflatex $(MAIN)
	biber -W $(AUX)

$(AUX):
	pdflatex $(MAIN)

clean:
	rm -f *~ *.log *.nav *.out *.snm *.toc
	rm $(AUX)
	rm $(BBL)

cleanall:
	make clean
	rm -f *.pdf
	rm -f *.bbl
		
