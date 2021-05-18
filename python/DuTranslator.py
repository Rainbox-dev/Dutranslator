# DuTranslatorLib
# Translator Framework Library
# Copyright (c) 2017,2018 Nicolas Dufresne, Rainbox Productions
# https://rainboxprod.coop
#
# _Contributors:_
# Nicolas Dufresne - Lead developer
#
# This file is part of DuAEF.
#
# DuAEF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DuAEF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DuAEF. If not, see <http://www.gnu.org/licenses/>.

import json


# TODO la déclaration du dict "translation" ici n'est pas utile
# on avait en JS la déclaration d'une classe, mais c'est overkill ; un dict n'a pas besoin d'être préparé à l'avance comme ça,
# juste on le crée au besoin dans la fonction qui l'utilise/le retourne (generate_translations par exemple)
translation = {}
"""A new string translation."""

translation["source"] = ""
"""The source string"""

translation["translations"] = ""
"""The translated string"""

translation["comment"] = ""
"""A comment to explain what needs to be explained"""

translation["context"] = ""
"""The context where the string is used"""

translation["context_id"] = 0
"""A unique id for the couple source/context"""

# TODO on verra à la fin, mais au final on a meme aps besoin de tout foutre dans un dict
# on poyurrait tout aussi bien juste avoir des variabkes simples
# current_language_id,
# current_language_name,
# languages
# etc etc
# on changera à la fin, parce que faudra aller chercher et remplacer partout "translator_settings["truc"]

translator_settings = {}

translator_settings["current"] = ""
"""The current language id (fr, en, ..)."""

translator_settings["current_name"] = ""
"""The current language name."""

translator_settings["languages"] = {}
"""
A dict containing available languages.
There is a language name and a file name for each language id.
languages["fr_FR"] ["name"] is "Francais" for example.
Will be filled when executing getAvailable().
"""

translator_settings["localized_strings"] = ()
"""
The translated strings  of the current language.
An array of compounds containing the source, the translation and the context.
"""

translator_settings["settings"] = {}
settings = translator_settings["settings"]
"""Some Settings for the translator"""

# TODO idem que translator settings, on a peut etre pas besoind e s'emmerder avec un dict, mais tout garder dans de simples variables

# DuAEF.Dutranslator.Settings.folder = File($.fileName).path + "/";  (JS)
settings["folder"] = "thisScriptFile/file/path/"
"""The folder containing the translation files (str)"""

# DuAEF.Dutranslator.Settings.prefix = File($.fileName).name.substring(0,File($.fileName).name.lastIndexOf('.'))
# + "_"; (JS)
settings["prefix"] = "thisScriptFileName_"
"""The prefix in the translation filenames (str) @default "thisScriptFile/file/path/" """

settings["suffix"] = ".json"
"""The suffix (including file extension) in the translation filenames (str) @default ".json" """

settings["name"] = "duaef"
"""The application name (root of the json translations) (str) @default "duaef" """

settings["original_language_id"] = "en"
"""The original languageId"""

settings["original_language_name"] = "English"
"""The original language name"""


def get_available():
    """
    Load the list of available languages.
    If the language id and or the language name can't be found in the file, the file name will be used
    to determine the language id and the name will be set as the id.
    Returns: A success code
        0	Success
        1	One of the file haven't been correctly opened
    """

    # Add original language
    languages = translator_settings["languages"]
    languages[settings["original_language_id"]] = {"name": settings["original_language_name"], "file": None}

    # en JS : lignes 166 à 169
    # var folder = new Folder(DuAEF.Dutranslator.Settings.folder);
    # // Get the list of translations
    # languageFiles = folder.getFiles(DuAEF.Dutranslator.Settings.prefix +'*'+ DuAEF.Dutranslator.Settings.suffix);
    # >>> D'où sortent le "Folder" et le "getFiles" ?? :-O
    # TODO Folder est une classe propre à Adobe qui permet de manipuler des dossiers.
    # en python, tout ce qu'elle fait correspond aux os.path.isdir, os.path.listdir, etc etc
    # getFiles, c'est justement le os.path.listdir (cf Ramses file manager, on l'utilise celle là, pour lister des fichiers dans un dossier)
    # j'ai un doute c'esty peut etre os.listdir ou autre truc qui ressemble ^^
    folder = settings["folder"]
    language_files = (settings["prefix"] + "*" + settings["suffix"])

    for i in range(len(language_files)): # TODO, si le "i" n'est pas utile dans la suite, autant écrire `for file_name in language_files:`
        file_name = language_files[i].name
        ## var langId = langName = ""; ??
        lang_id = lang_name = ""

        # Determine the language name and the language id by reading the file
        # Values are stored at the top so it should be fase
        ## var file = new File(folder.absoluteURI + "/" + fileName);   JS
        file = folder + "/" + file_name
        if not file.open("r"):
            return 1  # Unable to open the file

        # Line by line reading
        ## while(langName == "" || langId == "" && !file.eof ) JS : eof ??
        while (lang_name == "") or (lang_id == ""):
            line = file.readln()
            index_name = line.rindex("language_name")
            index_id = line.rindex("language_id")

            if (index_name != -1) and (lang_name == ""):
                index = index_name
            elif (index_id != -1) and (lang_id == ""):
                index = index_id
            else:
                continue
            # ..... "lang" : "value"

