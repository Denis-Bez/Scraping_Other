# Dictionary for correcting texts in ads

cleaning_url = {
    '%2F':'/', '%3A':':',
    '%25D1%2580%25D0%25BA':'рк',
    '%25E2%2580%2599':'’',
    '%3D':'=',
    '%25D0%25B0%25D1%2581':'ас',
    '%25D0%25BA':'к',
    '%25E2%2584%25961':'№1',
    }

correct_vendor = {
    "Am.Pm": "Am Pm",
    "Art&Max": "Art Max",
    "Black & White": "Black White",
    "Chilly's Bottles": "Chilly Bottles",
    "D&K": "DK",
    "Devon&Devon": "Devon",
    "E.C.A": "ECA",
    "G.Lauf": "G Lauf",
    "M&Z": "MZ",
    "Olive’S": "Olive",
    "Villeroy & Boch": "Villeroy Boch",
}

correct_vendorCode = {
    "/": "-",
    ":": "-",
    "(": "",
    ")": "",
    "*": "",
    ",": "",
    "+": "-",
    "_": "-",
    "#": "-",
    "’":" ",
    "&":" ",
}

correct_Text = {
    "`":"'",
    "’":"'",
    'й':'й',
    # ")":"", Why?
    "^":" ",
    "~":" ",
    "|":" ",
    "½":"",
    "Ø":"",
    "¾’":"",
    "'":" ",
    "×":"x",
    "/":"-",
    "  ":" ",
    "   ":" ",
}

correct_Serie = {
    "²":"",
    "/":"-",
    "°":"",
    "&":" ",
    "+":"",
}

correct_Suburl ={
    " ":"-",
    ".":"-",
}