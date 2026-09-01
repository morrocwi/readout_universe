from pathlib import Path

SRC = Path('papers/why_we_phobia_RRHM_full_medical_journal_v3.tex')
OUT = Path('papers/why_we_phobia_RRHM_full_medical_journal_arxiv_v1.tex')

src = SRC.read_text(encoding='utf-8')
body = src.split(r'\begin{document}', 1)[1].rsplit(r'\end{document}', 1)[0]

# A standard longtable cannot live inside two-column mode. Give the cross-phobia
# table a dedicated full-width page, then return to two-column text.
body = body.replace(r'\begin{longtable}', r'\onecolumn\begin{longtable}', 1)
body = body.replace(r'\end{longtable}', r'\end{longtable}\twocolumn', 1)

# Let the structured abstract span both columns.
body = body.replace(r'\begin{abstract}', r'\begin{strip}\begin{abstract}', 1)
body = body.replace(r'\end{abstract}', r'\end{abstract}\end{strip}', 1)

preamble = r'''\documentclass[9pt,twocolumn]{article}
\usepackage[a4paper,top=1.35cm,bottom=1.45cm,left=1.45cm,right=1.45cm,columnsep=0.58cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}
\usepackage[scaled=0.92]{helvet}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs,longtable,array,tabularx}
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{cuted}
\usepackage{balance}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{setspace}
\usepackage{etoolbox}

\definecolor{RRHMNavy}{HTML}{17263A}
\definecolor{RRHMSlate}{HTML}{5A6877}
\definecolor{RRHMLight}{HTML}{E9EEF3}
\definecolor{RRHMBlue}{HTML}{315D86}

\hypersetup{
  colorlinks=true,
  linkcolor=RRHMNavy,
  citecolor=RRHMBlue,
  urlcolor=RRHMBlue,
  pdfauthor={Yaoharee Lahtee},
  pdftitle={Why We Phobia? The Regulatory Recoverability Horizon Model of Specific Phobia},
  pdfsubject={Medical Hypothesis / Translational Systems Neuroscience},
  pdfkeywords={specific phobia, systems neuroscience, recoverability, psychophysiology, computational psychiatry}
}

\setlength{\parindent}{1em}
\setlength{\parskip}{0.18em}
\setlength{\columnsep}{0.58cm}
\setlength{\emergencystretch}{1.5em}
\raggedbottom
\sloppy
\allowdisplaybreaks
\setlist{nosep,leftmargin=1.25em}

\titleformat{\section}
  {\sffamily\bfseries\color{RRHMNavy}\large}
  {\thesection}{0.45em}{}
\titleformat{\subsection}
  {\sffamily\bfseries\color{RRHMNavy}\normalsize}
  {\thesubsection}{0.42em}{}
\titleformat{\subsubsection}
  {\sffamily\bfseries\color{RRHMSlate}\small}
  {\thesubsubsection}{0.40em}{}
\titlespacing*{\section}{0pt}{1.0em}{0.38em}
\titlespacing*{\subsection}{0pt}{0.72em}{0.25em}
\titlespacing*{\subsubsection}{0pt}{0.55em}{0.2em}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\sffamily\scriptsize\color{RRHMSlate} WHY WE PHOBIA?}
\fancyhead[R]{\sffamily\scriptsize\color{RRHMSlate} RRHM \textbullet\ MEDICAL HYPOTHESIS}
\fancyfoot[C]{\sffamily\scriptsize\color{RRHMSlate}\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\footrulewidth}{0pt}

\renewenvironment{abstract}
{\small\noindent\textsf{\bfseries\color{RRHMNavy}ABSTRACT}\par\smallskip\noindent}
{\par\vspace{0.5em}}

\captionsetup{font=small,labelfont={bf,sf,color=RRHMNavy}}
\renewcommand{\arraystretch}{1.05}

\title{\vspace{-1.2em}
{\sffamily\bfseries\fontsize{19}{21}\selectfont\color{RRHMNavy} Why We Phobia?}\\[0.38em]
{\sffamily\bfseries\fontsize{12.2}{14}\selectfont The Regulatory Recoverability Horizon Model of Specific Phobia}\\[0.22em]
{\sffamily\fontsize{9.3}{11}\selectfont\color{RRHMSlate} A Translational Systems-Neuroscience Hypothesis for Acquisition, Persistence, Remission, and Relapse}}
\author{\sffamily\bfseries Yaoharee Lahtee}
\date{\sffamily\small 1 September 2026}
'''

OUT.write_text(
    preamble + '\n\\begin{document}\n' + body + '\n\\balance\n\\end{document}\n',
    encoding='utf-8',
)
print(f'Generated {OUT}')
