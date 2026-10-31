"""Question record shared by the data files."""
from dataclasses import dataclass, field

PAPERS = {
    'p0': 'BITS Goa 2024',
    'p1': 'BITS Hyderabad 2024',
    'p2': '2025 paper (campus not named)',
    'p3': 'BITS Hyderabad 2025',
    'p4': 'Delhi campus 2024',
    'p5': 'IIIT Delhi 2025',
    'p6': 'IISc 2024',
    'p7': 'NIT Durgapur',
}

# The source PDFs, in the order of the p0..p7 keys above.
FILES = {
    'p0': 'QUALCOMM (BITS GOA_24).pdf',
    'p1': 'QualComm 24 BITS Hyd.pdf',
    'p2': 'Qualcomm 2025_250610_125802.pdf',
    'p3': 'Qualcomm 25-BITSHyd.pdf',
    'p4': 'Qualcomm-DLHI.pdf',
    'p5': 'Qualcomm_2025_iiitd.pdf',
    'p6': 'Qualcomm_IISc_24[1].pdf',
    'p7': 'Qualcomm_NIT Durgapur .pdf',
}


@dataclass
class Q:
    topic: str
    src: list
    text: str
    opts: list
    ans: object
    expl: str
    conf: str = 'high'
    note: str = ''
    fig: str = ''
    code: str = ''
    table: str = ''
    figcap: str = ''
    extra: dict = field(default_factory=dict)
