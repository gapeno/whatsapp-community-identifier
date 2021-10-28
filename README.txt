#Authors: Gabriel Peres Nobre, Carlos Henrique Gomes Ferreira, Jussara Marques de Almeida
#2021

Script to read a Database file of messages and, in the end, extract user communities based on content co-sharing.

The near duplicate content has been previously indentified in the database file.

Database file columns:
Timestamp, Snapshot ID, Group ID, User ID, Message ID, Type (text, imagem, audio, video), Misinformation Flag

How to run:
1. Install dependencies:
1.1 Networkx module: https://pypi.org/project/networkx/
1.2 Community module: https://python-louvain.readthedocs.io/en/latest/

2. Run the following functions in sequence:
2.1 csv_parser()
2.2 network_generator()
2.3 backbone_extractor()
2.4 community_identifier()
2.5 analysis()
