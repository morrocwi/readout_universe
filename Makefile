COQPATH := -Q evidence URR

verify: verify-urr-coq verify-native
	python3 code/LTP1_logic_as_residual_flow.py
	python3 code/LTP2_3_4_battery.py
	coqc code/UPL_Sorites.v

verify-urr-coq:
	coqc $(COQPATH) evidence/RD.v
	coqc $(COQPATH) evidence/DRL_Discrete.v
	coqc $(COQPATH) evidence/DRL_General_Legendre.v
	coqc $(COQPATH) evidence/URR_C_Foundational_Chain.v
	coqc $(COQPATH) evidence/DRL_General_EL.v
	coqc $(COQPATH) evidence/DRL_Finite_Cut_Balance.v
	coqc $(COQPATH) evidence/DRL_Forced_Master.v
	coqc $(COQPATH) evidence/DRL_Hidden_Elimination_Convolution.v
	coqc $(COQPATH) evidence/DRL_NoGo_Single_Field.v
	coqc $(COQPATH) evidence/RetentionLoopClosureMonotone.v

verify-native:
	python3 -m pytest -q tests/test_omega_all.py tests/test_claim_ir.py tests/test_native_logic.py tests/test_from_omega.py

pdf:
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex

all: verify pdf
