'''devlog:
17-11-15 18.00 - 19.30
JPM: Kuvaus, metodit, metodien kuvakset, main-metodi
18-11-15 19.00 - 21:00
JPM:
lueLokiTiedosto() - valmis
JPM:
19-11-15 12:30 - 16:30
valmiiksi

parityo

tuntirapottiohjelma

Input:
tekstitiedosto, jossa kirjautumisloki
#muoto: kirjautumiset.txt

Output:
kirjautumisloki-kopio - vanhat lokitiedostot jaavat talteen.
#muotoa: kirjautumiset_210315-280315.txt

tuntiraportti - viimeisimman aikavalin kirjautumiset ja niista lasketut tyotunnit
#muotoa: tyotuntiraportti_210315-280315.txt

Selite:
Raportit luodaan tietyin aikavalein - esim. joka viikon maanantaina klo 01:00.
Talloin raportti luodaan edellisen viikon kirjautumistiedoista.

Raportista ilmenee jokaisen tyontekijan kunakin paivana tekemat tyotunnit.
Lisaksi tyontekijan tyotunnit lasketaan yhteen palkkajakson 
'''
import time
from datetime import date
from datetime import timedelta
from datetime import datetime


def main():
    lokiTiedotStr= lueLokiTiedosto()
    
    #tallennaTiedostoPvmLeimalla(lokiFile, tiedostonimi)
    #tehdaan tiedoston pvmLeimalla tallennus lueLokiTiedosto-metodin sisalla
    raporttiTiedot = lokiListaSanakirjaksi(lokiTiedotStr)
    #print('main')
    #print(raporttiTiedot)
    raportti = luoRaportti(raporttiTiedot)
    tallennaRaportti(raportti)
    #print(raportti)
    
	
def lueLokiTiedosto():
    '''Lukee tiedoston ja palauttaa sen sisalto str-muodossa

    Lokitiedosto kirjautumiset.txt luetaan pythonin str-muuttujaan.
    Kirjautumiset.txt oltava ohjelman kanssa samassa hakemistossa.

    Returns:
    tiedoston sisalto str-muodossa
    '''

    #lue file-muuttujaan
    #tallennaTiedostoPvmLeimalla
    #tallenna file riveittain listaan
    #sulje file
    #palauta lista

    #avataan tiedosto
    tiedosto_nimi = 'kirjautumiset.txt'
    tiedosto_olio = open('kirjautumiset.txt', 'r')
    #tiedoston sisalto talteet
    tiedosto_str = tiedosto_olio.read()
    tiedosto_olio.close()

    #tallennetaan tiedoston sisalto talteen uudella nimella
    #tiedostonimeen lisataan edellisen paivan pvm
    tallennaTiedostoPvmLeimalla(tiedosto_str, tiedosto_nimi)

    #luodaan uusi tyhja kirjautumislokitiedosto
    '''
    #kirjautumiset.txt tyhjennys
    tiedosto_olio3 = open('kirjautumiset.txt', 'w')
    tiedosto_olio3.close()
    '''
    #poistetaan viimeinen rivivaihto
    tiedosto_str = tiedosto_str.rstrip('\n')
    #palautetaan kirjautumistiedot str-muodossa
    return tiedosto_str
    


	
def tallennaTiedostoPvmLeimalla(tiedosto_str, tiedosto_nimi):
    '''Tallentaa merkkijonon .txt-tiedostoksi lisaten aikaleiman tiedostonimeen

    Tiedosto tallennetaan sellaisenaan samaan kansioon ohjelman kanssa.
    Parametri tiedostonimi on muodossa 'kirjautumiset.txt'
    Tiedosto tallentaan muodossa 'kirjautumiset_210315.txt'
    Lisattava aikaleima on ohjelman ajohetkesta edellinen (eilinen) paiva.

    Ohjelma ajetaan maanantaisin, leimaksi tultava edellisen viikon viimeinen paiva.

    Keyword arguments:
    tiedostoStr - tallennettava .txt-tiedosto merkkijonona
    tiedostonimi - str, johon lisattaan aikaleima

    Returns:
    -
    '''
    #lisataan tiedostonimeen eilisen pvm
    eilisenPvm = yesterdaysDateString()
    tiedosto_nimi = tiedosto_nimi[:-4] + '_' + eilisenPvm + '.txt'

    #tallennetaan tiedoston sisalto uudelleen nimettyyn tiedostoon
    tiedosto_olio = open(tiedosto_nimi, 'w')
    tiedosto_olio.write(tiedosto_str)
    tiedosto_olio.close()

def yesterdaysDateString():
    today = date.today()
    one_day = timedelta(days=1)
    yesterday = today - one_day
    yesterday = yesterday.strftime("%d%m%y")
    return yesterday

def getLastMondayStr():
    today = date.today()
    one_day = timedelta(days=7)
    maanantai = today - one_day
    maanantai = maanantai.strftime("%d%m%y")
    return maanantai

