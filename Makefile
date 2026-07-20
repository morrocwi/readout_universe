COQPATH := -Q evidence URR

verify: verify-urr-coq
	python3 code/LTP1_logic_as_residual_flow.py
	python3 code/LTP2_3_4_battery.py
	coqc code/UPL_Sorites.v

verify-urr-coq:
	coqc $(COQPATH) evidence/RD.v
	coqc $(COQPATH) evidence/DRL_Discrete.v
	coqc $(COQPATH) evidence/DRL_General_Legendre.v
	coqc $(COQPATH) evidence/URR_C_Foundational_Chain.v

pdf:
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex

all: verify pdf
