# YT overblik

Denne mappe kommer til at indeholde kode til at skabe et tabulært dataset over dine sete videoer på youtube og relevant metadata scrapet via YouTubes egen API. 

Målet er at bruge alt dette data til at gruppere dine sete videoer og give et tematisk overblik over hvad du har set på hvilke tidspunkter. 

```zsh
# alt her køres i terminalen! 
# for at opdatere listen med pakker! 
conda list --export > package-list.txt

# nytilkomne kan lave deres eget conda environment og installere alt sådan her:
conda create -n myenv --file package-list.txt

# put html file of watch history in raw_data/<folder_number>
# first parse html into simple dataframe
python3 create_df/html_parser.py <folder_number> <OPTIONAL: True if watch history is in danish>

# then enrich dataset with info from API – make sure you have enough credentials for the # of videos in watch history
# for most that should be 3-4 credentials top
python3 create_df/api_info.py <folder_number>

# now you can create a barchart-race with
python3 Analyse/bcr.py <folder_number> <OPTIONAL: n_bars><OPTIONAL: cutoff>
# n_bars define how many bars the graph shows 
# cutoff is how many views a channel needs to have across the whole period to show up in the graph

# and create yearly csv matrices for visualizing tag co-occurence networks
python3 Analyse/network.py <folder_number> <OPTIONAL: another period delimiter instead of years – could be Q for quarters>

These csv matrices needs to be visualized in gephi or another software.
```

TODO 
- [ ] Hent længde af videoer og kategori id (og en liste over kategorier indenfor personens land!)
- [ ] Lav et plot over kategoriers andele over tid! 
- [ ] Find ud af hvad der så skal ske :tada: 

Current directory structure
```
.
├── Analyse
│   ├── bcr.py
│   └── network.py
├── README.md
├── cleaned_data
│   ├── 01
│   │   ├── 2021.csv
│   │   ├── 2022.csv
│   │   ├── bcr.gif
│   │   ├── history_df.csv
│   │   ├── history_info_df.csv
│   │   └── missing_tags.csv
│   ├── 02
│   ├── 03
│   ├── 04
│   ├── 05
│   ├── 06
│   ├── 07
│   ├── 08
│   ├── 09
│   ├── 10
├── create_df
│   ├── api_info.py
│   ├── clean_json.py
│   ├── html_parser.py
│   └── test.ipynb
├── credentials
│   ├── credentials1.json
│   ├── credentials2.json
│   ├── credentials3.json
│   ├── credentials4.json
│   ├── credentials5.json
│   └── credentials6.json
├── package-list.txt
├── raw_data
│   ├── 01
│   │   └── watch-history.json
│   ├── 02
│   ├── 03
│   ├── 04
│   ├── 05
│   ├── 06
│   ├── 07
│   ├── 08
│   ├── 09
│   ├── 10
└── results
    ├── 01
    │   ├── 2021.pdf
    │   ├── 2022.pdf
    │   ├── bcr.gif
    │   └── bcr.mp4
    ├── 02
    ├── 03
    ├── 04
    ├── 05
    ├── 06
    ├── 07
    ├── 08
    ├── 09
    ├── 10
```
