# Module to handle quran data transformation
# Author: arenodi

## import load from json lib to  open json file to python obj
from json import load

# import copy module for dealing with dictionaries
from copy import deepcopy


# function to transform the quran data
def quaran_transform(filepath):
    try:
        # loads file to python dict
        with open(filepath) as raw_quran:
            # dict to hold the data
            raw_data = load(raw_quran)

        # Each raw quran edition is structured by surahs, the quran has 114 surahs
        # This script is going to iterate over each surah to generate a restructured version.
        # number of surahs
        number_of_surahs = len(raw_data["surahs"])

        # dict to hold the restructured version, it will start getting the edition data from
        # the raw quran dict
        transformed_quran = raw_data["edition"]
        # create new key for holding the juz, at the end of the process
        # this list needs to hold 30 items. The quran has 30 juz in total.
        transformed_quran["content"] = []

        # variable to hold the context juz number. This is needed because within
        # a surah the juz number may change.
        context_juz = 1
        # for loop to iterate over all the surahs
        for surah in raw_data["surahs"]:
            # for loop to iterate over all the ayahs in each surah
            surah_data = {
                "type": "surah",
                "number": surah["number"],
                "name": surah["englishNameTranslation"],
                "ayahs": [],
            }
            for ayah in surah["ayahs"]:
                ayah_data = {
                    "type": "ayah",
                    "number": ayah["number"],
                    "text": ayah["text"],
                }
                # get juz number from the ayah
                juz = ayah["juz"]
                # if the length of the transformed quran content is smaller than the juz number
                # then it adds an new dict for holding the juz content
                if len(transformed_quran["content"]) < juz:
                    transformed_quran["content"].append(
                        {"type": "juz", "number": juz, "content": []}
                    )
                # check if the context juz is the same of the ayah
                if context_juz == juz:
                    # surah_data[ayahs] is updated with current ayah
                    surah_data["ayahs"].append(ayah_data)
                # else
                else:
                    # the surah_data dict will be added to the context juz
                    transformed_quran["content"][context_juz - 1]["content"].append(
                        deepcopy(surah_data)
                    )
                    # the surah_data[ayahs] attr will be reseted
                    surah_data["ayahs"] = []
                    # surah_data[ayahs] is updated with current ayah
                    surah_data["ayahs"].append(ayah_data)
                    # the context_juz will be updated
                    context_juz = juz

            # append surah data to context juz before moving on to next surah
            transformed_quran["content"][context_juz - 1]["content"].append(
                deepcopy(surah_data)
            )

    except:
        print("error")

    finally:
        return transformed_quran
