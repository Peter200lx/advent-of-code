from collections import Counter

DATA = """crruafyzloguvxwctqmphenbkd
srcjafyzlcguvrwctqmphenbkd
srijafyzlogbpxwctgmphenbkd
zrijafyzloguvxrctqmphendkd
srijabyzloguvowcqqmphenbkd
srijafyzsoguvxwctbmpienbkd
srirtfyzlognvxwctqmphenbkd
srijafyzloguvxwctgmphenbmq
senjafyzloguvxectqmphenbkd
srijafyeloguvxwwtqmphembkd
srijafyzlogurxtctqmpkenbkd
srijafyzlkguvxictqhphenbkd
srijafgzlogunxwctqophenbkd
shijabyzloguvxwctqmqhenbkd
srjoafyzloguvxwctqmphenbwd
srijafyhloguvxwmtqmphenkkd
srijadyzlogwvxwctqmphenbed
brijafyzloguvmwctqmphenhkd
smijafyzlhguvxwctqmphjnbkd
sriqafvzloguvxwctqmpheebkd
srijafyzloguvxwisqmpuenbkd
mrijakyuloguvxwctqmphenbkd
srnfafyzloguvxwctqmphgnbkd
srijadyzloguvxwhfqmphenbkd
srijafhzloguvxwctdmlhenbkd
srijafyzloguvxwcsqmphykbkd
srijafyzlogwvxwatqmphhnbkd
srijafyzlozqvxwctqmphenbku
srijafyzloguvxwcbamphenbgd
srijafyzlfguvxwctqmphzybkd
srijafyzloguqxwetqmphenkkd
srijafyylogubxwttqmphenbkd
srijafyzloguvxzctadphenbkd
srijafyzloguoxwhtqmchenbkd
srijafyzloguvxwcvqmzhenbko
srijnfyzloguvxwctqmchenjkd
srijaryzloggvxwctqzphenbkd
srijafhzleguvxwcxqmphenbkd
ssijafyzllguvxfctqmphenbkd
srijafyzloguvxdctqmfhenbcd
srijafyzloguvxfctqmplynbkd
srijaftzlogavxwcrqmphenbkd
sriwaoyzloguvxwctqmphenbtd
srijahyzlogunxwctqmphenbvd
srjjafyzloguzxwctumphenbkd
nrijafyzlxguvxwctqmphanbkd
srijafezlqguyxwctqmphenbkd
srijafygloguvxwjtqcphenbkd
erijafyzloguvxoctqmnhenbkd
ssijafyzllguvxwbtqmphenbkd
sriaafyzloguvxwctqqphenbkv
frijafyzloguvswctwmphenbkd
srijafyzyogkvxwctqmprenbkd
syijafyzuoguvxwctqmkhenbkd
srijafyzloganxwctqmphenbkf
srijafyzloguvxwftqmxhenbkq
srijafyflogxvxwctqmghenbkd
srijafyzsoguvxwctqmpjenwkd
srujafylloguvxwctqmphenckd
srijafyzlpzuvxwctqmphenbud
srijafyzlogfvxwctqmhhenbwd
srijafjzlogusxwctqmphepbkd
srijlfyzloguvxwctqfphenzkd
srijafyzlogwvxwctqyphenbqd
srijafyzloluvxwctqtphenukd
srizafyzlowuvxwctqmphqnbkd
sritafkzlkguvxwctqmphenbkd
sbijafdzloguvxgctqmphenbkd
crijafyeloguvxwctqmpsenbkd
srijafyvlogulxwctqmphenbkk
srijafyologuvxwctqmehegbkd
siijafyzloguvxwctjmphenbmd
srijafyzlupuvxwctqmpheabkd
srijafyzlogumxwctqqphanbkd
srijxfyzlogujxwcqqmphenbkd
irijafizeoguvxwctqmphenbkd
sgijafyzloguvtwctqmpfenbkd
srijzfyzloguvmwctnmphenbkd
srijafyzwohuvxwctqmthenbkd
srijafyzlhguvxoctqwphenbkd
srgjafyplogxvxwctqmphenbkd
srijafyqlogovxwctqzphenbkd
srijafjzloguvlnvtqmphenbkd
srijafyzooguvxwctqmphenvud
srijafyzgoguvxwctumphgnbkd
srijaffzloguvxwdqqmphenbkd
srijafyzlogugxwctqxphenbkr
srijafyzlogutxwctqmmcenbkd
srifafyzlhguwxwctqmphenbkd
mrimajyzloguvxwctqmphenbkd
sriyafyzloguvxwcthmphejbkd
srieakyzlokuvxwctqmphenbkd
srisafyzloguhxwctqmphecbkd
srijanyzloguvxcctqmxhenbkd
srijafyzypguvxwctqmqhenbkd
sryjtfyzlvguvxwctqmphenbkd
srijafyzlsguvxwctqmqfenbkd
srijafyzlogudxwbtqwphenbkd
srijysyzloguvxwctqmpvenbkd
srijafyzloggvxwjtqmphegbkd
srijgfyzloguvxwctqmbhdnbkd
ssijufyzloguvawctqmphenbkd
skojafyzloguvxwctqmphenbnd
srijafylloguvxwcqqmpienbkd
trioafyzloguvqwctqmphenbkd
srijafydloguvxwctqmpzjnbkd
saijafvzloguvxwcqqmphenbkd
srhjapyzloguvxwctqmbhenbkd
srijafyzlfguvxwcsqmpwenbkd
shijafyzboguvxwctqmphenbmd
srizafysloguvxwrtqmphenbkd
srijafyzloguvxwciqmwhenbkj
qrijafyzloduvxwctqmphenbko
srijefyuloguvxwctqmphenbed
srijafyzlobuvxwctqmphenhbd
srijafyzloxuvxwctqmpheabkq
srijafyzloguvrwctqmghenkkd
sfisafywloguvxwctqmphenbkd
srgjafyzlogurxwctqmphenbkp
srijafhzloguvxwcjqmphenhkd
srijafyylogufxwrtqmphenbkd
srijafyzvoguvxwzkqmphenbkd
sqijafyzloguvxwctqmpheqbxd
srijafyvloguvxwctqzpherbkd
srijufyzloguvxlcsqmphenbkd
srijafykloguvxlccqmphenbkd
srijafyzloguexwcrqmphenzkd
sridifyzloguyxwctqmphenbkd
srijafyzlogfvxwctqlphenbkl
srijafyzlodqdxwctqmphenbkd
srijafyzloruvxactqmphenekd
grijafyzloguvxpctmmphenbkd
srsjakyzloguvxwctqmphvnbkd
srikafyvloguvxwrtqmphenbkd
srijafyzloguvxwctqjpserbkd
jrijafyzloguvxwctqmpgesbkd
swijafyzluguvxwctqmfhenbkd
srijanynlogovxwctqmphenbkd
jrijafyzloguvxwctymphrnbkd
srinafyzloguvewctqmphenbzd
srijakyzloguvxwctqmphcnbka
srijafyhlobuvxwctqmphenbka
srijafyzcogusxwctqmphwnbkd
srijavyzlosuvxwctqmphjnbkd
orijafyzxoguvxwcnqmphenbkd
srijafyzlogcvxwvtqmthenbkd
srijapyzloauvxwctqmphenvkd
srijaflzloguhxwctqmphenbwd
smijafyzlonuvxwctqmphenbkw
jrijafyzloguvxwclqmnhenbkd
srijaqyzloguvqwctqmphenskd
srijasyzloguvxwctqmvhenbku
crijtfyzloguvxwctqmthenbkd
srrkafyzvoguvxwctqmphenbkd
srijatyzloguvewctqmphenbld
srfjafyyloguvnwctqmphenbkd
srijafyzloguvxwctqjpbenbkt
hrijafyzooguvxwctqmphenbld
srijafbzlogscxwctqmphenbkd
srinafyzlogxvxwctqqphenbkd
slijafyzloglvxwctqmphenbdd
srijafyzlogjvxwcsqmphenbld
sryjcfyzloguvewctqmphenbkd
srijafyzloguexwctqmohknbkd
jaijafyzlogevxwctqmphenbkd
srijafbzlogavxwctqmphenbki
srijafozlogpvxwctqmphgnbkd
srijdfyzloguvxwczqmphenbkm
srijafyzlobuvxwctqmphxndkd
mrijifyzlhguvxwctqmphenbkd
srijafyzloguvxbctumphjnbkd
srijafyzloyuvxwptqmphlnbkd
arijafyzloguvxwcsqmohenbkd
srijaftzioguvxwttqmphenbkd
srijafyzlqsuvxwctqmphxnbkd
srijafyzioguvxwctqnphetbkd
prijafbzloguvxdctqmphenbkd
srijaeyzlnguvxwmtqmphenbkd
srijofyzloguvqwctqmphonbkd
srixaryzpoguvxwctqmphenbkd
srijafyzlowuvxwcwhmphenbkd
srijafydloguvxwctqmptenikd
srijqfyzlogtvfwctqmphenbkd
srijafyzloguvxlctqmpvenbgd
srijafyzlbguvxwjtqgphenbkd
srijafyzlohuqxwctqmphenbka
srijafyzroguvxictqmphynbkd
srijafyzloguvxdctjmphenjkd
srijaoczloguvxwctqmphenbjd
srajafhzloguvxwctqmphenbke
srijofyzloduvxwctqmphanbkd
srijafytloguvxwmtnmphenbkd
srijafyzuoguvxwceqmpgenbkd
rrijafyzloyuvxwctqmphlnbkd
srljafyzloguvxictqmohenbkd
srijafyzlogulxwcrqrphenbkd
srajafyzloguvxwctqmphanbke
srijafyzlhguvxwxtqmpheabkd
sxijafyzloggwxwctqmphenbkd
srijafyultguvxwctqmphinbkd
srijafyzloguvtwctqmfhvnbkd
srijafwzloruvxwctquphenbkd
srbjafyzxoguuxwctqmphenbkd
erijafyzlxguvxbctqmphenbkd
srijagyzlojubxwctqmphenbkd
srijafyzloguvxwdtqmchenakd
srijafkzlogukxwctqiphenbkd
mridafyzloguvxwctqmphenrkd
szqjafyzloguvxwctqmpheibkd
srijahyzloguvxwctcmphenekd
srijafyzloguvxwczpuphenbkd
srijafyzcoguvfwctqmphenbkq
qriiafyzloguvxwctqmpheebkd
srijpfyzloguvxlctqmphenokd
srijzfyzlotuvxwcjqmphenbkd
srinafyqloguvxwctfmphenbkd
srijafyzlogjvxpltqmphenbkd
srijafyzlotuvxwutqmphenbtd
sridafyzloguvxwctqmpyenokd
srxjafyzqogyvxwctqmphenbkd
ssijafyzzoguvxwctqmphenbad
srijafrzloguvxwctqmphekpkd
srijafyzlfgrvxactqmphenbkd
srijafyzroguvxwttqmphekbkd
srijefyzloguvxwctqmpqenbrd
srijefycloguvxwctqmchenbkd
srzjafyzloguvxwcqqmphanbkd
srijauyzlhguvxwctqmphenbgd
srijafyzloguvmwvnqmphenbkd
srihafyzloguvlwotqmphenbkd
srigafyzloguvxwctqmphennsd
sriuafzzloguvxwcuqmphenbkd
srijavuzllguvxwctqmphenbkd
srijafjzloguvlnctqmphenbkd
lrirafyzloguvxwctqmphenbld
soijarxzloguvxwctqmphenbkd
srijapyzlnguvxwctqmdhenbkd
srijafyzkogujxmctqmphenbkd
srijafuzloguvxwcsqvphenbkd
srijagyzzoguvxwctqmpvenbkd
srijafyzlovuvxwctqmrhenbxd
srijafyzqoguvxwctwmpienbkd
sxijafyzloguvxwutqmphenlkd
srijafyzlhgzvxwctqmphqnbkd
srijajyzloguvxwcbwmphenbkd
srijazyzloguvxwhtqmphenbkx
srgjafyzloguvvwctqmphdnbkd
rrivafyzloguvxjctqmphenbkd
srijifyzdoguvxwctqmphenbka
hrijafyzloguvxectqmpheybkd""".split('\n')


def checksum_n(box, n):
    counts = Counter(box)
    if n in counts.values():
        return 1
    return 0


def part_2(box):
    for string in box:
        for string2 in box:
            if string == string2:
                continue
            mismatch_loc = []
            for i, c in enumerate(string):
                if string2[i] == c:
                    continue
                mismatch_loc.append(i)
            if len(mismatch_loc) == 1:
                return string[:mismatch_loc[0]] + string[mismatch_loc[0] + 1:]


if __name__ == '__main__':
    print(sum([checksum_n(s, 2) for s in DATA]) * sum([checksum_n(s, 3) for s in DATA]))
    print(part_2(DATA))