def lokiListaSanakirjaksi(lokiTietoStr):
    '''Muuttaa lokiTieto merkkijonon sanakirjaksi

    Parametrina annettava lokiTietoStr on merkkijono.
    Kirjautumistiedot ovat muodossa:
    id in dd-mm-yy hh.mm
    #selite:
    (tyontekijaID) ('in'/'out' -sisaan tai uloskirjautuminen) (pmv) (klo)
    tietoalkiot erotettu valilyonnilla

    Rivien sisalto tallennetaan sanakirjaan seuraavasti:
    key = int id
    data = object[] loggauslista

    id: luetaan rivin alusta ja muutetaan kokonaisluvuksi
    loggauslista: ko. id:n tekemat kirjautumiset listana, jonka alkiot tupleja.
            tuple sisaltaa: (srt suunta, datetime ajankohta)
                    suunta: 'in' tai 'out'
                    ajankohta: pvm ja klo datetime-muotoon muutettuna (str:sta)

    Kirjatumiset ovat valmiiksi jarjestyksessa lokiTiedostossa.
    Ne tulevat listaan automaattisesti jarjestykseen appendilla.

    Keyword arguments:
    lokiTiedosto - Str

    Returns:
    Sanakirja - kirjautumistiedot dictionary-tietorakenteessa
    '''
    #print('moi!')
    sanakirja = {}
    lokiTietoLista = lokiTietoStr.split('\n')
    for rivi in lokiTietoLista:
        rivilistana = rivi.split(' ')
        

        hloID= rivilistana[0]
        suunta = rivilistana[1]
        pvm = rivilistana[2]
        klo = rivilistana[3]
        aikaleima = pvmKloStrToDateTime(pvm, klo)

        #print(aikaleima)

        sanakirja = lisaaAvainSanakirjaan(sanakirja, hloID)

        lisaaDataSanakirjaan(sanakirja, hloID, suunta, aikaleima)
    #print('keys:')
    #print(sanakirja.keys())
    #print(sanakirja.values())
    #print(sanakirja)
    #for alkio in sanakirja.values():
    #    print(alkio)
    #    print('value')
    return sanakirja

def lisaaDataSanakirjaan(sanakirja, hloID, suunta, aika):
    '''Lisaa kirjautumisdata sanakirjaan
    
    tapaukset:

    ensimmainen: hlon kirjautumislista on tyhja
    
    normaali: edellinen suunta eri

    virhe: edellinen suunta sama

    -oletetaan etta suunta on aina oikein
    -mahdollinen virhe johtuu unohtuneesta kirjautumisesta

    Keyword arguments:
    sanakirja - dictionary johon data lisataan
    hloID - str, kenen kirjautminen lisataan
    suunta - 'in' tai 'out'
    aika - datetime muodossa (pvm+klo)
    '''
    hlonKirjautumisetLista = sanakirja[hloID]
    if not hlonKirjautumisetLista: #python: empty sequence is false
        if (suunta == 'out'):
            sanakirja[hloID].append(['in', aika])
            sanakirja[hloID].append(['out', aika])
        elif (suunta == 'in'):
            sanakirja[hloID].append(['in', aika])
    else:
        viimeisinKirjautuminen = hlonKirjautumisetLista[-1]
        viimeisinSuunta = viimeisinKirjautuminen[0]
        viimeinenAika = viimeisinKirjautuminen[1]
        
        #joku kirjautuminen jaanyt tekematta
        if (viimeisinSuunta == suunta):
            #aamulla kirjautuminen unohtunut
            if (viimeisinSuunta == 'out'):
                #aamulle luodaan haamukirjautuminen
                sanakirja[hloID].append(['in', aika])
                #normaali uloskirjautuminen
                sanakirja[hloID].append(['out', aika])
            #"eilisillan uloskirjautuminen unohtunut"
            elif (viimeisinSuunta == 'in'):
                #luodaan eiliselle haamukirjautuminen
                #ajaksi tulee eilisaamun aika
                sanakirja[hloID].append(['out', viimeinenAika])
                #normaali sisaankirjautuminen
                sanakirja[hloID].append(['in', aika])
        else:
            #suunta eri kuin viimeisin, normaali lisays
            sanakirja[hloID].append([suunta, aika])

    #print(sanakirja)        
    return sanakirja            
		
def lisaaAvainSanakirjaan(sanakirja, avain):
    if (avain not in sanakirja):
        sanakirja[avain] = []
    return sanakirja


def pvmKloStrToDateTime(pvm, klo):
    aika = pvm + ' ' + klo    
    aikaleima = datetime.strptime(aika, "%d-%m-%y %H:%M")
    return aikaleima

def tallennaRaportti(merkkijono):
    sunnuntai = yesterdaysDateString()
    maanantai = getLastMondayStr()
    tiedostonimi = 'raportti_' + maanantai + '-' + sunnuntai + '.txt'
    tiedosto = open(tiedostonimi, 'w')
    tiedosto.write(merkkijono)
    tiedosto.close()
    
def luoRaportti(raporttiTiedot):
    '''Luo txt-raportin tyotunneista

    Luo txt.raportin sanakirjan sisaltamista tyotunneista muodossa:

    #otsikkoalue
    otsikko: tyotuntiraportti
    yrityksen nimi
    pvm - pvm

    #taulukointi tyotunneista henkiloittain, sarakkeet:
    id		pvm		in		out		total
    (int)	(date)	(time)	(time)	(h)

    #yhteenvetoalue
    id		tunnit-yht

    Keyword arguments:
    raporttiTiedot - sanakirja, jossa key=id, data=lista, jonka alkio sisaltaa: 
    (str, date-time) -pareja (tuple)

    Returns:
    -
    '''
    raportti = ''
    raportti += 'Firma Oy\n'
    sunnuntai = yesterdaysDateString()
    #voisi hakea pvmt sanakirjasta tms
    maanantai = getLastMondayStr()
    raportti += maanantai + '-' + sunnuntai + '\n\n'
    raportti += 'id\tpvm\t\tsisaan\tulos\ttunnit\n'
    avaimet = raporttiTiedot.keys()

    #print(raportti)
    #print(avaimet)
    #kaydaan henkilot lapi
    for avain in avaimet:
      