def get_pretty_name(lang_id):
    """
    Returns the pretty name of a given language.
    Args:
        lang_id: (str) The id of the request language

    Returns:

    """
    if not lang_id in translator_settings["languages"]:
        return ""
    return translator_settings["languages"][lang_id]["name"]

def get_language_id(pretty_name):
    """
    Returns the language id of a given language name
    Args:
        pretty_name: (str) The pretty name of the request language

    Returns:

    """
    for lang_id in translator_settings["languages"]:
        if translator_settings["languages"][lang_id]["name"] == pretty_name:
            return lang_id
    return ""

def get_pretty_names():  # docstring en JS ligne 246 : @param {string} langId - The id of the request language ?
    """
    Returns a list containing pretty names of all languages
    """
    res = []
    for lang_id in translator_settings["languages"]:
        res.append( translator_settings["languages"][lang_id]["name"] )

    # Order the list by name
    res = sorted(res)
    return res

def set_language(language_id):
    """
    Set the current language
    Args:
        language_id: (str) The id of the language to set.

    Returns:
        success code
        0	Everything went ok
        1	The file linked to the given id can't be opened
        2	The json content doesn't match a translation file
    """
    settings = translator_settings["settings"]

    for lang_id in translator_settings["languages"]:
        if lang_id == language_id:
            translator_settings["current"] = language_id
            translator_settings["current_name"] = get_pretty_name(
                language_id)  ## Donner un argument à la fonction ligne 148

            if language_id == settings["original_language_id"]:
                return 0  # Default language, no translation

            # Parse process
            f_path = translator_settings["languages"][lang_id]["file"]
            # var file = new File(f_path);  ??   JS Ligne 284
            # var jsonData = DuAEF.DuJS.Fs.parseJSON(file);  ?? JS Ligne 286
            json_data = parse_json(f_path)

            if (not json_data[settings["name"]]) or (
                    len(json_data[settings["name"]]) != 2) or (
                    not json_data[settings["name"][1]["translations"]]):
                return 2  # Wrong json format

            translations = json_data[settings["name"][1]["translations"]]
            translator_settings["localized_strings"] = translations

            return 0

def set_pretty_language(language_name):
    """
    Set the current language with a given pretty name
    Args:
        language_name: (str) The pretty name of the language to set.

    Returns:
        success code
        0	Everything went ok
        -1   Can't find any language with the given pretty name
        >0  Call to setLanguage(languageId) failed
    """
    lang_id = get_language_id(language_name)
    if lang_id == 1:
        return -1

    return set_language(lang_id)

def generate_translations(strings):
    """
    Converts an list of strings to a list of empty translations (dicts)
    Args:
        {string[]} strings - The base strings to convert.

    Returns:
        {Translation[]} The empty translations
    """
    strings = remove_duplicates(strings)

    translations = []
    for i in range(len(strings)):
        translations.append(strings[i])
        # TODO
        # ne pas append strings[i]
        # mais ce dict :
        # translation = {}
        # translation["source"] = strings[i]
        # translation["translations"] = ""
        # translation["comment"] = ""
        # translation["context"] = ""
        # translation["context_id"] = 0
        # ce sont des valeurs par défaut, sauf la source qui est la chaine en question
        # et puis là ya plus qu'à append ce dict à translations ; le dict remplace la classe Translation utilisée en js (et pas vraiment utile, c'est overkill une classe pour ça)

    return translations

def generate_translation_file(file, translations=translator_settings["localized_strings"], app_name="dutranslator",
                              version="0.0",
                              language_id=translator_settings["current"],
                              language_name=translator_settings["current_name"]):  # TODO : A verifier
    """
    Creates a file for translation with the given base strings.
    Args:
        file: (file or str) The file or URI
        translations: (translation[] or str) The translations or source strings to be included in the translation file.
                [translations=localizedStrings]
        app_name: (str) A name for the app using this translation file. [appName="dutranslator"]
        version: (str) A version (as a string) for this translation file or app. [version="0.0"]
        language_id: (str) A version (as a string) for this translation file or app. [languageId=current]
        language_name: (str) A version (as a string) for this translation file or app. [languageName=currentName]
    """

    # if (!(file instanceof File)) file = new File(file);  JS ligne 330 !?
    app_name = app_name.lower()
    if len(translations) == 0:
        return None

    # if translations is an array of strings, convert to translations
    if isinstance(translations[0], str):
        translations = generate_translations(translations)

    data = {}
    metadata = {}
    translations_object = {}

    metadata["language_id"] = language_id
    metadata["language_name"] = language_name
    metadata["version"] = version

    translations_object["translations"] = translations

    data[app_name] = [metadata, translations_object]

    save_json(data, file)

