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

def build_name( card_id ):
    suitname = card_id.split( '_' )[0]
    valname = card_id.split( '_' )[1]

    return 'CardsFR/card'+dicsuit[suitname]+dicval[valname]+'.svg'

## Ajoute un node au template
def create_file_from_template( node, node_id ):
    # charge le template
    template = ET.parse( 'one_card_template.svg' )
    temproot = template.getroot()
    temproot.append( node )
    template.write( build_name( node_id ))



def update_suit_in_card( card_elem, suitname ):
    ## Reposition the first 2 occurences of '#suitnam' in 'use' child
    ## of the card_elem

    ## card transform
    print( "T={}".format( card_elem.attrib['transform'] ))
    numbers = card_elem.attrib['transform'].split( '(' )[1]
    tok = numbers.split( ',')
    card_x = float(tok[0])
    card_y = float(tok[1].split( ')' )[0])
    print( "  x,y = ({}, {}) => {}".format( card_x, card_y, card_x+card_y ))
    suit_changed = 0
    # change links
    for elem in card_elem.findall( 'svg:use', ns ):
        att_suit = elem.attrib[ns['link']+'href']
        print( "Link=",att_suit )
        # change first two occurence of suitname
        if suit_changed < 2 and att_suit == '#'+suitname:
            suit_changed += 1
            symb_x = float(elem.attrib['x'])
            symb_y = float(elem.attrib['y'])
            elem.set( 'x', str( symb_x + off_x ))
            elem.set( 'y', str( symb_y + off_y ))
        #add fn in front of att_suit
        elem.set( ns['link']+'href', fn+att_suit )
        
    print( "__ After update" )
    for child in card_elem:
        print( child.tag, child.attrib )
    

# charge toutes les définition
alldef = ET.parse( 'svg-cards.svg' )
allroot = alldef.getroot()

# construit tous les noms de carte
allnames = []
for suit in allsuits:
    for val in allvalues:
        allnames.append( suit+'_'+val )

## pour chaque node g id=name, créer un fichier séparé
for gelem in allroot[0].findall( 'svg:g', ns):
    if gelem.attrib['id'] in allnames:
        suitname = gelem.attrib['id'].split( '_' )[0]
        update_suit_in_card( gelem, suitname )
        create_file_from_template( gelem, gelem.attrib['id'] )


        
        
        
    
