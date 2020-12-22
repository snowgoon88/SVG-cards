#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Permet de créer un fichier .svg par cartes qui correspong au produit cartésien
de 'allvalues' x 'allsuits', à partir du fichier "svg-cards.svg"

On peut ensuite transformer en pnb avec la commande
$> inkscape --export-png=filename.png -w 140 -h 190 filename.svg

Voir ./to_png.sh
"""

import xml.etree.ElementTree as ET 

ns = { 'svg' : 'http://www.w3.org/2000/svg',
       'link' : '{http://www.w3.org/1999/xlink}' }
fn = 'svg-cards.svg'
off_x = -18
off_y = +40

dicval = { '1':'A', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6',
           '7':'7', '8':'8', '9':'9', '10':'10',
           'jack':'J', 'queen':'Q', 'king':'K'}
dicsuit = { 'club': 'Clubs', 'spade':'Spades', 'diamond':'Diamonds',
            'heart':'Hearts'}

allvalues = [ "1", "2", "3","4", "5", "6", "7", "8", "9", "10",
              "jack", "queen", "king" ]
allsuits = [ "club", "spade", "heart", "diamond" ]

an = [ "club_1", "diamond_1", "diamond_10", "spade_jack" ]

# *********************************************************************** ALLREF
# charge toutes les définition
alldef = ET.parse( 'svg-cards.svg' )
allroot = alldef.getroot()
        
# ******************************************************************************
# ************************************************************************* HBAR
hbar_elem = None
## Find the element with a single horizontal in the jack of spade
for gelem in allroot[0].findall( 'svg:g', ns):
    if gelem.attrib['id'] == "spade_jack":
        hbar_elem = gelem[1]

print( "__HBAR ***************** ")
for child in hbar_elem:
    print( child.tag, child.attrib )

# remove the verical bar
vbar1 = hbar_elem[0]
vbar2 = hbar_elem[3]
hbar_elem.remove( vbar1 )
hbar_elem.remove( vbar2 )

print( "__ vbar removed ")
for child in hbar_elem:
    print( child.tag, child.attrib )

# update hbar
print( "__update" )
hbar1 = hbar_elem[0]
print( "  "+hbar1.attrib['d'])
hbar1.set( 'd', "m 1815.0,497.745 -100.0,0" )
hbar2 = hbar_elem[1]
hbar2.set( 'd', "m 1705.0,731.682 100.0,0" )
print( "__new ")
for child in hbar_elem:
    print( child.tag, child.attrib )

def update_hbar( base_x, base_y ):
    hb1_str = "m {},{} -100,0".format( base_x+140, base_y-232 )
    hb2_str = "m {},{} 100,0".format( base_x+30, base_y+2 )
    hbar1.set( 'd', hb1_str )
    hbar2.set( 'd', hb2_str )
# ******************************************************************************


def build_name( card_id ):
    suitname = card_id.split( '_' )[0]
    valname = card_id.split( '_' )[1]

    return 'CardsFR/card'+dicsuit[suitname]+dicval[valname]+'.svg'
    #return 'newcard'+dicsuit[suitname]+dicval[valname]+'.svg'

## Ajoute un node au template
def create_file_from_template( node, node_id ):
    # charge le template
    template = ET.parse( 'one_card_template.svg' )
    temproot = template.getroot()
    temproot.append( node )
    template.write( build_name( node_id ))



def update_suit_in_card( card_elem, suitname, valname ):
    ## Reposition the first 2 occurences of '#suitnam' in 'use' child
    ## of the card_elem

    ## card transform
    print( "T={}".format( card_elem.attrib['transform'] ))
    numbers = card_elem.attrib['transform'].split( '(' )[1]
    tok = numbers.split( ',')
    card_x = float(tok[0])
    card_y = float(tok[1].split( ')' )[0])
    print( "  x,y = ({}, {}) => {}".format( card_x, card_y, card_x+card_y ))
    elem_base = None
    suit_changed = 0
    # change links
    for elem in card_elem.findall( 'svg:use', ns ):
        att_suit = elem.attrib[ns['link']+'href']
        print( "Link=",att_suit )
        # mark elem to remove
        if att_suit == '#base':
            elem_base = elem
        # change first two occurence of suitname
        if suit_changed < 2 and att_suit == '#'+suitname:
            suit_changed += 1
            symb_x = float(elem.attrib['x'])
            symb_y = float(elem.attrib['y'])
            elem.set( 'x', str( symb_x + off_x - 120)) # to other corner
            elem.set( 'y', str( symb_y + off_y ))
        #add fn in front of att_suit
        elem.set( ns['link']+'href', fn+att_suit )

    # remove the black card border => not needed, stroke is in white now
    # card_elem.remove( elem_base )

    # remove previous bar if needed
    if valname in ["jack", "queen", "king"]:
        bar_elem = card_elem[1]
        card_elem.remove( bar_elem )
    
    # then insert hbar
    update_hbar( float(elem_base.attrib['x']), float(elem_base.attrib['y']) )
    card_elem.insert( 1, hbar_elem )
    
    print( "__ After update" )
    for child in card_elem:
        print( child.tag, child.attrib )
    
    
# construit tous les noms de carte
allnames = []
for suit in allsuits:
    for val in allvalues:
        allnames.append( suit+'_'+val )
#allnames = an

## pour chaque node g id=name, créer un fichier séparé
for gelem in allroot[0].findall( 'svg:g', ns):
    if gelem.attrib['id'] in allnames:
        suitname = gelem.attrib['id'].split( '_' )[0]
        valname = gelem.attrib['id'].split( '_' )[1]
        update_suit_in_card( gelem, suitname, valname )
        create_file_from_template( gelem, gelem.attrib['id'] )


        
        
        
    
