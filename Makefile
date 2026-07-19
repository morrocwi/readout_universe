verify:
	python3 code/LTP1_logic_as_residual_flow.py
	python3 code/LTP2_3_4_battery.py
	coqc code/UPL_Sorites.v
pdf:
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex
all: verify pdf
