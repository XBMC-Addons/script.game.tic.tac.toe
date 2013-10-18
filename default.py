
# script constants
__script__       = "Tic Tac Toe"
__addonID__      = "script.game.tic.tac.toe"
__author__       = "Frost"
__url__          = "http://code.google.com/p/passion-xbmc/"
__svn_url__      = "http://passion-xbmc.googlecode.com/svn/trunk/addons/script.game.tic.tac.toe/"
__credits__      = "Team XBMC, http://xbmc.org/"
__platform__     = "xbmc media center, [ALL]"
__date__         = "16-12-2010"
__version__      = "1.0.2"
__svn_revision__ = "$Revision: 916 $"


#Modules general
import os
import sys
import random
from traceback import print_exc

#Modules XBMC
import xbmc
import xbmcgui
import xbmcaddon

 
__addon__ = xbmcaddon.Addon( __addonID__ )
__language__ = __addon__.getLocalizedString

CWD = os.getcwd().rstrip( ";" )


def getUserSkin():
    current_skin = xbmc.getSkinDir()
    force_fallback = os.path.exists( os.path.join( CWD, "resources", "skins", current_skin ) )
    if not force_fallback: current_skin = "Default"
    return current_skin, force_fallback


#class TTT( xbmcgui.WindowXML ):
class TTT( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        #xbmcgui.WindowXML.__init__( self, *args, **kwargs )
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

        # XBMC Artificial Intelligence
        self.xbmc_art = XBMC_ART( self )

        self.fanart_win = False

    def set_button_hard( self, statut=1 ):
        #self.getControl( 350 ).setSelected( 0 )
        self.getControl( 350 ).setEnabled( statut )
        self.getControl( 350 ).setVisible( statut )

    def onInit( self ):
        try:
            self.resetScores()
            self.resetContainer()
            self.player_vs_who = ( "XBMC", "P2", )[ 0 ]
            self.list_item.setProperty( "toplay", __language__( 32100 ) )
        except:
            print_exc()
            raise

    def resetScores( self ):
        self.score_player_one = 0
        self.score_player_two = 0

    def resetContainer( self ):
        self.getControl( 150 ).reset()
        self.list_item = xbmcgui.ListItem( "Container" )

        if self.fanart_win:
            self.list_item.setProperty( "fanart_win", "fanart_win.png" )

        #player images selected
        self.list_item.setProperty( "L1R1", "" )
        self.list_item.setProperty( "L1R2", "" )
        self.list_item.setProperty( "L1R3", "" )
        self.list_item.setProperty( "L2R1", "" )
        self.list_item.setProperty( "L2R2", "" )
        self.list_item.setProperty( "L2R3", "" )
        self.list_item.setProperty( "L3R1", "" )
        self.list_item.setProperty( "L3R2", "" )
        self.list_item.setProperty( "L3R3", "" )

        #lines win
        self.list_item.setProperty( "Line1win", "" )
        self.list_item.setProperty( "Line2win", "" )
        self.list_item.setProperty( "Line3win", "" )
        self.list_item.setProperty( "Line4win", "" )
        self.list_item.setProperty( "Line5win", "" )
        self.list_item.setProperty( "Line6win", "" )
        self.list_item.setProperty( "Line7win", "" )
        self.list_item.setProperty( "Line8win", "" )

        #others properties
        self.list_item.setProperty( "haswinner", "" )
        self.list_item.setProperty( "playerIItoplay", "" )
        self.list_item.setProperty( "score_player_one", str( self.score_player_one ) )
        self.list_item.setProperty( "score_player_two", str( self.score_player_two ) )

        self.getControl( 150 ).addItem( self.list_item )

        #default values for start new game
        self.winner = False
        self.player_to_play = 1
        self.player_images = "X.png", "player_one.png"
        self.list_item.setProperty( "toplay", __language__( 32102 ) )
        self.tilesID = {
            "L1R1": 11, "L1R2": 12, "L1R3": 13,
            "L2R1": 21, "L2R2": 22, "L2R3": 23,
            "L3R1": 31, "L3R2": 32, "L3R3": 33
            }
        self.tiles = TILES()
        self.first_round = False
        xbmc.sleep( 100 )

    def onFocus( self, controlID ):
        pass

    def onClick( self, controlID ):
        try:
            if not self.xbmc_art._is_playing:
                if controlID in ( 11, 12, 13, 21, 22, 23, 31, 32, 33 ):
                    if self.tilesID and not self.winner:
                        L, R = list( str( controlID ) )
                        property =  "L%sR%s" % ( L, R, )
                        self.list_item.setProperty( property, self.player_images[ 1 ] )
                        xbmc.sleep( 500 ) # used for default skin
                        self.list_item.setProperty( property, self.player_images[ 0 ] )

                        if self.player_to_play == 1:
                            self.tiles.setTile( property, "X" )
                        elif self.player_vs_who != "XBMC":
                            self.tiles.setTile( property, "O" )
                        del self.tilesID[ property ]

                        self.switch_player()

                elif controlID == 310:
                    self.resetScores()
                    self.resetContainer()
                    self.setFocusId( 9000 )
                    if self.player_vs_who == "XBMC":
                        self.player_vs_who = "P2"
                        self.list_item.setProperty( "toplay", __language__( 32101 ) )
                        self.set_button_hard( 0 )
                    elif self.player_vs_who == "P2":
                        self.player_vs_who = "XBMC"
                        self.list_item.setProperty( "toplay", __language__( 32100 ) )
                        self.set_button_hard( 1 )

                elif controlID == 320:
                    self.resetContainer()
                    self.setFocusId( 9000 )

                elif controlID == 321:
                    self.resetScores()
                    self.resetContainer()
                    self.setFocusId( 9000 )

            if controlID in ( 300, 330 ):
                self._close_game()

        except:
            print_exc()

    def switch_player( self ):
        # change player
        self.have_winner()
        if self.tilesID and not self.winner:
            self.setFocusId( 9000 )
            if self.player_to_play == 1:
                self.player_to_play = 2
                self.player_images = "O.png", "player_two.png"
                self.list_item.setProperty( "toplay", __language__( 32103 ) )
                self.list_item.setProperty( "playerIItoplay", "2" )

                #xbmc to play :)
                if self.tilesID and self.player_vs_who == "XBMC":
                    self.list_item.setProperty( "toplay", __language__( 32104 ) )
                    self.xbmc_art.suspense()
            else:
                self.player_to_play = 1
                self.player_images = "X.png", "player_one.png"
                self.list_item.setProperty( "toplay", __language__( 32102 ) )
                self.list_item.setProperty( "playerIItoplay", "" )
        else:
            self.setFocusId( 320 )

    def have_winner( self ):
        try:
            linewin, who = self.tiles.check_winner()

            if linewin:
                self.winner = True
                self.list_item.setProperty( "haswinner", "true" )
                self.list_item.setProperty( "Line%iwin" % linewin, "true" )
                if "X" == who:
                    self.list_item.setProperty( "toplay", __language__( 32105 ) )
                    self.score_player_one += 1
                    self.list_item.setProperty( "score_player_one", str( self.score_player_one ) )
                    self.list_item.setProperty( "fanart_win", "fanart_win.png" )
                    self.fanart_win = True
                elif "O" == who:
                    self.list_item.setProperty( "toplay", ( __language__( 32106 ), __language__( 32107 ) )[ ( self.player_vs_who == "XBMC" ) ] )
                    self.score_player_two += 1
                    self.list_item.setProperty( "score_player_two", str( self.score_player_two ) )
                    self.list_item.setProperty( "fanart_win", "" )
                    self.fanart_win = False
                self.setFocusId( 320 )
                #self.tiles.print_tiles()
            elif not self.tilesID:
                self.list_item.setProperty( "toplay", __language__( 32108 ) )
                xbmc.sleep( 1000 )
                self.setFocusId( 320 )
                #self.tiles.print_tiles()
        except:
            print_exc()

    def onAction( self, action ):
        if action in ( 9, 10 ):
            self._close_game()

    def _close_game( self ):
        self.resetContainer()
        xbmc.sleep( 100 )
        self.close()


class XBMC_ART:
    """ Artificial Intelligence """
    def __init__( self, XBMC ):
        self.XBMC = XBMC
        self._is_playing = False

        # hard level
        self.obstruct = {
            "L1R1": ( [ "L2R1", "L1R3" ], [ "L1R2", "L3R1" ] ),
            "L1R3": ( [ "L1R2", "L3R3" ], [ "L2R3", "L1R1" ] ),
            "L3R1": ( [ "L3R2", "L1R1" ], [ "L2R1", "L3R3" ] ),
            "L3R3": ( [ "L2R3", "L3R1" ], [ "L3R2", "L1R3" ] )
            }

    def hard( self ):
        _tile = None
        if self.XBMC.getControl( 350 ).isSelected():
            _tiles = {}
            for tiles in self.XBMC.tiles.values():
                _tiles.update( tiles )
            for tile, value in self.obstruct.items():
                if _tile: break
                for val in value:
                    if _tiles[ val[ 0 ] ] == _tiles[ val[ 1 ] ] == "X":
                        _tile = tile
                        break
        return _tile

    def suspense( self ):
        self._is_playing = True
        xbmc.executebuiltin( "Dialog.Close(Pointer,true)" )
        self.XBMC.setFocusId( 9000 )
        for x in range( 5 ):
            #xbmc.executebuiltin( "Dialog.Close(Pointer,true)" )
            for key, control_id in sorted( self.XBMC.tilesID.items(), key=lambda k: k[ 0 ] ):
                #xbmc.executebuiltin( "Dialog.Close(Pointer,true)" )
                self.XBMC.setFocusId( control_id )
                xbmc.sleep( 25 )

        first_round = ""
        property = ""
        properties = self.XBMC.tilesID.keys()

        if not self.XBMC.first_round:
            self.XBMC.first_round = True
            #first choice center or top corner left
            for first in [ "L2R2", "L1R1" ]:
                if first in properties:
                    first_round = first
                    break

        #set XBMC_ART choice, check if possible win, check P1 if win on next round, check first tiles and finally use random choice for easy
        property = self.analysis_tiles( "O" ) or self.analysis_tiles() or first_round
        property = property or self.hard() or properties[ random.choice( range( len( properties ) ) ) ]
        self.XBMC.setFocusId( self.XBMC.tilesID[ property ] )

        self.XBMC.list_item.setProperty( property, self.XBMC.player_images[ 1 ] )
        xbmc.sleep( 500 )
        self.XBMC.list_item.setProperty( property, self.XBMC.player_images[ 0 ] )

        self.XBMC.tiles.setTile( property, "O" )
        del self.XBMC.tilesID[ property ]

        self._is_playing = False
        self.XBMC.switch_player()

    def analysis_tiles( self, item="X" ):
        # item = "X" or "O", default "X"
        _tile = None
        for tiles in self.XBMC.tiles.values():
            if _tile: break
            if tiles.values().count( item ) == 2:
                for tile, value in tiles.items():
                    if not value:
                        _tile = tile
                        break
        return _tile


class TILES( dict ):
    """ L = Line and R = Row
    L1R1 | L1R2 | L1R3
    ---- + ---- + ----
    L2R1 | L2R2 | L2R3
    ---- + ---- + ----
    L3R1 | L3R2 | L3R3
    """

    def __init__( self ):
        self[ 1 ] = { "L1R1": "", "L1R2": "", "L1R3": "" }
        self[ 2 ] = { "L2R1": "", "L2R2": "", "L2R3": "" }
        self[ 3 ] = { "L3R1": "", "L3R2": "", "L3R3": "" }
        self[ 4 ] = { "L1R1": "", "L2R1": "", "L3R1": "" }
        self[ 5 ] = { "L1R2": "", "L2R2": "", "L3R2": "" }
        self[ 6 ] = { "L1R3": "", "L2R3": "", "L3R3": "" }
        self[ 7 ] = { "L1R1": "", "L2R2": "", "L3R3": "" }
        self[ 8 ] = { "L3R1": "", "L2R2": "", "L1R3": "" }

    def setTile( self, tile, value ):
        # tile = key, value = "X" or "O"
        for line, tiles in self.items():
            if tiles.has_key( tile ):
                tiles[ tile ] = value

    def check_winner( self ):
        linewin = 0
        who = None
        for line, tiles in self.items():
            tiles = tiles.values()
            O = tiles.count( "O" ) == 3
            X = tiles.count( "X" ) == 3
            if X or O:
                linewin = line
                who = tiles[ 0 ]
                break
        return linewin, who

    def print_tiles( self ):
        tiles = r"""[B]
        %s | %s | %s
        - + - + -
        %s | %s | %s
        - + - + -
        %s | %s | %s[/B]"""
        tiles = tiles % ( self[ 1 ][ "L1R1" ] or "_", self[ 1 ][ "L1R2" ] or "_", self[ 1 ][ "L1R3" ] or "_",
            self[ 2 ][ "L2R1" ] or "_", self[ 2 ][ "L2R2" ] or "_", self[ 2 ][ "L2R3" ] or "_",
            self[ 3 ][ "L3R1" ] or "_", self[ 3 ][ "L3R2" ] or "_", self[ 3 ][ "L3R3" ] or "_" )
        print tiles.lower()


if  __name__ == "__main__":
    current_skin, force_fallback = getUserSkin()
    try: w = TTT( "TTT-main.xml", CWD, current_skin, "PAL" )
    except: w = TTT( "TTT-main.xml", CWD, current_skin, force_fallback )
    w.doModal()
    del w
