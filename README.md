# YT overblik

Denne mappe kommer til at indeholde kode til at skabe et tabulært dataset over dine sete videoer på youtube og relevant metadata scrapet via YouTubes egen API. 

Målet er at bruge alt dette data til at gruppere dine sete videoer og give et tematisk overblik over hvad du har set på hvilke tidspunkter. 

```zsh
# alt her køres i terminalen! 
# for at opdatere listen med pakker! 
conda list --export > package-list.txt

# nytilkomne kan lave deres eget conda environment og installere alt sådan her:
conda create -n myenv --file package-list.txt
```

TODO 
- [X] Hent video beskrivelsen via api
- [ ] Forsøg med hSBM til inddeling af videoer
- [ ] Find ud af hvad der så skal ske :tada: 