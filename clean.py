text=open('lyrics - Copy (2).txt', encoding="utf8").read()
print(text[:100])

replace=[('\xa0',' '),('\ufeff',' '),('\uf608',' '),('\u200b',' '),('–','-'),('—','-'),('―','-'),('‘',"'"),('’',"'"),('“','"'),('”','"'),('″','"')]

for old, new in replace:
    text=text.replace(old, new)

with open("lyrics.txt", "w", encoding="utf-8") as f:
    f.write(text)