import signal
import sys
import math
import time
import urllib2
import Adafruit_CharLCD as LCD
import HTMLParser

# setup appropriate GPIO ports to appropriate inputs on display
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 21
lcd_d7 = 22
lcd_backlight = 4

lcd_columns = 16
lcd_rows = 2
# initialize lcd screen
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


# needed to identify index of start of game information
def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index + len(char)] == char:
                    return index

            index += 1

    return -1


# get nba scores from URL HTML
url_nba_scores = "http://www.espn.com/nba/bottomline/scores"
response = urllib2.urlopen(url_nba_scores)
html_nba_scores = response.read()

# output response to console for testing
print(html_nba_scores)

# declare iterator to 1 since 1 is needed the first needed to append to search of game index
i = 1

# will run in loop with game indicated by nba_s_left and then i until there are more
while i == 1:

    # get information from espn for the NBA. Gets games that are running, not started or finished
    url_nba_scores = "http://www.espn.com/nba/bottomline/scores"
    response = urllib2.urlopen(url_nba_scores)
    html_nba_scores = response.read()

    # output response to screen for testing
    print(html_nba_scores)

    while True:

        # find index of start of a game in string returned from url. Games start after nba_s_left(#)
        game_index_start = find_str(html_nba_scores, "nba_s_left" + str(i))

        # output of start of game index in string console output
        print(game_index_start)

        # when game index was checked if the next game was not found (last game was already displayed)
        #   the function to get the index returns -1. If a next game was found it does not return -1, returns index
        # If next game was found perform operations to display it. Else, if next game was not found then
        #   then reset the iterator to 1 and break out of this loop so that parent loop can run again to update
        #   the scores.
        if game_index_start != -1:

            # move index to where data we want is and move all data from URL after that into variable. Will be parsed
            game_html = html_nba_scores[game_index_start + 12:]
            print(game_html)

            # trims data to the right of the game that we want. Game data stops at '&' character
            game_score = game_html.partition("&")[0]
            # trims data before '(' character. After '(' is the time left or if game is final
            game_score = game_score.partition("(")[0]

            # some team names have '^' in them. This is to remove them so that they can be displayed without error
            if game_score.find("^") != -1:
                game_score = game_score.replace("^", "")

            # print to console for testing
            print(game_score)

            # games that have not started have "at" where there is usually another %20.
            #   to handle these we check of the game we check for the string below. If it is present
            #   then we split at the the "at" and split the teams names and scores into 2 different variables
            if game_score.find("%20at%20") != -1:
                team_1, team_2 = game_score.split("at")
                # append the "at" since team 1 is the away team so it can be displayed on the screen
                team_1 = team_1 + "at"
            else:
                # if the game is in progress or has ended the teams this will be where the names and scores are split
                team_1, team_2 = game_score.split("%20%20%20")

            # replace with spaces
            team_1 = team_1.replace("%20", " ")
            team_2 = team_2.replace("%20", " ")

            # set display to first line and display first team
            lcd.set_cursor(0, 0)
            lcd.message(team_1)

            # set display to second line and display second team
            lcd.set_cursor(0, 1)
            lcd.message(team_2)

            # sleep so that display can be read
            time.sleep(3)
            # increase iterator so that script can get next game next loop
            i += 1
            # clear after displaying so that next game can be displayed
            lcd.clear()

        else:
            # In the case that the next game cannot be found set iterator to 1 so that loop can
            #   run again and pull updated scores
            i = 1
            break