def remove_duplicates(l):
    newList = []
    for i in l:
        if not i in newList:
            newList.append(i)
    return newList

def parse_json(file):
    """Open a file, loads the contents and with json, extract infos"""

    # est-ce que ça vaut le coup d'ajouter un : if file != None : pour éviter les erreurs ?
    with open(file, "r") as read_file:
        read_string = read_file.read()
        file_dict = json.loads(read_string)

        translation["translations"] = file_dict["translations"]

        return translation["translations"]

        # if "name" in file_dict:
        #     settings["name"] = file_dict["name"]
        # if "folder" in file_dict:
        #     settings["folder"] = file_dict["folder"]
        # if "original_language_id" in file_dict:
        #     settings["original_language_id"] = file_dict["original_language_id"]
        # if "original_language_name" in file_dict:
        #     settings["original_language_name"] = file_dict["original_language_name"]
        # if "prefix" in file_dict:
        #     settings["prefix"] = file_dict["prefix"]
        # if "suffix" in file_dict:
        #     settings["suffix"] = file_dict["suffix"]
        #
        #     return settings

def save_json(data, file):
    """From a dict, with json, save in file"""

    # TODO : pas besoin de ça je pense, la fonction est toute con en python, juste elle écrit direct la data 
    dict = {
        settings["name"]: data["name"],
        translation["translations"]: data["translations"]
    }

    # ou alors :
    # dict[settings["name"] = date["name"]
    # dict[translation["translations"] = data["translations]

    with open(file, "w") as written_file:
        # written_file.write(json.dumps(dict, indent=4))
        json.dump(dict, written_file, indent=4)

    # TODO à tester oui !
    # on peut éventuellement ajouter à la fonction .dump un paramètre pour les accents (è) 
    # json.dumps(dict, written_file, ensure_ascii= False, indent=4)

def tr(string, context, args):
    """
    Translate a given string based on the current setted language.
    see {@link DuAEF.Dutranslator} for more details about the translation framework.
    Args:
        string: (str) The text to be translated.
        context: (int or str) Can be an integer or a string which is related to contextId or context in a translation file.
        args: (str[]) Args to format into the translated string, default is [].
        For example, when calling tr("Welcome {#}", -1, "Paul"), the output will be "Welcome Paul".
        If too many args are given, there are ignored.
        If not enough args are given, the {#} are replaced with ?

    Returns:
        (str) The translated text or s if nothing is set or available.
    """
    # Default args
    use_context_id = True

    if not isinstance(string, str):
        ## DuAEF.Debug.throwTypeError( str, "str", "String", "DuTranslator::tr()");
        raise TypeError(string, "str", "String", "DuTranslator::tr()")

    if isinstance(context, str):
        use_context_id = False
    if context is None:
        context = -1
    elif context < 0:
        context = -1
    if args is None:
        args = []
    if isinstance(args, str):
        args = [args]

    language_number = -1
    res = string

    # a function to get the translation id from a given string
    def get_translation_id(stri, no_caps_nor_spaces = False):
        for i in range(len(translator_settings["localized_strings"])):
            localized_string = translator_settings["localized_strings"][i]
            test_string = localized_string["source"]
            if no_caps_nor_spaces:
                test_string = test_string.replace("\s", "\\n", "\\r", "\g", '')  ## ??
                ## if (noCapsNorSpaces) testString = testString.replace(/[\s\n\r]+/g,'');

            if test_string == stri:
                # Check context
                if use_context_id and (context > -1):
                    if localized_string["context_id"] == context:
                        return i
                elif not use_context_id:
                    if localized_string["context"] == context:
                        return i
                else:
                    return i
        return -1

    # If a language is set, search for the translation
    if translator_settings["current"] != settings["original_language_id"]:

        # Get the translation
        string_number = get_translation_id(string)  # args : no_caps_nor_spaces ?

        # If a translation is found, set it to res
        if string_number > -1:
            res = translator_settings["localized_strings"][string_number]["translation"]
        if res is None:
            res = string
        if res == "":
            res = string

    # Args process
    while res.index("{#}") != -1:

        # While there is stuff to format
        if len(args) < 1:
            # If no more args, replace with ?
            res = res.replace("{#}", "?")  # Will replace the first occurence

        else:
            arg = args.pop(0)  # Take the first arg and remove it
            res = res.replace("{#}", arg)

    return res