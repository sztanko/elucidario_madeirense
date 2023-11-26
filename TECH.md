

## Software used:

- PDFMiner https://pypi.org/project/pdfminer/


## Documented discrepancies

### Some artcile titles are hidden

Some artcile titles get not noticed and are in the body of the previous articles

Example:
```
</span><span>Bancos. Têm agencias na Madeira as seguintes instituições de 
```

### Some articles have subchapters

Example: Levadas have many other subtitles, and they are also marked as <b> and they are indistuinguishable from the main headers.

### Some articles have bold text

Example: Origem da Ilha da Madeira., 

```
Pelo «argumento», que a seguir transcrevemos, se pode ajuizar do merecimento da obr<b>a:</b>
```

### Titles have parts in parenthesis, not in the <b> section

They are in italic. But the parenthesis themselves are not italic neither bold.

