# YT overblik
This folder includes code to create a tabular dataset from downloaded watch history from YT. It also includes a script to enrich this dataset with more information from YT's API and scripts to create a bar chart race and datsets for tag co-occurence networks.

```zsh
# To update the list of packages 
conda list --export > package-list.txt

# Newcomers can create their own conda environment and install everything needed like this:
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
